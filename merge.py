import re

base = r'C:\Users\贺靖茹\AppData\Roaming\TRAE SOLO CN\ModularData\ai-agent\work-mode-projects\6a48da929047ff4eccbf5a53\clife-annual-report'

with open(base + r'\part1.html', 'r', encoding='utf-8') as f:
    p1 = f.read()
with open(base + r'\part2.html', 'r', encoding='utf-8') as f:
    p2 = f.read()

p1_lines = p1.split('\n')

# Find slide 17 start (closing page to remove)
slide17_start = None
for i, line in enumerate(p1_lines):
    if 'data-slide="17"' in line:
        slide17_start = i
        break

# Find stage closing </div> after slide 17
stage_close = None
for i in range(slide17_start + 1, len(p1_lines)):
    if '</div>' in p1_lines[i] and '<!--' not in p1_lines[i]:
        stage_close = i
        break

# Part1 before slide 17 (CSS + slides 0-16)
p1_before = '\n'.join(p1_lines[:slide17_start])
# Part1 controls + JS after stage close
p1_after = '\n'.join(p1_lines[stage_close+1:])

# Part2: extract ALL slides (0-11), keep cover
p2_lines = p2.split('\n')
# Find first slide
slide2_start = None
for i, line in enumerate(p2_lines):
    if 'data-slide="0"' in line and '<section' in line:
        slide2_start = i
        break
# Find last </section>
slide2_end = None
for i in range(len(p2_lines)-1, 0, -1):
    if '</section>' in p2_lines[i]:
        slide2_end = i
        break

p2_slides = '\n'.join(p2_lines[slide2_start:slide2_end+1])

# Renumber part2 slides: 0->17, 1->18, ..., 11->28
for old_num in range(11, -1, -1):
    new_num = old_num + 17
    p2_slides = p2_slides.replace(f'data-slide="{old_num}"', f'data-slide="{new_num}"')

# Add "PART 1" to part1 cover (slide 0)
# Find the cover slide and add PART 1 text
p1_before = p1_before.replace(
    '<p class="r cover-year d4">NINE YEARS OF GROWTH</p>',
    '<p class="r cover-year d4">NINE YEARS OF GROWTH</p>\n    <p class="r brand d5" style="margin-top:1.5rem">PART 1</p>'
)

# Add "PART 2" to part2 cover (now slide 17)
# Part2 cover has: <p class="r cover-year d4">一起来回顾下C_Life在这一年的精彩瞬间吧~</p>
p2_slides = p2_slides.replace(
    '<p class="r cover-year d4">一起来回顾下C_Life在这一年的精彩瞬间吧~</p>',
    '<p class="r cover-year d4">一起来回顾下C_Life在这一年的精彩瞬间吧~</p>\n    <p class="r brand d5" style="margin-top:1.5rem">PART 2</p>'
)

