import csv
import json
import re

# Regex patterns for standalone PII
PII_PATTERNS = {
    "phone": r"\b\d{10}\b",
    "aadhar": r"\b\d{4}\s?\d{4}\s?\d{4}\b",
    "passport": r"\b[A-Z]{1}[0-9]{7}\b",
    "upi_id": r"\b[\w\.\-]+@[\w]+\b"
}

# Combinatorial PII keys
COMBINATORIAL_KEYS = {"name", "email", "address", "ip_address", "device_id"}

# Redaction logic
def redact(key, value):
    if key == "phone":
        return value[:2] + "XXXXXX" + value[-2:]
    elif key == "aadhar":
        return "XXXX XXXX XXXX"
    elif key == "passport":
        return "PXXXXXXX"
    elif key == "upi_id":
        return "[REDACTED_UPI]"
    elif key in COMBINATORIAL_KEYS:
        return "[REDACTED_PII]"
    return value

# Check for standalone PII
def contains_standalone_pii(key, value):
    pattern = PII_PATTERNS.get(key)
    if pattern and re.search(pattern, str(value)):
        return True
    return False

# Check for combinatorial PII
def contains_combinatorial_pii(data):
    present_keys = set(data.keys())
    return len(COMBINATORIAL_KEYS.intersection(present_keys)) >= 2

# Process each record
def process_record(record_id, data_json):
    try:
        data = json.loads(data_json)
    except json.JSONDecodeError:
        return record_id, "{}", False

    is_pii = False
    redacted_data = {}

    for key, value in data.items():
        if contains_standalone_pii(key, value):
            is_pii = True
            redacted_data[key] = redact(key, str(value))
        else:
            redacted_data[key] = str(value)

    if not is_pii and contains_combinatorial_pii(data):
        is_pii = True
        for key in COMBINATORIAL_KEYS:
            if key in redacted_data:
                redacted_data[key] = redact(key, redacted_data[key])

    return record_id, json.dumps(redacted_data), is_pii

# Main execution
def main():
    input_file = "iscp_pii_dataset.csv"
    output_file = "redacted_output_candidate_full_name.csv"

    with open(input_file, mode="r", encoding="utf-8") as infile, \
         open(output_file, mode="w", newline="", encoding="utf-8") as outfile:

        reader = csv.DictReader(infile)
        fieldnames = ["record_id", "redacted_data_json", "is_pii"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            record_id, redacted_json, is_pii = process_record(row["record_id"], row["data_json"])
            writer.writerow({
                "record_id": record_id,
                "redacted_data_json": redacted_json,
                "is_pii": str(is_pii)
            })

if __name__ == "__main__":
    main()
