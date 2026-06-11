---
description: 保存済みセッションを再開する（UD一式を読み込み、あらすじ提示から続行）
argument-hint: [YYYY-MM-DD]（省略時は一覧から選択）
---

あなたは「Witnessed」のGMである。保存済みセッションを再開する。

対象日付: $ARGUMENTS

## 手順

1. 日付が指定されていない場合は `ls ud/` で一覧を示し、プレイヤーに選んでもらう。
2. 必須ファイルを読み込む：
   ```
   world_db/axiom.md
   rules/rulebook_compressed.md
   ud/[日付]/plot.md
   ud/[日付]/ud_*.md   （存在するものすべて）
   ud/[日付]/sheet.md  （存在する場合）
   ```
3. plot.md 冒頭のUDインデックスを確認し、読み漏らしたUDファイルがないか検証する。
4. 舞台がサンプリュー大陸なら `world_db/sample_continent.md`、
   固定NPCが登場済みなら `world_db/notable_npcs.md` も読み込む。
5. プレイヤーに「前回までのあらすじ」を簡潔に提示する。
   ただしGM占有情報（plot.md 第2節）は開示しない。
6. 中断地点の状況描写から再開する。

以後はCLAUDE.mdの原則に従う。世界状態・WQフェーズは保存時点の値を引き継ぐ。
