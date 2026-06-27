# NPCFramework.md · NPC 模板

> 所有 NPC（包括当前 4 人和未来扩展）按此模板定义。
> 目标：未来 100 个 NPC 也可以填入同一张表。

---

## 一、NPC 数据模板

```json
{
  "id": "string",
  "name": "string",
  "age": 0,
  "occupation": "string",
  "scene": "string",
  "weather": "string",
  "coreConflict": "string",
  "hiddenSecret": "string",
  "keywords": ["string"],
  "intro": {
    "sceneDescription": "string",
    "autoLines": [
      { "speaker": "string|null", "text": "string" }
    ]
  },
  "conflict1": {
    "triggerLine": "string",
    "contextNote": "string",
    "responses": [
      {
        "attitude": "understand|challenge|tease|data",
        "yaozhenLine": "string",
        "npcReaction": [{ "speaker": "string|null", "text": "string" }]
      }
    ]
  },
  "unfold1": {
    "pathA": [{ "speaker": "string|null", "text": "string" }],
    "pathB": [{ "speaker": "string|null", "text": "string" }]
  },
  "conflict2": {
    "triggerLine": "string",
    "contextNote": "string",
    "responses": [
      {
        "attitude": "understand|challenge|tease|data",
        "yaozhenLine": "string",
        "npcReaction": [{ "speaker": "string|null", "text": "string" }]
      }
    ]
  },
  "unfold2": {
    "pathA": [{ "speaker": "string|null", "text": "string" }],
    "pathB": [{ "speaker": "string|null", "text": "string" }]
  },
  "judgment": {
    "triggerLine": "string",
    "contextNote": "string",
    "endings": [
      {
        "type": "continue|open|friend",
        "yaozhenLine": "string",
        "npcReaction": "string",
        "diaryLine": "string"
      }
    ]
  },
  "observationPoints": [
    {
      "category": "behavior|object|appearance|environment|speech|hidden",
      "hotspotPosition": "string",
      "factText": "string",
      "tag": "string"
    }
  ],
  "aftermathPoints": [
    { "factText": "string" },
    { "factText": "string" }
  ]
}
```

---

## 二、字段说明

### 基础属性

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 唯一标识。如 `"chensiyuan"` |
| `name` | string | 显示名。如 `"陈思远"` |
| `age` | int | 年龄 |
| `occupation` | string | 职业 |
| `scene` | string | 对应场景 ID，如 `"cafe"` |
| `weather` | string | 天气，如 `"rain"` |
| `coreConflict` | string | 一句话概括核心矛盾。用于系统自动匹配新闻。 |
| `hiddenSecret` | string | 隐藏信息。在对话中逐渐暴露。 |
| `keywords` | string[] | 3-5 个关键词。用于标签和搜索。 |

### 对话数据结构

| 字段 | 说明 |
|------|------|
| `intro` | 开场。自动播放。5-7 行。 |
| `conflict1` | 第一个冲突节点。4 个态度 × 对应反应。 |
| `unfold1` | 展开段落。2 条路径（取决于 conflict1 选择）。 |
| `conflict2` | 第二个冲突节点。同上。 |
| `unfold2` | 展开段落。同上。 |
| `judgment` | 最终判断。3 个结局方向。 |

### 态度选项的 4 个值

| attitude 值 | 含义 |
|------------|------|
| `understand` | 🙂 理解——共情但不拯救 |
| `challenge` | 🤔 追问——挑战预设 |
| `tease` | 😏 调侃——消解紧张 |
| `data` | 📊 数据——理性对撞 |

### 观察点数据结构

| 字段 | 说明 |
|------|------|
| `category` | 类别：`behavior`/`object`/`appearance`/`environment`/`speech`/`hidden` |
| `hotspotPosition` | 在屏幕上的位置描述。如 `"left-table-cup"` |
| `factText` | 事实先于评价。如「杯里的水已经凉了。」 |
| `tag` | 2-5 字标签。如「紧张」。写入第一印象面板。 |

### 结局类型

| endingType 值 | 含义 |
|--------------|------|
| `continue` | 继续了解——瑶珍表达了真实兴趣 |
| `open` | 开放结局——不完全关闭 |
| `friend` | 转朋友——明确的非浪漫出口 |

---

## 三、100 个 NPC 时的扩展策略

### 不需要修改的

- 以上 JSON 模板结构
- 6 个 Block 的对话框架
- 4 个态度选项
- 3 种结局类型
- 观察点 6 类别

### 按难度分层

| 层 | NPC 数量 | 内容复杂度 | 适用 |
|----|---------|-----------|------|
| L1 手写 | 4-10 个 | 全部手写。冲突独特。 | Demo / 核心角色 |
| L2 模板填充 | 11-50 个 | 共享 5-8 个「冲突类型模板」。填入不同观察点和关键句。 | 常规扩展 |
| L3 程序化 | 51-100 个 | 从「冲突类型库」中 2 组合。观察点从「观察点库」按场景分配。 | 大量填充 |

### 冲突类型库（示例）

```
职业焦虑型     —— 「我喜欢工作，但社会说男人不该有事业心」
年龄恐慌型     —— 「最佳生育年龄又提前了」
身体规训型     —— 「我为了相亲专门剃了/穿了/戒了」
家庭压力型     —— 「我妈让我来的」
梦想贬低型     —— 「我喜欢XX，但别人说这有什么用」
情感创伤型     —— 「被拒绝太多次，我学会了先拒绝别人」
讨好消耗型     —— 「我一直在猜对方想要什么」
```

一个新 NPC = 从库中选 2 个冲突类型 + 填观察点 + 填场景。

---

## 四、当前 4 个 NPC 的模板映射

| NPC | coreConflict | hiddenSecret | 冲突①类型 | 冲突②类型 |
|-----|-------------|-------------|----------|----------|
| 陈思远 | 自我物化——把「好男人标准」彻底内化 | 他其实不喜欢小孩 | 身体规训型 | 家庭压力型 |
| 林哲 | 事业与男德的矛盾——想升职但「男人不该太有野心」 | 「如果我不写代码，我还是我吗」 | 职业焦虑型 | 讨好消耗型 |
| 周文涵 | 22 次失败后筑墙——用效率保护自己 | 墙上有一页空白 | 情感创伤型 | 身体规训型 |
| 宋潇 | 年龄焦虑——深信自己「快过期了」 | 床底下有一套情绪拼图设计 | 年龄恐慌型 | 梦想贬低型 |
