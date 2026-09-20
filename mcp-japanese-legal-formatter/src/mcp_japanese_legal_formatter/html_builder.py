import html
import re
import urllib.parse

def build_stacked_bilingual_html(
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
    Builds a responsive, split-screen bilingual Japanese-Chinese HTML document with original PDF viewer iframe, 
    Japanese furigana, pitch accents, TTS audio reader, and responsive PDF zoom controls.
    """
    if heading_indices is None:
        heading_indices = [0]
    
    card_blocks_html = []
    for i in range(len(japanese_blocks)):
        jp_inner = japanese_blocks[i].strip()
        zh_text = chinese_translations[i] if i < len(chinese_translations) else ""
        zh_escaped = html.escape(zh_text).replace('\n', '<br>')
        
        jp_plain = re.sub(r'<rt>.*?</rt>', '', jp_inner)
        jp_plain = re.sub(r'<[^>]+>', '', jp_plain)
        jp_clean = re.sub(r'\s+', ' ', jp_plain).strip()
        
        # Skip empty blocks to prevent phantom cards
        if not jp_clean or jp_clean == '*** EMPTY JP! ***':
            continue
            
        is_heading_block = (
            i in heading_indices or 
            jp_clean.startswith('SPECIAL FEATURE') or
            (jp_clean.startswith('▶') and len(jp_clean) < 60)
        )
        if is_heading_block:
            card = f'''
        <section id="card-{i}" class="my-6 rounded-xl bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white p-5 sm:p-6 shadow-md border border-indigo-900/80 transition-all duration-300">
            <div class="flex items-center justify-between mb-2">
                <h2 class="text-lg sm:text-xl font-bold tracking-wide font-serif text-amber-300">{jp_inner}</h2>
                <button onclick="playCardText({i})" class="shrink-0 flex items-center space-x-1 bg-amber-400/20 hover:bg-amber-400/30 text-amber-300 text-xs font-semibold px-2.5 py-1 rounded-lg border border-amber-400/40 transition-colors">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"></path></svg>
                    <span>朗讀標題</span>
                </button>
            </div>
            <div class="text-sm sm:text-base font-medium text-indigo-200 font-sans">{zh_escaped}</div>
        </section>'''
        else:
            card = f'''
        <article id="card-{i}" class="card-item bg-white rounded-xl shadow-sm border border-slate-200/80 p-5 sm:p-6 my-4 hover:shadow-md transition-all duration-300">
            <!-- Japanese Original Text (Top) -->
            <div class="jp-col font-serif tracking-normal pb-4 border-b border-slate-100 relative group">
                <div class="flex justify-end mb-2">
                    <button onclick="playCardText({i})" class="flex items-center space-x-1 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 text-xs font-semibold px-2.5 py-1 rounded-md border border-indigo-200/60 transition-colors select-none">
                        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"></path></svg>
                        <span>朗讀本段</span>
                    </button>
                </div>
                <div class="jp-text-content">
                    {jp_inner}
                </div>
            </div>
            <!-- Traditional Chinese Translation (Bottom) -->
            <div class="zh-col font-sans tracking-normal pt-4 flex items-start space-x-3">
                <span class="inline-flex items-center justify-center bg-indigo-100 text-indigo-800 text-xs font-bold px-2.5 py-1 rounded mt-0.5 shrink-0 select-none border border-indigo-200/60">
                    譯文
                </span>
                <div class="text-slate-700 font-normal">{zh_escaped}</div>
            </div>
        </article>'''
        card_blocks_html.append(card)

    cards_joint_html = '\n'.join(card_blocks_html)

    subtitle_display = f'{html.escape(subtitle)} <span class="text-indigo-300/80 text-xs font-normal">{html.escape(subtitle_zh)}</span>' if subtitle else html.escape(subtitle_zh)

    return f"""<!DOCTYPE html>
<html lang="zh-TW">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)} - 左右對照朗讀與翻譯版</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- PDF.js library for cross-browser, cross-device HTML5 canvas PDF rendering -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>
    <script>
        if (typeof window !== 'undefined' && window.pdfjsLib) {{
            pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
        }}
    </script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;600;700&family=Noto+Sans+TC:wght@400;500;700&display=swap');
        
        body {{
            font-family: 'Noto Sans TC', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: #0f172a;
            color: #1e293b;
        }}

        .font-serif {{
            font-family: 'Noto Serif JP', "MS Mincho", serif;
        }}

        .font-sans {{
            font-family: 'Noto Sans TC', sans-serif;
        }}

        .jp-col {{
            font-size: 1.05rem;
            line-height: 3.1;
            letter-spacing: 0.02em;
            word-break: break-word;
            color: #0f172a;
        }}

        ruby {{
            ruby-position: over;
            display: inline-ruby;
        }}

        rt {{
            font-size: 0.52em;
            color: #475569;
            letter-spacing: 0.01em;
            font-weight: normal;
            line-height: 1.0;
            user-select: none;
        }}

        u {{
            text-decoration: none;
            border-bottom: 2px solid #ef4444;
            padding-bottom: 2px;
        }}

        .zh-col {{
            font-size: 1.0rem;
            line-height: 1.75;
        }}

        .playing-card {{
            box-shadow: 0 0 0 3px #6366f1, 0 10px 15px -3px rgba(0, 0, 0, 0.1) !important;
            background-color: #f5f3ff !important;
        }}
    </style>
