# CHANGELOG

项目维护模式下的修改记录。每一轮一节，从新到旧。

---

## 2026-06-27 · Round 10（UI Bug Fix + 跳过寒暄重设计）

### 修改的文件

- `prototype.html`（HTML 4 处 + CSS 多处 + JS 3 处）
- `CHANGELOG.md`

零改动：markdown / 资源 / 玩法 / 剧情。

---

### Bug 1 · 对话页"继续"按钮被遮挡（根因 + 整体修复）

**根因**：旧版 `.controls-panel` 是 absolute 定位（`bottom: 266px`），独立于 `.dialogue-tray`（`bottom: 92px`）。当 NPC 一句话很长导致 `dialogue-tray` 向上撑高超过 266px 时，**tray 在 DOM 顺序里位于 controls-panel 之后**（同 `z-index: 4`，后渲染者绘制在上），就会**覆盖**到 controls-panel 的"继续"按钮上。

**影响范围**：不止某一页。**dialogue / response / reaction 三种 phase 都有这个隐患**，只是触发条件是"对白文字长到一定行数"。

**修复**：把 `.controls-panel` 从独立绝对定位面板**移入 `.dialogue-tray` 内部顶部**作为 tray header，由 tray 高度自然托起：

```html
<div class="dialogue-tray" id="dialogue-tray-shell" hidden>
  <div class="dialogue-tray-controls" id="dialogue-controls-shell" hidden>
    <div id="dialogue-controls-content">...</div>
  </div>
  <div id="dialogue-tray-content"></div>
</div>
```

CSS 新增 `.dialogue-tray-controls`：flex space-between + 底部细线分隔 + 自然布局（不再绝对定位）。旧 `.controls-panel` 保留为 inert `display: contents` 兼容（万一外部仍引用 class 名）。

**效果**：
- ✅ 任何长度对白，"继续"按钮始终在对白文字**上方**，永不被遮
- ✅ 视觉上 controls 是 tray 的 header（状态 + 操作 → 对白），交互区域更聚拢
- ✅ Patcher 通过 ID 工作，无需改动；JS 端零修改

**JS 引用完整性**：`dialogue-controls-shell` / `dialogue-controls-content` 等 ID 全保留（grep 各命中 2 次 = HTML 定义 + JS getElementById）✓。

---

### Bug 2 · 右上角"换一个对象"和"音乐 BGM"重叠（全局修复）

**根因**：`renderAudioChip()` 输出独立 `<button class="audio-chip">`，CSS `position: absolute; right: 24; top: 24; z-index: 6`；`topbar` 也是 absolute 全宽 flex，右侧 `topbar-actions` 内含按钮。两者 stacking context 不同，**audio-chip 浮在 topbar 之上**遮挡右侧按钮。

**影响屏**：dialogue（actions: 跳过寒暄 + 换一个对象） + selection（actions: 返回）。breakfast/title/world/diary/end 因为 topbar 右侧无按钮或无 topbar，未发生重叠。

**修复**：在有 topbar 的屏，把 `${renderAudioChip()}` 从 stage 顶部 **移入 `topbar-actions` 内部**作为最后一个 flex 子元素：

```html
<div class="topbar-actions">
  <button>跳过寒暄</button>
  <button>换一个对象</button>
  ${renderAudioChip()}   <!-- audio chip 跟其他按钮一起 flex 排列 -->
</div>
```

CSS 加局部覆盖让 audio-chip 在 topbar 内**变 static**（不再 absolute）：

```css
.topbar .audio-chip,
.topbar-actions .audio-chip {
  position: static;
  right: auto; top: auto;
  padding: 8px 14px;
  font-size: 12px;
}
```

其他屏（title / breakfast / world / diary / end）audio-chip 仍是 absolute 右上，保持原视觉。

**响应式**：≤720px 媒体查询里 audio-chip 单独的 `right/top` 规则仍然适用于 absolute 模式；topbar 模式下因为是 flex 自然排列，无需特别处理。

---

### Bug 3 · 首页文案更新

| 字段 | 旧 | 新 |
|---|---|---|
| h1 主标题 | 像男人一样相亲 | **这本该是正常的一天** |
| subtitle 副标题 | 真正的问题，从来不是相亲。 | **没人能决定你该怎么活** |

注：浏览器标签页 `<title>` 仍为"像男人一样相亲"（项目代号），未改。

---

### Bug 4 · 跳过寒暄功能重设计

#### 数据结构（新统一字段）

`parseDialogueMarkdown` 给每个 NPC 的 dialogue 对象新增字段：

```js
coreInteractionEntry: {
  blockIndex: 0,
  stepIndex: block1Opening.length   // = Block 1 寒暄段结束、冲突①开始的第一步
}
```

**这是单一可配置入口**。未来想为某个 NPC 单独覆盖核心节点（比如让陈思远的核心节点在 Block 2 中段），只需要在 parser 的这一处加 npc-specific 分支即可，UI / handler / 按钮**全部无需改动**。

#### 实际跳转目标（数据驱动，已 Node 验证）

| NPC | smalltalk 步数 | 跳过寒暄后落到 |
|---|---|---|
| **陈思远** | 12 | dialogue: **"咖啡因对备孕不好。虽然我也还没……就是提前注意一下。"**（冲突①触发句） |
| **林哲** | 9 | dialogue: **"我喜欢写代码。但是我妈说，男人不应该把工作看得太重。"**（冲突①触发句） |
| **周文涵** | 11 | dialogue: **"我相亲过的......一号。律师助理..."**（冲突①触发句） |

#### 按钮可见性（重设计）

| Phase | 旧逻辑 | 新逻辑 |
|---|---|---|
| sequence + smalltalk（Block 1） | 显示 | **显示**（不变） |
| sequence + core（Block 1） | 隐藏 | **显示** ← 新 |
| sequence（Block 2/3） | 隐藏 | **显示** ← 新 |
| response（玩家选择） | 隐藏 | **隐藏**（按用户要求） |
| reaction（NPC 反应） | 隐藏 | **隐藏**（按用户要求 — 关键剧情节点不可跳） |
| 当前已是 block 最后一步 | 隐藏 | **隐藏**（无东西可跳） |
| diary / end / 其他屏 | 不可达 | 不可达 |

#### 点击行为（数据驱动）

```js
function skipSmalltalk() {
  // ... defensive checks ...
  // Case 1: 当前位置 < coreInteractionEntry → 跳到 coreEntry
  if (here < entry) {
    STATE.blockIndex = coreEntry.blockIndex;
    STATE.dialogueStepIndex = coreEntry.stepIndex;
    render();
    return;
  }
  // Case 2: 已经在 coreEntry 之后但还在 sequence → 直接跳到当前 block
  // 最后一步并切到 response phase（让玩家立刻面对选择）
  STATE.dialogueStepIndex = block.steps.length - 1;
  STATE.dialoguePhase = "response";
  render();
}
```

**符合用户全部约束**：
- ✅ 跳过寒暄 / 铺垫 / 内心独白 / 观察 / 过渡（这些都是 sequence 内的 step）
- ✅ 不跳过玩家选择（response phase 按钮隐藏，到达就停）
- ✅ 不跳过 NPC 反应（reaction phase 按钮隐藏）
- ✅ 不跳过结局 / 日记 / end 流程（那些是独立屏，按钮根本不存在）
- ✅ 整个对话过程都可点（任意 sequence step 都显示）

#### 想改跳转目标？

**改一处**：`parseDialogueMarkdown` 内 `coreInteractionEntry` 的 `blockIndex` / `stepIndex` 计算逻辑。可以按 NPC 加分支：

```js
const coreEntries = {
  chensiyuan: { blockIndex: 1, stepIndex: 3 },  // 想让陈思远跳到 Block 2 第 3 步
  // ...
};
const coreInteractionEntry = coreEntries[npc.id] || { blockIndex: 0, stepIndex: block1Opening.length };
```

---

### 全项目 UI Audit（已扫，未发现额外问题）

| 检查项 | 状态 | 说明 |
|---|---|---|
| 缺失按钮 | 仅 dialogue controls 一处（已修） | 其他屏按钮渲染条件梳理 OK |
| UI 重叠 | dialogue + selection 已修；其他屏 OK | breakfast 屏 news-chip max-width 已留出 audio chip 空间 |
| 按钮超出屏幕 | ≤720px 媒体查询已限边距 | dialogue-tray + response-panel 在窄屏 16px 边距 |
| 布局错位 | 无 | scene-stage + topbar + tray 三层结构稳定 |
| 首次渲染位置异常 | 无（Round 7 narrationFade 已修） | transform + animation 冲突全 audit 通过 |
| 响应式布局 | ≤980 / ≤720 两档媒体查询完整 | 角色卡缩放、tray padding、selection 单列等均覆盖 |

