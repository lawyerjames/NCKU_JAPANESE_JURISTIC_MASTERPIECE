"""
MCP Server for Japanese Legal Text Annotation and Bilingual Formatting.
"""

__version__ = "0.1.0"

from .furigana_annotator import format_japanese_text, sanitize_furigana_ruby, audit_annotations, PITCH_DB
from .html_builder import build_stacked_bilingual_html
from .pdf_ocr import process_pdf_smart_ocr
