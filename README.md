# Witnessed — TRPG リポジトリ

ソロプレイ用ハイファンタジーTRPG「Witnessed」のGMデータリポジトリ。
Claude Code をGMとして遊ぶ。

## 遊び方（スラッシュコマンド）

| コマンド | 内容 |
|---|---|
| `/session-start` | 新規セッションを開始する |
| `/resume [日付]` | 保存済みセッションを再開する |
| `/chapter-end` | 章末処理を実行する |
| `/session-end` | セッション終了処理（保存・エンドロール） |
| `/sheet [日付]` | キャラクターシートビューアを生成する |

自然文での依頼でも同じ手順で進行する（`CLAUDE.md` 参照）。
起動時に保存済みセッションの一覧が自動表示される（`.claude/settings.json` のフック）。

## ブランチ運用

**mainブランチを直接編集する。フィーチャーブランチは使用しない。**

```
git push -u origin main
```

## ファイル構成

```
CLAUDE.md        — GMプロンプト（セッション開始手順・振る舞い原則）
world_db/        — WD（周回をまたいで変わらない世界の骨子）
rules/           — ルールブック（圧縮版＝毎回読込 / 詳細版＝参照用）
ud/YYYY-MM-DD/   — UD（セッションごとの生成データ：plot.md・sheet.md 等）
templates/       — 各種テンプレート・アーティファクト仕様
.claude/         — スラッシュコマンドと起動フック
```

## セッション開始

`/session-start` を実行するか、`CLAUDE.md` を参照。
