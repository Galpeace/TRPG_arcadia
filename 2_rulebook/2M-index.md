# 索引と読み込みプロトコル

## このファイルの位置

ルールブック全体の見取り図。LLMがどのファイルをいつ読むべきかを定める。各ロール（SONNET、OPUS、評価更新OPUS、アーカイバOPUS）の起動時に最初に読むファイル。

## 三秒で読む要約

役割と場面ごとに「読むべきファイル」が決まっている。迷ったらこのファイルを再度開く。

----

# 1. ファイル全体構成

## 1.1 トップレベル構造

プロジェクト全体は6つのフォルダで構成される。

```yaml
構造:
  1. 設定/:
    内容: 世界の物理法則（魔法、歴史、種族、神々、ダンジョン、経済など、世界が「どう在るか」）
    最上位ファイル: 1T-core_theme.md（中核テーマ）

  2. ルールブック/:
    内容: プレイ運用規則（GM・PCが「どう振る舞うか」）
    本ファイル所在: ここ

  3. 国家・地域リスト/:
    内容: 地理データ

  4. キャラクターリスト/:
    内容: NPC一覧。周回プレイで更新される

  5. モンスターリスト/:
    内容: 魔物・魔族の個体・種族データ

  6. クエストリスト/:
    内容: ワールド・クエストの保管場所
```

## 1.2 ルールブック内のプレフィックス

ルールブック内のファイルは以下のプレフィックスを持つ。

| プレフィックス | 用途 |
|---|---|
| `2T-` | テーマ運用ルール |
| `2R-` | ルール本体 |
| `2O-` | ロール定義（起動プロンプト） |
| `2F-` | フォーマット（テンプレート） |
| `2M-` | メタ（用語集、索引、アンチパターン、応答プロトコル） |
| `2S-` | 状態ファイルテンプレート |

設定フォルダ内も同様にプレフィックスを使う。

| プレフィックス | 用途 |
|---|---|
| `1T-` | 中核テーマ |
| `1W-` | 世界設定本体 |

----

# 2. ロール別の読み込みプロトコル

各ロールは起動時に以下のファイル群を読み込む。

## 2.1 SONNET（章中の現場運用）

最頻使用ロール。各シーンの描写・判定・NPC運用を担当する。

```yaml
SONNET起動時に必ず読むファイル:
  最上位:
    - 1_setting/1T-core_theme.md       # 中核テーマ
  メタ:
    - 2_rulebook/2M-glossary.md         # 用語集
    - 2_rulebook/2M-index.md            # 本ファイル
    - 2_rulebook/2M-response_protocol.md # 応答前チェックリスト
    - 2_rulebook/2M-antipatterns.md     # 違反兆候
  ルール本体:
    - 2_rulebook/2R-core_principles.md  # GMの基本原則
    - 2_rulebook/2R-judgment.md         # 判定システム
    - 2_rulebook/2R-description.md      # 描写指針
    - 2_rulebook/2R-evaluation.md       # メタ評価（描写時参照）
    - 2_rulebook/2R-irreversible.md     # 不可逆行動
  ロール定義:
    - 2_rulebook/2O-sonnet_runtime.md   # 自分自身のロール定義
  状態ファイル（実プレイで生成済みなら）:
    - 該当する S- ファイル群
  シナリオ仕様書:
    - 当該章のシナリオ仕様書
```

SONNETが必要に応じて参照するファイル（常時読み込みは不要）：

- `2R-skill.md`：スキル判定が発生した時
- `2R-race_job.md`：種族・ジョブが論点になった時
- `2R-equipment.md`：装備・所持品が論点になった時
- `2R-time.md`：時間進行が論点になった時
- `2R-npc_autonomy.md`：NPC自律行動の描写時
- `2R-divine.md`：神々・精霊が論点になった時
- `1_setting/` 配下：世界設定の詳細が必要な時
- `3_geography/` 配下：地理の詳細が必要な時
- `4_character_list/` 配下：NPCの詳細が必要な時

## 2.2 OPUS（設計・章末監督）

シナリオ設計、章末処理、設計判断を担当する。

```yaml
OPUS起動時に必ず読むファイル:
  最上位:
    - 1_setting/1T-core_theme.md
  メタ:
    - 2_rulebook/2M-glossary.md
    - 2_rulebook/2M-index.md
    - 2_rulebook/2M-antipatterns.md
  ルール本体:
    - 2_rulebook/2R-core_principles.md
    - 2_rulebook/2R-scenario.md          # シナリオ運用
    - 2_rulebook/2R-chapter_end.md       # 章末処理
    - 2_rulebook/2R-quest.md             # クエスト体系
    - 2_rulebook/2R-skill.md             # 成長判断
    - 2_rulebook/2R-race_job.md          # 進化判断
  ロール定義:
    - 2_rulebook/2O-opus_design.md
  フォーマット:
    - 2_rulebook/2F-scenario_spec.md     # シナリオ仕様書テンプレート
    - 2_rulebook/2F-chapter_end.md       # 章末処理出力テンプレート
  状態ファイル:
    - 該当する S- ファイル群
```

