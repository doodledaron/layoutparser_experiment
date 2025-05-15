import json
import argparse
from collections import Counter

def count_labels(annotation_path):
    with open(annotation_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    cat_id_to_name = {cat["id"]: cat["name"] for cat in data["categories"]}
    category_counts = Counter()

    for ann in data["annotations"]:
        category_counts[ann["category_id"]] += 1

    total = sum(category_counts.values())

    print(f"\nLabel distribution in: {annotation_path}\n")
    for cat_id, count in category_counts.items():
        percent = 100 * count / total if total > 0 else 0
        print(f"{cat_id_to_name.get(cat_id, str(cat_id))}: {count} ({percent:.2f}%)")
    print(f"\nTotal annotations: {total}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        required=True,
        help="Path to COCO-style annotation JSON (e.g., train.json)",
    )
    args = parser.parse_args()
    count_labels(args.input)
