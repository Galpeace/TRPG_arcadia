# 観測のアルカディア ルールブック

ソロプレイ向けTRPG「観測のアルカディア」のルールブック最終版です。

## 中核思想

「観測のアルカディア」では、PCが世界を観測し、世界もまたPCを観測します。世界は固定的であり、PCはその上を通過する不確定な因子（化学変化）として位置付けられます。評価の非対称（PCの自己認識と世界の評価のズレ）が物語の核です。周回プレイを前提とします。

## ファイル構造

```
1_setting/
  1T-core_theme.md         中核テーマ

2_rulebook/
  メタ系（M）:
    2M-glossary.md         用語集
    2M-index.md            プロトコル索引
    2M-antipatterns.md     違反兆候集
    2M-response_protocol.md 応答プロトコル
  
  ルール本体（R、14ファイル）:
    2R-core_principles.md  GMの基本原則
    2R-judgment.md         判定処理
    2R-description.md      描写指針、装飾仕様
    2R-evaluation.md       評価システム
    2R-scenario.md         シナリオ運用
    2R-chapter_end.md      章末処理
    2R-quest.md            クエスト
    2R-skill.md            スキル
    2R-race_job.md         種族・ジョブ
    2R-character.md        キャラメイク
    2R-equipment.md        装備・所持品
    2R-time.md             時間進行
    2R-npc_autonomy.md     NPC自律行動
    2R-divine.md           神々・精霊との交渉
  
  ロール定義（O、3ファイル）:
    2O-sonnet_runtime.md   SONNETロール（章中現場運用）
    2O-opus_design.md      OPUS設計（章末・シナリオ設計）
    2O-opus_archivist.md   OPUSアーカイバ（周回末処理）
  
  フォーマット（F、6ファイル）:
    2F-scenario_spec.md    シナリオ仕様書様式
    2F-character_sheet.md  キャラクターシート様式
    2F-chapter_end.md      章末処理出力様式
    2F-evaluation_record.md 評価記録様式
    2F-quest_record.md     クエスト記録様式
    2F-cycle_patch.md      周回末更新パッチ様式

MASTERPLAN.md              全体設計方針
```

## 装飾仕様

本ルールブックの運用では、以下の装飾仕様を採用します（本文描写、章末段階1・2、メタ宣言応答、章開始時舞台開示に適用）。

- 視点: 三人称固定
- PCの呼称: 「あなた」
- 場所ラベル: インラインコード（バッククォートで囲む）
- 本文: 無装飾の散文
- セリフ: 引用ブロック
- 判定処理: yamlブロック

シナリオ仕様書、キャラクターシート、章末処理段階3〜5は従来形式（構造化情報主体）を維持します。

## ロール切り替え

```yaml
技術的前提:
  SONNETとOPUSは別モデル（Claude SonnetとClaude Opus）。
  モデル切り替えはプレイヤーがclaude.aiの画面UIで行う。
  LLM側からは自動切り替えできない。

運用フロー:
  1: LLMが切り替えタイミングを察知
  2: LLMが応答末尾で促す
     例: 「画面上部からOpusに切り替えて、次の応答をお願いします」
  3: プレイヤーが画面UIでモデルを切り替える
  4: プレイヤーが何らかのメッセージを送る
  5: 新しいモデルが応答（新しいロールとして動作）
     冒頭で「OPUSとして章末処理を開始します」のように明示
```

## 読み始め方

1: `MASTERPLAN.md` で全体設計方針を確認
2: `1_setting/1T-core_theme.md` で中核思想を確認
3: `2_rulebook/2M-index.md` でプロトコル索引を確認
4: 必要に応じて各ファイルを参照

## 周辺フォルダ（別途管理）

以下のフォルダはルールブックの外で管理されます：

- `3_geography/`: 地理設定
- `4_character_list/`: 重要NPC一覧
- `5_monster_list/`: モンスター一覧
- `6_quest_list/`: ワールド・クエスト一覧

これらは周回末更新パッチ（2F-cycle_patch.md）を通じて随時更新されます。

## 履歴

このルールブックは、LLM運用に最適化された抜本改革版です。旧B群（B1〜B12）から、構造、装飾仕様、ロール切り替え運用などを全面的に見直して構築されました。
