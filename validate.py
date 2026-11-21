#!/usr/bin/env python3
"""sushi-calendar.json の形を検査する（GitHub Actions と手元の両方で使う）。

  python3 validate.py sushi-calendar.json [last-good.json]

検査：schema=1、updated と各 date が実在する YYYY-MM-DD、items が1件以上、
airport / lounge / detail が空でない200字以内の文字列、source_url が空か https://。
last-good.json を渡すと、件数が6件以上減っていないかも見る（記録の消失を防ぐ）。
合格なら終了コード0、不合格なら理由を表示して1。
"""
import datetime as dt, json, re, sys

DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def errors(d, prev=None):
    e = []
    if not isinstance(d, dict):
        return ["JSONの一番外がオブジェクトでない"]
    if d.get("schema") != 1:
        e.append("schema が 1 でない")
    for k in ("updated",):
        v = d.get(k)
        if not (isinstance(v, str) and DATE.match(v)):
            e.append(f"{k} が YYYY-MM-DD でない")
        else:
            try:
                dt.date.fromisoformat(v)
            except ValueError:
                e.append(f"{k} が実在しない日付")
    items = d.get("items")
    if not isinstance(items, list) or not items:
        return e + ["items が1件以上の配列でない"]
    for i, it in enumerate(items, 1):
        if not isinstance(it, dict):
            e.append(f"{i}件目がオブジェクトでない"); continue
        v = it.get("date")
        try:
            if not (isinstance(v, str) and DATE.match(v)):
                raise ValueError
            dt.date.fromisoformat(v)
        except ValueError:
            e.append(f"{i}件目の date が不正：{v!r}")
        for k in ("airport", "lounge", "detail"):
            s = it.get(k)
            if not (isinstance(s, str) and s.strip() and len(s) <= 200):
                e.append(f"{i}件目の {k} が空か長すぎる")
        u = it.get("source_url", "")
        if not (u == "" or (isinstance(u, str) and re.match(r"^https://[^\s\"'<>]+$", u))):
            e.append(f"{i}件目の source_url が https でない：{u!r}")
    if prev and isinstance(prev.get("items"), list) and len(items) < len(prev["items"]) - 5:
        e.append(f"件数が {len(prev['items'])} から {len(items)} に減った")
    return e


def main(argv):
    d = json.load(open(argv[1], encoding="utf-8"))
    prev = json.load(open(argv[2], encoding="utf-8")) if len(argv) > 2 else None
    errs = errors(d, prev)
    for m in errs[:20]:
        print("NG:", m)
    if not errs:
        print(f"OK: {len(d['items'])}件、updated {d['updated']}")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
