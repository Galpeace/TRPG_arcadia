#!/usr/bin/env python3
"""技能判定。rules/system.md §1 のコア判定（2d6 + 修正 vs 難易度）を裁定する。

- 6ゾロ =〈脚光〉: 自動成功。注視点 1 を得る（state.py attention で加算すること）
- 1ゾロ =〈暗転〉: 自動失敗。物語が悪い方へ転がる

使い方:
    python tools/check.py --dc 9 --mod 3 --label 隠密
    python tools/check.py --dc 11 --mod 2 --dice 2d6   # ダイス明示も可
"""
import argparse

from roll import roll_expr


def main():
    ap = argparse.ArgumentParser(description="技能判定")
    ap.add_argument("--dice", default="2d6", help="判定ダイス（既定: 2d6）")
    ap.add_argument("--mod", type=int, default=0, help="修正値（能力＋技能タグ＋注視点ボーナス）")
    ap.add_argument("--dc", type=int, required=True, help="難易度（易7/並9/難11/無謀13）")
    ap.add_argument("--label", default=None, help="判定名（隠密・説得など）")
    args = ap.parse_args()

    raw, detail, rolls = roll_expr(args.dice)
    total = raw + args.mod
    mod_str = f" {'+' if args.mod >= 0 else '-'} 修正({abs(args.mod)})" if args.mod else ""
    label = f"[{args.label}] " if args.label else ""

    crit = len(rolls) == 2 and all(r == 6 for r in rolls)
    fumble = len(rolls) == 2 and all(r == 1 for r in rolls)
    if crit:
        verdict = "〈脚光〉自動成功！ 注視点+1"
    elif fumble:
        verdict = "〈暗転〉自動失敗…"
    else:
        margin = total - args.dc
        verdict = f"{'成功' if total >= args.dc else '失敗'}（差分 {margin:+d}）"

    print(f"{label}{detail}{mod_str} = {total} vs DC{args.dc} … {verdict}")


if __name__ == "__main__":
    main()
