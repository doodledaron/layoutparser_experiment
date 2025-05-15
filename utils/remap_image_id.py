import json

input_path = "datasets/phase_1_training_minimal/annotations/val_phase_1_minimal_v2.json"
output_path = "datasets/phase_1_training_minimal/annotations/val_phase_1_minimal_v2_remapped_test.json"

with open(input_path, "r") as f:
    data = json.load(f)

# Remap image ids to be sequential starting from 1
old_to_new_image_id = {}
for idx, img in enumerate(data["images"], start=1):
    old_to_new_image_id[img["id"]] = idx
    img["id"] = idx

# Update annotation image_id references
for ann in data["annotations"]:
    ann["image_id"] = old_to_new_image_id[ann["image_id"]]

with open(output_path, "w") as f:
    json.dump(data, f, indent=2)

print(f"Remapped image ids and saved to {output_path}")