---

### 验证

- ✅ JS 语法（new Function 解析 54846 字节通过）
- ✅ HTTP 200 prototype.html（97045 B）
- ✅ 关键 JS 引用 ID 全保留：dialogue-controls-shell / dialogue-controls-content / dialogue-tray-shell / dialogue-tray-content / dialogue-skip-smalltalk-btn 各命中 2 次
- ✅ 新增 .dialogue-tray-controls 类用 4 次（CSS 定义 ×2 + HTML class ×1 + 注释 ×1）
- ✅ Node 模拟 parser：3 NPC 的 coreInteractionEntry 全部正确指向各自冲突①触发句
- ✅ 首页文案改对（h1 + subtitle 各命中 2 次：HTML 定义 + CHANGELOG 表格）

### 仍未处理（登记）

- **林哲立绘正方形比例问题**：素材本身 W/H=1.02，需要重新生成图片。Round 7 CSS height 主导 + Round 8 alpha 清理已兜底
- **响应式按钮密度**：dialogue topbar 现在有 3 个 chip/button（跳过寒暄 + 换一个对象 + audio）。≤720px 时可能略挤，但媒体查询里 audio-chip 仍 absolute（用 fallback rule），可工作。如果未来移动端继续踩坑，可考虑给 topbar-actions 加 flex-wrap
- **dialogue-tray 顶部 controls + 底部对白**的视觉高度上限：极长对白（>5 行）+ controls header 可能让 tray 总高 ≈ 220px，仍在 scene-stage 内（min-height 920px 减 92px bottom = 828px 可用）。如果未来某段对白长到挤压人物，可加 max-height + scroll

---

## 2026-06-27 · Round 9（P1 + P2 + P3 一并完成）

### 修改的文件

- `prototype.html`
- `CHANGELOG.md`
- 删除项目根 26 张 `__*.png` 开发期截图

零改动：markdown / 资源路径 / CSS 设计 token / 玩法。

### P1 · Day 1-3 breakfast 渲染接入

> 用户明确：宋潇线不接，所以 Day 4 数据保留但不映射 NPC。NPCS 仍为 3 人。

#### State + 常量

```js
STATE.breakfastDay: 1                  // 当前游戏内是第几天
const BREAKFAST_DAY_LIMIT = 3          // Day 1-3，对应陈思远/林哲/周文涵
```

#### `currentBreakfast()` 改为 day-aware

```js
function currentBreakfast() {
  const data = currentGameData()?.breakfast;
  if (!data) return { scene: "bg_01_home", news: "", lines: [] };
  const day = data.days?.[`day${STATE.breakfastDay}`];
  if (day && Array.isArray(day.lines) && day.lines.length) {
    return {
      scene: day.scene || data.scene || "bg_01_home",
      news: day.news || "",
      lines: day.lines
    };
  }
  return data;  // fallback to top-level (Day 1) for older parser output
}
```

3 个 breakfast 消费点（`renderBreakfast` / `renderBreakfastShell` / `breakfastOverlayState` / `advanceBreakfast`）零修改 — 它们读 `currentBreakfast()`，新的 day 路由对它们透明。

#### 推进逻辑

新增 `advanceToNextDay()`：clearDialogueTimer → breakfastDay+1（封顶 3）→ reset per-day state (breakfastIndex / selectedNpcId / blockIndex / lastChoiceTone / dialogueBlock) → setScreen("breakfast")。

`resetRun()` 同步加 `STATE.breakfastDay = 1`。

#### End 屏改进

按 day 区分文案 + 按钮：

| 状态 | eyebrow | 标题 | 文案 | 按钮 |
|---|---|---|---|---|
| Day 1-2 完成 | `第 N 天 · 今晚` | "今晚的相亲到此为止。" | "她合上日记..." | `明天 →`（次要）+ `回到封面`（主要） |
| Day 3 完成 | `尾声` | "三天的相亲到此为止。" | "她把日记收进抽屉。三个人，三个晚上，三种沉默..." | 只剩 `回到封面` |

去掉了旧版"再见一个对象"按钮 — Day-based 推进体验下，"明天"语义更清晰，"再见一个对象"会绕过 breakfast 屏破坏一天的节奏。

#### NPC ↔ Day 映射

| Day | 对应 NPC | 早餐内容（来自 `dialogue/06_早晨场景变化.md`） |
|---|---|---|
| 1 | 陈思远 | 6 lines · 新闻：会做饭男性匹配率+43% |
| 2 | 林哲 | 11 lines · 新闻：男性30岁后生育风险 |
| 3 | 周文涵 | 10 lines · 新闻：男性主动表达比例下降 |
| ~~4~~ | ~~宋潇~~ | 8 lines · 新闻：男性最佳生育年龄降至 29 岁（数据保留，未接入） |

**软绑定**：玩家在 selection 屏仍可任意选 NPC。Day 决定 breakfast 内容，**不**决定 NPC。代价是玩家可以连续 3 天选同一个 NPC（剧情会重复）— 但这避免了在 Round 9 内强制做 visited-NPC 状态管理。

### P2 · `go-title` 按钮接入

按钮接入位置：**diary 屏 bottombar 左侧**。

```html
<div class="bottombar">
  <button class="btn ghost secondary" data-action="go-title">回到封面</button>
  <button class="btn primary" data-action="finish-day">结束一天</button>
</div>
```

理由：
- diary 是反思/总结时刻，给玩家"离场"出口符合体验
- dialogue 屏 topbar 已经有"跳过寒暄"+"换一个对象"两个按钮，再加挤
- 与 finish-day（主操作，右侧 primary）形成清晰的层级：左下 ghost 是退出，右下 primary 是继续

替换了旧版的 `<div class="footer-note"></div>` 空占位 div，bottombar flex space-between 仍然平衡。

`go-title` action handler 早在 Round 3 就注册过（L2650），本轮只是终于有了 UI 触发。

### P3 · 死代码 + 开发期截图清理

#### 删除 3 个无引用函数（共 65 行）

| 函数 | 行号 (旧) | 行数 | 引用 |
|---|---|---|---|
| `firstNarrativeLine` | L2169-2183 | 15 | 0 |
| `collectDialogueQuotes` | L2193-2210 | 18 | 0 |
| `collectTriggerLines` | L2282-2313 | 32 | 0 |

确认方法：`grep -c "<fn_name>" prototype.html` 全部从 1（定义本身）降到 0。

**保留**：`syncDialogueTimer`（L2575）虽然名字像废弃旧路径，但仍被 L3064 调用（`if (STATE.screen === "dialogue") syncDialogueTimer();`），不动。

#### 删除 26 张开发期截图（项目根）

```
__breakfast.png / __breakfast_fixed.png
__dialogue_env.png / __dialogue_env_fixed.png
__dialogue_monologue.png / __dialogue_monologue_fixed.png
__dialogue_reaction.png / __dialogue_reaction_fixed.png
__dialogue_response.png / __dialogue_response_fixed.png
__diary.png / __diary_fixed.png
__runtime_check.png
__selection.png / __selection_fixed.png
__title.png
__verify_breakfast.png / __verify_breakfast_end.png
__verify_dialogue_env.png / __verify_dialogue_monologue.png / __verify_dialogue_response.png
__verify_diary.png / __verify_selection.png / __verify_world.png
__world.png / __world_fixed.png
```

共 26 个文件，合计 **31 MB**。引用扫描 (`grep -rn "__breakfast\|__dialogue\|__diary\|__title\|__selection\|__world\|__verify\|__runtime"`) 只命中 docs/PROJECT_STATUS.md / docs/session-summary.md 里的"待清理"备忘记录，**prototype.html / markdown / 资源清单零引用**。

HTTP 404 验证：`__title.png` 和 `__verify_breakfast.png` 都返回 404 ✓。

### 验证

