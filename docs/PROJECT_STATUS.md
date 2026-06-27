# PROJECT_STATUS

> 项目：像男人一样相亲（Vertical Slice Demo）
> 状态文档生成日期：2026-06-27（Round 3 收尾）
> 维护模式（Project Maintainer Mode）下持续更新。

---

## 1. 项目当前状态（一句话）

`prototype.html` 单文件 web app 已恢复完整入口：title → breakfast → world → selection → dialogue → diary → end → 回 title。所有 9 屏完整、跳转无死路径、Parser 干净、Day 1-4 数据已就绪、UI 设计语言一致。Round 1/2/3 全部完成。

---

## 2. 三轮已完成内容（从早到晚）

### Round 1 · 维护模式启动（2026-06-26）

- 修复 `AUDIO_MAP.title` key 拼错 `bgm` → `primary`
- 验证全部运行时资源 200

### Round 2 · Parser 收口 + UI metadata 清理（2026-06-27 上半场）

- **阶段 A**：核对 Parser 接线，确认 5 个辅助函数（`stripAllStageDirections` / `isPureSystemMarker` / `isDevMetaParagraph` / `extractAutoPlayObservation` / `stripDirectorCuePrefix`）已在 `parseSectionSequence` + `parseBreakfastMarkdown` 接通，6 类 metadata 全部被拦截
- **阶段 B**：抽出 `parseBreakfastDaySection`，主函数改为路由，返回 `{ scene, news, lines, days: { day1..day4 } }`，向后兼容
- **阶段 C**：caption-chip 死代码彻底清理（CSS + JS 共 8 处）
- **阶段 D**：文档同步 — `asset_manifest.md` 修一行、合并双份 Dev Notes、新建 `Parser_Report.md`、追加 `CHANGELOG.md`、重写 PROJECT_STATUS.md

### Round 3 · 封面 + 跳转 + UI（2026-06-27 下半场）

- **阶段 1**：新增 `renderTitle()` + `AUDIO_MAP.title` + STATE 默认 "title" + render() 路由分支 + `begin-day` / `go-title` actions + restart / retry-load 重定向 + resetRun 改回 title + end 屏按钮文案"再来一天" → "回到封面"
- **阶段 2**：跳转核查报告 — 13 actions × 7 setScreen 目标全核对，无死路径
- **阶段 3**：UI 美化 — `renderBreakfastShell` / `renderDialogueShell` 补 scene-transition、`.btn:disabled` 备用状态、loading-pulse 呼吸动画
- **阶段 4**：9 屏完整性 audit + 顺手补 end 屏 audio chip（与 title 屏对称）
- **阶段 5**：本地 HTTP 验证 — 静态校验 + 8 个资源 200 + JS 语法解析通过

---

## 3. 修改了哪些文件（三轮累计）

| 文件 | 累计改动 |
|---|---|
| `prototype.html` | 2562 → 2691 行（+129）。Round 1 改 AUDIO_MAP；Round 2 接线 Parser + caption-chip 清理 + breakfast Day 1-4；Round 3 新增 renderTitle + 路由 + UI 美化 + end audio chip |
| `asset_manifest.md` | L60 `news.mp3` → `news_breakfast.mp3` |
| `DevelopmentNotes.md` | 合并英文 Flow Concerns + 更新剩余问题 |
| `CHANGELOG.md` | 三轮节全部写入 |
| `docs/PROJECT_STATUS.md` | 重写到 Round 3 现状（本文件） |
| `Parser_Report.md` | **新建**（Round 2 产出） |
| `docs/session-summary.md` | **新建**（会话保存点） |
| `Development Notes.md`（带空格副本） | **删除**（已合并） |

---

## 4. 目前还有哪些问题

### P1 · Day 2-4 渲染未接入

- Parser 已能返回 `breakfast.days.day1..day4`
- 但 `STATE` 没有 `breakfastDay` 字段，渲染层全部走顶层 `lines`（= Day 1）
- 玩家在任何 NPC 路径下都只看到 Day 1 早餐
- **未做原因**：属于"新增功能"边缘，需先定义 4 个 NPC 各自对应哪一天（陈思远=Day1 / 林哲=Day2 / 周文涵=Day3 / 宋潇=Day4？）以及 STATE 重置策略

### P2 · 第二轮图片资产批处理未做

- 所有人物 PNG（`generated_characters/` 8 张 + `assets/characters/` 备份）需要：
  - 去除残留白边 / 白底
  - 清理锯齿
  - Feather（边缘柔化）适度处理
  - 去除白色溢色（White Fringe）
  - 保持透明 PNG
  - 不改变人物比例
  - 不降低清晰度
