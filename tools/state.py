#!/usr/bin/env python3
"""キャラクター・キャンペーン状態の読み書き。数値の増減は必ずここを通す。

使い方:
    python tools/state.py show                      # 全体表示
    python tools/state.py show altea                # 1キャラ表示
    python tools/state.py new altea アルテア --hp 24            # キャラ登録
    python tools/state.py damage altea 7            # ダメージ
    python tools/state.py heal altea 5              # 回復
    python tools/state.py gold altea -200           # 所持金の増減
    python tools/state.py item add altea 松明 2     # アイテム追加
    python tools/state.py item remove altea 松明    # アイテム削除（1個）
    python tools/state.py set altea stats.dex 3     # 任意フィールド設定
    python tools/state.py flag set 廃坑_解放 true   # キャンペーンフラグ
    python tools/state.py flag get 廃坑_解放
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PARTY = ROOT / "state" / "party.json"
CAMPAIGN = ROOT / "state" / "campaign.json"


def load(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def get_char(party: dict, char_id: str) -> dict:
    chars = party.setdefault("characters", {})
    if char_id not in chars:
        sys.exit(f"エラー: キャラ '{char_id}' は未登録。登録済み: {', '.join(chars) or 'なし'}")
    return chars[char_id]


def fmt_char(char_id: str, c: dict) -> str:
    hp = c.get("hp", {})
    items = ", ".join(
        f"{i['name']}x{i['count']}" if i.get("count", 1) != 1 else i["name"]
        for i in c.get("items", [])
    )
    return (
        f"{c.get('name', char_id)} ({char_id}): "
        f"HP {hp.get('current', '?')}/{hp.get('max', '?')}, "
        f"所持金 {c.get('gold', 0)}G, 所持品 [{items or 'なし'}]"
    )


def cmd_show(args, party):
    chars = party.get("characters", {})
    targets = [args.char] if args.char else list(chars)
    if args.char and args.char not in chars:
        sys.exit(f"エラー: キャラ '{args.char}' は未登録")
    if not targets:
        print("キャラ未登録。`state.py new <id> <名前> --hp <最大HP>` で登録する。")
    for cid in targets:
        print(fmt_char(cid, chars[cid]))
    campaign = load(CAMPAIGN)
    if not args.char and campaign:
        print(f"--- キャンペーン: {json.dumps(campaign, ensure_ascii=False)}")


def cmd_new(args, party):
    chars = party.setdefault("characters", {})
    if args.id in chars:
        sys.exit(f"エラー: '{args.id}' は登録済み")
    chars[args.id] = {
        "name": args.name,
        "hp": {"current": args.hp, "max": args.hp},
        "gold": args.gold,
        "items": [],
        "stats": {},
    }
    save(PARTY, party)
    print(f"登録: {fmt_char(args.id, chars[args.id])}")


def cmd_hp(args, party, sign):
    c = get_char(party, args.char)
    hp = c["hp"]
    before = hp["current"]
    hp["current"] = max(0, min(hp["max"], before + sign * args.amount))
    save(PARTY, party)
    word = "ダメージ" if sign < 0 else "回復"
    note = "【戦闘不能】" if hp["current"] == 0 else ""
    print(f"{c['name']}: {word} {args.amount} → HP {before} → {hp['current']} / {hp['max']} {note}")


def cmd_gold(args, party):
    c = get_char(party, args.char)
    before = c.get("gold", 0)
    after = before + args.amount
    if after < 0:
        sys.exit(f"エラー: 所持金不足（現在 {before}G、必要 {-args.amount}G）")
    c["gold"] = after
    save(PARTY, party)
    print(f"{c['name']}: 所持金 {before}G → {after}G（{args.amount:+d}）")


def cmd_item(args, party):
    c = get_char(party, args.char)
    items = c.setdefault("items", [])
    found = next((i for i in items if i["name"] == args.name), None)
    if args.action == "add":
        if found:
            found["count"] = found.get("count", 1) + args.count
        else:
            items.append({"name": args.name, "count": args.count})
        save(PARTY, party)
        print(f"{c['name']}: {args.name} x{args.count} を入手")
    else:  # remove
        if not found or found.get("count", 1) < args.count:
            sys.exit(f"エラー: {args.name} が足りない（所持 {found.get('count', 1) if found else 0}）")
        found["count"] = found.get("count", 1) - args.count
        if found["count"] == 0:
            items.remove(found)
        save(PARTY, party)
        print(f"{c['name']}: {args.name} x{args.count} を消費")
    print(fmt_char(args.char, c))


def cmd_set(args, party):
    c = get_char(party, args.char)
    keys = args.path.split(".")
    node = c
    for k in keys[:-1]:
        node = node.setdefault(k, {})
    try:
        value = json.loads(args.value)
    except json.JSONDecodeError:
        value = args.value
    node[keys[-1]] = value
    save(PARTY, party)
    print(f"{c['name']}: {args.path} = {value}")


def cmd_flag(args):
    campaign = load(CAMPAIGN)
    flags = campaign.setdefault("flags", {})
    if args.action == "set":
        try:
            value = json.loads(args.value)
        except json.JSONDecodeError:
            value = args.value
        flags[args.name] = value
        save(CAMPAIGN, campaign)
        print(f"フラグ設定: {args.name} = {json.dumps(value, ensure_ascii=False)}")
    else:
        print(f"{args.name} = {json.dumps(flags.get(args.name), ensure_ascii=False)}")


def main():
    ap = argparse.ArgumentParser(description="状態管理")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("show", help="状態表示")
    p.add_argument("char", nargs="?")

    p = sub.add_parser("new", help="キャラ登録")
    p.add_argument("id")
    p.add_argument("name")
    p.add_argument("--hp", type=int, required=True)
    p.add_argument("--gold", type=int, default=0)

    for name in ("damage", "heal"):
        p = sub.add_parser(name)
        p.add_argument("char")
        p.add_argument("amount", type=int)

    p = sub.add_parser("gold", help="所持金増減（+500 / -200）")
    p.add_argument("char")
    p.add_argument("amount", type=int)

    p = sub.add_parser("item")
    p.add_argument("action", choices=["add", "remove"])
    p.add_argument("char")
    p.add_argument("name")
    p.add_argument("count", nargs="?", type=int, default=1)

    p = sub.add_parser("set", help="任意フィールド設定")
    p.add_argument("char")
    p.add_argument("path", help="例: stats.dex")
    p.add_argument("value")

    p = sub.add_parser("flag")
    p.add_argument("action", choices=["set", "get"])
    p.add_argument("name")
    p.add_argument("value", nargs="?")

    args = ap.parse_args()
    party = load(PARTY)

    if args.cmd == "show":
        cmd_show(args, party)
    elif args.cmd == "new":
        cmd_new(args, party)
    elif args.cmd == "damage":
        cmd_hp(args, party, -1)
    elif args.cmd == "heal":
        cmd_hp(args, party, +1)
    elif args.cmd == "gold":
        cmd_gold(args, party)
    elif args.cmd == "item":
        cmd_item(args, party)
    elif args.cmd == "set":
        cmd_set(args, party)
    elif args.cmd == "flag":
        cmd_flag(args)


if __name__ == "__main__":
    main()
