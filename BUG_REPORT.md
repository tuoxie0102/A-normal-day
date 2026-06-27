# Bug Report

## 1. 闪白问题是否彻底解决

已在当前运行时结构内解决。

本轮处理后：

- 不再整页白闪
- 不再对白框白闪
- 背景、人物、对白框容器保持常驻
- 点击后只替换文字内容
- 动画只保留在文字层的轻微 `textFade`

## 2. 是哪个 CSS / JS 导致闪白

### CSS 原因

- `prototype.html` 里的 `.dialogue-tray` 之前带有 `animation: dialogueFade`
- 环境提示类元素会重复插入，旧结构下容易形成“白一下”的观感
- 旧结构每次都重建带背景色的块，而不是只改文字

### JS 原因

- 旧的对白渲染会反复替换 overlay 大块 HTML
- 早餐场景点击继续会整屏 `renderBreakfast()`，导致容器重建
- 旧对白状态机按 `environment / monologue / response` 自动切换，内容块会不断重插

### 本轮修复位置

- `prototype.html`
  - `.dialogue-tray`
  - `.narration-panel`
  - `@keyframes textFade`
  - `mountBreakfastScreen()`
  - `patchBreakfastScreen()`
  - `mountDialogueScreen()`
  - `patchDialogueScreen()`

## 3. MD 中环境描写现在如何识别

当前规则：

- 普通段落：识别为 `narration`
- 普通列表项：识别为 `narration`
- `> **角色名**：内容`：识别为 `dialogue`
- `>` 开头但不是角色说话：识别为 `narration`
- 括号里的“自动播放结束”“她注意到……”这类内容：识别为 `narration`
- `**玩家选择**` 和表格：不进入叙述/对白序列，交给 response 逻辑

核心代码在 `prototype.html`：

- `parseSectionSequence()`
- `parseDialogueMarkdown()`

## 4. 环境描写显示在哪里

环境描写现在单独显示在对白框上方的独立叙述面板里，不再塞进角色对白框。

对应容器：

- `.narration-panel`

角色真正说出口的话显示在：

- `.dialogue-tray`

玩家选择显示在：

- `.response-panel`

## 5. 早餐 Scene 当前读取哪一个 news 音频文件

当前读取：

- 文件名：`news_breakfast.mp3`
- 代码路径：`assets/audio/news/news_breakfast.mp3`
- 代码位置：`prototype.html` 的 `AUDIO_TRACKS.news_breakfast`
- 运行时映射：`prototype.html` 的 `AUDIO_MAP.breakfast.primary`

实际文件路径：

- `assets/audio/news/news_breakfast.mp3`

本地文件存在性：

- `Test-Path assets/audio/news/news_breakfast.mp3` = `True`

## 6. 早餐 Scene 是否已关闭 BGM

已关闭。

当前早餐场景不再读取 `bgm_breakfast.m4a`，而是只读取：

- `news_breakfast.mp3`

也就是说：

- 早餐 Scene：新闻音频
- 非早餐 Scene：BGM

## 7. 如果新闻音频没播出来，具体原因是什么

当前代码路径和实际文件路径是一致的，未发现 404：

- 当前代码读取路径：`assets/audio/news/news_breakfast.mp3`
- 实际文件路径：`assets/audio/news/news_breakfast.mp3`
- 本地存在：是

如果浏览器里仍然没播出来，剩余高概率原因只有两类：

### 自动播放策略

- 早餐新闻会在进入早餐 Scene 时尝试自动播放
- 某些浏览器可能拦截首个未授权播放
- 右上角按钮可用于手动继续播放

### 浏览器编码支持异常

- 当前文件格式是 `mp3`
- 运行时声明 MIME：`audio/mpeg`
- 常见现代浏览器一般支持

## 附加验证

### Block 是否跑通

已验证跑通：

- 陈思远：`Block1 -> Response1 -> Block2 -> Response2 -> Block3 -> Diary`
- 林哲：`Block1 -> Response1 -> Block2 -> Response2 -> Block3 -> Diary`
- 周文涵：`Block1 -> Response1 -> Block2 -> Response2 -> Block3 -> Diary`

### 当前阅读节奏

已改为手动点击推进：

- 环境描写
- 点击继续
- 角色对白
- 点击继续
- 下一段叙述 / 对白
- 最后进入玩家回应

默认不再强制自动快速播放。
