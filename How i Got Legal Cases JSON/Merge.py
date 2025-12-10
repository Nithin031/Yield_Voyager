import json
import os

# ---- PATHS ----

ORIGINAL_JSON = r"C:\Users\nithi\Downloads\legal_cases.json"  # your existing data

GENERATED_1 = r"D:\ACM TASKS\New folder\legal_cases_1_280.json"
GENERATED_2 = r"D:\ACM TASKS\New folder\legal_cases_281_600.json"

OUTPUT_JSON = r"C:\Users\nithi\Downloads\legal_cases_merged_full.json"


# ---- LOAD FILES ----

def load_json(path):
    print(f"📄 Loading → {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


original_cases = load_json(ORIGINAL_JSON)
generated_1 = load_json(GENERATED_1)
generated_2 = load_json(GENERATED_2)


# ---- MERGE ----

print("\n🔄 Merging case datasets...")

all_cases = original_cases + generated_1 + generated_2

# Remove duplicates by case_name
unique_cases = {}
for c in all_cases:
    unique_cases[c["case_name"]] = c

merged = list(unique_cases.values())


# ---- SAVE ----

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(merged, f, indent=2)

print(f"\n🎉 MERGE COMPLETE!")
print(f"Total cases after merging: {len(merged)}")
print(f"Saved to → {OUTPUT_JSON}")
