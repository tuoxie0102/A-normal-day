# Parser_Report

> 生成日期：2026-06-27（Round 2 收尾）
> 范围：`prototype.html` 内 Markdown → 运行时数据的解析层修复

---

## 1. 修复目标

Round 1 验证全部运行时资源 200 后，发现 Markdown Parser 把开发期控制内容当对白渲染。Round 2 在不改剧情、不改 Markdown 正文、不改资源路径的前提下，把这些 metadata 隔离出 displayContent。

## 2. 拦截的 6 类 metadata 泄漏

| # | 类型 | 真实示例 | 来源文件 |
|---|------|---------|---------|
| 1 | 自动播放控制标记 | `（自动播放结束。瑶珍注意到他只喝水。...）` | 02 L22 / 03 L22 / 04 L26 |
| 2 | 系统标记 | `（展开自动推进到收尾时刻。）` | 03 L84 |
| 3 | 条件分支说明 | `- 若之前选了理解/数据：陈思远...` / `- 若选了理解/调侃：林哲...` | 02 L52-53 / 03 L51-52 / 04 L98-99 |
| 4 | 结构过渡注释 | `过渡对话。瑶珍的回应自然引出后续。` / `无论哪条路径，对话最终收束到...` / `两个方向最终都引向...` / `瑶珍的回应决定了接下来的情绪走向。` | 02 L50/L55 / 03 L49/L54 / 04 L59 |
| 5 | 导演指令前缀 | `> 背景变暗。咖啡杯的微光。雨声压到极低。` | 02 L32 / 03 L32 / 04 L40 |
| 6 | 对白行内动作 | `> **陈思远**：没有没有。我也刚到。（把拿铁推过去）前面问过你喜欢拿铁。` | 02 L20 等多处 |

## 3. Parser 辅助函数 → 接线点（`prototype.html`）

| 辅助函数 | 行号 | 在 `parseSectionSequence` 的接线位置 |
|---------|------|-----------------------------------|
| `stripAllStageDirections(text)` | L1534-1539 | L1669 dialogue 分支 `parsed.spoken` 后 |
| `isPureSystemMarker(rawLine)` | L1541-1550 | L1651 主循环 skip |
| `isDevMetaParagraph(rawLine)` | L1552-1564 | L1652 主循环 skip |
| `extractAutoPlayObservation(rawLine)` | L1566-1572 | L1654 抽 narration 内层 |
| `stripDirectorCuePrefix(text)` | L1574-1576 | L1680 narration + `inTrigger` 分支 |

## 4. 早餐 Parser 改造：Day 1-4

### 旧实现

```js
function parseBreakfastMarkdown(markdown) {
  const section = findSectionByPrefix(markdown, "## Day 1");
  // ... 单 Day 解析
  return { scene: "bg_01_home", news, lines };
}
```

### 新实现

```js
function parseBreakfastDaySection(section) { /* 单 Day 提取 */ }

function parseBreakfastMarkdown(markdown) {
  const days = {
    day1: parseBreakfastDaySection(findSectionByPrefix(markdown, "## Day 1")),
    day2: parseBreakfastDaySection(findSectionByPrefix(markdown, "## Day 2")),
    day3: parseBreakfastDaySection(findSectionByPrefix(markdown, "## Day 3")),
    day4: parseBreakfastDaySection(findSectionByPrefix(markdown, "## Day 4"))
  };
  return {
    scene: days.day1.scene,
    news: days.day1.news,
    lines: days.day1.lines,
    days
  };
}
```

### 向后兼容性

- 所有现有消费点（`currentGameData()?.breakfast`、`renderBreakfast()`、`renderBreakfastShell()`、`breakfastOverlayState()`、`STATE.breakfastIndex` 步进）只读 `breakfast.scene / .news / .lines`
- 顶层三字段 = Day 1 的值，行为零变化
- Day 2-4 数据可通过 `breakfast.days.dayN` 访问，渲染层接入留作下一轮（需 `STATE.breakfastDay` 路由）

## 5. 验证

对照 02_陈思远.md / 03_林哲.md / 04_周文涵.md 全文逐行追踪 `parseSectionSequence`，确认 6 类 metadata 均被拦截：

- 第 1 类 → `extractAutoPlayObservation` 抽出 X，前缀"自动播放结束。"被去掉
- 第 2 类 → `isPureSystemMarker` 直接 `continue`
- 第 3 类 → `isDevMetaParagraph` 先 strip `^[-*]\s*` 再匹配 `^若(之前选|选了|选)` `continue`
- 第 4 类 → `isDevMetaParagraph` 匹配 `^过渡对话` / `^无论` / `^两个方向` / `^瑶珍的回应` `continue`
- 第 5 类 → narration 分支 + `inTrigger` 时调 `stripDirectorCuePrefix` 去前缀
- 第 6 类 → dialogue 分支 `stripAllStageDirections` 去 `（...）`

对照 06_早晨场景变化.md，Day 1-4 均能正确解析 `**新闻**：` 和 `**爸爸/妈妈/瑶珍**：` 段。

## 6. 副作用 / 已知边界

### `isDevMetaParagraph` 宽松匹配

`^瑶珍的回应` 会把 02_陈思远.md L83 `瑶珍的回应带来一个短暂的安静时刻。雨还在下，但小了一些。` 整行滤掉。

- 前半句"瑶珍的回应带来一个短暂的安静时刻"确实是 dev meta
- 后半句"雨还在下"是有效环境描写
- 决定：暂保持现状，登记在册。expand2Section 后续 L85-87 的叙述仍可见，玩家体验上不缺失

### Day 2-4 渲染未接入

`parseBreakfastMarkdown` 已能返回 4 天数据，但 `STATE` 没有 `breakfastDay` 字段，渲染层全部走顶层 `lines`（= Day 1）。属于"新增功能"边缘，需要明确指令再做。

### `block.sourceHeading` 仍存在但仅供日志

阶段 C 清理 caption-chip 后，`sourceHeading` 在数据层仍保留（`parseDialogueMarkdown` L1847/L1862/L1877），仅供 `logCurrentBlock` 的 `console.log` 输出（L2136）。UI 不再消费它，**不影响玩家**。

## 7. 文件改动总览

| 文件 | 改动 | 行号 |
|------|------|------|
| `prototype.html` | 5 个辅助函数定义 | L1530-1576 |
| `prototype.html` | `parseSectionSequence` 接线 4 个分支 + dialogue 分支 stripAll | L1651/L1652/L1654/L1669/L1680 |
| `prototype.html` | 抽出 `parseBreakfastDaySection` + `parseBreakfastMarkdown` 改路由 | L1752-1804 |
| `prototype.html` | 阶段 C 清理 caption-chip 死代码 8 处 | CSS L279/L327 etc.，JS L2147 起 |
| `asset_manifest.md` | `news.mp3` → `news_breakfast.mp3` | L60 |
| `DevelopmentNotes.md` | 合并英文 Flow Concerns 节 | 文末追加 |
| `Development Notes.md`（带空格） | 删除 | 整文件 |
