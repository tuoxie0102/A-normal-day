# 像男人一样相亲

一个单文件 Web 叙事原型。玩家以女主视角经历连续 3 天的相亲流程：早餐场景、世界观过场、对象选择、分段对话、日记总结与日终收束。

## 当前版本

- 入口流程：`title -> breakfast -> world -> selection -> dialogue -> diary -> end`
- 可体验对象：陈思远 / 林哲 / 周文涵
- 支持 Day 1-3 主线推进
- 支持当天主线完成后的“再聊一次”模式
- 对白与早餐内容来自 `dialogue/` 下的 Markdown 文件

## 运行方式

项目不能直接用 `file://` 打开，因为运行时会 `fetch` 本地 Markdown。

在项目根目录启动一个静态服务器，例如：

```bash
python -m http.server 8000
```

然后在浏览器打开：

```text
http://localhost:8000/prototype.html
```

## 目录说明

- `prototype.html`：主运行时，包含 UI、状态机、Parser、音频与路由
- `dialogue/`：早餐、对白、日记等 Markdown 内容源
- `generated_characters/`：运行时人物立绘资源
- `assets/`：场景、海报、物件、音频等资源
- `docs/`：项目状态和开发过程文档

## 项目维护规则

- 每次修改前先阅读 `README.md`、`docs/archives/`、`docs/reports/`，以及当前任务直接相关的文件。
- 每次修改前必须先执行 `git status`。
- 根目录不要继续堆放新的报告类 Markdown；临时报告统一放到 `docs/reports/`。
- 过期文档统一移入 `docs/archives/`，不要直接删除。
- 每次修改后都要说明改了哪些文件。
- 每完成一个独立任务，执行一次 commit。
- commit message 规范：
  - `feat:` 新功能
  - `fix:` 修复问题
  - `ui:` 界面优化
  - `docs:` 文档更新
  - `chore:` 项目整理
  - `release:` 发布版本
- 未经确认，不删除源码、素材、对白文本或 `README.md`。
- 未经明确要求，不重写核心业务逻辑。
- 如果发现 Git 异常，必须先停止并报告，不能自行强推。

## 已知边界

- 当前发布版本主流程覆盖 Day 1-3
- 宋潇相关内容和 Day 4 资源已存在，但未接入当前主流程
- 刷新页面后不会保留当天运行中的状态

## 发布说明

这是一个前端原型项目，未引入构建系统，也没有外部依赖安装步骤。只要静态文件与资源完整，即可本地运行。
