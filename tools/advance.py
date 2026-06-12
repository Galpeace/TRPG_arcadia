#!/usr/bin/env python3
"""早送り（P2）。revision.md §2.2 の手順 1〜2 を機械実行する。

    python tools/advance.py 7        # 7日進める
    python tools/advance.py 0        # 日数を進めず、期限の来た進行判定だけ処理

実行内容:
  1. 世界時計を進める
  2. 期限が来たタイムラインの進行判定（2d6＋事情: 10+で2段階 / 7-9で1段階 / 6-停滞）
  3. 噂の伝播更新と、新たに到達した経由地ごとの歪み判定
手順3（道中イベント表）と4（資源消費）はGMが別途宣言して行う。
出力はGMが物語に翻訳する。台帳の数字をそのまま地の文に書かないこと。
"""
import json
import sys
from pathlib import Path

from roll import roll_expr

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "state"
CAMPAIGN = STATE / "campaign.json"
TIMELINES = STATE / "timelines.json"
RUMORS = STATE / "rumors.json"

DISTORT_NORMAL = [(3, "主体の入替（別人の仕業に）"), (5, "動機の誤解"), (8, "誇張"),
                  (10, "ほぼ正確"), (12, "正確・細部まで鮮明")]
DISTORT_MONSTER = [(3, "主体の入替（別の怪異の仕業に）"), (5, "動機・習性の誤解"), (9, "脅威の誇張"),
                   (11, "ほぼ正確"), (12, "正確・細部まで鮮明")]


def load(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def lookup(table, total):
    for ceiling, label in table:
        if total <= ceiling:
            return label
    return table[-1][1]


def main():
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        sys.exit("使い方: python tools/advance.py <日数>")
    days = int(sys.argv[1])

    campaign = load(CAMPAIGN, {"day": 0, "flags": {}})
    day_from = campaign.get("day", 0)
    day_to = day_from + days
    campaign["day"] = day_to
    save(CAMPAIGN, campaign)
    print(f"=== 早送り: Day {day_from} → Day {day_to} ===")

    # 2. タイムライン進行判定
    tdata = load(TIMELINES, {"timelines": []})
    for t in tdata["timelines"]:
        if t["status"] != "active":
            continue
        while t["next_check"] <= day_to and t["status"] == "active":
            check_day = t["next_check"]
            raw, detail, _ = roll_expr("2d6")
            mod = t.get("mod", 0)
            total = raw + mod
            mod_str = f" + 事情({mod:+d})" if mod else ""
            if total >= 10:
                step, verdict = 2, "加速（2段階進行）"
            elif total >= 7:
                step, verdict = 1, "進行（1段階）"
            else:
                step, verdict = 0, "停滞・横道"
            before = t["phases"][t["phase"]] if t["phase"] < len(t["phases"]) else "完了"
            t["phase"] = min(t["phase"] + step, len(t["phases"]))
            after = t["phases"][t["phase"]] if t["phase"] < len(t["phases"]) else "完了"
            if t["phase"] >= len(t["phases"]) - 0 and after == "完了":
                t["status"] = "done"
            print(f"[{t['id']}] {t['name']} Day{check_day} 進行判定: "
                  f"{detail}{mod_str} = {total} … {verdict}"
                  + (f" 「{before}」→「{after}」" if step else f" （「{before}」のまま）"))
            t["next_check"] = check_day + t["pace"]
    save(TIMELINES, tdata)

    # 3. 噂の伝播と歪み
    rdata = load(RUMORS, {"rumors": [], "reputation": {}})
    for r in rdata["rumors"]:
        traveled = (day_to - r["day_started"]) * r["speed_kmd"]
        table = DISTORT_MONSTER if r.get("monster") else DISTORT_NORMAL
        for w in r["route"]:
            if w["reached_day"] is None and w["km"] <= traveled:
                w["reached_day"] = r["day_started"] + -(-w["km"] // r["speed_kmd"])  # 切り上げ
                raw, detail, _ = roll_expr("2d6")
                w["distortion"] = lookup(table, raw)
                print(f"[{r['id']}] 噂「{r['summary']}」が {w['place']} に到達"
                      f"（Day{w['reached_day']}）: 歪み判定 {detail} = {raw} … {w['distortion']}")
    save(RUMORS, rdata)

    print("=== 早送り終了。道中イベント表と資源消費はGMが宣言して処理すること ===")


if __name__ == "__main__":
    main()
