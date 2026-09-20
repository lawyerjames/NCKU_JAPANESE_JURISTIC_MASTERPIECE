import asyncio
import json
import sys
from mcp.server.fastmcp import FastMCP

from .furigana_annotator import sanitize_furigana_ruby, audit_annotations, format_japanese_text
from .html_builder import build_stacked_bilingual_html
from .pdf_ocr import process_pdf_smart_ocr

mcp = FastMCP("Japanese Legal Text Formatter & Bilingual Annotator")

@mcp.tool()
def format_japanese_legal_text(text: str) -> str:
    """
    Formats Japanese legal text with:
    1. Bunsetsu boundaries tagged with <u>...</u>.
    2. Kanji annotated with <ruby>kanji<rt>reading(pitch)</rt></ruby>.
    3. Legal domain-specific pitch accents from comprehensive PITCH_DB.
    """
    return format_japanese_text(text)

@mcp.tool()
def sanitize_japanese_furigana(html_text: str) -> str:
    """
    Sanitizes ruby tags in Japanese text to ensure furigana is placed ONLY over Kanji characters,
    removes Romaji from <rt> tags, and fixes unclosed HTML tags.
    """
    return sanitize_furigana_ruby(html_text)

@mcp.tool()
def audit_furigana_annotations(html_text: str) -> str:
    """
    Audits Japanese ruby, rt, and u (red pause line) tags balance and checks for Romaji errors.
    """
    result = audit_annotations(html_text)
    return json.dumps(result, ensure_ascii=False, indent=2)

@mcp.tool()
def generate_stacked_bilingual_document(
    japanese_blocks: list[str],
    chinese_translations: list[str],
    title: str = "法学日本語",
    subtitle: str = "",
    subtitle_zh: str = "",
    author: str = "",
    heading_indices: list[int] = None,
    pdf_filename: str = ""
) -> str:
    """
    Generates a responsive, stacked top-and-bottom Japanese-Chinese bilingual HTML document with zero line collisions,
    1-to-1 card alignment, interactive TTS reading, and integrated PDF split viewer.
    """
    return build_stacked_bilingual_html(
        japanese_blocks=japanese_blocks,
        chinese_translations=chinese_translations,
        title=title,
        subtitle=subtitle,
        subtitle_zh=subtitle_zh,
        author=author,
        heading_indices=heading_indices,
        pdf_filename=pdf_filename
    )

@mcp.tool()
def extract_pdf_smart_ocr(
    pdf_path: str,
    output_path: str = None,
    remove_footnotes: bool = True
) -> str:
    """
    Extracts text from scanned or raster PDFs using native macOS Vision OCR.
    Automatically detects 1-column vs 2-column/mixed layout, sorts text reading order,
    and dynamically filters out bottom footnotes and citations when remove_footnotes=True.
    """
    return process_pdf_smart_ocr(pdf_path, output_path=output_path, remove_footnotes=remove_footnotes)

def main():
    mcp.run()

if __name__ == "__main__":
    main()
