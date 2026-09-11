# Plan: 第9次翻转的全屏庆祝效果

## Summary

将第9次翻转后的普通弹窗改为全屏"HAPPY 9TH ANNIVERSARY!"庆祝效果，包含烟花、彩纸爆炸、会员照片全亮、9个C单词环绕飘浮，点击屏幕任意位置消失。

## Current State

- `closing_remark.html` 第392-396行定义了3个里程碑（3/6/9次翻转）
- `checkMilestone()` 函数（404-418行）在第9次翻转时显示普通弹窗，内容为"All Nine United"
- 弹窗使用 `.modal-overlay` + `.modal` 样式（196-217行），与第3次和第6次翻转的弹窗完全相同
- 页面已有一个轻量 confetti 层（37-40行，18个慢速飘浮emoji）
- 24张会员照片以 opacity 0.6 散布在背景中

## Proposed Changes

### 文件：`closing_remark.html`

### 1. CSS：新增全屏庆祝层样式

新增 `.celebration` 覆盖层：
- `position:fixed; inset:0; z-index:200` — 在所有元素之上
- `background:radial-gradient(circle at center, rgba(255,215,0,.15), transparent 60%), rgba(10,5,20,.85)` — 金色光晕从中心散开 + 半透明深色遮罩
- `display:none` 默认隐藏，`.show` 时 `display:flex`

中心文字：
- `font-size:clamp(2.5rem, 8vw, 6rem)` — 大字
- `font-weight:900; font-style:italic` — Playfair Display 斜体粗
- `background:linear-gradient(135deg, #ffd700, #ff5c8d, #667eea)` — 三色渐变
- `-webkit-background-clip:text` — 渐变文字
- `filter:drop-shadow(0 0 30px rgba(255,215,0,.5))` — 金色发光
- 弹入动画：`scale(0) rotate(-10deg)` → `scale(1) rotate(0)`，弹性缓动 1s

底部提示：
- "Tap anywhere to continue" — 小字，闪烁动画

### 2. CSS：烟花粒子样式（从文字背后爆发）

新增 `.firework` 烟花粒子：
- 所有粒子从文字中心位置（`left:50%; top:50%`）爆发
- 每个粒子是一个小圆点，`position:absolute`
- 使用 CSS 自定义属性 `--tx` 和 `--ty` 控制爆炸方向（360度均匀分布）
- 粒子 `z-index` 在文字之下（文字 z-index:10，粒子 z-index:5），从文字背后透出
- `animation:fireworkBurst 1.5s ease-out forwards` — 从文字背后向四周扩散
- `@keyframes fireworkBurst`：
  - `0%: transform:translate(-50%,-50%) scale(0); opacity:0` — 从中心零尺寸开始
  - `15%: transform:translate(-50%,-50%) scale(1.5); opacity:1` — 快速放大爆发
  - `100%: transform:translate(calc(-50% + var(--tx)), calc(-50% + var(--ty))) scale(0); opacity:0` — 向外飞散消失
- 粒子颜色随机从金/粉/蓝/绿/紫中选取
- 分两波爆发：第一波 60 个粒子，0ms 触发；第二波 40 个粒子，800ms 触发（持续感）
- 每个粒子的 `--tx`/`--ty` 按极坐标计算：`angle = 随机 0-360°, distance = 200-500px`

### 3. CSS：彩纸爆炸样式（从文字背后射出）

新增 `.confetti-burst` 彩纸条：
- 与现有 `.cf` 不同，这是爆炸式的
- 同样从文字中心位置爆发，`z-index:5`（在文字背后）
- `--tx`/`--ty` 控制方向，带旋转
- `animation:confettiExplode 2s ease-out forwards`
- `@keyframes confettiExplode`：
  - `0%: transform:translate(-50%,-50%) rotate(0) scale(0); opacity:0`
  - `10%: opacity:1; transform:translate(-50%,-50%) rotate(180deg) scale(1)`
  - `100%: transform:translate(calc(-50% + var(--tx)), calc(-50% + var(--ty))) rotate(720deg) scale(0.5); opacity:0`
- 多种形状：长条矩形(8x24px) + 圆形(8x8px) + 星形(emoji)
- 颜色使用九宫格的9种主题色
- 50 个彩纸条，与烟花同时触发

### 4. CSS：9个C单词环绕飘浮

新增 `.c-word`：
- 9个单词从屏幕中心向外扩散，缓慢飘浮
- `position:absolute`，使用 `--angle` 和 `--radius` 控制位置
- `animation:wordOrbit 8s ease-in-out infinite` — 缓慢公转 + 自转
- 颜色与对应卡片背面的颜色一致
- `opacity:0.7`，不抢中心文字的视觉

### 5. CSS：会员照片全亮

- 庆祝触发时，所有 `.member-photo` 的 opacity 从 0.6 升到 0.9
- 添加 `.member-photo.celebrate { opacity:0.9; filter:drop-shadow(0 2px 20px rgba(255,215,0,.2)) }`
- 过渡时间 1.5s，缓慢渐变

### 6. JS：修改 `checkMilestone()`

第9次翻转时不再走普通弹窗逻辑：
```
if(flipCount===9){
  triggerCelebration();
  return; // 不显示普通弹窗
}
```

### 7. JS：`triggerCelebration()` 函数

- 显示 `.celebration` 层
- 触发烟花：从文字中心位置生成两波粒子（第一波60个0ms，第二波40个800ms），按极坐标计算 `--tx`/`--ty` 散射方向
- 触发彩纸：从文字中心生成50个彩纸条，随机角度和距离
- 所有会员照片添加 `.celebrate` 类
- 9个C单词动态生成并添加到庆祝层
- 底部 footer 更新为 "C_Life 2026 · To be continued"
- 点击屏幕任意位置：隐藏庆祝层，烟花和彩纸元素移除

### 8. JS：复位按钮同步

复位时同时隐藏庆祝层，移除 `.celebrate` 类，清理烟花/彩纸 DOM。

### 9. 保留前两个里程碑弹窗不变

第3次和第6次翻转仍然使用普通弹窗（Three of a Kind / Halfway There），只有第9次使用全屏庆祝。

## Assumptions & Decisions

- 不修改前两个里程碑弹窗，只改第9个
- 烟花和彩纸用纯 CSS + JS DOM 动态生成，不依赖外部库
- 点击任意位置关闭庆祝层，关闭后页面回到正常状态（所有照片保持0.9透明度可见）
- 9个C单词关闭后也移除，不留在页面上
- 庆祝层的 z-index=200，高于弹窗(100)和复位按钮(20)

## Verification

1. 翻转9张卡片，确认全屏庆祝效果出现
2. 确认烟花在5个位置炸开
3. 确认彩纸从中心向四周射出
4. 确认"HAPPY 9TH ANNIVERSARY!"文字大且有渐变发光
5. 确认9个C单词环绕飘浮
6. 确认所有24张会员照片从0.6升到0.9透明度
7. 点击屏幕任意位置，确认庆祝层消失
8. 确认前3次和6次翻转的弹窗不受影响
9. 点击复位按钮，确认所有状态正确重置
