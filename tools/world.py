#!/usr/bin/env python3
"""世界台帳の管理（P2）。タイムライン・噂・目撃者・地域評判を記帳する。

シミュレーションはしない。記帳だけする。解釈と語りはGMの仕事である。
state/ 配下はすべて UD（周回終了で初期化）。

使い方:
    python tools/world.py day
    python tools/world.py timeline add wq01 王冠の暗夜 --phases "緊張,実行準備,暗殺決行,継承戦争" --pace 7
    python tools/world.py timeline set wq01 --phase 1 --mod -1   # PC介入を事情として記録
    python tools/world.py timeline list
    python tools/world.py rumor add r1 --about 路地の影 --summary "衛兵殺し" --from ミレル村 \
        --speed fast --route "カラム町:30,街道宿場:80,王都:210" [--monster]
    python tools/world.py rumor list
    python tools/world.py witness add w1 宿屋の親父 --saw "PCが死体を運ぶのを見た" --place ミレル村
    python tools/world.py witness kill w1
    python tools/world.py rep 王都 路地の影 --fame 0 --infamy 2
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "state"
CAMPAIGN = STATE / "campaign.json"
TIMELINES = STATE / "timelines.json"
RUMORS = STATE / "rumors.json"
WITNESSES = STATE / "witnesses.json"

SPEED = {"slow": 20, "normal": 40, "fast": 100}  # km/日（口伝/行商・旅人/早馬・伝書）


def load(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def current_day() -> int:
    return load(CAMPAIGN, {}).get("day", 0)


def find(items, item_id, kind):
    for it in items:
        if it["id"] == item_id:
            return it
    sys.exit(f"エラー: {kind} '{item_id}' は未登録")


def fmt_timeline(t) -> str:
    phases = t["phases"]
    cur = phases[t["phase"]] if t["phase"] < len(phases) else "完了"
    flow = " → ".join(
        f"【{p}】" if i == t["phase"] else p for i, p in enumerate(phases)
    )
    mod = f", 事情{t['mod']:+d}" if t.get("mod") else ""
    return (f"[{t['id']}] {t['name']} ({t['scale']}, {t['status']}): {flow}\n"
            f"    現在「{cur}」, 次の進行判定 Day {t['next_check']}, 間隔 {t['pace']}日{mod}"
            + (f"\n    備考: {t['notes']}" if t.get("notes") else ""))


def fmt_rumor(r) -> str:
    done = [w for w in r["route"] if w.get("reached_day") is not None]
    rest = [w for w in r["route"] if w.get("reached_day") is None]
    arrived = " / ".join(f"{w['place']}(Day{w['reached_day']}着: {w['distortion']})" for w in done)
    pending = " / ".join(f"{w['place']}({w['km']}km)" for w in rest)
    tag = "・モンスター歪み表" if r.get("monster") else ""
    return (f"[{r['id']}] 「{r['summary']}」 身元: {r['about']}, 発生: {r['origin']} Day{r['day_started']}, "
            f"速度 {r['speed_kmd']}km/日{tag}\n"
            f"    既達: {arrived or 'なし'}\n    未達: {pending or 'なし'}")


def cmd_timeline(args):
    data = load(TIMELINES, {"timelines": []})
    tls = data["timelines"]
    if args.action == "add":
        if any(t["id"] == args.id for t in tls):
            sys.exit(f"エラー: '{args.id}' は登録済み")
        t = {"id": args.id, "name": args.name, "scale": args.scale,
             "phases": [p.strip() for p in args.phases.split(",")],
             "phase": args.phase, "pace": args.pace,
             "next_check": current_day() + args.pace,
             "mod": 0, "status": "active", "notes": args.notes or ""}
        tls.append(t)
        save(TIMELINES, data)
        print("登録:\n" + fmt_timeline(t))
    elif args.action == "set":
        t = find(tls, args.id, "タイムライン")
        for key in ("phase", "mod", "pace", "status", "notes"):
            v = getattr(args, key)
            if v is not None:
                t[key] = v
        save(TIMELINES, data)
        print("更新:\n" + fmt_timeline(t))
    else:  # list
        if not tls:
            print("タイムライン未登録")
        for t in tls:
            print(fmt_timeline(t))


def cmd_rumor(args):
    data = load(RUMORS, {"rumors": [], "reputation": {}})
    rs = data["rumors"]
    if args.action == "add":
        if any(r["id"] == args.id for r in rs):
            sys.exit(f"エラー: '{args.id}' は登録済み")
        route = []
        for part in args.route.split(","):
            place, km = part.rsplit(":", 1)
            route.append({"place": place.strip(), "km": int(km),
                          "reached_day": None, "distortion": None})
        route.sort(key=lambda w: w["km"])
        r = {"id": args.id, "about": args.about, "summary": args.summary,
             "origin": getattr(args, "from"), "day_started": current_day(),
             "speed_kmd": SPEED[args.speed], "monster": args.monster, "route": route}
        rs.append(r)
        save(RUMORS, data)
        print("記帳:\n" + fmt_rumor(r))
    else:  # list
        if not rs:
            print("噂未登録")
        for r in rs:
            print(fmt_rumor(r))


def cmd_witness(args):
    data = load(WITNESSES, {"witnesses": []})
    ws = data["witnesses"]
    if args.action == "add":
        if any(w["id"] == args.id for w in ws):
            sys.exit(f"エラー: '{args.id}' は登録済み")
        w = {"id": args.id, "name": args.name, "saw": args.saw, "place": args.place,
             "day": current_day(), "identity": args.identity or "不明", "alive": True}
        ws.append(w)
        save(WITNESSES, data)
        print(f"記帳: [{w['id']}] {w['name']} @ {w['place']} Day{w['day']} — "
              f"目撃「{w['saw']}」（観測された身元: {w['identity']}）")
    elif args.action == "kill":
        w = find(ws, args.id, "目撃者")
        w["alive"] = False
        save(WITNESSES, data)
        print(f"[{w['id']}] {w['name']} は死亡。この者から未伝播の観測は失われる。"
              f"既に伝播した噂は死なない（revision.md §3.4。何が未伝播かはGMが裁定）")
    else:  # list
        if not ws:
            print("目撃者未登録")
        for w in ws:
            mark = "" if w["alive"] else "【死亡】"
            print(f"[{w['id']}] {w['name']}{mark} @ {w['place']} Day{w['day']} — "
                  f"「{w['saw']}」（身元: {w['identity']}）")


def cmd_rep(args):
    data = load(RUMORS, {"rumors": [], "reputation": {}})
    rep = data["reputation"].setdefault(args.place, {}).setdefault(
        args.identity, {"知名度": 0, "悪名": 0})
    if args.fame is not None:
        rep["知名度"] = max(-3, min(3, rep["知名度"] + args.fame))
    if args.infamy is not None:
        rep["悪名"] = max(-3, min(3, rep["悪名"] + args.infamy))
    save(RUMORS, data)
    print(f"{args.place} における「{args.identity}」: 知名度 {rep['知名度']:+d}, 悪名 {rep['悪名']:+d}"
          f"（反応表修正に使用。revision.md §3.3）")


def main():
    ap = argparse.ArgumentParser(description="世界台帳")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("day", help="現在日を表示")

    p = sub.add_parser("timeline")
    p.add_argument("action", choices=["add", "set", "list"])
    p.add_argument("id", nargs="?")
    p.add_argument("name", nargs="?")
    p.add_argument("--phases", help="カンマ区切り")
    p.add_argument("--pace", type=int, default=7, help="進行判定の間隔（日）")
    p.add_argument("--scale", choices=["world", "region", "quest"], default="region")
    p.add_argument("--phase", type=int, default=None)
    p.add_argument("--mod", type=int, default=None, help="進行判定への事情修正（PC介入等）")
    p.add_argument("--status", choices=["active", "halted", "done"], default=None)
    p.add_argument("--notes", default=None)

    p = sub.add_parser("rumor")
    p.add_argument("action", choices=["add", "list"])
    p.add_argument("id", nargs="?")
    p.add_argument("--about", help="観測された身元")
    p.add_argument("--summary", help="噂の内容（発生時点）")
    p.add_argument("--from", dest="from", help="発生地")
    p.add_argument("--speed", choices=list(SPEED), default="normal")
    p.add_argument("--route", help="経由地:累積km をカンマ区切り（例 カラム町:30,王都:210）")
    p.add_argument("--monster", action="store_true", help="脅威誇張の歪み表を使う（§6.2）")

    p = sub.add_parser("witness")
    p.add_argument("action", choices=["add", "kill", "list"])
    p.add_argument("id", nargs="?")
    p.add_argument("name", nargs="?")
    p.add_argument("--saw", help="目撃内容")
    p.add_argument("--place", help="場所")
    p.add_argument("--identity", help="観測された身元（§3.7）")

    p = sub.add_parser("rep", help="地域別の知名度/悪名（−3〜＋3）")
    p.add_argument("place")
    p.add_argument("identity")
    p.add_argument("--fame", type=int, default=None)
    p.add_argument("--infamy", type=int, default=None)

    args = ap.parse_args()
    if args.cmd == "day":
        print(f"現在 Day {current_day()}")
    elif args.cmd == "timeline":
        if args.action == "add" and not (args.id and args.name and args.phases):
            sys.exit("エラー: add には id・name・--phases が必要")
        if args.action == "add" and args.phase is None:
            args.phase = 0
        cmd_timeline(args)
    elif args.cmd == "rumor":
        if args.action == "add" and not (args.id and args.about and args.summary
                                         and getattr(args, "from") and args.route):
            sys.exit("エラー: add には id・--about・--summary・--from・--route が必要")
        cmd_rumor(args)
    elif args.cmd == "witness":
        if args.action == "add" and not (args.id and args.name and args.saw and args.place):
            sys.exit("エラー: add には id・name・--saw・--place が必要")
        cmd_witness(args)
    elif args.cmd == "rep":
        cmd_rep(args)


if __name__ == "__main__":
    main()
