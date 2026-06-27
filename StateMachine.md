# StateMachine.md · 游戏状态机

> 每个 State 定义：进入条件、退出条件、保存数据、所需 UI。

---

## 状态图

```
TITLE
  │
  ▼
HOME
  │
  ▼
VENUE ──→ OBSERVATION（子状态）
  │           │
  │           ▼
  │       OBS_DONE
  │           │
  ◄───────────┘
  │
  ▼
DIALOGUE
  │
  ├── DIALOGUE_INTRO（自动）
  │       │
  │       ▼
  ├── DIALOGUE_CONFLICT_1（互动）
  │       │
  │       ▼
  ├── DIALOGUE_UNFOLD_1（自动）
  │       │
  │       ▼
  ├── DIALOGUE_CONFLICT_2（互动）
  │       │
  │       ▼
  ├── DIALOGUE_UNFOLD_2（自动）
  │       │
  │       ▼
  └── DIALOGUE_JUDGMENT（互动）
          │
          ▼
AFTERMATH
  │
  ▼
RECORD
  │
  ▼
HOME（Day N+1）或 WEEK_SUMMARY
```

---

## 状态详细定义

### TITLE

| 属性 | 值 |
|------|-----|
| 进入条件 | 游戏启动 |
| 退出条件 | 点击「开始游戏」 |
| 保存数据 | 无（新游戏）/ 读取存档（继续） |
| 所需 UI | 标题字。3 个按钮（开始 / 档案 / 退出）。 |

### HOME

| 属性 | 值 |
|------|-----|
| 进入条件 | TITLE → 开始 / RECORD → 下一天 |
| 退出条件 | 早晨对话播放完毕 |
| 保存数据 | `currentDay`、`dayNews`、`dayNpcId`、`dayBento` |
| 所需 UI | 场景背景。电视新闻。对话文本框（自动播放）。 |

### VENUE

| 属性 | 值 |
|------|-----|
| 进入条件 | HOME 结束 |
| 退出条件 | 玩家选择「坐下」或进入 OBSERVATION 子状态 |
| 保存数据 | 无（过渡状态） |
| 所需 UI | 场景背景。NPC 角色图。「他还没发现你」选择框（2 个按钮）。 |

### OBSERVATION（子状态）

| 属性 | 值 |
|------|-----|
| 进入条件 | VENUE 中选择「先观察一下」 |
| 退出条件 | 时间耗尽 OR 玩家点击「坐下」按钮 |
| 保存数据 | `observedTags[]`（语境标签列表）、`timeRemaining`（剩余时间） |
| 所需 UI | 闪烁物品热点。时间条（绿→黄→红）。第一印象面板（标签淡入）。「坐下」按钮。 |

### DIALOGUE（含 6 个子状态）

| 属性 | 值 |
|------|-----|
| 进入条件 | VENUE 结束 或 OBSERVATION 结束 |
| 退出条件 | 最终判断选择完毕 + 道别动画结束 |
| 保存数据 | `choiceHistory[]`（每次冲突节点的选择索引）、`endingType`（继续/开放/朋友） |
| 所需 UI | 对话文本框。态度选择按钮（4+1）。跳过按钮。冲突节点遮罩。关键句高亮框。 |

#### DIALOGUE_INTRO

| 属性 | 值 |
|------|-----|
| 类型 | 自动 |
| 时长 | ~30s |
| 退出条件 | 台词播放完毕或玩家跳过 |
| UI | 文本框 + 跳过按钮 |

#### DIALOGUE_CONFLICT_1

| 属性 | 值 |
|------|-----|
| 类型 | 互动 |
| 退出条件 | 玩家选择态度 |
| 保存 | `choiceHistory[0]` = 选择索引（0-4） |
| UI | 遮罩 + 关键句高亮 + 4-5 个态度按钮 |

#### DIALOGUE_UNFOLD_1

| 属性 | 值 |
|------|-----|
| 类型 | 自动 |
| 路径 | `choiceHistory[0] < 2` → 路径A，否则 → 路径B |
| 退出条件 | 台词播放完毕或跳过 |
| UI | 文本框 + 跳过按钮 |

#### DIALOGUE_CONFLICT_2

| 属性 | 值 |
|------|-----|
| 类型 | 互动 |
| 退出条件 | 玩家选择态度 |
| 保存 | `choiceHistory[1]` = 选择索引（0-4） |
| UI | 同 CONFLICT_1 |

#### DIALOGUE_UNFOLD_2

| 属性 | 值 |
|------|-----|
| 类型 | 自动 |
| 路径 | `choiceHistory[1] < 2` → 路径A，否则 → 路径B |
| 退出条件 | 台词播放完毕或跳过 |
| UI | 文本框 + 跳过按钮 |

#### DIALOGUE_JUDGMENT

| 属性 | 值 |
|------|-----|
| 类型 | 互动 |
| 退出条件 | 玩家选择结局方向 |
| 保存 | `endingType` = 0/1/2（继续/开放/朋友） |
| UI | 遮罩 + 关键句高亮 + 3 个结局按钮 + 道别动画 |

### AFTERMATH

| 属性 | 值 |
|------|-----|
| 进入条件 | DIALOGUE 结束 |
| 退出条件 | 玩家选择「再看看」或「等他回来」 |
| 保存 | `aftermathObserved` = 索引或 null |
| 所需 UI | 「他走开了」选择框（2 个按钮）。 |

### RECORD

| 属性 | 值 |
|------|-----|
| 进入条件 | AFTERMATH 结束 |
| 退出条件 | 点击「下一天」 |
| 保存 | 完整记录写入 `records[]` |
| 所需 UI | 《今日相亲记录》面板。可滚动。「下一天」按钮。 |

---

## 跨状态持久化数据

```js
gameState = {
  currentDay: 1,           // 当前天数（1-4）
  records: [],             // 每日记录 [{npcId, endingType, tags, keyLines, diaryLine}]
  unlockedNpcs: [],        // 已解锁后续对话的 NPC ID
  totalPlaytime: 0,        // 累计时间（可选）
}
```

## 单日临时数据

```js
dayState = {
  npcId: "chensiyuan",     // 当天 NPC
  sceneId: "cafe",         // 当天场景
  weather: "rain",         // 天气
  news: "...",             // 当天新闻标题
  observedTags: [],        // 观察阶段收集的标签
  choiceHistory: [],       // [conflict1_choice, conflict2_choice]
  endingType: 0,           // 0=继续 1=开放 2=朋友
  aftermathObserved: null, // 买单阶段观察结果
}
```
