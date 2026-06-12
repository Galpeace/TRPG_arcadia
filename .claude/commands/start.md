---
description: Witnessed セッション（周回）を開始する
---
セッションを開始する。CLAUDE.md の読み込み順序に従い、axiom.md・
rulebook_compressed.md・revision.md §1 を読んでから以下を行う。

1. `python tools/state.py show` で状態を確認。前周回のデータが残っていれば、
   UD破棄（state/*.json の初期化、ud/ の整理）を確認してから始める。
2. プレイヤーに方向性を確認する:
   - A. GM裁量起点 — キャラと舞台を聞き、GMがクエストを構築
   - B. WQ選択 — world_db/sample_continent.md のWQから選ぶ
   - C. クエスト方向性 — やりたいことを一言で
   - D. 継続キャラクター — characters/ の保存シートを読み込む（死亡PCは不可）
   モンスターPCも正規の選択肢である（revision.md §6。知性プロファイルから作る）。
3. キャラクターシートを templates/character_sheet.md に沿って確定し、
   `tools/state.py new` で登録、シートを ud/[日付]/sheet.md に書く。
4. `ud/[日付]/plot.md` を templates/plot_template.md から作成し、以下を**固定**する:
   - セッション形式（短編/中編）
   - 致死性条項（revision.md §1.5）— 以後周回中の変更禁止
   - タイムライン初期値（WQフェーズ等。P2以降は state/timelines.json にも記載）
5. **ユニーククエストの場合**: 真相（黒幕・動機・隠れた因果・固有の致死条件）を
   `ud/[日付]/sealed/truth.md` に書き、直ちに単独でコミットする（revision.md §4.2）。
   ワールドクエストには封緘しない。
6. 導入描写から開始する。