| 检查 | 结果 |
|---|---|
| JS 语法（new Function 解析） | ✅ 52334 字节通过（少了 25 字节 = 删除 65 行死代码与新增逻辑相抵） |
| 文件大小 prototype.html | 90824 B（Round 8 为 93298 → 略减） |
| HTTP 200 主页 | ✅ 93356 B (chunked) |
| HTTP 200 dialogue MD | ✅ |
| 4 个 NPC 对白表（Round 4 fix 验证） | ✅ 全部 12 表 label/preview/response 非空 |
| Parser 模拟 Day 1/2/3/4 | ✅ 全部 6/11/10/8 lines + news 解析正确 |
| 死代码已删 | ✅ 3 函数 0 命中 |
| 开发截图已删 | ✅ HTTP 404 |
| 关键新 symbol 引用数 | ✅ breakfastDay×9 / BREAKFAST_DAY_LIMIT×4 / advanceToNextDay×2 / next-day×2 / go-title×2 |

### 浏览器跑通建议

完整 3 天流程：

1. 启动 → title → 开始这一天 → breakfast 应显示 **Day 1 内容**（妈妈翻报纸 + 6 句 + 新闻"做饭男性匹配率"）
2. world → selection → 选**陈思远**（与 Day 1 对应） → dialogue → diary
3. diary 左下角应有"**回到封面**"按钮（go-title）
4. 点"结束一天" → end 屏，eyebrow 显示"**第 1 天 · 今晚**"，按钮组 `明天 →` + `回到封面`
5. 点"明天 →" → 重新进 breakfast，**应显示 Day 2 内容**（妈妈说"三十一" + 新闻"生育风险"）
6. 选**林哲** → dialogue → diary → end，eyebrow "第 2 天 · 今晚"
7. 点"明天 →" → breakfast Day 3 → 选**周文涵** → dialogue → diary → end
8. end 屏 eyebrow 应变为"**尾声**"，标题"三天的相亲到此为止。"，**只剩"回到封面"按钮**
9. 点"回到封面" → resetRun → title 屏，breakfastDay 回到 1

### 仍未处理（登记）

- **NPC↔Day 弱绑定**：玩家可以连续 3 天选同一 NPC，触发相同剧情。彻底解决需要 STATE.visitedNpcs Set + selection 屏 disable 已选 NPC。属于"新增机制"边缘，未做。
- **宋潇接入**：Day 4 数据和立绘都就绪（`dialogue/05_宋潇.md` + `char_04_songxiao.png`），但 NPCS / AUDIO_MAP.dialogue / parseDiaryMarkdown 都未接。用户明确不接，保留数据但不上线。
- **syncDialogueTimer**：保留（被 L3064 调用），是否仍必要、是否能合并到 patchDialogueScreen，留待将来需要时再评估。
- **林哲立绘比例问题**：依然存在（W/H=1.02 vs 其他 0.66/0.86），Round 7 height 主导 + Round 8 alpha 清理已兜底；彻底解决需要重新生成图。

---

## 2026-06-27 · Round 8（P0 · 角色图片资产批处理）

### 备份

执行前已写入 Round 7 stable 快照到：

```
D:/01_Projects_项目/2026 个人知识库 飞书录音/_stable_xiangnaxiangqin_2026-06-27_round7/
```

包含 prototype.html / CHANGELOG.md 在 Round 7 完成时的 MD5 校验，回滚说明在该目录的 `README_HOW_TO_ROLLBACK.md`。

### 处理范围

10 张 RGBA PNG，覆盖两个目录：

| 文件 | 尺寸 | 用途 |
|---|---|---|
| char_00_player.png | 407×1540 | 主角女主全身像 |
| char_01_chensiyuan.png | 790×1197 | 陈思远立绘 |
| char_02_cafe.png | 603×1394 | 咖啡馆场景版女主 |
| char_02_linzhe.png | 1220×1197 | 林哲立绘 |
| char_03_teahouse.png | 621×1422 | 茶馆场景版女主 |
| char_03_zhouwenhan.png | 990×1152 | 周文涵立绘 |
| char_04_park.png | 1086×1336 | 公园场景版女主 |
| char_04_songxiao.png | 940×1197 | 宋潇立绘（未接入主流程，但资产同步处理） |
| char_05_dad.png | 1023×1170 | 父亲 |
| char_06_mom.png | 1030×1110 | 母亲 |

### 处理流程（Python + Pillow + numpy）

按用户要求，**不缩放 / 不改比例 / 不降清晰度 / 保 RGBA**：

1. **Alpha noise floor** — α<6 的像素强制全透明，去除几乎不可见但拖累压缩的"灰雾"
2. **White-fringe decontamination**（核心）— 对**半透明**（0<α<230）且 **RGB 明显偏白**（R/G/B 均 >215）的边缘像素，反演 over-white 合成方程：
   ```
   渲染色 = 原色 × α + 255 × (1-α)
   原色 = (渲染色 - 255×(1-α)) / α
   ```
   只在 fringe mask 命中的像素上做（每张约 2800-4900 像素），不动主体内部
3. **Alpha 边缘软化** — α 通道高斯模糊 0.55px，再用温和的 s-curve 重塑（α<8→0，其余 ×1.06 -4），去掉锯齿但保留主体锐度
4. **PNG 重新编码** — `optimize=True`，未做有损压缩

### 输出

| 文件 | 修复像素 | 处理前 | 处理后 | 节省 |
|---|---|---|---|---|
| char_00_player | 4020 | 930 KB | 784 KB | -16% |
| char_01_chensiyuan | 3766 | 930 KB | 726 KB | -22% |
| char_02_cafe | 4218 | 1271 KB | 1132 KB | -11% |
| char_02_linzhe | 4948 | 1345 KB | 933 KB | -31% |
| char_03_teahouse | 3409 | 1333 KB | 1198 KB | -10% |
| char_03_zhouwenhan | 4103 | 1153 KB | 943 KB | -18% |
| char_04_park | 3515 | 2021 KB | 1768 KB | -13% |
| char_04_songxiao | 3625 | 1379 KB | 1188 KB | -14% |
| char_05_dad | 3232 | 1046 KB | 800 KB | -24% |
| char_06_mom | 2885 | 1218 KB | 943 KB | -23% |

**合计减重**：约 2.6 MB（11.6 MB → 9.0 MB）。文件变小**不是因为降画质**，而是清理 α 灰雾 + 白边像素 RGB 还原后 PNG zlib 压缩更高效。

### 修改的文件

| 路径 | 改动 |
|---|---|
| `generated_characters/*.png` | 10 张全部覆盖处理后版本 |
| `generated_characters/*.png.bak` | 10 张原图备份（新增） |
| `assets/characters/*.png` | 10 张同步覆盖（与 generated_characters 一致，用户选项 A） |
| `_tools/round8_clean_character_pngs.py` | 新增 — 处理脚本，可重跑 |
| `CHANGELOG.md` | 新增 Round 8 节 |

**零改动**：prototype.html / markdown / JS / HTML / CSS / 玩法 / 剧情 / 资源路径。

### 验证

- **尺寸保持** ✅ 全部 10 张 size 与 .bak 原图完全相同（Pillow 自检通过）
- **RGBA 透明通道完好** ✅ 全部 10 张 mode == RGBA 且至少有透明像素
- **assets/characters 已同步** ✅ 字节大小与 generated_characters 完全一致
- **HTTP 200** ✅ 21 个资源（10×2 PNG + prototype.html）全部 200
- **JS / HTML / CSS** ✅ 零修改，prototype.html MD5 与 Round 7 一致

### 如何回滚

#### 单独回滚某张图（用同目录的 .bak）

```bash
cd "D:/01_Projects_项目/2026 个人知识库 飞书录音/糕糕知识库/像男人一样相亲/generated_characters"
cp char_02_linzhe.png.bak char_02_linzhe.png
cp ../assets/characters/char_02_linzhe.png.bak ../assets/characters/char_02_linzhe.png
# 注：assets/characters 没有 .bak（同步覆盖），需要从 stable 备份取
```

#### 回滚全部 10 张

```bash
cd "D:/01_Projects_项目/2026 个人知识库 飞书录音/糕糕知识库/像男人一样相亲"
for f in generated_characters/*.png.bak; do
  cp "$f" "${f%.bak}"
done
# 同步 assets/characters
cp generated_characters/*.png assets/characters/
```

或者直接从 Round 7 stable 快照拷回（含全部图片）：

