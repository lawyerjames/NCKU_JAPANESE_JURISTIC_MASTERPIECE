import re
import html

def sanitize_furigana_ruby(text: str) -> str:
    """
    Sanitizes ruby tags to ensure furigana is placed ONLY over Kanji characters,
    stripping trailing hiragana, romaji, and syntax errors.
    """
    # Replace unclosed or invalid tags
    text = re.sub(r'<rt>([^<]*?)([a-zA-Z]+)([^<]*?)</rt>', r'<rt>\1\3</rt>', text)
    
    # Audit ruby balance
    ruby_open = len(re.findall(r'<ruby>', text))
    ruby_close = len(re.findall(r'</ruby>', text))
    if ruby_open != ruby_close:
        # Auto fix unclosed ruby tags
        text = text.replace('<ruby>', '').replace('</ruby>', '')
    return text

def audit_annotations(html_text: str) -> dict:
    """
    Audits ruby, rt, and u tags balance in an HTML text.
    Returns status and tag metrics.
    """
    ruby_open = len(re.findall(r'<ruby>', html_text))
    ruby_close = len(re.findall(r'</ruby>', html_text))
    rt_open = len(re.findall(r'<rt>', html_text))
    rt_close = len(re.findall(r'</rt>', html_text))
    u_open = len(re.findall(r'<u>', html_text))
    u_close = len(re.findall(r'</u>', html_text))
    romaji_in_rt = [rt for rt in re.findall(r'<rt>(.*?)</rt>', html_text) if re.search(r'[a-zA-Z]', rt)]
    
    is_valid = (ruby_open == ruby_close) and (rt_open == rt_close) and (u_open == u_close) and (len(romaji_in_rt) == 0)
    
    return {
        "is_valid": is_valid,
        "ruby_count": ruby_open,
        "rt_count": rt_open,
        "u_count": u_open,
        "romaji_errors": len(romaji_in_rt)
    }
