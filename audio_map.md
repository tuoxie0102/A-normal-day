# Audio Map

## Runtime Owner

- JS: `prototype.html`
  - `AUDIO_TRACKS`
  - `AUDIO_MAP`
  - `currentAudioConfigForState()`
  - `currentTrackIdForState()`
  - `syncAudioForState()`
- JSON: 当前没有独立音频 JSON
- Markdown:
  - `audio_map.md`
  - `assets/audio/README.md`

## Scene Mapping

### Scene 1

- Name: `Breakfast`
- Primary Audio: `assets/audio/news/news_breakfast.mp3`
- BGM: `关闭`
- Runtime screen key: `breakfast`

### Scene 2

- Name: `World`
- BGM: `assets/audio/bgm/bgm_world.m4a`
- Runtime screen key: `world`

### Scene 3

- Name: `Selection`
- BGM: `assets/audio/bgm/bgm_world.m4a`
- Runtime screen key: `selection`

### Scene 4

- Name: `Coffee / 陈思远`
- BGM: `assets/audio/bgm/bgm_cafe.m4a`
- Runtime screen key: `dialogue.chensiyuan`

### Scene 5

- Name: `Teahouse / 林哲`
- BGM: `assets/audio/bgm/bgm_teahouse.m4a`
- Runtime screen key: `dialogue.linzhe`

### Scene 6

- Name: `Park / 周文涵`
- BGM: `assets/audio/bgm/bgm_park.m4a`
- Runtime screen key: `dialogue.zhouwenhan`

### Scene 7

- Name: `Diary`
- BGM: `assets/audio/bgm/bgm_diary.m4a`
- Runtime screen key: `diary`

### Scene 8

- Name: `End`
- BGM: `assets/audio/bgm/bgm_world.m4a`
- Runtime screen key: `end`

## Current Notes

- 早餐场景当前只走新闻音频，不播放 BGM
- 右上角按钮在早餐场景控制的是新闻音频暂停 / 继续
- 旧命名资源保留在 `assets/audio/_legacy/`，运行时不再引用
