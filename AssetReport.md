# AssetReport

## 当前状态

- 试玩主流程已改为优先使用 `generated_characters/*.png` 作为透明人物图。
- 原始带白底文件仍保留在 `assets/characters/*.png`，没有被覆盖。
- 2026-06-26 实测页面中，早餐页、世界观页、选择页、对话页的人物白底已去除。

## 已去白底并已接入页面的图片

| 角色 / 用途 | 原始文件 | 当前实际显示文件 |
|---|---|---|
| 爸爸 | `assets/characters/char_05_dad.png` | `generated_characters/char_05_dad.png` |
| 妈妈 | `assets/characters/char_06_mom.png` | `generated_characters/char_06_mom.png` |
| 女主默认 | `assets/characters/char_00_player.png` | `generated_characters/char_00_player.png` |
| 女主咖啡厅姿势 | `assets/characters/char_02_cafe.png` | `generated_characters/char_02_cafe.png` |
| 女主茶室姿势 | `assets/characters/char_03_teahouse.png` | `generated_characters/char_03_teahouse.png` |
| 女主公园姿势 | `assets/characters/char_04_park.png` | `generated_characters/char_04_park.png` |
| 陈思远 | `assets/characters/char_01_chensiyuan.png` | `generated_characters/char_01_chensiyuan.png` |
| 林哲 | `assets/characters/char_02_linzhe.png` | `generated_characters/char_02_linzhe.png` |
| 周文涵 | `assets/characters/char_03_zhouwenhan.png` | `generated_characters/char_03_zhouwenhan.png` |

## 已处理但当前 Demo 尚未接入剧情流程的图片

| 角色 / 用途 | 原始文件 | 当前透明文件 |
|---|---|---|
| 宋潇 | `assets/characters/char_04_songxiao.png` | `generated_characters/char_04_songxiao.png` |

## 当前仍缺但不阻塞运行的素材

| 缺失项 | 建议路径 | 说明 |
|---|---|---|
| 奶茶店女主专用姿势 | `assets/characters/char_05_milktea.png` | 以后接宋潇时可直接自动映射 |
| 更多世界观城市广告背景 | `assets/posters/*.png` | 目前世界观页只有 1 张主背景 |

## 风险说明

- 当前透明版是程序抠底结果，已经能正常用于试玩。
- 如果后续要上更精细展示，仍建议你补一套原生透明 PNG，尤其是发丝、纸张边缘、浅色衣物边缘可以更稳。
- 目前最值得后续重出的不是功能素材，而是“高质量透明立绘源图”。
