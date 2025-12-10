import json
import re
import os

def parse_case_block(block):
    lines = [line.strip() for line in block.split("\n") if line.strip()]
    if len(lines) < 7:
        return None

    case = {
        "case_name": "",
        "case_type": "",
        "jurisdiction": "",
        "year_of_judgment": "",
        "key_legal_principles": [],
        "plaintiff_defendant_details": "",
        "case_outcome": ""
    }

    # Line 1 = Case X
    # Line 2 = case name
    case["case_name"] = lines[1]

    for line in lines[2:]:
        if line.startswith("Case Type"):
            case["case_type"] = line.split("—", 1)[1].strip()

        elif line.startswith("Jurisdiction"):
            case["jurisdiction"] = line.split("—", 1)[1].strip()

        elif line.startswith("Year of Judgment"):
            case["year_of_judgment"] = line.split("—", 1)[1].strip()

        elif line.startswith("Key Legal Principles"):
            raw = line.split("—", 1)[1].strip()
            case["key_legal_principles"] = [p.strip() for p in raw.split(",")]

        elif line.startswith("Plaintiff/Defendant Details"):
            case["plaintiff_defendant_details"] = line.split("—", 1)[1].strip()

        elif line.startswith("Case Outcome"):
            case["case_outcome"] = line.split("—", 1)[1].strip()

    return case


def convert_file(input_path, output_path):
    print(f"\n📄 Reading: {input_path}")

    text = open(input_path, "r", encoding="utf-8").read()

    # Split at "Case X"
    blocks_raw = re.split(r"(Case \d+)", text)

    # Reconstruct case blocks
    blocks = []
    current = ""

    for part in blocks_raw:
        if part.startswith("Case "):
            if current.strip():
                blocks.append(current.strip())
            current = part
        else:
            current += part

    if current.strip():
        blocks.append(current.strip())

    # Parse each case
    parsed_cases = []
    for block in blocks:
        case = parse_case_block(block)
        if case:
            parsed_cases.append(case)

    print(f"✅ Parsed {len(parsed_cases)} cases → {output_path}")

    # Save JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(parsed_cases, f, indent=2)

    print("💾 Saved:", output_path)

    return parsed_cases


FILE1 = r"D:\ACM TASKS\New folder\legal_cases_1_280.txt"
FILE2 = r"D:\ACM TASKS\New folder\legal_cases_281_600.txt"

OUT1 = r"D:\ACM TASKS\New folder\legal_cases_1_280.json"
OUT2 = r"D:\ACM TASKS\New folder\legal_cases_281_600.json"

cases_1 = convert_file(FILE1, OUT1)
cases_2 = convert_file(FILE2, OUT2)


ALL_OUT = r"D:\ACM TASKS\New folder\legal_cases_all_600.json"

all_cases = cases_1 + cases_2

with open(ALL_OUT, "w", encoding="utf-8") as f:
    json.dump(all_cases, f, indent=2)

print(f"\n🎉 All 600 cases saved to:")
print(" →", ALL_OUT)
