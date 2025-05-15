import json
from collections import Counter

annotation_path = "datasets/phase_1_training_minimal/annotations/train_phase_1_minimal_v2_remapped.json"

with open(annotation_path, "r") as f:
    data = json.load(f)

# Build category id to name mapping
cat_id_to_name = {cat["id"]: cat["name"] for cat in data["categories"]}

# Count annotations per category
category_counts = Counter()
for ann in data["annotations"]:
    category_counts[ann["category_id"]] += 1

total = sum(category_counts.values())

print("Label distribution (%):")
for cat_id, count in category_counts.items():
    percent = 100 * count / total if total > 0 else 0
    print(f"{cat_id_to_name[cat_id]}: {count} ({percent:.2f}%)")