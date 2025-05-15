import json
import os
import argparse
from pathlib import Path
from sklearn.model_selection import train_test_split

# PublayNet-compatible label map
LABEL_MAP = {
    "Text": 0,
    "Title": 1,
    "List": 2,
    "Table": 3,
    "Figure": 4,
}

def sanitize_filename(filename):
    """Remove any folder prefix from file_name field."""
    return os.path.basename(filename).replace("images\\", "").replace("images/", "")

def fix_annotation_categories(annotations, category_lookup):
    """Update annotation category_id based on label map."""
    for ann in annotations:
        name = category_lookup.get(ann['category_id'])
        if name in LABEL_MAP:
            ann['category_id'] = LABEL_MAP[name]
    return annotations

def convert_annotations(annotation_path, output_dir):
    with open(annotation_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    images = data['images']
    annotations = data['annotations']

    # Fix filenames
    for img in images:
        img['file_name'] = sanitize_filename(img['file_name'])

    # Split train/val
    train_imgs, val_imgs = train_test_split(images, test_size=0.3, random_state=42)
    train_ids = {img['id'] for img in train_imgs}
    val_ids = {img['id'] for img in val_imgs}

    # Build category ID -> name lookup
    category_lookup = {cat['id']: cat['name'] for cat in data['categories'] if cat['name'] in LABEL_MAP}

    # Filter and fix annotations
    train_anns = fix_annotation_categories(
        [a for a in annotations if a['image_id'] in train_ids], category_lookup)
    val_anns = fix_annotation_categories(
        [a for a in annotations if a['image_id'] in val_ids], category_lookup)

    # Build detectron2-style categories
    categories = [{"id": v, "name": k, "supercategory": k} for k, v in LABEL_MAP.items()]

    os.makedirs(output_dir, exist_ok=True)

    # Save
    with open(Path(output_dir) / "train.json", "w", encoding='utf-8') as f:
        json.dump({"categories": categories, "images": train_imgs, "annotations": train_anns}, f, indent=2)
    with open(Path(output_dir) / "val.json", "w", encoding='utf-8') as f:
        json.dump({"categories": categories, "images": val_imgs, "annotations": val_anns}, f, indent=2)

    print(f"[✓] Converted and saved to {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to result.json from Label Studio")
    parser.add_argument("--output", required=True, help="Directory to save converted train/val JSONs")
    args = parser.parse_args()
    convert_annotations(args.input, args.output)