## 2.3 評価更新OPUS

評価システムの更新専門。詳細仕様は確認事項5.5の回答待ち。

```yaml
評価更新OPUS起動時に必ず読むファイル:
  最上位:
    - 1_setting/1T-core_theme.md
  メタ:
    - 2_rulebook/2M-glossary.md
  ルール本体:
    - 2_rulebook/2R-evaluation.md
  ロール定義:
    - 2_rulebook/2O-opus_evaluator.md
  フォーマット:
    - 2_rulebook/2F-evaluation_record.md
  状態ファイル:
    - 2_rulebook/2S-evaluation_state.md（実プレイで生成済みのもの）
```

## 2.4 アーカイバOPUS（周回末）

周回末に世界状態を更新する専門ロール。詳細仕様は確認事項5.6の回答待ち。

```yaml
アーカイバOPUS起動時に必ず読むファイル:
  最上位:
    - 1_setting/1T-core_theme.md
  メタ:
    - 2_rulebook/2M-glossary.md
  ルール本体:
    - 2_rulebook/2R-quest.md             # 自律的進行のため
  ロール定義:
    - 2_rulebook/2O-opus_archivist.md
  フォーマット:
    - 2_rulebook/2F-cycle_patch.md
  対象ファイル（更新対象）:
    - 4_character_list/ 配下
    - 6_quest_list/ 配下
    - 1_setting/1W-* 配下（解像度更新分）
```

----

# 3. 場面別の参照プロトコル

特定場面で必ず参照すべきファイルを場面別に定める。

## 3.1 セッション開始時

```yaml
順序:
  1: 1T-core_theme.md を確認
  2: 2M-response_protocol.md を確認
  3: 既存の S- 状態ファイルを確認
  4: シナリオ仕様書を確認
  5: 開始する
```

## 3.2 判定が必要になった時

```yaml
順序:
  1: 2R-judgment.md を確認
  2: 該当スキルが論点なら 2R-skill.md を確認
  3: 動機・禁忌が文脈にあるか確認（PCの設定）
  4: 判断の透明化フォーマットで結果を提示
```

## 3.3 NPCの行動を描写する時

```yaml
順序:
  1: 該当NPCが 4_character_list/ にあるか確認
  2: あれば設定を参照
  3: 2R-npc_autonomy.md を確認（自律的行動の場合）
  4: PCの観測範囲かを 2R-description.md で確認（プレイヤーとPCの分離）
```

## 3.4 評価が更新される時

```yaml
順序:
  1: 2R-evaluation.md の四層分類を確認
  2: 章末描写での扱いか、章中の即時描写かを判断
  3: 章末の場合は章末処理段階2で描写、周回末で記録の本格化
```

## 3.5 章末を迎えた時

```yaml
順序:
  1: 2R-chapter_end.md でトリガー条件を確認
  2: SONNETが応答末尾で「画面上部からOpusに切り替えて、次の応答をお願いします」と促す
  3: プレイヤーが画面UIでOpusに切り替えて返信
  4: OPUSが章中文脈を確認した上で章末処理（五段階）を実行
  5: 必要に応じて 2F-chapter_end.md フォーマットで追加出力
  6: 周回末への移行が必要な場合のみアーカイバOPUSを起動
```

## 3.6 周回が終わる時

```yaml
順序:
  1: 2O-opus_archivist.md を起動
  2: 当該周回でのPCの活躍をプレイヤーが世界に反映させたいか確認
  3: 望めば 4_character_list/ にPC情報を追加
  4: 望めば 1W-* 等の解像度更新
  5: 望まなければ世界状態をリセット
```

----

# 4. ファイル間の依存関係

ファイル間の参照は一方向であるべきだが、いくつかは双方向になる。以下に依存関係を明示する。

## 4.1 一方向の依存

```yaml
1T-core_theme.md:
  上位: なし（最上位）
  下位: ほぼすべてのファイル

2M-glossary.md:
  上位: なし（参照専用）
  下位: すべてのファイル（用語使用時に参照される）

2R-core_principles.md:
  上位: 1T-core_theme.md
  下位: ほぼすべての 2R-* ファイル
```

## 4.2 双方向の関係

