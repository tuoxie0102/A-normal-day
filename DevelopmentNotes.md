# DevelopmentNotes

## 本次修复重点

1. 先恢复运行

- 实测以本地 HTTP 方式打开 `prototype.html`，页面可进入。
- 已排查并修复对白解析为空导致的"页面几乎什么都不显示"问题。
- 已补 `favicon` 占位，复测时未再出现 404。

2. 收口对白显示规则

- 对话框现在只保留真正说出口的话。
- 开头括号里的动作说明会在解析阶段被剥离，不再直接塞进对白框。
- 环境提示继续单独显示在场景中间。

3. 恢复五个核心页面

- 家庭开场
- 世界观 / 开始相亲页
- 相亲对象选择页
- 对话页
- 日记页

以上页面已在浏览器运行态下逐页验证。

4. 去掉人物白底

- 当前页面已切换为使用 `generated_characters/*.png`。
- 原始素材保留在 `assets/characters/*.png`，方便后续对比或重出。

## 仍然保留的范围控制

- 没有新增玩法。
- 没有新增剧情。
- 没有扩展世界结构。
- 只修运行、对白、页面节奏和立绘呈现。

## 当前已知剩余问题

- 早餐 Parser 已能读 Day 1-4（2026-06-27），但渲染层 STATE 仍只取 Day 1；Day 2-4 切换还没串进试玩流程，需要新增 `STATE.breakfastDay` 路由。
- 宋潇对白文件仍在仓库里，但当前 Demo 没有接入对应流程。
- 程序抠底已经可用，但如果要做正式展示，建议后续补原生透明 PNG。

---

## Flow Concerns Found During Slice Build

> 由原 `Development Notes.md`（带空格副本）合并而来，2026-06-27。

### 0. Previous dialogue rhythm felt like answering test questions

Why it felt off:
The old interaction loop forced the player to choose right after a single NPC line, which read like a quiz instead of a date.

What changed in this pass:
The demo now prototypes three pacing models where each Block has a listening phase first, then a response phase.

What still needs playtest validation:
Whether the best feeling comes from autoplay conversation, continuous chat flow, or cinematic pause-and-respond timing.

### 1. Coffee scene now includes candidate selection

Why it may feel off:
The current coffee scene is doing two jobs at once: scene arrival and three-man selection.

Why it was kept for now:
This keeps the Vertical Slice short and fully playable without inventing a new meta layer.

Suggested later optimization:
Split `ARRIVAL` and `SELECT_NPC` into two beats if pacing feels rushed in playtest.

### 2. Breakfast scene is manual-advance instead of timed auto-play

Why it may feel off:
The intended rhythm reads like an automatic morning routine, but button-based stepping feels more like a prototype slideshow.

Why it was kept for now:
Manual stepping is safer for demo validation and easier to test repeatedly.

Suggested later optimization:
Add optional auto-play with skip after the dialogue pacing is validated.

### 3. Dialogue blocks are concise by design

Why it may feel off:
Some players may want more follow-through after each choice.

Why it was kept for now:
The current goal is to validate the three-block conversation structure, not to write long scenes.

Suggested later optimization:
Only extend after we know which NPC and which tone produce the most interesting rhythm.

### 4. Diary is functional but emotionally light

Why it may feel off:
The current diary closes the loop, but it does not yet create a strong aftertaste.

Why it was kept for now:
The page exists, reads fake data, and proves the loop can end cleanly.

Suggested later optimization:
Upgrade diary tone only after playtest feedback confirms the current loop is worth deepening.
