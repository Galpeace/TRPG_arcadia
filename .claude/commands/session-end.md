---
description: セッション終了処理を実行する（エンドロール→session_ud.md→キャラ保存確認）
---

あなたは「Witnessed」のGMである。セッション終了処理を、省略せず順に実行せよ。

## 前提

直前の章の章末処理（/chapter-end）が未実行なら、先にそれを完了させる。

## 終了処理（CLAUDE.md セッション終了時ルール準拠）

1. **エンドロール描写** — 本作の核心として、必ず描写に格上げして出力する。
2. **session_ud.md の出力** — `ud/YYYY-MM-DD/session_ud.md` を作成する。
   雛形は `templates/play_log.md` を参照。
3. **キャラクター保存の確認** — プレイヤーに確認する：
   「キャラクターデータを保存しますか？」
4. **保存する場合：**
   - `ud/YYYY-MM-DD/sheet.md` を最終状態で更新する（雛形: `templates/character_sheet.md`）。
   - 任意で `ud/YYYY-MM-DD/sheet_view.html` を生成する（/sheet コマンドでも可）。
   - 保存データはUD性質を保つ。世界はこの記録を記憶しない。
5. **コミット** — 生成・更新したUDファイル一式を git でコミット・プッシュする
   （ブランチ運用は CLAUDE.md / README.md に従う）。

最後に、次回 `/resume YYYY-MM-DD` で再開できることをプレイヤーに伝える。
