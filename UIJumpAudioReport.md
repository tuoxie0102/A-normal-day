# UI / Jump / Audio Report

## 1. 改了哪些文件

- `prototype.html`
- `UIJumpAudioReport.md`

## 2. 人物尺寸规则在哪里

- 统一 sprite 容器规则在 `prototype.html:254` 的 `.character-figure`
- 早餐场景底边规则在 `prototype.html:288` 的 `.breakfast-figure`
- 角色分型 class 在 `prototype.html:292` 起的 `.sprite-*`
- 角色资源到分型 class 的映射在 `prototype.html:815` 的 `CHARACTER_ROLE_CLASS`

当前规则：
- `max-height` 受 `.character-figure` 约束，最高不超过舞台高度 `72%`
- 使用 `bottom: var(--sprite-bottom, 154px)` 保持贴近舞台底部 / 对话区上沿
- `img` 使用 `max-width: 100%` + `max-height: 100%` + `object-position: center bottom`，避免头部和身体被裁出屏幕

## 3. 解决整屏跳闪的代码位置

- 对白局部更新层在 `prototype.html:1568` 的 `renderDialogueOverlay`
- 对白场景骨架挂载在 `prototype.html:1668` 的 `mountDialogueScreen`
- 同场景只更新 overlay、不重挂背景和角色，在 `prototype.html:1675` 的 `patchDialogueScreen`
- 总渲染分支切换在 `prototype.html:1744` 的 `render()`，对白页优先走 `patchDialogueScreen()`

结果：
- 点击“继续”或推进对白时，不再 `app.innerHTML` 重建整页
- 背景、人物和顶栏保持不刷新
- 只更新对白层内容

## 4. 修复跳转逻辑的代码位置

- 选择回应的保护和状态推进在 `prototype.html:1806` 的 `chooseResponse(index)`
- 下一段 / 写日记的状态推进在 `prototype.html:1819` 的 `nextBlock()`
- 进入对白时的初始化在 `prototype.html:1784` 的 `startDialogue(npcId)`

修复点：
- `chooseResponse` 增加 index 有效性校验，避免无效选择把状态机卡死
- 选择后显式更新 `selectedResponseIndex`、`lastChoiceTone`、`dialoguePhase = "reaction"`
- `nextBlock` 只允许从 `reaction` 进入下一段，避免状态错位
- 下一段会正确递增 `blockIndex` 并执行 `resetDialogueBlock()`

## 5. 三个男主是否都已跑通

已跑通：
- 陈思远：寒暄 -> 第一次回应 -> 第二轮对话 -> 第二次回应 -> 结束 -> 日记
- 林哲：寒暄 -> 第一次回应 -> 第二轮对话 -> 第二次回应 -> 结束 -> 日记
- 周文涵：寒暄 -> 第一次回应 -> 第二轮对话 -> 第二次回应 -> 结束 -> 日记

验证方式：
- 使用 Node + VM 对 `prototype.html` 内联脚本做状态流模拟
- 验证对白期间 scene 没有被重新 mount
- 验证三条路线都能进入 `diary`

## 6. 音乐资源接入测试

### 当前读取的音频

- 文件：`bgm_morning.m4a`
- 路径：`assets/audio/bgm_morning.m4a`
- 配置位置：`prototype.html:806` 的 `AUDIO_TRACKS`

### 音频接入代码位置

- 音频状态单例：`prototype.html:828` 的 `AUDIO_STATE`
- 播放 / 复用逻辑：`prototype.html:912` 的 `playAudioTrack(trackId)`
- 暂停 / 继续逻辑：`prototype.html:945` 的 `toggleAudioTrack()`
- 早餐开场自动播放触发：`prototype.html:1865`
- 右上角喇叭按钮渲染：`prototype.html:878` 的 `renderAudioChip()`

### 测试结果

- 路径正确：是
- 浏览器读取路径：代码已指向 `assets/audio/bgm_morning.m4a`
- 404：本地脚本验证未发现 404
- 编码格式支持：当前使用 `m4a`，`Audio.canPlayType("audio/mp4")` 验证结果为 `probably`
- 成功播放：是
- 支持 loop：是
- 支持 pause / resume：是
- Scene 切换是否重载同一首音乐：否，同一 `Audio` 实例复用
- 点击“继续”是否会重新开始播放：否
- 刷新页面后行为：会重新播放，不保留进度

### Autoplay Policy

- 这轮实现把首次播放绑定到用户点击“进入早餐”之后，因此常见浏览器下通常不会被拦截
- 如果浏览器环境更严格，仍可能出现自动播放策略限制；代码会记录 `autoplayBlocked`
- 本地脚本模拟结果：`autoplayBlocked = false`