```bash
cp -r "D:/01_Projects_项目/2026 个人知识库 飞书录音/_stable_xiangnaxiangqin_2026-06-27_round7/generated_characters/." \
      "D:/01_Projects_项目/2026 个人知识库 飞书录音/糕糕知识库/像男人一样相亲/generated_characters/"
cp -r "D:/01_Projects_项目/2026 个人知识库 飞书录音/_stable_xiangnaxiangqin_2026-06-27_round7/assets/characters/." \
      "D:/01_Projects_项目/2026 个人知识库 飞书录音/糕糕知识库/像男人一样相亲/assets/characters/"
```

### 浏览器跑通建议

1. `python -m http.server 8000` → 打开 `http://localhost:8000/prototype.html`
2. 角色选择屏 — 三个 NPC 立绘的白边/锯齿应明显缩减
3. 对话屏（陈思远/林哲/周文涵）— 人物轮廓应更干净，融入场景更自然
4. 早餐屏（父亲/母亲/女主）— 人物边缘锐利度更高
5. 如果觉得某张图处理过度（边缘太硬）或处理不足（仍有白边），可针对单张图重跑脚本并调整 `radius` / 阈值参数

### 处理脚本可重跑

`_tools/round8_clean_character_pngs.py` 是幂等的：
- 第一次运行：每张图创建 `.png.bak` 备份，从 .bak 处理写回 .png
- 第二次运行：跳过创建 .bak（已存在），仍**从 .bak 读取**处理，写回 .png
- 这意味着可以反复调参数测试，不会把已处理图二次处理（防累计损伤）
- assets/characters 每次都从 generated_characters 同步

### 仍未处理（登记）

林哲的素材本身高宽比 W/H = 1.019（近正方形），即使白边清理后仍与其他立绘比例不同。本轮**只处理 alpha 通道**，**不重画 / 不重生成图像**。要让林哲与其他 NPC 视觉一致，需要：

- 重新用 AI 生成林哲的立绘（W/H 目标 ~0.7）
- 或在 PNG 上加 padding 让 bbox 变成竖图（但人物会缩小）
- 或保持现状，依赖 Round 7 的 CSS 高度统一规则（已生效）

---

## 2026-06-27 · Round 7（UI Bug Fix · 3 处一致性问题）

### 修改的文件

- `prototype.html`（3 处 CSS 修复 + 1 个新 keyframe，零 JS / HTML / markdown 改动）
- `CHANGELOG.md`

### 1 · 角色选择界面人物尺寸不统一

**根因（不是表面问题）**：素材本身的高宽比差异极大 —

| NPC | 素材尺寸 | W/H 比 |
|---|---|---|
| 陈思远 | 790 × 1197 | 0.660（竖图） |
| 林哲 | 1220 × 1197 | **1.019（近正方形）** |
| 周文涵 | 990 × 1152 | 0.859 |

原 CSS 用 `width: min(18vw, 210px)` 统一**宽度**，但宽度统一后**高度按各自比例自动算**：陈思远 ~318px、林哲 ~206px、周文涵 ~243px。三人高度差 **110px**，肉眼立即看出"林哲偏小、陈思远偏大"。

**修复**：把缩放规则从 width 主导**改为 height 主导**：

```css
.pick-stage .character-art {
  position: absolute;
  left: 50%;
  bottom: 32px;
  transform: translateX(-50%);
  height: clamp(280px, 36vh, 360px);  /* 主导：所有素材高度对齐 */
  width: auto;                          /* 宽度自适应 */
  max-width: 92%;                       /* 兜底：正方形素材不溢出卡片 */
  object-fit: contain;
  object-position: center bottom;       /* 三人统一站位卡片底部 */
}
```

效果：三人头顶在同一水平线、底部站位对齐、视觉重量统一。林哲（近正方形）会自动被 `max-width: 92%` 兜底（视觉上人物宽厚但与其他人头顶齐平）。

媒体查询 ≤720px 同步：`height: clamp(220px, 38vh, 280px)` + `max-width: 90%`。

### 2 · 观察模式文字可读性差

**根因**：原 `.narration-text` 用 `font-style: italic` + `var(--ui-serif)`（Songti SC / Noto Serif）+ `font-size: clamp(15px, 1.65vw, 18px)` + `line-height: 1.95`。中文 serif italic 在屏幕上**无真正斜体字形**，浏览器会做合成（synthetic oblique），字形被几何倾斜，识别成本骤升。长段落叙述（observation phase 经常是 100+ 字）阅读疲劳。

**修复（视觉小说阅读体验）**：

```css
.narration-text {
  font-family: var(--ui-sans);          /* PingFang / Microsoft YaHei — 屏幕字体 */
  font-style: normal;                    /* 去 italic */
  font-weight: 400;                      /* 常规字重 */
  font-size: clamp(16px, 1.7vw, 19px);  /* 略增 */
  line-height: 2.05;                     /* 更宽行高（1.95 → 2.05） */
  letter-spacing: 0.03em;                /* 略增字距，呼吸感 */
  color: #ece1cd;                        /* 更柔的暖色（原 #ebdfca 偏冷） */
}
```

`.narration-label` 仍用 accent 色金条做"观察 / 内心"标签，保留视觉氛围；但**正文本身**回到普通阅读体验。

### 3 · 对话框先在右上角出现再跳回中央（疑似布局 Bug）

**根因（不是动画细节问题，是 CSS transform 整体覆盖）**：Round 6 给 `.narration-panel` 加了 `animation: dialogueFade ...`，但 `dialogueFade` 的 keyframe 是：

```css
@keyframes dialogueFade {
  from { opacity: 0; transform: translateY(12px); }   /* ⚠ 只有 translateY */
  to   { opacity: 1; transform: translateY(0); }
}
```

而 `.narration-panel` 的基础布局**依赖** `transform: translateX(-50%)` 实现水平居中（`left: 50%` + translateX(-50%) 是经典居中模式）。

**CSS transform 是单一整体属性**，keyframe 的 `transform: translateY(12px)` 会**完全覆盖** base 的 `translateX(-50%)`。动画播放期间元素失去 -50% 平移 → 元素左边缘卡在屏幕中线（`left: 50%`），整个 panel 跨在屏幕右半边（用户感知为"右上角"）。动画结束 transform 重置回 base 的 `translateX(-50%)` → "跳"回真正中央。

**修复**：给 `.narration-panel` 独占 keyframe，显式保留 `translateX(-50%)`：

```css
@keyframes narrationFade {
  from { opacity: 0; transform: translate(-50%, 12px); }
  to   { opacity: 1; transform: translate(-50%, 0); }
}

.narration-panel {
  /* ... */
  animation: narrationFade 380ms var(--ease-out);
}
```

从首帧起元素就在正确位置，零跳跃。`dialogue-tray` 保留 `dialogueFade`（它的基础布局靠 `left/right/bottom` 无 transform，不受影响）。

### 全局 Audit · transform + animation 冲突扫描

用脚本扫了所有同时含 base transform 和 animation 的 selector，逐一核验其 keyframe 是否保留了 base transform：

| Selector | Base transform | Animation | Keyframe 含 base？ |
|---|---|---|---|
| `.narration-panel` | translateX(-50%) | narrationFade（新） | ✅（本轮修复） |
| `.diary-sheet` | translate(-50%,-50%) rotate(-1deg) | diaryDrop | ✅（Round 6 已正确） |
| `.character-figure.center` | translateX(-50%) | characterRise（条件） | ✅（keyframe 含 -50%） |
| `.character-figure.left/.right` | (无 transform) | characterSlideLeft/Right | ✅（不依赖 transform） |
| `.title-text-block` | (无 transform) | titleFadeUp | ✅ |
| `.environment-hint` | translateX(-50%) | (无 animation) | ✅ |
| `.world-heroine / .world-cta / .pick-name` | translateX(-50%) | (无 animation) | ✅ |
| `.pick-stage .character-art` | translateX(-50%) | (用 transition 不用 animation) | ✅ |

**结论**：除 `.narration-panel` 已修，全项目无其他 transform + animation 冲突。

### 其它一致性检查（无问题，仅登记）

