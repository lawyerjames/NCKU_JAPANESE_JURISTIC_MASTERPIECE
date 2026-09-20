import sys, os, json, re, subprocess

def run_swift_vision_ocr(pdf_path, languages=["ja-JP", "en-US"]):
    swift_script = f'''
import Foundation
import PDFKit
import Vision
import AppKit

struct RecognizedLine: Codable {{
    let page: Int
    let x: Double
    let y: Double
    let w: Double
    let h: Double
    let text: String
}}

let pdfPath = "{pdf_path}"
guard let doc = PDFDocument(url: URL(fileURLWithPath: pdfPath)) else {{
    print("Error: Failed to open PDF")
    exit(1)
}}

var results: [RecognizedLine] = []

for pageIdx in 0..<doc.pageCount {{
    guard let page = doc.page(at: pageIdx) else {{ continue }}
    let pageRect = page.bounds(for: .mediaBox)
    let pdfImage = page.thumbnail(of: CGSize(width: pageRect.width * 3, height: pageRect.height * 3), for: .mediaBox)
    guard let cgImage = pdfImage.cgImage(forProposedRect: nil, context: nil, hints: nil) else {{ continue }}
    
    let group = DispatchGroup()
    group.enter()
    
    let request = VNRecognizeTextRequest {{ request, error in
        defer {{ group.leave() }}
        guard let observations = request.results as? [VNRecognizedTextObservation] else {{ return }}
        for obs in observations {{
            guard let candidate = obs.topCandidates(1).first else {{ continue }}
            let bbox = obs.boundingBox
            let line = RecognizedLine(
                page: pageIdx + 1,
                x: Double(bbox.origin.x),
                y: Double(bbox.origin.y),
                w: Double(bbox.size.width),
                h: Double(bbox.size.height),
                text: candidate.string
            )
            results.append(line)
        }}
    }}
    request.recognitionLanguages = {json.dumps(languages)}
    request.usesLanguageCorrection = true
    
    let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])
    try? handler.perform([request])
    group.wait()
}}

let encoder = JSONEncoder()
encoder.outputFormatting = .prettyPrinted
if let data = try? encoder.encode(results) {{
    FileHandle.standardOutput.write(data)
}}
'''
    cache_dir = os.path.expanduser("~/.cache/antigravity_swift")
    os.makedirs(cache_dir, exist_ok=True)
    swift_file = os.path.join(cache_dir, "temp_ocr.swift")
    
    with open(swift_file, "w", encoding="utf-8") as f:
        f.write(swift_script)
    
    # Try swift runner, with xcrun swiftc fallback for toolchain mismatch
    cmd = ["swift", "-module-cache-path", cache_dir, swift_file]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        bin_file = os.path.join(cache_dir, "temp_ocr_bin")
        compile_cmd = ["xcrun", "-sdk", "macosx", "swiftc", swift_file, "-module-cache-path", cache_dir, "-o", bin_file]
        compile_res = subprocess.run(compile_cmd, capture_output=True, text=True)
        if compile_res.returncode == 0:
            res = subprocess.run([bin_file], capture_output=True, text=True)
        else:
            raise RuntimeError(f"OCR Swift Execution Error: {res.stderr}\nCompile Error: {compile_res.stderr}")
    
    try:
        return json.loads(res.stdout)
    except Exception as e:
        raise RuntimeError(f"Failed to parse Vision OCR JSON output: {e}")

def is_header_footer(line_text):
    t = line_text.strip()
    if any(k in t for k in ['TKCローライブラリー', 'YODB法学教室', '法学教室', '特集／', 'Journal']):
        return True
    if re.match(r'^(?:0\d{2}|\d{1,4})$', t):
        return True
    return False

# Explicit footnote markers: 1）, (1), 注1, 前掲注, etc.
FN_MARKER_REGEX = re.compile(r'^(?:\d{1,2}[\）\)]|\(\d{1,2}\)|注\s*\d+|前掲注|\*\d+|【註|\[註)')
CITATION_HINTS = ['頁', '年', '巻', '号', '判', '事件', '前掲', '参照', '著', '訳', '書房', '出版', '編']

def is_footnote_line(l):
    text = l['text'].strip()
    if l['y'] > 0.32:
        return False
    if FN_MARKER_REGEX.match(text):
        return True
    dot_match = re.match(r'^\d{1,2}[\.．]\s*(.*)', text)
    if dot_match:
        rest = dot_match.group(1).strip()
        # If it has citation hints and is substantial, it is a footnote; otherwise it is a section heading (e.g. 1. 形式)
        if any(h in rest for h in CITATION_HINTS) and len(rest) > 8:
            return True
        return False
    return False

def analyze_and_extract_page(page_lines, remove_footnotes=True):
    valid_lines = [l for l in page_lines if not is_header_footer(l['text'])]
    if not valid_lines:
        return ""
    
    fn_cutoff_y = 0.0
    for l in valid_lines:
        if is_footnote_line(l):
            fn_cutoff_y = max(fn_cutoff_y, l['y'] + 0.015)
    
    if remove_footnotes and fn_cutoff_y > 0:
        body_lines = [l for l in valid_lines if l['y'] >= fn_cutoff_y]
    else:
        body_lines = valid_lines
    
    if not body_lines:
        return ""

    left_cluster = [l for l in body_lines if l['x'] < 0.45 and (l['x'] + l['w']) < 0.52]
    right_cluster = [l for l in body_lines if l['x'] > 0.47]
    full_span_lines = [l for l in body_lines if l['w'] > 0.50 or (l['x'] < 0.35 and (l['x'] + l['w']) > 0.65)]
    
    is_two_column = (len(left_cluster) > 3 and len(right_cluster) > 3) and (len(full_span_lines) < len(body_lines) * 0.4)
    
    page_text = []
    if is_two_column:
        top_headers = sorted([l for l in body_lines if l['y'] > 0.65 and l in full_span_lines], key=lambda l: -l['y'])
        left_col = sorted([l for l in body_lines if l not in top_headers and l['x'] <= 0.47], key=lambda l: -l['y'])
        right_col = sorted([l for l in body_lines if l not in top_headers and l['x'] > 0.47], key=lambda l: -l['y'])
        
        for l in top_headers: page_text.append(l['text'].strip())
        for l in left_col: page_text.append(l['text'].strip())
        for l in right_col: page_text.append(l['text'].strip())
    else:
        sorted_lines = sorted(body_lines, key=lambda l: -l['y'])
        for l in sorted_lines: page_text.append(l['text'].strip())
        
    return "".join(page_text)

def process_pdf_smart_ocr(pdf_path: str, output_path: str = None, remove_footnotes: bool = True) -> str:
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    ocr_lines = run_swift_vision_ocr(pdf_path)
    if not ocr_lines:
        raise ValueError("No OCR lines extracted from PDF.")
    
    pages_dict = {}
    for l in ocr_lines:
        p = l['page']
        pages_dict.setdefault(p, []).append(l)
    
    full_doc_text = []
    for p_num in sorted(pages_dict.keys()):
        p_text = analyze_and_extract_page(pages_dict[p_num], remove_footnotes=remove_footnotes)
        full_doc_text.append(p_text)
    
    raw_combined = "".join(full_doc_text)
    
    if remove_footnotes:
        # Strip inline footnote callouts like 1）, 20）, (1), 10）
        raw_combined = re.sub(r'(?:(?<=[^\d])\d{1,2}[\）\)]|\(\d{1,2}\))', '', raw_combined)
    
    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(raw_combined)
            
    return raw_combined
