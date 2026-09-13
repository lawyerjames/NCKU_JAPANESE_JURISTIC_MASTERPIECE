# NCKU_JAPANESE_JURISTIC_MASTERPIECE

日本法學名著選讀課堂教材讀音譯文轉換，提供掃描 PDF 智慧 OCR（自動判斷單雙欄與去引註）、純 txt 加註漢字讀音、聲調、朗讀停頓底線及中文法律翻譯功能，請搭配 Codex, Claude Code, Cursor 或 Antigravity 使用。

An open-source **Model Context Protocol (MCP)** server for smart PDF OCR extraction (with dynamic 1-column vs 2-column layout detection and footnote filtering), annotating Japanese legal text with furigana (readings + pitch accents), reading pause underlines (`<u>`), and building responsive, stacked top-and-bottom Japanese-Chinese bilingual HTML documents.

---

## 🛠️ 提供之 MCP Tools

- `extract_pdf_smart_ocr(pdf_path, output_path=None, remove_footnotes=True)`:  
  使用 macOS 原生 Vision 引擎進行高精度 OCR 文字辨識，**自動判讀單欄/雙欄/混合論文版面**並修正閱讀順序，同時自動動態過濾頁尾註腳與引註標號。

- `sanitize_japanese_furigana(html_text)`:  
  自動將日文 `<ruby>` 假名限定標記於漢字上，並清除 `<rt>` 中的羅馬字及修復未閉合標籤。

- `audit_furigana_annotations(html_text)`:  
  稽核 `ruby`、`rt`、`u`（紅底線）標籤平衡度，回傳 JSON 格式品質報告。

- `generate_stacked_bilingual_document(japanese_blocks, chinese_translations, title, subtitle, subtitle_zh, author)`:  
  傳入日文段落陣列與中文翻譯陣列，一鍵生成無撞行問題的上下對照網頁。

---

## ✨ 功能特色

- 📄 **智慧 PDF OCR & 版面解析 (Smart PDF OCR & Layout Detection)**：
  - **原生引擎**：調用 macOS Vision Framework，高精準度辨識日文與英文法學文獻。
  - **動態版面辨識**：自動識別「單欄（1-Column）」、「雙欄（2-Column）」與「混合版面（全頁標題 + 雙欄內文）」，自動修復閱讀順序，解決傳統 OCR 跨欄混亂問題。
  - **智慧引註過濾**：自動識別頁尾註腳區塊與內文引註標籤（如 `17）`, `3）` 等），選擇性徹底自動過濾。
- 🎯 **假名標記校對**：自動清理 `<ruby>` 標籤，確保假名注音僅標記於漢字上，清除 `<rt>` 標籤內的羅馬字並修復 HTML 標籤閉合。
- 🔍 **品質稽核報告**：自動稽核 `ruby`、`rt`、`u`（紅底線）標籤數量與平衡度，確保 0 語法錯誤。
- 📱 **上下對照網頁生成**：採用「上方日文原文 + 下方中文譯文」獨立卡片容器排版，搭配 `line-height: 3.1`，徹底解決傳統左右分欄行距碰撞問題。

---

## 🚀 快速開始 (Quick Start)

### 1. 安裝套件 (Installation)

選取本專案並進行開發模式安裝：

```bash
cd mcp-japanese-legal-formatter
pip install -e .
```

### 2. 載入 MCP Server 設定

在您的 `~/.gemini/config/mcp_config.json`（或 Claude Desktop / Cursor 設定檔）中新增以下區塊：

```json
{
  "mcpServers": {
    "japanese-legal-formatter": {
      "command": "python3",
      "args": [
        "-m",
        "mcp_japanese_legal_formatter"
      ]
    }
  }
}
```

---

## 📄 授權條款 (License)

[MIT License](LICENSE)