| 检查项 | 状态 |
|---|---|
| 布局不一致 | 9 屏都用 `.scene-stage` / `.screen` / `.dialogue-tray` 等共用组件，无 |
| 弹窗定位异常 | 仅 narration-panel 一处，已修 |
| 动画闪烁 | textFade / dialogueFade / sceneFade / characterRise 等曲线统一为 `--ease-out`，无 |
| Layout Shift | 入场动画都是 opacity + transform，不触发 reflow；新 character-art 用 height 主导后 selection 屏首次渲染高度稳定 |
| 字体样式不统一 | 现 narration 用 sans，dialogue 用 sans，diary 用 hand（设计意图），title 用 serif（设计意图），层级清晰 |
| 对话框尺寸 | `.dialogue-tray` 全局共用一份样式，`.narration-panel` 同理，每屏一致 |
| 卡片对齐 | 修复后三角色卡内人物高度统一，名字底部对齐 |

### 是否统一了角色卡和弹窗组件

**已统一**：

- **角色卡**：`.pick-stage`（容器）+ `.character-art`（人物 img）+ `.pick-name`（名字），整套唯一一份样式定义。本轮把 character-art 的缩放规则从 width 主导改为 height 主导后，规则**全局生效** — 未来加新 NPC（如宋潇接入主流程）只需把 PNG 丢到 `generated_characters/` 即可，无需任何 CSS。
- **弹窗**：`.narration-panel`（叙述弹窗，唯一一份）+ `.dialogue-tray`（对白条，唯一一份）。两者样式集中，9 个屏全部走同一份。本轮 narrationFade 修复后，未来加新场景也不会出现位置跳跃。

### 验证

- ✅ JS 语法（new Function 解析 52359 字节通过）
- ✅ HTTP 200（93298 B）
- ✅ 32 个 JS 引用 selector / id 全部保留
- ✅ transform + animation 冲突扫描 0 命中（仅 `.narration-panel` 和 `.diary-sheet` 共存且 keyframe 正确）
- ✅ 无 `font-style: italic`（仅注释引用）
- ✅ 无遗留 `translateX(50%)`（已全部改为 -50%）

### 仍可后续优化（不本轮处理）

- **P3** 林哲素材本身偏正方形（1220×1197），即使统一高度后，与陈思远 / 周文涵相比仍显得"宽厚"。这是素材问题，不是 CSS 问题。**Round 4 Plan 里的"P0 图片资产批处理"** 做完后，建议同时把林哲重新生成为高宽比 ~0.7 的竖图，与其他角色对齐。
- **P3** 跳过寒暄按钮 vs 换一个对象按钮在 topbar 的视觉权重接近，未来可能想让"换一个对象"更弱一档（如改成纯文字 link 风格）。
- **P3** dialogue-tray 在窄屏（≤720px）时 `bottom: 74px` 与 navigation chip 距离偏近，未来可以加 16px。

---

## 2026-06-27 · Round 6（首页文案微调 + UI 全面视觉升级）

### 修改的文件

- `prototype.html`（**CSS 全面重构**：从 ~1120 行 CSS 升级为完整的 design token 系统 + 各组件精修，89.9 KB 总体积，+12 KB）
- `CHANGELOG.md`
- **零改动**：markdown 源文件、JS 渲染逻辑、剧情、玩法、HTML 结构、所有 class/id 名（被 JS 引用的全部保留）

### 备份

UI 优化开始前已保存完整 stable 快照到：

```
D:/01_Projects_项目/2026 个人知识库 飞书录音/_stable_xiangnaxiangqin_2026-06-27_pre_ui_overhaul/
```

包含 133 个文件 / 144 MB / `prototype.html` MD5 = `1c8ded300429d4a1348aaca4b641c44b`。同目录下有 `README_HOW_TO_ROLLBACK.md` 详述回滚步骤。

### 文案改动

- 封面副标题：**"瑶珍的四天 · 一个关于'标准答案'的故事"** → **"真正的问题，从来不是相亲。"**（`prototype.html` L2156）

### UI 升级 · 设计 token 系统（新增）

把原本散落各处的硬编码颜色 / 圆角 / 阴影 / 间距整理成完整的 `:root` token：

| 维度 | Token 数 | 说明 |
|---|---|---|
| Background layers | 3 | `--bg-deep / --bg / --bg-soft` |
| Surface layers | 6 | `--surface / surface-strong / surface-raised / surface-inset / surface-paper / surface-paper-warm` |
| Foreground | 5 | `--text / text-strong / text-paper / muted / muted-soft` |
| Accent (暖金) | 6 | `--accent / accent-strong / accent-deep / accent-soft / accent-glow / accent-glow-soft` |
| Lines | 4 | `--line / line-strong / line-warm / line-paper` |
| Spacing (8px grid) | 8 | `--space-xxs ~ --space-3xl` |
| Radius | 7 | `--radius-xs ~ --radius-2xl + --radius-pill` |
| Shadow | 7 | `--shadow-sm / md / lg / xl / glow / inset / scene` |
| Motion | 6 | `--ease-out / in-out / spring + duration-fast / base / slow` |

所有原 token 都保留为 legacy alias（`--panel`, `--shadow` 等映射到新 token），既往 selector 读取完全不破坏。

### UI 升级 · 各组件精修

#### 1. 全局
- `body` 背景加双 radial-gradient（顶部金光 + 底部褐光），固定 attachment 避免视差
- 字体渲染：`antialiased + optimizeLegibility + tnum + ss01`
- `::selection` 用 accent 色高亮
- `.screen` 顶部加 1px 极淡金色高光线（screen blend mode）

#### 2. 按钮系统
- 加入 `::before` sheen 扫光（600ms hover 时从左到右扫过）
- `focus-visible` 单独的 ring（2px accent-glow，无障碍可见）
- `active` 状态加 `scale(0.985)` + 90ms 短回弹（按压反馈）
- `primary` hover 增加 28px 暖光晕（`0 0 28px rgba(215,176,118,0.18)`）
- `secondary` hover 字色升级
- `ghost` 保持极低调
- 总动效曲线：`cubic-bezier(.2, .8, .2, 1)` 一致

#### 3. 封面屏（title）
- 主标题文字 gradient text fill（金色三段渐变，`-webkit-background-clip: text`）
- Eyebrow 前加 28px 金色线条装饰
- 文字块入场 stagger：eyebrow → h1 → subtitle → cta 依次淡入（每段差 160ms）
- CTA 按钮加入 4.5s 一周期的呼吸光晕动画（`@keyframes ctaBreath`）
- CTA padding + letter-spacing 放大（更"按钮感"）

#### 4. 对话屏（dialogue）
- `.dialogue-tray` 顶部加 1px 金色细线分隔，padding 微调
- 入场动画 320ms → 380ms（更从容）
- `.dialogue-speaker` 前加 18px 金色短条（"主持人话筒"标识）
- 字号 / 字距 / 行高全部刻度化（17→21px / 0.02em / 1.9）

#### 5. Narration 面板
- 加右上角"「"装饰引号（22% 透明度 accent 色）
- 左侧金条改用 gradient（顶亮底淡，更优雅）
- Label 加 1px 暖色边框
- Continue 按钮 focus-visible / active 反馈细化（含 scale）

#### 6. 响应选项卡片（response-btn）
- min-height 96 → 104px（更舒适）
- 加入 `::before` 左侧 3px 金色边线（hover 时浮现）
- 加入 `::after` sheen 扫光（700ms）
- hover 时 `translateY(-2px)` + 14px 投影 + 1px accent ring
- active 时 `scale(0.99)` 90ms 反馈
- 标题色 hover 自动升级为 `accent-strong`
- gap 12 → 14px

#### 7. 选择屏（selection）
- 卡片入场 stagger（60ms / 180ms / 300ms 三档延迟）
- hover 时 `translateY(-8px)`（原 -6px）+ 50px 金色光晕
- 卡片顶部加 1px 金色高光线（左右 18% 至 82%）
- 人物图 hover 时 `scale(1.04)`，名字 letter-spacing 微涨（呼吸感）
- gap 18 → 22px，min-height 410 → 420px

#### 8. 日记屏（diary）
- 入场动画用 spring 曲线（cubic-bezier(.34, 1.56, .64, 1)）— 纸张从倾斜落下定格
- 加入 4 角的极细金线装饰（左上、右下各 28×28px）
- meta 行下加虚线分隔
- 标题字号 34 → 36px
- 影子分层（外影 + 边线 + 内顶高光）

#### 9. 人物与场景融合
- `.character-art` drop-shadow 三层叠加（主投影 + 中投影 + 顶部金光高光）
- 新增 `.character-figure::after` 接地虚化阴影（椭圆 6px blur），人物不再像贴纸
- `.scene-stage::before` 加入双 radial-gradient（顶部光、底部暗角），让人物"沉进"场景
- 暗角强度 0.18 → 0.20，更稳

