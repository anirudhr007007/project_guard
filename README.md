# Project Guardian 2.0 — PII Detector & Redactor

This project is part of a cybersecurity challenge focused on preventing personal data leaks in real-time systems. It includes a Python-based tool to detect and redact Personally Identifiable Information (PII) from structured data streams.

---

## Files Included

- `detector_full_candidate_name.py` — Main Python script for PII detection and redaction
- `iscp_pii_dataset.csv` — Input dataset containing JSON records
- `redacted_output_candidate_full_name.csv` — Output file with redacted data and PII flags
- `deployment_strategy.md` — Proposed architecture for deploying the solution

---

## How to Run

Make sure all files are in the same folder. Then run:

```bash
python3 detector_full_candidate_name.py iscp_pii_dataset.csv
