---
description: セッションをセーブする（ログ書き出し + コミット）
---
現在の進行をセーブする。

1. プレイログを sessions/YYYY-MM-DD.md に templates/play_log.md の形式で書き出す
   （同日2回目以降は追記）。
2. ud/[日付]/ の各ファイル（plot.md ほか）を現状に合わせて更新する。
3. `python tools/state.py show` で state/ とプレイ内容の一致を確認する。
4. ログ末尾に「次回への引継ぎ」を3〜5行（現在地・直近の目的・動いているタイムライン）。
5. git add して「セーブ: <一言要約>」でコミットする。
   ※ sealed/ への追記が必要だった場合は、別コミットに分ける（revision.md §4.2）。

章末を跨ぐ場合は先に /endchapter を実行すること。