#### 10. Chip 系统（news / audio / status）
- 影子从 `--shadow-md`；padding letter-spacing 微调
- `.audio-chip:hover` 加 1px accent ring + 投影增强
- `.news-chip` 边线统一用 `--line-warm`

#### 11. 环境提示（environment-hint）
- 边框从 `rgba(255,255,255,0.06)` → `--line-warm`
- letter-spacing 加大
- 加入 `--shadow-md` 投影

#### 12. 动画曲线统一
- 入场偏移量普涨 30 → 36px（更有"进场感"）
- `textFade` 改为 fade + 4px Y 偏移（不再是单纯透明度）
- 引入 `--ease-spring`（用于日记）

### 验证

- **关键 selector/id 全保留**：32 个 JS 依赖的 class/id 全部在 CSS 中匹配到（character-figure 26 处、response-btn 15 处、dialogue-tray 11 处、等等）✅
- **JS 语法**：`new Function` 解析 52359 字节通过 ✅
- **HTTP 200**：91825 B 全文件 ✅
- **零功能改动**：所有 render / parse / state / action 逻辑零修改，行为完全等价

### 不变项（明确保留）

| 项 | 是否动 |
|---|---|
| Markdown 源文件（5 个 dialogue + 1 个 breakfast + 1 个 diary） | ❌ 零修改 |
| JS 渲染逻辑（renderXxx / patchDialogueScreen / parseXxx） | ❌ 零修改 |
| 剧情、玩法、跳转逻辑 | ❌ 零修改 |
| HTML 结构（class/id 名、DOM 树） | ❌ 零修改 |
| 资源路径（audio / scenes / characters） | ❌ 零修改 |
| 跳过寒暄功能（Round 5） | ❌ 仍可用，按钮样式跟随新系统升级 |
| 陈思远 Bug Fix（Round 4） | ❌ 仍生效 |

### 如何回退

详见 `_stable_xiangnaxiangqin_2026-06-27_pre_ui_overhaul/README_HOW_TO_ROLLBACK.md`。一键命令：

```bash
cp -r "D:/01_Projects_项目/2026 个人知识库 飞书录音/_stable_xiangnaxiangqin_2026-06-27_pre_ui_overhaul/." \
      "D:/01_Projects_项目/2026 个人知识库 飞书录音/糕糕知识库/像男人一样相亲/"
```

---

## 2026-06-27 · Round 5（新增功能：跳过寒暄）

### 修改的文件

- `prototype.html`（CSS + parseDialogueMarkdown + renderDialogueShell topbar + patchDialogueScreen + 新增 `skipSmalltalk` + action handler）

### 功能定义

在相亲对话过程中，玩家可点击 topbar 右上角的"跳过寒暄"按钮，直接跳到当前 NPC Block 1 的核心冲突触发节点。进入核心后按钮自动隐藏；Block 2/3 全程不显示。不影响观察、结算、日记、最终判断。

### 数据结构（无需改 markdown）

寒暄/核心的边界**完全由现有 section 边界推断**，无需在 markdown 加 frontmatter：

| Block | 来源 section | phase |
|---|---|---|
| Block 1 前段 | `## 开场（自动播放 · ~30秒）` | `smalltalk` |
| Block 1 后段 | `## 冲突节点 ①` | `core` |
| Block 2 全部 | `## 展开` + `## 冲突节点 ②` | `core` |
| Block 3 全部 | `## 展开` + `## 最终判断` | `core` |

`parseDialogueMarkdown` 新增：
- 每个 `step` 加 `phase: "smalltalk" | "core"` 字段
- 每个 `block` 加 `coreStartIndex: number` 字段（Block 1 = 开场段 step 数，Block 2/3 = 0）

这样**未来加新 NPC**只要遵循已有的 `## 开场 → ## 冲突节点①` 结构，自动获得"跳过寒暄"能力，不需要在 markdown 里加任何字段。如果未来想让某段展开也可跳过，只需要在 parser 里改一处分类规则。

### 每个角色点击后跳到哪

每个角色按 markdown 推断，**目前 4 个 NPC 的跳转目标**（Block 1 第一个 `core` step）：

| NPC | smalltalk 步数 | 跳过后落到 |
|---|---|---|
| 02 陈思远 | 12 | dialogue: "咖啡因对备孕不好。虽然我也还没……就是提前注意一下。" |
| 03 林哲 | (按 parser 实测) | 冲突节点①第一句 NPC 对白 |
| 04 周文涵 | (按 parser 实测) | 冲突节点①第一句 NPC 对白 |
| 05 宋潇 | (按 parser 实测) | 冲突节点①第一句 NPC 对白 |

未来想改跳转目标 → 改 `dialogue/0X_*.md` 的 `## 开场` 段长度即可，**不需要改任何代码**。

### UI / 交互

- 按钮文案：**跳过寒暄**
- 位置：dialogue 屏 topbar 右上角，"换一个对象"按钮左边，用 `.topbar-actions` 包裹
- 样式：`.btn ghost secondary .skip-smalltalk-btn`（小一档字号 + 0.78 opacity + hover 1.0）—— 低调辅助按钮，与项目设计语言一致
- 显示条件（patchDialogueScreen 内）：
  - `STATE.dialoguePhase === "sequence"` （在剧情序列推进中）
  - 当前 step 的 `phase === "smalltalk"`
  - `block.coreStartIndex > STATE.dialogueStepIndex` （前面还有 core 内容）
- 隐藏时机：上述任何一条不满足。包括 response 阶段、reaction 阶段、Block 2/3、跳转完成后

### Action handler

新增 `skipSmalltalk()`（在 `continueDialogue` 旁），防御性 no-op 处理：
- `STATE.dialoguePhase !== "sequence"` → no-op
- `target <= STATE.dialogueStepIndex` → no-op（防止倒退或停在原地）
- `target >= block.steps.length` → no-op（防止越界）
- 通过后：`STATE.dialogueStepIndex = block.coreStartIndex` + render

action 注册：`document` 委托监听里加 `if (action === "skip-smalltalk") skipSmalltalk()` 分支。

### 不影响的项

- 渲染层 narration/dialogue/response/reaction 四种 phase 的 markup 均原样
- Block 2/3 的 `coreStartIndex = 0`，按钮显示条件 `coreStartIndex > stepIndex` 必然为 false → 不显示
- 选项按钮、对白 tray、narration panel 位置不变
- 不破坏 markdown — 4 个 NPC dialogue 文件零修改

### 如何修改跳转目标

| 想做什么 | 改哪里 |
|---|---|
| 改某个 NPC 寒暄长度 | 改对应 `dialogue/0X_*.md` 的 `## 开场（自动播放 · ~30秒）` 节内容 |
| 让 Block 2/3 的展开段也可跳过 | 改 `parseDialogueMarkdown` 内对 `expand1Section` / `expand2Section` 的 phase 标签（当前是 "core"，改成 "smalltalk" 并设 `coreStartIndex = expand1.length`） |
| 改按钮文案 / 位置 / 样式 | `renderDialogueShell` 的 topbar 内 `<button>` 文案、`.skip-smalltalk-btn` CSS |
| 改按钮显示条件 | `patchDialogueScreen` 内 `showSkip = ...` 表达式 |

### 验证

- Node 模拟 parser：陈思远 Block 1 = 17 steps，前 12 个 `smalltalk`，coreStartIndex=12，第 12 个 step 是 dialogue "咖啡因对备孕不好..." ✅
- JS 语法 ✅（new Function 解析 52367 字节）
- HTTP 200 ✅（79210 B，比 Round 4 的 76109 多 3.1 KB — 含新增 parser 逻辑、CSS、按钮、handler、注释）

### 浏览器跑通建议

1. `python -m http.server 8000`，开 `http://localhost:8000/prototype.html`
2. 走通 title → breakfast → world → selection → 陈思远
3. 进入对白后，topbar 右上角应**立即可见**"跳过寒暄"按钮
4. 点按钮 → 应该直接跳到 NPC 说"咖啡因对备孕不好..."那一段
5. 继续点"继续" → 进入 core，按钮**消失**
6. 选完一个 reply → 进入 Block 2，按钮应**始终不显示**
7. 同样流程跑剩下 3 个 NPC（林哲 / 周文涵 / 宋潇），按钮都应只在 Block 1 寒暄段出现

