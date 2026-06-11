#!/usr/bin/env python3
"""判定。rules/system.md §2 のコア判定（2d6 + 真髄修正 vs 相対難易度）を裁定する。

- 6ゾロ =〈万雷〉: 自動成功。喝采 1 を得る（state.py applause で加算すること）
- 1ゾロ =〈野次〉: 自動失敗。だが喝采 1 を得る——神々は転落も愛でる

使い方:
    python tools/check.py --dc 9 --mod 2 --label 猫の傍を抜ける
"""
import argparse

from roll import roll_expr


def main():
    ap = argparse.ArgumentParser(description="判定")
    ap.add_argument("--dice", default="2d6", help="判定ダイス（既定: 2d6）")
    ap.add_argument("--mod", type=int, default=0, help="修正値（該当する真髄1つにつき+1、最大+3）")
    ap.add_argument("--dc", type=int, required=True,
                    help="難易度（少し難しい7/難しい9/至難11/無謀13——その存在にとって）")
    ap.add_argument("--label", default=None, help="判定名")
    args = ap.parse_args()

    raw, detail, rolls = roll_expr(args.dice)
    total = raw + args.mod
    mod_str = f" {'+' if args.mod >= 0 else '-'} 修正({abs(args.mod)})" if args.mod else ""
    label = f"[{args.label}] " if args.label else ""

    crit = len(rolls) == 2 and all(r == 6 for r in rolls)
    fumble = len(rolls) == 2 and all(r == 1 for r in rolls)
    if crit:
        verdict = "〈万雷〉自動成功！ 桟敷が沸く——喝采+1"
    elif fumble:
        verdict = "〈野次〉自動失敗… だが喝采+1（神々は転落も愛でる）"
    else:
        margin = total - args.dc
        verdict = f"{'成功' if total >= args.dc else '失敗'}（差分 {margin:+d}）"

    print(f"{label}{detail}{mod_str} = {total} vs DC{args.dc} … {verdict}")


if __name__ == "__main__":
    main()
