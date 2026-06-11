---
description: キャラクターシートビューア（sheet_view.html）を生成・更新する
argument-hint: [YYYY-MM-DD]（省略時は最新セッション）
---

対象日付: $ARGUMENTS

## 手順

1. 日付が省略されている場合は `ls ud/` で最新のセッションディレクトリを特定する。
2. `ud/[日付]/sheet.md` を読み込む。存在しない場合はその旨を伝えて終了する。
3. `templates/character_view_template.html` を読み込み、テンプレートHTML末尾の
   コメントにある生成ガイドに従って `{{PLACEHOLDER}}` を sheet.md の実データで置換する。
4. `ud/[日付]/sheet_view.html` として出力する。
5. ローカルでブラウザから開けるパスをプレイヤーに伝える。

ビューアは閲覧専用。データの正本はあくまで sheet.md であり、HTMLは生成物である。
