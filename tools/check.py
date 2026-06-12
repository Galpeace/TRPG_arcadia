#!/usr/bin/env python3
"""判定。revision.md §1 の裁定（2d6 ＋ 事情差×2）を執行する。

結果が明白なら振らないこと（自動成否）。振るのは不確実なときだけ。
事情は振る前に数え上げて宣言する。振った後の数え直しは禁止。

使い方:
    python tools/check.py --fav 2 --unfav 1 --label 衛兵をまく
    python tools/check.py --label 反応表 --table   # 修正なしの素の2d6（反応表など）
"""
import argparse

from roll import roll_expr

MOD_CAP = 4


def main():
    ap = argparse.ArgumentParser(description="判定（2d6＋事情差×2）")
    ap.add_argument("--fav", type=int, default=0, help="有利事情の数")
    ap.add_argument("--unfav", type=int, default=0, help="不利事情の数")
    ap.add_argument("--label", default=None, help="判定名")
    ap.add_argument("--table", action="store_true",
                    help="成否を表示しない（反応表・歪み表など出目を表に当てる用途）")
    args = ap.parse_args()

    mod = (args.fav - args.unfav) * 2
    capped = ""
    if abs(mod) > MOD_CAP:
        mod = MOD_CAP if mod > 0 else -MOD_CAP
        capped = "（±4上限。差が大きすぎる場合は自動成否を検討せよ）"

    raw, detail, _ = roll_expr("2d6")
    total = raw + mod
    label = f"[{args.label}] " if args.label else ""
    parts = [detail]
    if args.fav or args.unfav:
        parts.append(f"+ 事情(有利{args.fav}/不利{args.unfav} → {mod:+d}){capped}")

    if args.table:
        print(f"{label}{' '.join(parts)} = {total}")
        return

    if total >= 10:
        verdict = "成功"
    elif total >= 7:
        verdict = "部分成否（成功するが代償・複雑化を伴う）"
    else:
        verdict = "失敗（状況は悪化しうる）"
    print(f"{label}{' '.join(parts)} = {total} … {verdict}")


if __name__ == "__main__":
    main()
