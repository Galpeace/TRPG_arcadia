#!/usr/bin/env python3
"""キャラクター・キャンペーン状態の読み書き。数値・状態の変更は必ずここを通す。

Witnessed にHPは無い。負傷は段階（無傷/軽傷/中傷/重傷/瀕死/死亡）で管理する。
state/ 配下はすべて UD であり、周回終了時に初期化される。

使い方:
    python tools/state.py show                       # 全体表示
    python tools/state.py new pc1 ヴェイル --gold 5000
    python tools/state.py wound pc1 中傷             # 負傷段階の設定
    python tools/state.py cond add pc1 毒            # 状態異常
    python tools/state.py cond remove pc1 毒
    python tools/state.py gold pc1 -200
    python tools/state.py item add pc1 松明 2
    python tools/state.py item remove pc1 松明
    python tools/state.py set pc1 識別名.路地の影 '{"悪名": 2}'   # 任意フィールド
    python tools/state.py flag set 橋_焼失 true     # キャンペーンフラグ
    python tools/state.py flag get 橋_焼失
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PARTY = ROOT / "state" / "party.json"
CAMPAIGN = ROOT / "state" / "campaign.json"

WOUND_LEVELS = ["無傷", "軽傷", "中傷", "重傷", "瀕死", "死亡"]
WOUND_PENALTY = {"無傷": 0, "軽傷": 0, "中傷": 1, "重傷": 2}


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


def wound_note(wound: str) -> str:
    if wound == "瀕死":
        return "（行動原則不可。未処置で場面が進むごとに維持判定 2d6 公開ロール、6以下で死亡）"
    if wound == "死亡":
        return "（死は正規の結末である）"
    p = WOUND_PENALTY.get(wound, 0)
    return f"（判定の不利{p}）" if p else ""


def fmt_char(char_id: str, c: dict) -> str:
    items = ", ".join(
        f"{i['name']}x{i['count']}" if i.get("count", 1) != 1 else i["name"]
        for i in c.get("items", [])
    )
    conds = "・".join(c.get("conditions", []))
    return (
        f"{c.get('name', char_id)} ({char_id}): "
        f"負傷[{c.get('wound', '無傷')}]{wound_note(c.get('wound', '無傷'))}, "
        f"状態[{conds or 'なし'}], "
        f"所持金 {c.get('gold', 0)}G, 所持品 [{items or 'なし'}]"
    )


def cmd_show(args, party):
    chars = party.get("characters", {})
    targets = [args.char] if args.char else list(chars)
    if args.char and args.char not in chars:
        sys.exit(f"エラー: キャラ '{args.char}' は未登録")
    if not targets:
        print("キャラ未登録。`state.py new <id> <名前> [--gold N]` で登録する。")
    for cid in targets:
        print(fmt_char(cid, chars[cid]))
        extra = {k: v for k, v in chars[cid].items()
                 if k not in ("name", "wound", "conditions", "gold", "items")}
        if extra and args.char:
            print(f"  その他: {json.dumps(extra, ensure_ascii=False)}")
    campaign = load(CAMPAIGN)
    if not args.char and campaign:
        print(f"--- キャンペーン: {json.dumps(campaign, ensure_ascii=False)}")


def cmd_new(args, party):
    chars = party.setdefault("characters", {})
    if args.id in chars:
        sys.exit(f"エラー: '{args.id}' は登録済み")
    chars[args.id] = {
        "name": args.name,
        "wound": "無傷",
        "conditions": [],
        "gold": args.gold,
        "items": [],
    }
    save(PARTY, party)
    print(f"登録: {fmt_char(args.id, chars[args.id])}")


def cmd_wound(args, party):
    c = get_char(party, args.char)
    if args.level not in WOUND_LEVELS:
        sys.exit(f"エラー: 負傷段階は {'/'.join(WOUND_LEVELS)} のいずれか")
    before = c.get("wound", "無傷")
    if before == "死亡":
        sys.exit("エラー: 死亡は回復不可（rulebook.md）。負傷段階の変更はできない")
    c["wound"] = args.level
    save(PARTY, party)
    print(f"{c['name']}: 負傷 {before} → {args.level} {wound_note(args.level)}")


def cmd_cond(args, party):
    c = get_char(party, args.char)
    conds = c.setdefault("conditions", [])
    if args.action == "add":
        if args.name in conds:
            sys.exit(f"エラー: 状態 '{args.name}' は付与済み")
        conds.append(args.name)
        verb = "付与"
    else:
        if args.name not in conds:
            sys.exit(f"エラー: 状態 '{args.name}' は付いていない")
        conds.remove(args.name)
        verb = "解除"
    save(PARTY, party)
    print(f"{c['name']}: 状態異常 '{args.name}' を{verb} → [{('・'.join(conds)) or 'なし'}]")


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
    print(f"{c['name']}: {args.path} = {json.dumps(value, ensure_ascii=False)}")


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
    p.add_argument("--gold", type=int, default=0)

    p = sub.add_parser("wound", help="負傷段階の設定")
    p.add_argument("char")
    p.add_argument("level", help="/".join(WOUND_LEVELS))

    p = sub.add_parser("cond", help="状態異常の付与/解除")
    p.add_argument("action", choices=["add", "remove"])
    p.add_argument("char")
    p.add_argument("name")

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
    p.add_argument("path", help="例: 識別名.路地の影")
    p.add_argument("value")

    p = sub.add_parser("flag")
    p.add_argument("action", choices=["set", "get"])
    p.add_argument("name")
    p.add_argument("value", nargs="?")

    args = ap.parse_args()
    party = load(PARTY)

    dispatch = {
        "show": cmd_show, "new": cmd_new, "wound": cmd_wound, "cond": cmd_cond,
        "gold": cmd_gold, "item": cmd_item, "set": cmd_set,
    }
    if args.cmd == "flag":
        cmd_flag(args)
    else:
        dispatch[args.cmd](args, party)


if __name__ == "__main__":
    main()