```yaml
2R-evaluation.md ↔ 2R-quest.md:
  理由: クエストへの関与が評価四層に影響し、評価がクエスト関連の選択肢に影響する

2R-skill.md ↔ 2R-race_job.md:
  理由: Sランク到達が種族・ジョブ進化の条件、進化がユニークスキルに影響
```

## 4.3 ロールファイルの位置

ロール定義（2O-*）は本ファイル（2M-index.md）と並んで、各ロールの起動時の最初の参照点となる。ロール定義は他のすべてのファイルを参照しうるが、他のファイルがロール定義を参照することはない。

----

# 5. 全ファイル一覧（フェーズ別実装状況）

## 5.1 フェーズ1：基盤整備

| ファイル | 状態 |
|---|---|
| `1_setting/1T-core_theme.md` | 作成済み |
| `2_rulebook/2M-glossary.md` | 作成済み |
| `2_rulebook/2M-index.md` | 作成済み（本ファイル） |
| `2_rulebook/2M-antipatterns.md` | 未作成 |
| `2_rulebook/2M-response_protocol.md` | 未作成 |

## 5.2 フェーズ2：ルール本体

旧B1〜B12をリライトして以下に再編する。

| ファイル | 旧B番号 | 状態 |
|---|---|---|
| `2R-core_principles.md` | B1 | 未作成 |
| `2R-judgment.md` | B2 | 未作成 |
| `2R-description.md` | B3 | 未作成 |
| `2R-evaluation.md` | B4 | 未作成 |
| `2R-irreversible.md` | B5 | 未作成 |
| `2R-scenario.md` | B6 | 未作成 |
| `2R-chapter_end.md` | B7 | 未作成 |
| `2R-quest.md` | B8 | 未作成 |
| `2R-character.md` | B9 | 未作成 |
| `2R-skill.md` | B10 | 未作成 |
| `2R-race_job.md` | B11 | 未作成 |
| `2R-equipment.md` | B12 | 未作成 |

新規追加（改革案14、15、16、18由来）：

| ファイル | 由来 | 状態 |
|---|---|---|
| `2R-divine.md` | 神々・精霊との交渉ルール | 未作成 |
| `2R-time.md` | 時間進行ルール | 未作成 |
| `2R-npc_autonomy.md` | NPC自律行動シミュレーション | 未作成 |

## 5.3 フェーズ3：ロールとフォーマット

| ファイル | 用途 | 状態 |
|---|---|---|
| `2O-sonnet_runtime.md` | 現場運用ロール | 未作成 |
| `2O-opus_design.md` | 設計ロール | 未作成 |
| `2O-opus_evaluator.md` | 評価更新ロール | 未作成（仕様確認待ち） |
| `2O-opus_archivist.md` | アーカイバロール | 未作成（仕様確認待ち） |
| `2F-character_sheet.md` | キャラシート様式 | 未作成 |
| `2F-scenario_spec.md` | シナリオ仕様書様式 | 未作成 |
| `2F-evaluation_record.md` | 評価記録様式 | 未作成 |
| `2F-quest_record.md` | クエスト記録様式 | 未作成 |
| `2F-chapter_end.md` | 章末処理出力様式 | 未作成 |
| `2F-cycle_patch.md` | 周回末更新パッチ様式 | 未作成 |

## 5.4 フェーズ4：世界設定の再編

| ファイル | 由来 | 状態 |
|---|---|---|
| `1_setting/1W-magic.md` | 旧A1から分離 | 未作成 |
| `1_setting/1W-history.md` | 旧A1から分離 | 未作成 |
| `1_setting/1W-races.md` | 旧A1から分離 | 未作成 |
| `1_setting/1W-gods_spirits.md` | 旧A1から分離・拡張 | 未作成 |
| `1_setting/1W-dungeons.md` | 改革案15・新規 | 未作成 |
| `1_setting/1W-economy.md` | 改革案17・新規 | 未作成 |

## 5.5 フェーズ5：状態ファイルテンプレート

| ファイル | 用途 | 状態 |
|---|---|---|
| `2S-character.md.template` | PC現状 | 未作成 |
| `2S-world.md.template` | 世界現状 | 未作成 |
| `2S-quests.md.template` | クエスト進行 | 未作成 |
| `2S-cycle.md.template` | 周回間引き継ぎ | 未作成（仕様確認待ち） |
| `2S-evaluation_state.md.template` | 評価状態 | 未作成 |

----

# 6. このファイルの保守

本ファイルは新規ファイルの追加・統廃合のたびに更新する。とくに以下のタイミングで更新する。

- 新規ファイル作成時：5節の一覧と該当ロールの「読むファイル」に追記
- ファイル統廃合時：5節と読み込みプロトコルの双方を更新
- 新ロール追加時：2節と5節に新規追加
