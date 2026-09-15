---
name: pdf-smart-ocr
description: >-
  Extracts text from scanned or raster PDFs using native macOS Vision OCR.
  Automatically detects 1-column vs 2-column layout, sorts text reading order,
  and optionally removes footnotes and citations.
---

# Smart PDF OCR & Layout Parser Skill

This skill allows Antigravity to parse scanned PDFs, image PDFs, or legal/academic papers in Japanese, English, or Chinese.

## Key Features
1. **Native macOS Vision OCR**: High precision OCR using `ja-JP` and `en-US` language models.
2. **Dynamic Layout Detection**: Automatically detects whether a page or section is 1-column, 2-column, or mixed layout, ensuring proper reading order.
3. **Footnote Filtering**: Automatically identifies bottom footnote blocks and filters out inline footnote callouts (`17）`, `3）`, etc.) when `remove_footnotes=true`.

## Usage Instructions

To run OCR on any PDF file:

```bash
python3 scratch/pdf_smart_ocr.py <path_to_pdf> [output_path]
```

### Arguments:
- `<path_to_pdf>`: Path to the input PDF file.
- `[output_path]`: Optional path for saved text/markdown output. (Default: `<pdf_name>_ocr.md`)
