import re
from pathlib import Path
import fitz

# Extract the Claim id
def extract_claim_id(pdf_path:Path) -> str:
    match = re.search(r"CLM\d+", str(pdf_path), re.IGNORECASE)
    if match:
        return match.group(0).upper()
    return "Unknown_claim"

# Extract text from PDF
def extract_text_from_pdf(pdf_path:Path) -> str:
    text_by_page = []
    with fitz.open(pdf_path) as document:
        for page_number, page in enumerate(document, start=1):
            page_text = page.get_text()
            text_by_page.append(f"\n {page_number} ---\n{page_text}")

    return "\n".join(text_by_page).strip()

# Process PDFs
def process_pdf(raw_dir:Path, processed_dir:Path) ->list[Path]:
    processed_dir.mkdir(parents=True, exist_ok=True)
    text_output_dir = processed_dir / "extracted_text"
    pdf_files = sorted(raw_dir.rglob("*.pdf"))
    output_files = []

    if not pdf_files:
        print(f"No PDF files found in {raw_dir}.")
        return output_files

    for pdf_path in pdf_files:
        # Group each PDF output by the claim id found in the path
        claim_id = extract_claim_id(pdf_path)
        claim_output_dir = text_output_dir / claim_id
        claim_output_dir.mkdir(parents=True, exist_ok=True)

        output_path = claim_output_dir / f"{pdf_path.stem}.txt"

        if output_path.exists():
            print(f"Skipping already extracted PDF: {pdf_path.name} ({claim_id})")
            output_files.append(output_path)
            continue

        extract_text = extract_text_from_pdf(pdf_path)
        output_path.write_text(extract_text, encoding="utf-8")
        output_files.append(output_path)

        print(f"Processed PDF: {pdf_path.name} ({claim_id})")
        print(f"Saved text to {output_path}")

    return output_files