# Part2 unique CSS
p2_unique_css = """
  /* === part2: scrapbook / polaroid / edit mode === */
  .bg-emoji{position:absolute;font-size:38vh;line-height:1;opacity:.04;z-index:0;user-select:none;pointer-events:none}
  .scrapbook{position:relative;width:92%;max-width:960px;height:62vh;margin-top:1.2rem}
  .title-group{position:relative;top:-30px;text-align:center}
  .polaroid,.vid-frame,.vid-ph{
    position:absolute;background:#fff;padding:10px;border-radius:4px;
    box-shadow:0 8px 24px rgba(0,0,0,.14),0 2px 8px rgba(0,0,0,.08);
    opacity:0;transform:translateY(40px) scale(.75) rotate(var(--rot,0deg));
    transition:opacity .6s ease,transform .8s cubic-bezier(.34,1.56,.64,1)}
  .slide.active .polaroid,
  .slide.active .vid-frame,
  .slide.active .vid-ph{opacity:1;transform:rotate(var(--rot,0deg))}
  .slide.active .pd1{transition-delay:.3s}
  .slide.active .pd2{transition-delay:.5s}
  .slide.active .pd3{transition-delay:.7s}
  .slide.active .pd4{transition-delay:.9s}
  .polaroid{max-width:500px}
  .polaroid img{display:block;width:100%;height:auto;border-radius:2px}
  .vid-frame video{display:block;border-radius:2px;width:100%;height:auto}
  .unmute-btn{position:absolute;top:18px;right:18px;background:rgba(0,0,0,.45);color:#fff;border:none;
    border-radius:999px;padding:4px 10px;font-size:.75rem;cursor:pointer;backdrop-filter:blur(4px);z-index:5}
  .vid-ph{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:.6rem;
    background:rgba(255,255,255,.5);border:2px dashed rgba(255,92,141,.3)}
  .vid-ph .icon{font-size:2.2rem}
  .vid-ph .text{color:var(--muted);font-size:.82rem;letter-spacing:.1em}
  .center-box{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:1rem;
    border:2px dashed rgba(255,92,141,.3);border-radius:16px;padding:3rem 4rem;
    background:rgba(255,255,255,.5);color:var(--muted)}
  .center-box .icon{font-size:3rem}
  .center-box .text{font-size:1rem;letter-spacing:.12em}
  @media(max-width:900px){.scrapbook{height:50vh}.polaroid{max-width:180px!important}.polaroid img{width:100%!important}}
  /* edit mode */
  .edit-toggle{font-size:1.1rem}
  body.edit-mode .slide.active .polaroid,
  body.edit-mode .slide.active .vid-frame,
  body.edit-mode .slide.active .vid-ph{cursor:grab;opacity:1;transform:rotate(var(--rot,0deg));transition:none;touch-action:none}
  body.edit-mode .polaroid.dragging,
  body.edit-mode .vid-frame.dragging,
  body.edit-mode .vid-ph.dragging{cursor:grabbing;z-index:20}
  body.edit-mode .polaroid.selected,
  body.edit-mode .vid-frame.selected,
  body.edit-mode .vid-ph.selected{box-shadow:0 0 0 3px var(--accent),0 0 0 6px rgba(255,92,141,.2)}
  .resize-handle{display:none;position:absolute;bottom:-7px;right:-7px;width:16px;height:16px;background:var(--accent);border:2px solid #fff;border-radius:50%;cursor:nwse-resize;z-index:10;touch-action:none}
  body.edit-mode .selected .resize-handle{display:block}
  body.edit-mode .controls{bottom:220px}
  body.edit-mode .helper{display:none}
  .edit-help{display:none;position:fixed;top:1rem;left:1.2rem;background:rgba(255,255,255,.92);padding:8px 14px;border-radius:8px;font-size:.72rem;color:var(--ink);z-index:100;border:1px solid var(--rule)}
  body.edit-mode .edit-help{display:block}
  .code-panel{display:none;position:fixed;bottom:0;left:0;right:0;background:#1a1a2e;color:#a6e3a1;padding:12px 16px;font-family:Consolas,'Cascadia Code',monospace;font-size:11px;line-height:1.5;z-index:100;max-height:200px;overflow:auto;border-top:2px solid var(--accent)}
  body.edit-mode .code-panel{display:block}
  .code-panel pre{white-space:pre-wrap;word-break:break-all;margin:0}
  .copy-code-btn{position:sticky;top:0;float:right;background:var(--accent);color:#fff;border:none;border-radius:6px;padding:5px 12px;font-size:11px;cursor:pointer;margin-bottom:4px}
  .copy-code-btn:hover{background:var(--accent2);color:var(--ink)}
  .save-file-btn{position:sticky;top:0;float:right;background:var(--accent3);color:#fff;border:none;border-radius:6px;padding:5px 12px;font-size:11px;cursor:pointer;margin:0 4px 4px 0}
  .save-file-btn:hover{background:var(--accent2);color:var(--ink)}
"""

# Insert part2 CSS before close-title in part1
p1_before = p1_before.replace('  .close-title{', p2_unique_css + '\n  .close-title{')

# Build merged JS
p1_js_start = p1.index('<script>') + 8
p1_js_end = p1.index('</script>')
p1_js = p1[p1_js_start:p1_js_end]

p2_js_start = p2.index('<script>') + 8
p2_js_end = p2.index('</script>')
p2_js = p2[p2_js_start:p2_js_end]

# Part1 data (LB, TTM, CATS, buildLane, buildBars, awards)
p1_data_end = p1_js.index('var slides=')
p1_data = p1_js[:p1_data_end]

# Part2 navigation + video + edit mode
p2_nav_start = p2_js.index('var slides=')
p2_nav = p2_js[p2_nav_start:]

# Update storage key and save filename
p2_nav = p2_nav.replace('clife_part2_layout', 'clife_merged_layout')
p2_nav = p2_nav.replace("'part2.html'", "'clife-merged.html'")

merged_js = p1_data + p2_nav

# Controls HTML
controls = """</div>

<div class="progress" id="progress"></div>
<div class="helper" id="helper"><kbd>←</kbd><kbd>→</kbd> 翻页 · <kbd>空格</kbd> 切换模式</div>
<div class="controls">
  <button class="ctrl-btn" id="prev" title="上一页">‹</button>
  <div class="dots" id="dots"></div>
  <button class="ctrl-btn" id="next" title="下一页">›</button>
  <button class="ctrl-btn" id="play" title="切换自动/手动">❚❚ 自动</button>
  <button class="ctrl-btn edit-toggle" id="edit" title="布局编辑">📐</button>
</div>

<div class="edit-help" id="editHelp">📐 拖拽移动 · 拖右下角⚪调整大小 · 选中后 ←→ 旋转</div>
<div class="code-panel" id="codePanel"><button class="save-file-btn" id="saveFile">💾 保存到文件</button><button class="copy-code-btn" id="copyCode">复制代码</button><pre id="codeOutput"></pre></div>

<script>"""

final = p1_before + '\n\n' + p2_slides + '\n\n' + controls + '\n' + merged_js + '\n</script>\n</body>\n</html>'

out_path = base + r'\desktop.html'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(final)

print(f'Done! Written to {out_path}')
print(f'Total slides: 29 (0-28)')
print(f'Part1: slides 0-16 (with PART 1 on cover)')
print(f'Part2: slides 17-28 (with PART 2 on cover)')
