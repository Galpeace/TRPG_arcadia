# TRPG Arcadia

Claude Code の中で遊ぶソロプレイTRPG。**Claudeが物語を、コードが数字を担当する。**

- ダイスは `tools/roll.py` が OS の乱数源で振る（GMの脳内ロール禁止）
- HP・所持金・アイテムは `state/*.json` が正で、`tools/state.py` 経由でのみ更新
- セーブは git コミット。`git log` がそのままプレイ履歴になる

## 遊び方

Claude Code をこのリポジトリで開いて:

| コマンド | 内容 |
|---|---|
| `/start` | セッション開始（状態読み込み or キャラメイク） |
| `/recap` | これまでのあらすじ |
| `/save` | プレイログ書き出し + コミット |
| `/handoff` | 次のチャットへの引継ぎ書を生成 |

コマンドを使わず普通に話しかけても、GM（CLAUDE.md）が同じ手順で動く。

## 状態

骨組みのみ完成。ゲームシステム（`rules/system.md`）と世界設定（`world/world.md`）は
新規設計中で、各ファイルに設計チェックリストがある。
