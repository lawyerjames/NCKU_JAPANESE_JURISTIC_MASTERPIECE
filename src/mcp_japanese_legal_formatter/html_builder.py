import html

def build_stacked_bilingual_html(
    japanese_blocks: list[str],
    chinese_translations: list[str],
    title: str = "デジタル時代に対応する刑事訴訟法",
    subtitle: str = "——我が国の刑事手続を規律する基本原理",
    subtitle_zh: str = "（規範我國刑事程序之基本原理）",
    author: str = "山田峻悠（中京大学准教授 / YAMADA Takaharu）",
    heading_indices: list[int] = None
) -> str:
    """
    Builds a responsive, stacked top-and-bottom bilingual Japanese-Chinese HTML document.
    """
    if heading_indices is None:
        heading_indices = [0]
    
    card_blocks_html = []
    for i in range(len(japanese_blocks)):
        jp_inner = japanese_blocks[i].strip()
        zh_text = chinese_translations[i] if i < len(chinese_translations) else ""
        zh_escaped = html.escape(zh_text).replace('\n', '<br>')
        
        if i in heading_indices or jp_inner.startswith('▶') or jp_inner.startswith('Ⅰ') or jp_inner.startswith('Ⅱ') or jp_inner.startswith('Ⅲ') or jp_inner.startswith('★'):
            card = f'''
        <section id="card-{i}" class="my-8 rounded-xl bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white p-6 shadow-md border border-indigo-900/80 transition-all duration-300">
            <div class="flex items-center justify-between mb-2">
                <h2 class="text-xl sm:text-2xl font-bold tracking-wide font-serif text-amber-300">{jp_inner}</h2>
                <button onclick="playCardText({i})" class="shrink-0 flex items-center space-x-1 bg-amber-400/20 hover:bg-amber-400/30 text-amber-300 text-xs font-semibold px-3 py-1.5 rounded-lg border border-amber-400/40 transition-colors">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"></path></svg>
                    <span>朗讀標題</span>
                </button>
            </div>
            <div class="text-base sm:text-lg font-medium text-indigo-200 font-sans">{zh_escaped}</div>
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

    return f"""<!DOCTYPE html>
<html lang="zh-TW">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)} - 上下對照朗讀與翻譯版</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;600;700&family=Noto+Sans+TC:wght@400;500;700&display=swap');
        
        body {{
            font-family: 'Noto Sans TC', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: #f8fafc;
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

<body class="py-8 px-4 sm:px-6 lg:px-8 pb-28">
    <div class="max-w-4xl mx-auto bg-white rounded-2xl shadow-xl border border-gray-200/80 overflow-hidden">
        <!-- Document Header -->
        <header class="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white py-8 px-6 sm:px-10 border-b border-indigo-900 shadow-lg">
            <div class="max-w-3xl">
                <span class="inline-block bg-indigo-500/20 text-indigo-300 text-xs font-semibold px-3 py-1 rounded-full uppercase tracking-wider mb-3 border border-indigo-400/30">
                    法學日文上下對照朗讀版
                </span>
                <h1 class="text-2xl sm:text-3xl font-bold tracking-tight text-white mb-2 font-serif">
                    {html.escape(title)}
                </h1>
                <p class="text-indigo-200 text-base sm:text-lg font-medium mb-3">
                    {html.escape(subtitle)} <span class="text-indigo-300/80 text-sm font-normal">{html.escape(subtitle_zh)}</span>
                </p>
                <div class="flex items-center text-xs sm:text-sm text-slate-300 pt-3 border-t border-indigo-900/80 mt-2">
                    <span class="font-semibold text-indigo-300">作者：</span>
                    <span class="ml-1.5 text-slate-200">{html.escape(author)}</span>
                </div>
            </div>
        </header>

        <!-- Document Content -->
        <main class="p-4 sm:p-6 lg:p-8 space-y-2">
{''.join(card_blocks_html)}
        </main>

        <!-- Footer -->
        <footer class="bg-slate-50 border-t border-slate-200 py-6 px-8 text-center text-sm text-slate-500">
            <p>{html.escape(title)} — 上下對照朗讀與翻譯版</p>
        </footer>
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
                <div id="tts-detail" class="text-slate-400 text-xs truncate max-w-[150sm:250px]">點擊按鈕開啟日文語音朗讀</div>
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

    <!-- Speech Synthesis JavaScript -->
    <script>
        let synth = window.speechSynthesis;
        let currentUtterance = null;
        let playQueue = [];
        let currentCardIndex = -1;
        let isPlayingAll = false;
        let speechRate = 1.0;
        let japaneseVoice = null;

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
            
            // Critical fix: Remove all rt elements so furigana and pitch accent numbers (0), (1) are NOT read out by speech engine
            const rts = clone.querySelectorAll('rt');
            rts.forEach(rt => rt.remove());
            
            let text = clone.textContent || '';
            // Remove remaining pitch accent numbers or button text
            text = text.replace(/\\(\\d+\\)/g, '').replace(/朗讀本段|朗讀標題/g, '').trim();
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