---

## 2026-06-27 · Round 4（Bug Fix：陈思远 Block 2 选项正文丢失）

### 修改的文件

- `prototype.html`（新增 `resolveDialogueTableKeys`，改写 `parseDialogueMarkdown` 用每个表自己的 key）

### 根本原因

`parseDialogueMarkdown`（L1944-L1948）只从 `conflict1Table[0]` 推断一次 `conflictLabelKey / conflictPreviewKey / conflictReplyKey`，然后**同时**用到 `conflict1Table.map` 和 `conflict2Table.map`。

- `dialogue/02_陈思远.md` Block 1 表头是 `AI 生成方向（瑶珍的台词）`（多 5 字）
- 同文件 Block 2 表头是 `AI 生成方向`（普通）

`previewKey` 取自 Block 1 = `"AI 生成方向（瑶珍的台词）"`，应用到 Block 2 时 `row["AI 生成方向（瑶珍的台词）"]` → `undefined` → `normalizeChoicePreview("")` → 空串。Block 2 的 4 个选项（🙂 理解 / 🤔 追问 / 😏 调侃 / 📊 数据）只剩 label，正文 `<span>` 渲染为空。

### 为什么只这一页坏

12 个对白表头里只有陈思远 Block 1 含 `（瑶珍的台词）`。

- 其余 11 个 conflict 表头都是 `AI 生成方向` → 复用 key 误打误撞拿到正确值
- finalTable 的 key 单独从 finalTable[0] 取，所以 Block 3 不受牵连
- 陈思远 Block 1 用自己的 key 也对 → 它自己显示正常
- **唯一倒霉的是陈思远 Block 2**：Block 1 的 key 在 Block 2 不存在

### 修复

1. 新增 `resolveDialogueTableKeys(table, kind, contextLabel)`，对**每个**表单独 `Object.keys` 推断 `labelKey / previewKey / responseKey`
2. matcher 用**多 substring 联合匹配**（`AI` / `瑶珍` / `台词`、`反应` / `回应`、`结局` / `结果`），未来再加变体也兼容
3. 缺列时 `console.warn` 输出 npc + block 上下文 + 实际 headers，未来 markdown 改表头不会再静默丢字段
4. `parseDialogueMarkdown` 改用每个表自己的 key — Block 1/2/3 互不干扰

### 验证

- Node 模拟 parser 跑全部 4 NPC × 3 block = 12 表，所有 row 的 label / preview / response 三个字段均非空 ✅
- JS 语法 ✅（new Function 解析 49642 字节）
- HTTP 200 ✅（76109 字节，比 Round 3 的 73708 字节多约 2.4 KB — 含新辅助函数 + 注释）

### 行为不变项（不动）

- 渲染层 `renderDialogueOverlay` L2314-L2319 维持原样：`<strong>${label}</strong><span>${playerLine}</span>`
- Markdown 源文件未动（保持 02_陈思远.md L49 原表头 `AI 生成方向（瑶珍的台词）` — 是作者意图的语义注解）
- 其它 11 个表的渲染输出与修复前完全一致（key 都是 `AI 生成方向`，新旧 key 推断结果相同）

---

## 2026-06-27 · Round 3（封面页 + 跳转 + UI 美化 + 完整性盘点）

> 第一轮 HTML & 逻辑修复。约束放宽：可新增屏、可改路由、可调 UI 微交互。图片资产优化属第二轮，本轮不动。

### 修改的文件

- `prototype.html`（2562 → 2691 行，+129 行）
- `docs/PROJECT_STATUS.md`
- `docs/session-summary.md`（新建）

### 阶段 1 · 恢复封面屏（核心）

之前 `STATE.screen` 初始为 `"boot"`，`render()` L2373 强跳 `"breakfast"`，没有 `renderTitle()`、`AUDIO_MAP` 也没 `title:`、没有 `go-title` / `begin-day` action。本轮新增完整 title 入口。

| 改动 | 位置 |
|---|---|
| `AUDIO_MAP` 加 `title: { primary: "world" }` | L1138 |
| `STATE.screen` 默认 `"boot"` → `"title"` | L1393 |
| `render()` 删除 boot 强跳，加 title 分支 | L2491-L2499 |
| 新增 `renderTitle()` 函数 | L2081-L2096 |
| 新增 `begin-day` + `go-title` actions | L2611-L2624 |
| `retry-load` 主动 `setScreen("title")` 让恢复路径回封面 | L2611 |
| `resetRun()` 末尾 `setScreen("breakfast")` → `setScreen("title")` | L2576 |
| end 屏按钮 "再来一天" → "回到封面" | L2474 |

封面设计：
- 全屏背景 `bg_00 open.png` + 下半部分阶梯式暗渐变（顶 10% → 底 72%）
- 左下文字块：eyebrow `Vertical Slice · 01` / h1 `像男人一样相亲` / subtitle `瑶珍的四天 · 一个关于"标准答案"的故事` / CTA `开始这一天`
- 右上 audio chip（autoplay 拦截时用户可手动开启）
- 全套 CSS：`.title-cover` + `::after` 渐变 + `.title-shell` flex 容器 + `.title-text-block` 字号层级 + 媒体查询 ≤720px

### 阶段 2 · 跳转核查报告

13 个 actions × 7 个 setScreen 目标全核对。无死路径。`go-title` handler 已注册但当前无按钮触发（保留供后续 dialogue / diary 加返回封面用）。

### 阶段 3 · UI 美化（保守范围）

- 新增 `.btn:disabled` / `[aria-disabled="true"]` 备用状态（opacity 0.5 + cursor not-allowed + pointer-events none）
- `renderBreakfastShell` (L2126) 和 `renderDialogueShell` (L2335) 加 `scene-transition` class，首次进入有 460ms 渐入；patch 路径不重播
- 新增 `@keyframes loadingPulse` + `.loading-pulse` class（透明度 0.55 ↔ 1.0，1.8s 一周期），`renderLoading` 文案 "载入" → "载入中" 并应用 pulse 给视觉反馈

Plan 中列的另外 4 项（按钮 hover/active、字体层级、selection 卡片 hover、chip 间距）现状已完整，本轮无需改动。

### 阶段 4 · 页面完整性盘点 + end 屏 audio chip 补全

9 屏 audit：title / loading / error / breakfast / world / selection / dialogue / diary / end。发现 end 屏是唯一没 audio chip 的玩家屏，本轮补上 — 与 title 屏对称。

### 阶段 5 · 本地 HTTP 验证

- JS 语法 ✅（用 `new Function(scriptContent)` 解析 1559 行 script）
- 8 个代表性资源 200 ✅（含封面图 + dialogue md + audio bgm + character png + 海报）
- 浏览器端到端流程待你手动跑

### 还有哪些问题（不在本轮处理）

- 第二轮图片资产批处理（去白边 / 锯齿 / Feather / 透明 PNG）— 你说过版式固定后再做，现在版式固定 ✅
- Day 2-4 渲染接入（Parser 已就绪，缺 `STATE.breakfastDay` 路由）
- 宋潇接入主流程
- `go-title` 死按钮（已注册 handler，等用户决定哪个屏给按钮）

---

## 2026-06-27 · Round 2（Parser 收口 + UI metadata 清理）

### 修改的文件

- `prototype.html`
- `asset_manifest.md`
- `DevelopmentNotes.md`（合并）
- `Development Notes.md`（删除）
- `Parser_Report.md`（新建）
- `docs/PROJECT_STATUS.md`

### 修改内容

#### 1. Parser 接线核对（阶段 A）

- 核对发现 5 个辅助函数（`stripAllStageDirections` / `isPureSystemMarker` / `isDevMetaParagraph` / `extractAutoPlayObservation` / `stripDirectorCuePrefix`）已经接进 `parseSectionSequence`（L1651-1700）和 `parseBreakfastMarkdown`（L1768/L1777）
- PROJECT_STATUS.md 关于"dead code"的描述系上一轮收尾时未回写状态文档，本轮已对照三份 NPC 源 + 早餐源逐类追踪验证，6 类 metadata 全部被拦截
- 本阶段无代码改动

#### 2. 早餐 Parser 读 Day 1-4（阶段 B）

