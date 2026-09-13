import asyncio
import json
import sys
from mcp.server.fastmcp import FastMCP

from .furigana_annotator import sanitize_furigana_ruby, audit_annotations
from .html_builder import build_stacked_bilingual_html

mcp = FastMCP("Japanese Legal Text Formatter & Bilingual Annotator")

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
    title: str = "デジタル時代に対応する刑事訴訟法",
    subtitle: str = "——我が国の刑事手続を規律する基本原理",
    subtitle_zh: str = "（規範我國刑事程序之基本原理）",
    author: str = "山田峻悠（中京大学准教授 / YAMADA Takaharu）"
) -> str:
    """
    Generates a responsive, stacked top-and-bottom Japanese-Chinese bilingual HTML document with zero line collisions and 1-to-1 card alignment.
    """
    return build_stacked_bilingual_html(
        japanese_blocks=japanese_blocks,
        chinese_translations=chinese_translations,
        title=title,
        subtitle=subtitle,
        subtitle_zh=subtitle_zh,
        author=author
    )

def main():
    mcp.run()

if __name__ == "__main__":
    main()
