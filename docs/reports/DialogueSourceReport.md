# DialogueSourceReport

## 结论

当前 HTML Demo 已确认不再读取旧的内嵌对白常量。

当前实际运行时对白源只有一套：

- `dialogue/06_早晨场景变化.md`
- `dialogue/02_陈思远.md`
- `dialogue/03_林哲.md`
- `dialogue/04_周文涵.md`
- `dialogue/08_日记模板.md`

## 当前实际读取文件

### 早餐

- `dialogue/06_早晨场景变化.md`
- 当前 Demo 实际接通的是 `## Day 1 · 陈思远见面日`

### 角色对白

- `dialogue/02_陈思远.md`
- `dialogue/03_林哲.md`
- `dialogue/04_周文涵.md`

### 日记

- `dialogue/08_日记模板.md`

## Loader 与读取流程

### 早餐

`dialogue/06_早晨场景变化.md`

↓

`parseBreakfastMarkdown()`

↓

`currentBreakfast()`

↓

`renderBreakfast()`

### 角色对白

`dialogue/02_陈思远.md` / `03_林哲.md` / `04_周文涵.md`

↓

`parseDialogueMarkdown()`

↓

`currentDialogue()`

↓

`currentBlock()`

↓

`renderDialogue()`

### 日记

`dialogue/08_日记模板.md`

↓

`parseDiaryMarkdown()`

↓

`currentDiaryEntry()`

↓

`renderDiary()`

## 当前 Loader 所在文件

- `prototype.html`

运行方式：

- 浏览器通过 `fetch()` 读取 Markdown
- 不再依赖旧版内嵌对象

## 当前不参与运行时读取的相关文件

- `dialogue/01_相亲流程总控.md`
- `dialogue/05_宋潇.md`
- `dialogue/07_新闻池.md`
- `dialogue/09_社会期待层.md`
- `dialogue/10_便当观察点.md`
- `dialogue/11_语境选项完整映射.md`
- `dialogue.md`
- `《相亲流程总控》版本 2.md`

## Debug Mode

开启方式：

- URL 加 `?debugDialogue=1`
- 或控制台执行 `localStorage.setItem('debugDialogue', '1')`

控制台会输出：

`Loaded:`

`dialogue/02_陈思远.md`

`↓`

`陈思远`

`↓`

`Block 1`

以及文件级读取日志，方便确认当前页面到底读了哪一个角色文件。
