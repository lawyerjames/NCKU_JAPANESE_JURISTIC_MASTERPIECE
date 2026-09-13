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
        <section class="my-8 rounded-xl bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white p-6 shadow-md border border-indigo-900/80">
            <h2 class="text-xl sm:text-2xl font-bold tracking-wide font-serif text-amber-300 mb-1.5">{jp_inner}</h2>
            <div class="text-base sm:text-lg font-medium text-indigo-200 font-sans">{zh_escaped}</div>
        </section>'''
        else:
            card = f'''
        <article class="bg-white rounded-xl shadow-sm border border-slate-200/80 p-5 sm:p-6 my-4 hover:shadow-md transition-shadow">
            <!-- Japanese Original Text (Top) -->
            <div class="jp-col font-serif tracking-normal pb-4 border-b border-slate-100">
                {jp_inner}
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
    </style>
</head>

<body class="py-8 px-4 sm:px-6 lg:px-8">
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
</body>

</html>
"""