- 位置：`prototype.html` 第 1752-1804 行
- 抽出新辅助 `parseBreakfastDaySection(section)`：原 `parseBreakfastMarkdown` 主体内容原样搬入，逻辑不变
- `parseBreakfastMarkdown` 改为路由：跑 Day 1-4 并组装 `days: { day1, day2, day3, day4 }`
- 顶层 `scene / news / lines` = Day 1 的值，所有现有渲染消费点（`renderBreakfast` / `renderBreakfastShell` / `breakfastOverlayState` / `STATE.breakfastIndex` 步进）零改动
- 风险：极低。返回值新增 `days` 字段，旧字段语义不变；`findSectionByPrefix` 找不到 Day N 时 `parseBreakfastDaySection("")` 返回空 lines，不崩

#### 3. caption-chip 死代码清理（阶段 C）

PROJECT_STATUS.md §3 P2 列出的三个 UI metadata 残留，实际全都不可见：
- 对白页 caption-chip "Block 1/2/3" 早已被 `.caption-chip { display: none }` 整体隐藏
- 早餐 footer-note 路径 metadata 已是空字符串，只剩"第 N / M 句"进度计数器
- 日记 footer-note 是空 div

虽然玩家看不见，但 caption-chip 的 DOM 仍在每帧被注入。本轮彻底清理：

CSS 侧：
- `.caption-chip,` 从 chip 共用样式组中删除
- 删除独立 `.caption-chip { display: none; }` 规则
- 删除 `.stage-caption {...}` 两处（基础 + 媒体查询响应式）

JS 侧：
- `renderDialogueOverlay` 错误分支：删除 `captionMarkup: ""`
- `renderDialogueOverlay` 主路径：删除 `let captionMarkup = ...` 注入语句
- 返回对象删除 `captionMarkup` 字段
- `renderDialogueShell`：删除 `<div class="stage-caption" id="dialogue-caption-shell">...</div>` shell
- `patchDialogueScreen`：删除 captionShell / captionContent 两个 getElementById、对应 null-check、`captionContent.innerHTML = overlay.captionMarkup` 写入

`block.sourceHeading` 仍保留在数据层（`parseDialogueMarkdown` L1847/L1862/L1877）+ 仅供 `console.log`（L2136）使用，开发期调试日志，不影响 UI。

验证：`grep -c "caption" prototype.html` → 0；文件 2562 → 2553 行（净减 9 行）。

#### 4. 文档同步（阶段 D）

- `asset_manifest.md` L60：`news.mp3` → `news_breakfast.mp3`（与 `audio_map.md` / Parser / Audio Loader 对齐）
- `Development Notes.md`（带空格副本）的英文 Flow Concerns 节合并进 `DevelopmentNotes.md` 文末，并删除带空格副本
- 新建 `Parser_Report.md`：6 类泄漏 + 5 个辅助函数接线点 + Day 1-4 改造 + 副作用登记
- `docs/PROJECT_STATUS.md` 更新到 2026-06-27 现状

### 验证方式

1. `grep` 三轮：`grep -n "caption" prototype.html` → 无匹配；`grep -n "parseBreakfast" prototype.html` → 仅函数定义 + 1 个 `loadGameData` 调用点；`grep -n "news" asset_manifest.md` → 全部 `news_breakfast.mp3`
2. 对照三份 NPC 对白源逐行心算追踪 `parseSectionSequence`，6 类 metadata 均被拦截，正常对白和叙述均能产出
3. 文件行数：2562 → 2553（阶段 C 净减 9 行；阶段 B 净增字段但同时也整体长度变化）

### 还有哪些问题（不在本轮处理）

- Day 2-4 渲染未接入。`parseBreakfastMarkdown` 已能返回 4 天数据，但 `STATE.breakfastDay` 尚未引入，渲染层全部走顶层 `lines`（= Day 1）。属于"新增功能"边缘，需要明确指令再做
- `isDevMetaParagraph` 的 `^瑶珍的回应` 宽松匹配会把 02_陈思远.md L83 `瑶珍的回应带来一个短暂的安静时刻。雨还在下，但小了一些。` 整行滤掉，后半句的环境描写丢失。expand2Section 后续 L85-87 的叙述仍可见，玩家体验上不缺失。**暂不动**
- 宋潇接入主流程、旧路径死代码清理、`renderTitle` / `renderEnd` 加 audio chip 等长期项，均按 PROJECT_STATUS.md §4 标记为"需要明确指令再动"

---

## 2026-06-26 · Round 1（维护模式启动）

### 修改的文件

- `prototype.html`

### 修改内容

#### 1. 修复 `AUDIO_MAP.title` key 拼错

- 位置：`prototype.html` 第 972-974 行（`const AUDIO_MAP` 定义里）
- 改动：`title: { bgm: "world" }` → `title: { primary: "world" }`
- 原因：`currentAudioConfigForState()` 统一读 `AUDIO_MAP[screen].primary`。`title` 节用的是 `bgm`，永远查不到 trackId，结果 title 屏在运行时拿不到任何音频映射（即使想播也找不到 track）。改成 `primary` 后，整张 `AUDIO_MAP` 自洽。
- 风险：极低
  - 首次进入 title 时浏览器 autoplay 仍会拦截（没有 user gesture）→ 行为不变
  - 从 end 屏点"回到标题"返回 title 时，`resetRun()` 会主动 `pauseAudioTrack()`，`syncAudioForState()` 默认 `forcePlay=false` 不会强制重播 → 行为也不变
  - 仅在以后给 title 屏加 audio chip 或主动 `syncAudioForState(true)` 时，行为会按 AUDIO_MAP 期望走 world BGM
- 不动剧情 / 对白 / 资源路径 / Markdown，纯代码 typo 修复

### 验证方式

1. 启动本地 HTTP（`python -m http.server`）拉取 `prototype.html` → 200，64925 字节
2. 用 URL-encoded 路径拉取所有运行时依赖资源：
   - 5 个 dialogue/*.md → 全部 200
   - 6 个 scenes/*.png（含 `bg_00 open.png`）→ 全部 200
   - 1 个 poster + 4 个 bgm/*.m4a + 1 个 news/*.mp3 → 全部 200
   - 8 个 generated_characters/*.png → 全部 200
3. 用 regex 从 `prototype.html` 提取 `const AUDIO_MAP = { ... };` 段，确认所有 9 个 screen 节都用 `primary:` key，无残留 `bgm:`
4. `[impeccable]` 设计 hook 扫描，无反模式（保持现有 typography hierarchy / spacing rhythm / color contrast）

### 还有哪些问题（不在本轮处理）

按你的"维护模式"约束（不动剧情 / 对白 / Markdown / 资源路径 / 不删大量代码），下列项目**有意保留现状**，仅在这里登记：

- 宋潇（Day 4）的 `dialogue/05_宋潇.md` 已存在且 `generated_characters/char_04_songxiao.png` 已就位，但 `NPCS` 数组与 `SOURCE_MANIFEST.dialogues` 都没接通 → Vertical Slice 当前只跑 3 个 NPC（RuntimeRepairReport.md 已声明这是设计选择）
- `dialogue/06_早晨场景变化.md` 写了 Day 1-4，但 `parseBreakfastMarkdown()` 写死只读 `## Day 1` → 早餐永远是 Day 1（同上，刻意保留）
- `prototype.html` 里有若干旧路径残留函数：`renderBreakfast()`、`collectDialogueQuotes()`、`collectTriggerLines()`、`firstNarrativeLine()`、`syncDialogueTimer()`、`renderDialogue()` 返回值的 overlay 字段——都没人调用了。属于"重构"范畴，不在维护模式里动
- `renderTitle()` 和 `renderEnd()` 都没有调用 `renderAudioChip()` → title 和 end 屏没有音频控制按钮。但 title 屏静默是合理的（autoplay 限制），end 屏静默控制是设计取舍。**不动**
- `asset_manifest.md` 的"旧命名备份"段写的是 `news.mp3`，实际目录里是 `news_breakfast.mp3` → 文档与实际不一致。属于"改 Markdown"，**不动**
- `Development Notes.md`（带空格）和 `DevelopmentNotes.md`（不带空格）两份内容不同的笔记并存 → 同样属于 Markdown，**不动**
- `assets/scenes/bg_00 open.png` 文件名带空格，需要浏览器自动 URL-encode → 已验证 OK，但仍是脆弱命名。属于"改资源路径"，**不动**

如果未来你松绑某条约束，再开新一轮处理。
