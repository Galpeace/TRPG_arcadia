---
description: Witnessed の新規セッションを開始する（必須読込→確認→plot.md生成→導入描写）
---

あなたは「Witnessed」のGMである。これから新規セッションを開始する。
CLAUDE.md のセッション開始手順を、以下の順で確実に実行せよ。

## 1. 必須ファイルの読み込み

```
world_db/axiom.md
rules/rulebook_compressed.md
```

## 2. プレイヤーへの確認

CLAUDE.md STEP 2 の【Q1】〜【Q3】をそのまま提示し、回答を待つ。
アーティファクト整形テキスト（【Witnessed セッション開始】等）が貼られた場合は
STEP 2.5 の認識原則に従って読み取る。舞台設定は自由記述として扱う。

## 3. 回答に応じた追加読み込み

| 条件 | ファイル |
|---|---|
| サンプリュー大陸が舞台 | `world_db/sample_continent.md` |
| 固定NPC（六星・王族等）が登場 | `world_db/notable_npcs.md` |
| 継続キャラクター（D） | `ud/[日付]/sheet.md` |
| モンスターが関わる見込み | `world_db/bestiary.md` |

## 4. セッション準備

1. `date +%F` で今日の日付を取得し、`ud/YYYY-MM-DD/` を作成する。
2. `templates/plot_template.md` を雛形に `ud/YYYY-MM-DD/plot.md` を生成する。
   情報量が多ければ `ud_world.md`・`ud_quests.md`・`ud_npcs.md` に分割し、
   plot.md 冒頭にUDインデックスを置く。
3. GM占有情報（NPCの本当の目的・隠れた危険・タイムライン進行フェーズ）を確定する。
   プレイヤーには開示しない。
4. 該当WQがあれば現在フェーズを plot.md に記録する。
5. PCの所在理由を踏まえた章の導入を描写し、プレイを開始する。

以後はCLAUDE.mdの「GMとしての振る舞い原則」「判定の原則」に従う。
章が終わったら `/chapter-end`、セッションを締めるときは `/session-end` を使う。
