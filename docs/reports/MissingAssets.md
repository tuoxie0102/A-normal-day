# MissingAssets

## Missing Or Not Yet Wired For This Slice

| Suggested Name | Suggested Size | Suggested Use | Why It Matters |
|---|---|---|---|
| `bg_06_title.png` | 1920x1080 | Dedicated title screen background | Current title screen uses a gradient placeholder because there is no title background in `assets/scenes/` |
| `char_00_player.png` | 1200x1600 | Player-side seated silhouette or back-view figure | Dialogue scene now places both sides into the cafe composition, and the player seat currently uses a placeholder block |
| `obj_11_bento.png` | 1080x1080 | Breakfast scene prop / diary callback | Breakfast copy references home-life setup, but this slice does not yet have the bento image described in `assets/objects/README.md` |
| `obj_12_notes.png` | 1080x1080 | Breakfast scene prop / father's note | Would help breakfast scene feel more specific without adding new mechanics |

## Placeholder Behavior

- All missing images fall back to a visible placeholder panel inside `prototype.html`.
- No asset directories were changed.
- Naming suggestions follow the existing asset logic already present in the project.