</head>

<body class="h-screen overflow-hidden flex flex-col bg-slate-950">
    <!-- Top Fixed Header -->
    <header class="h-14 bg-slate-950 text-white px-4 sm:px-6 border-b border-slate-800 shrink-0 flex items-center justify-between shadow-md z-40">
        <div class="flex items-center space-x-3 truncate">
            <a href="index.html" class="bg-slate-800 hover:bg-slate-700 text-indigo-300 hover:text-white px-3 py-1.5 rounded-lg text-xs font-semibold border border-slate-700 transition-colors flex items-center space-x-1 shrink-0 select-none">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
                <span>總覽</span>
            </a>
            <h1 class="text-sm sm:text-base font-bold truncate font-serif text-slate-100">
                {html.escape(title)}
            </h1>
        </div>
        <div class="flex items-center space-x-2 shrink-0">
            <button onclick="togglePdfPanel()" class="bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold px-3 py-1.5 rounded-lg transition-colors flex items-center space-x-1 select-none">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                <span id="toggle-pdf-text">隱藏/顯示 原文PDF</span>
            </button>
        </div>
    </header>

    <!-- Split View Container (Height = 100vh - 3.5rem) -->
    <div class="flex-1 flex flex-col lg:flex-row w-full overflow-hidden h-[calc(100vh-3.5rem)]">
        <!-- Left Panel: Fixed Original PDF Viewer with Canvas & Zoom Controls -->
        <div id="pdf-panel" class="w-full lg:w-1/2 h-1/2 lg:h-full bg-slate-900 border-r border-slate-800 flex flex-col shrink-0">
            <!-- PDF Zoom & Control Bar -->
            <div class="bg-slate-950 px-3 py-2 border-b border-slate-800 flex flex-wrap items-center justify-between text-xs shrink-0 select-none gap-2">
                <div class="flex items-center space-x-2">
                    <span class="text-slate-300 font-semibold flex items-center">
                        <svg class="w-3.5 h-3.5 mr-1 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                        原文 PDF
                    </span>
                    <span id="pdf-page-count" class="bg-slate-800 text-indigo-300 text-[11px] px-2 py-0.5 rounded border border-slate-700 font-mono">載入中...</span>
                </div>
                <div class="flex items-center space-x-1.5">
                    <button onclick="zoomPdf(0.9)" class="bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold px-2 py-0.5 rounded border border-slate-700 transition-colors" title="縮小">-</button>
                    <span id="pdf-zoom-val" class="font-mono text-indigo-300 w-12 text-center">100%</span>
                    <button onclick="zoomPdf(1.1)" class="bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold px-2 py-0.5 rounded border border-slate-700 transition-colors" title="放大">+</button>
                    <button onclick="setPdfZoom(1.25)" class="bg-slate-800 hover:bg-slate-700 text-indigo-300 px-2 py-0.5 rounded border border-slate-700 transition-colors hidden sm:inline">1.25x</button>
                    <button onclick="setPdfZoom(1.5)" class="bg-slate-800 hover:bg-slate-700 text-indigo-300 px-2 py-0.5 rounded border border-slate-700 transition-colors hidden sm:inline">1.5x</button>
                    <button onclick="resetPdfZoom()" class="bg-slate-800 hover:bg-slate-700 text-slate-400 px-2 py-0.5 rounded border border-slate-700 transition-colors">重置</button>
                    <a id="pdf-external-link" href="{urllib.parse.quote(pdf_filename)}" target="_blank" class="bg-indigo-600 hover:bg-indigo-500 text-white font-semibold px-2.5 py-0.5 rounded border border-indigo-500 transition-colors flex items-center space-x-1 text-[11px] shadow-sm ml-1" title="在新分頁開啟或下載原文 PDF">
                        <span>新分頁開啟</span>
                        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
                    </a>
                </div>
            </div>
            <!-- PDF Canvas Container with Independent Scrolling -->
            <div id="pdf-container" class="flex-1 w-full h-full overflow-y-auto overflow-x-auto bg-slate-900/90 p-3 sm:p-4 relative">
                <div id="pdf-render-container" class="w-full flex flex-col items-center space-y-4">
                    <!-- Dynamic PDF Pages will be rendered here by PDF.js -->
                </div>
            </div>
        </div>

        <!-- Right Panel: Independently Scrolling Translated Content & Audio Reader -->
        <div id="content-panel" class="w-full lg:w-1/2 h-1/2 lg:h-full bg-slate-950 overflow-y-auto px-4 sm:px-6 lg:px-8 py-6 pb-32 transition-all duration-300">
            <div class="max-w-3xl mx-auto space-y-4">
                <!-- Banner Card -->
                <div class="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white p-6 rounded-2xl shadow-xl border border-indigo-900">
                    <span class="inline-block bg-indigo-500/20 text-indigo-300 text-xs font-semibold px-3 py-1 rounded-full uppercase tracking-wider mb-2 border border-indigo-400/30">
                        法學日文左右對照朗讀版
                    </span>
                    <h2 class="text-xl sm:text-2xl font-bold tracking-tight text-white mb-2 font-serif">
                        {html.escape(title)}
                    </h2>
                    <p class="text-indigo-200 text-sm sm:text-base font-medium mb-3">
                        {subtitle_display}
                    </p>
                    <div class="text-xs text-slate-300 pt-3 border-t border-indigo-900/80">
                        <span class="font-semibold text-indigo-300">作者：</span>{html.escape(author)}
                    </div>
                </div>

                <!-- Main Paragraphs -->
                <main class="space-y-4">
{cards_joint_html}
                </main>
            </div>
        </div>
    </div>

    <!-- Floating Audio Control Bar -->
    <div class="fixed bottom-4 left-1/2 transform -translate-x-1/2 w-11/12 max-w-2xl bg-slate-900/95 backdrop-blur text-white px-5 py-3.5 rounded-2xl shadow-2xl border border-slate-700/80 flex items-center justify-between z-50">
        <div class="flex items-center space-x-3">
            <button id="btn-play-all" onclick="togglePlayAll()" class="bg-indigo-600 hover:bg-indigo-500 text-white font-bold p-2.5 rounded-xl transition-colors shadow-md flex items-center justify-center">
                <svg id="icon-play" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                <svg id="icon-pause" class="w-5 h-5 hidden" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 9v6m4-6v6m7-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            </button>
            <button onclick="stopSpeech()" class="bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold p-2.5 rounded-xl border border-slate-700 transition-colors">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 10a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1v-4z"></path></svg>
            </button>
            <div class="text-xs sm:text-sm">
                <div id="tts-status" class="font-medium text-slate-200">準備朗讀</div>
                <div id="tts-detail" class="text-slate-400 text-xs truncate max-w-[150px] sm:max-w-[200px]">點擊按鈕開啟日文語音朗讀</div>
            </div>
        </div>

        <div class="flex items-center space-x-2">
            <label class="text-xs text-slate-400 select-none hidden sm:inline">語速</label>
            <select id="select-rate" onchange="changeRate()" class="bg-slate-800 text-xs text-slate-200 border border-slate-700 rounded-lg px-2 py-1.5 focus:outline-none focus:border-indigo-500">
                <option value="0.75">0.75x</option>
                <option value="1.0" selected>1.0x (標準)</option>
                <option value="1.25">1.25x</option>
                <option value="1.5">1.5x</option>
            </select>
        </div>
    </div>

    <!-- Speech Synthesis & PDF Zoom JavaScript -->
    <script>
        let synth = window.speechSynthesis;
        let currentUtterance = null;
        let playQueue = [];
        let currentCardIndex = -1;
        let isPlayingAll = false;
        let speechRate = 1.0;
        let japaneseVoice = null;
        
        // ================= PDF.js ENGINE =================
        let pdfDoc = null;
        let currentPdfZoom = 1.0;
        let isPdfRendering = false;
        const pdfBaseSrc = '{urllib.parse.quote(pdf_filename)}';

        function setPdfZoom(scaleFactor) {{
            currentPdfZoom = scaleFactor;
            applyPdfZoom();
        }}

        function zoomPdf(ratio) {{
            currentPdfZoom = Math.max(0.5, Math.min(3.0, currentPdfZoom * ratio));
            applyPdfZoom();
        }}

        function resetPdfZoom() {{
            currentPdfZoom = 1.0;
            applyPdfZoom();
        }}

        function applyPdfZoom() {{
            const zoomPercent = Math.round(currentPdfZoom * 100);
            const zoomEl = document.getElementById('pdf-zoom-val');
            if (zoomEl) zoomEl.textContent = zoomPercent + '%';
            if (pdfDoc) {{
                renderAllPdfPages();
            }}
        }}

        async function initPdfViewer() {{
            const container = document.getElementById('pdf-render-container');
            const pageCountEl = document.getElementById('pdf-page-count');
            
            if (typeof window.pdfjsLib === 'undefined') {{
                console.warn('PDF.js not loaded, falling back to native iframe');
                fallbackToNativeIframe();
                return;
            }}

            container.innerHTML = `
                <div class="flex flex-col items-center justify-center py-20 text-slate-400 space-y-3">
                    <svg class="animate-spin w-8 h-8 text-indigo-500" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    <div class="text-xs font-medium text-slate-300">正在透過 HTML5 引擎載入原文 PDF...</div>
                </div>
            `;

            try {{
                const loadingTask = pdfjsLib.getDocument({{
                    url: pdfBaseSrc,
                    cMapUrl: 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/cmaps/',
                    cMapPacked: true
                }});
                pdfDoc = await loadingTask.promise;
                if (pageCountEl) pageCountEl.textContent = `共 ${{pdfDoc.numPages}} 頁`;
                await renderAllPdfPages();
            }} catch (err) {{
                console.error('PDF.js loading failed:', err);
                fallbackToNativeIframe();
            }}
        }}

        async function renderAllPdfPages() {{
            if (!pdfDoc || isPdfRendering) return;
            isPdfRendering = true;
            const container = document.getElementById('pdf-render-container');
            container.innerHTML = '';
            
            const pdfContainerEl = document.getElementById('pdf-container');
            const containerWidth = (pdfContainerEl ? pdfContainerEl.clientWidth : 500) - 36;
            
            for (let pageNum = 1; pageNum <= pdfDoc.numPages; pageNum++) {{
                try {{
                    const page = await pdfDoc.getPage(pageNum);
                    const unscaledViewport = page.getViewport({{ scale: 1.0 }});
                    
                    let baseScale = containerWidth > 200 ? (containerWidth / unscaledViewport.width) : 1.1;
                    const scale = baseScale * currentPdfZoom;
                    const viewport = page.getViewport({{ scale: scale }});
                    
                    const pageCard = document.createElement('div');
                    pageCard.className = 'w-full flex flex-col items-center mb-6';
                    pageCard.id = 'pdf-page-' + pageNum;
                    
                    const badge = document.createElement('div');
                    badge.className = 'text-[11px] font-mono text-slate-400 mb-1.5 flex items-center space-x-1.5';
                    badge.innerHTML = `<span class="bg-slate-800 text-slate-300 px-2 py-0.5 rounded border border-slate-700">第 ${{pageNum}} / ${{pdfDoc.numPages}} 頁</span>`;
                    
                    const canvas = document.createElement('canvas');
                    canvas.className = 'rounded-lg shadow-xl max-w-full bg-white border border-slate-700 transition-all';
                    const context = canvas.getContext('2d');
                    
                    const outputScale = window.devicePixelRatio || 1;
                    canvas.width = Math.floor(viewport.width * outputScale);
                    canvas.height = Math.floor(viewport.height * outputScale);
                    canvas.style.width = Math.floor(viewport.width) + 'px';
                    canvas.style.height = Math.floor(viewport.height) + 'px';
                    
                    const transform = outputScale !== 1 ? [outputScale, 0, 0, outputScale, 0, 0] : null;
                    
                    pageCard.appendChild(badge);
                    pageCard.appendChild(canvas);
                    container.appendChild(pageCard);
                    
                    await page.render({{
                        canvasContext: context,
                        transform: transform,
                        viewport: viewport
                    }}).promise;
                }} catch (pageErr) {{
                    console.error(`Error rendering page ${{pageNum}}:`, pageErr);
                }}
            }}
            isPdfRendering = false;
        }}

        function fallbackToNativeIframe() {{
            const container = document.getElementById('pdf-render-container');
            const pageCountEl = document.getElementById('pdf-page-count');
            if (pageCountEl) pageCountEl.textContent = '原生預覽';
            container.innerHTML = `
                <div class="w-full h-full min-h-[500px] flex flex-col">
                    <div class="p-3 bg-indigo-950/40 border border-indigo-500/30 rounded-lg text-xs text-indigo-200 mb-3 flex items-center justify-between">
                        <span>如瀏覽器未直接顯示 PDF，請點擊右側按鈕：</span>
                        <a href="${{pdfBaseSrc}}" target="_blank" class="bg-indigo-600 hover:bg-indigo-500 text-white font-bold px-3 py-1 rounded">在新分頁開啟</a>
                    </div>
                    <iframe id="pdf-frame" src="${{pdfBaseSrc}}" class="w-full flex-1 min-h-[600px] rounded-xl bg-white shadow-inner border border-slate-700"></iframe>
                </div>
            `;
        }}

        window.addEventListener('DOMContentLoaded', () => {{
            initPdfViewer();
        }});

        function togglePdfPanel() {{
            const pdfPanel = document.getElementById('pdf-panel');
            const contentPanel = document.getElementById('content-panel');
            if (pdfPanel.classList.contains('hidden')) {{
                pdfPanel.classList.remove('hidden');
                contentPanel.className = 'w-full lg:w-1/2 h-1/2 lg:h-full bg-slate-950 overflow-y-auto px-4 sm:px-6 lg:px-8 py-6 pb-32 transition-all duration-300';
            }} else {{
                pdfPanel.classList.add('hidden');
                contentPanel.className = 'w-full lg:w-full h-full bg-slate-950 overflow-y-auto px-4 sm:px-6 lg:px-8 py-6 pb-32 transition-all duration-300';
            }}
        }}

        function loadVoices() {{
            let voices = synth.getVoices();
            japaneseVoice = voices.find(v => v.lang === 'ja-JP' || v.lang.startsWith('ja')) || null;
        }}

        if (speechSynthesis.onvoiceschanged !== undefined) {{
            speechSynthesis.onvoiceschanged = loadVoices;
        }}
        loadVoices();

        function getCleanText(cardId) {{
            const cardEl = document.getElementById('card-' + cardId);
            if (!cardEl) return '';
            
            let targetEl = cardEl.querySelector('.jp-text-content') || cardEl.querySelector('h2') || cardEl;
            const clone = targetEl.cloneNode(true);
            
            const rts = clone.querySelectorAll('rt');
            rts.forEach(rt => rt.remove());
            
            let text = clone.textContent || '';
            text = text.replace(/\\(\\d+\\)/g, '')
                       .replace(/朗讀本段|朗讀標題/g, '')
                       .replace(/^[▶・★\\s]+/g, '')
                       .replace(/[①-⑳]/g, '')
                       .replace(/(?:(?<=[^\\d])\\d{1,2}[\\）\\)]|\\(\\d{1,2}\\))/g, '')
                       .trim();
            return text;
        }}

        function highlightCard(index) {{
            document.querySelectorAll('.playing-card').forEach(el => el.classList.remove('playing-card'));
            if (index >= 0) {{
                const el = document.getElementById('card-' + index);
                if (el) {{
                    el.classList.add('playing-card');
                    el.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                }}
            }}
        }}

        function updateUIState(playing) {{
            const iconPlay = document.getElementById('icon-play');
            const iconPause = document.getElementById('icon-pause');
            const statusEl = document.getElementById('tts-status');
            
            if (playing) {{
                iconPlay.classList.add('hidden');
                iconPause.classList.remove('hidden');
                statusEl.textContent = '朗讀中...';
            }} else {{
                iconPlay.classList.remove('hidden');
                iconPause.classList.add('hidden');
                statusEl.textContent = '已暫停 / 準備就緒';
            }}
        }}

        function playCardText(index) {{
            stopSpeech();
            isPlayingAll = false;
            currentCardIndex = index;
            const text = getCleanText(index);
            if (!text) return;
            
            speakText(text, index, () => {{
                highlightCard(-1);
                updateUIState(false);
                document.getElementById('tts-detail').textContent = '朗讀完成';
            }});
        }}

        function speakText(text, cardIndex, onEndCallback) {{
            if (synth.speaking) synth.cancel();
            
            highlightCard(cardIndex);
            updateUIState(true);
            document.getElementById('tts-detail').textContent = text.substring(0, 30) + '...';
            
            currentUtterance = new SpeechSynthesisUtterance(text);
            currentUtterance.lang = 'ja-JP';
            if (japaneseVoice) currentUtterance.voice = japaneseVoice;
            currentUtterance.rate = speechRate;
            
            currentUtterance.onend = function() {{
                if (onEndCallback) onEndCallback();
            }};
            
            currentUtterance.onerror = function(e) {{
                console.error('Speech synthesis error:', e);
                highlightCard(-1);
                updateUIState(false);
            }};
            
            synth.speak(currentUtterance);
        }}

        function togglePlayAll() {{
            if (synth.speaking && isPlayingAll) {{
                if (synth.paused) {{
                    synth.resume();
                    updateUIState(true);
                }} else {{
                    synth.pause();
                    updateUIState(false);
                }}
                return;
            }}
            
            stopSpeech();
            isPlayingAll = true;
            let totalCards = document.querySelectorAll('[id^="card-"]').length;
            let queue = [];
            for (let i = 0; i < totalCards; i++) {{
                queue.push(i);
            }}
            
            playNextInQueue(queue);
        }}

        function playNextInQueue(queue) {{
            if (!isPlayingAll || queue.length === 0) {{
                isPlayingAll = false;
                highlightCard(-1);
                updateUIState(false);
                document.getElementById('tts-detail').textContent = '全文朗讀完畢';
                return;
            }}
            
            let nextIndex = queue.shift();
            currentCardIndex = nextIndex;
            const text = getCleanText(nextIndex);
            
            if (!text) {{
                playNextInQueue(queue);
                return;
            }}
            
            speakText(text, nextIndex, () => {{
                if (isPlayingAll) playNextInQueue(queue);
            }});
        }}

        function stopSpeech() {{
            isPlayingAll = false;
            if (synth.speaking || synth.paused) {{
                synth.cancel();
            }}
            highlightCard(-1);
            updateUIState(false);
            document.getElementById('tts-detail').textContent = '已停止朗讀';
        }}

        function changeRate() {{
            const select = document.getElementById('select-rate');
            speechRate = parseFloat(select.value);
            if (synth.speaking && currentCardIndex >= 0) {{
                let wasPlayingAll = isPlayingAll;
                let cardToResume = currentCardIndex;
                stopSpeech();
                if (wasPlayingAll) {{
                    isPlayingAll = true;
                    let totalCards = document.querySelectorAll('[id^="card-"]').length;
                    let queue = [];
                    for (let i = cardToResume; i < totalCards; i++) queue.push(i);
                    playNextInQueue(queue);
                }} else {{
                    playCardText(cardToResume);
                }}
            }}
        }}
    </script>
</body>

</html>
"""