- 完成后替换项目中所有旧资源，而不是只修当前页面引用
- **未做原因**：你明确说"等版式固定后再做"，现在版式固定 ✅，可以开第二轮

### P2 · `go-title` 是死按钮

- handler 已注册（L2620）
- 当前 UI 没有按钮触发它
- end 屏的"回到封面"用 `restart` action（间接 `setScreen("title")`），功能等价
- **未做原因**：预留，未来在 dialogue / diary 内若想加"返回封面"可直接用

### P2 · `isDevMetaParagraph` 宽松匹配的副作用

- `^瑶珍的回应` 会把 `02_陈思远.md` L83 整行（含有效环境描写"雨还在下，但小了一些"）滤掉
- expand2Section 后续 L85-87 的叙述仍可见，玩家体验上不缺失
- **未做原因**：暂保持现状，登记在册

### P2 · `block.sourceHeading` 仅供日志

- Round 2 已切断 UI 路径
- 数据层仍保留（`parseDialogueMarkdown` L1862/L1877/L1894），仅供 `logCurrentBlock` 的 `console.log`
- **未做原因**：开发期调试日志，不影响玩家

### P3 · 长期登记不动项

- 宋潇（Day 4 男角色）已有 `dialogue/05_宋潇.md` + `char_04_songxiao.png`，但 `NPCS` 数组未接入
- 多个旧路径残留函数（`collectDialogueQuotes` / `collectTriggerLines` / `firstNarrativeLine` / `syncDialogueTimer`）无引用
- `assets/scenes/bg_00 open.png` 文件名带空格（浏览器会自动 URL-encode，已验证 OK）
- 项目根散落 `__verify_*.png` / `__breakfast*.png` 等开发期截图

---

## 5. 下一步建议

### 最优先 · 直接接着干

**第二轮：图片资产统一优化**

- 批处理 `generated_characters/` 8 张 PNG
- 检查 `assets/characters/` 备份是否也需要同步（决定保留作对比 vs 删除）
- 处理流程：去白边 → 清锯齿 → Feather → 去 White Fringe → 保持透明 → 不改比例 → 不降清晰度
- 替换项目中所有旧资源引用（注意 `prototype.html` 通过 `generated_characters/` 路径加载，所以重点是覆盖这个目录）

### 中期 · 可独立成轮

- **Day 1-4 渲染接入**：新增 `STATE.breakfastDay`，定义 NPC ↔ Day 映射，改 3 个 breakfast 渲染函数
- **宋潇接入主流程**：NPCS 数组 + AUDIO_MAP.dialogue + parseDiaryMarkdown 同步加 songxiao

### 长期 · 需要明确指令再动

- `go-title` 按钮接入位置
- 旧路径死代码清理（重构）
- 项目根开发期截图清理

---

## 6. 当前项目是否可以运行

**可以运行 ✅**

- 启动方式：在项目根目录跑 `python -m http.server`（或任何静态 HTTP 服务器），浏览器打开 `http://localhost:8000/prototype.html`
- 不能 `file://` 直接打开（fetch dialogue/*.md 会失败）
- 默认入口：**封面屏**（renderTitle），点"开始这一天"进 breakfast
- 完整跑通：title → breakfast → world → selection → 任选 NPC → Block 1→2→3 → diary → end → 回 title
- 所有改动均向后兼容，没有引入已知回归
- 本地 HTTP + JS 语法 + 8 个资源 200 均验证通过

---

## 7. ⚠️ Git 仓库状态异常

- 项目根 `.git/` 目录残缺（只有 `info/` 子目录）
- `git rev-parse --git-dir` 报 `fatal: not a git repository`
- 父目录 `糕糕知识库/.git` 存在（看起来是 Obsidian 仓库）
- **本会话所有修改都未进入 git**

### 三个保存选项

1. 修复或重建当前项目仓：`rm -rf .git && git init && git add . && git commit -m "..."`（会丢失任何已有的 git 历史）
2. 用父目录仓提交（如果父仓正常）
3. 文件系统备份 / 压缩整个项目目录

---

## 维护原则备忘

- 不重构、不推翻架构（除非用户明确松绑约束）
- 不改剧情对白 Markdown 正文、不改资源路径
- 兼容现有实现优先
- 每轮结束写 CHANGELOG、重大状态变化更新 `docs/PROJECT_STATUS.md`
- 会话末尾写 `docs/session-summary.md` 留接入点
