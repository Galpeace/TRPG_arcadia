#!/usr/bin/env python3
"""ダイスロール。OSの乱数源（secrets）を使うため、結果の操作は不可能。

使い方:
    python tools/roll.py 2d6+3
    python tools/roll.py 1d20 1d20        # 複数指定でまとめて振る
    python tools/roll.py 1d100 --label 遭遇判定
"""
import argparse
import re
import secrets
import sys

MAX_DICE = 100
MAX_FACES = 1000


def roll_expr(expr: str):
    """'2d6+3' のような式を振り、(合計, 内訳文字列) を返す。"""
    s = expr.replace(" ", "").lower()
    if not re.fullmatch(r"[+-]?[0-9d]+([+-][0-9d]+)*", s):
        raise ValueError(f"式を解析できない: {expr}")
    tokens = re.findall(r"[+-]?[0-9d]+", s)
    total = 0
    parts = []
    for tok in tokens:
        sign = -1 if tok.startswith("-") else 1
        body = tok.lstrip("+-")
        m = re.fullmatch(r"(\d*)d(\d+)", body)
        if m:
            n = int(m.group(1) or 1)
            faces = int(m.group(2))
            if not (1 <= n <= MAX_DICE):
                raise ValueError(f"ダイス数は1〜{MAX_DICE}: {tok}")
            if not (2 <= faces <= MAX_FACES):
                raise ValueError(f"面数は2〜{MAX_FACES}: {tok}")
            rolls = [secrets.randbelow(faces) + 1 for _ in range(n)]
            total += sign * sum(rolls)
            prefix = "-" if sign < 0 else ("+" if parts else "")
            parts.append(f"{prefix}{n}d{faces}{rolls}")
        elif re.fullmatch(r"\d+", body):
            total += sign * int(body)
            parts.append(f"{'-' if sign < 0 else '+'}{body}")
        else:
            raise ValueError(f"式を解析できない: {tok}")
    return total, " ".join(parts)


def main():
    ap = argparse.ArgumentParser(description="ダイスロール")
    ap.add_argument("exprs", nargs="+", metavar="EXPR", help="例: 2d6+3")
    ap.add_argument("--label", default=None, help="何のロールかの注記")
    args = ap.parse_args()

    for expr in args.exprs:
        try:
            total, detail = roll_expr(expr)
        except ValueError as e:
            print(f"エラー: {e}", file=sys.stderr)
            sys.exit(1)
        label = f"[{args.label}] " if args.label else ""
        print(f"{label}{expr}: {detail} = {total}")


if __name__ == "__main__":
    main()
