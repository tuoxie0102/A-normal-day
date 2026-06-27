# TextEditGuide

以下路径以“当前 Demo 实际运行时会读到哪里”为准。

## 当前唯一文本源

- `dialogue/06_早晨场景变化.md`
- `dialogue/02_陈思远.md`
- `dialogue/03_林哲.md`
- `dialogue/04_周文涵.md`
- `dialogue/08_日记模板.md`

`prototype.html` 现在只负责：

- Loader
- Parser
- Scene / Dialogue UI

不再保存正文对白。

## 早餐新闻文字

- 文件：`dialogue/06_早晨场景变化.md`
- 修改位置：`**新闻**：...`

## 早餐对白

### 爸爸

- 文件：`dialogue/06_早晨场景变化.md`

### 妈妈

- 文件：`dialogue/06_早晨场景变化.md`

### 女主（早餐中的瑶珍）

- 文件：`dialogue/06_早晨场景变化.md`

说明：

- 当前 HTML Demo 实际接通的是 `## Day 1 · 陈思远见面日`

## 开始相亲页文字

- 当前页面主按钮文字写在 `prototype.html`
- 按钮位置：`renderWorld()`
- 当前文案：`开始相亲`

说明：

- 世界观页主要靠背景环境表达，没有额外大段说明文字。

## 三个男性对象资料 / 名称

- 文件：`prototype.html`
- 变量：`NPCS`

当前字段：

- `name`
- `archetype`
- `portrait`
- `scene`
- `dialogueFile`

说明：

- 当前选择页不会展示长资料，只显示人物和名字。

## 对话 Block 内容

### 陈思远

- 文件：`dialogue/02_陈思远.md`

### 林哲

- 文件：`dialogue/03_林哲.md`

### 周文涵

- 文件：`dialogue/04_周文涵.md`

当前解析结构：

- `## 开场`
- `## 冲突节点 ①`
- `## 冲突节点 ②`
- `## 最终判断`

## 玩家回应选项

- 文件：对应角色自己的 `.md`
- 来源：每个冲突节点和最终判断下方的 Markdown 表格

## 环境提示

- 文件：对应角色自己的 `.md`
- 来源：段落里的叙述句

说明：

- 当前规则是“对白框只放台词”，所以动作 / 环境 / 气氛会优先从叙述句里抽成环境提示。

## 日记内容

- 文件：`dialogue/08_日记模板.md`
- 当前结构：
- `## 陈思远`
- `## 林哲`
- `## 周文涵`
- 每个角色下面的 `### A / B / C`

## 当前不参与运行时读取的文件

- `dialogue/05_宋潇.md`
- `dialogue/07_新闻池.md`
- `dialogue/09_社会期待层.md`
- `dialogue/10_便当观察点.md`
- `dialogue/11_语境选项完整映射.md`
- `dialogue.md`
- `《相亲流程总控》版本 2.md`
