#!/usr/bin/env python3
"""技能判定・対抗判定。成否の裁定まで機械的に行う。

※ 仮実装。判定方式（基本ダイス・成功基準）はゲームシステム設計の確定後に
   rules/system.md に合わせて調整する。それまではダイスと修正値を明示指定する。

使い方:
    python tools/check.py --dc 12 --mod 3 --label 隠密
    python tools/check.py --dice 2d6 --dc 9 --mod -1
"""
import argparse

from roll import roll_expr


def main():
    ap = argparse.ArgumentParser(description="技能判定")
    ap.add_argument("--dice", default="1d20", help="判定ダイス（既定: 1d20、システム確定後に変更）")
    ap.add_argument("--mod", type=int, default=0, help="修正値")
    ap.add_argument("--dc", type=int, required=True, help="目標値")
    ap.add_argument("--label", default=None, help="判定名（隠密・説得など）")
    args = ap.parse_args()

    raw, detail = roll_expr(args.dice)
    total = raw + args.mod
    mod_str = f" {'+' if args.mod >= 0 else '-'} 修正({abs(args.mod)})" if args.mod else ""
    verdict = "成功" if total >= args.dc else "失敗"
    margin = total - args.dc
    label = f"[{args.label}] " if args.label else ""
    print(f"{label}{detail}{mod_str} = {total} vs DC{args.dc} … {verdict}（差分 {margin:+d}）")


if __name__ == "__main__":
    main()
