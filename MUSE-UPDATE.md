# Muse（メイン）の更新手順：寿司カレンダー

PPログの JAL ページは、このリポジトリの `sushi-calendar.json` を直接読んで表を描きます。Mac や Bot は中継しません。Muse が書けば数分（最大5分のキャッシュ）でページに出ます。

## いつ
- 今の定期調査（毎週月・木 12:13 ごろ、Grok で X を検索 → 原文と画像を確認）が終わり、記録を更新した直後。
- 中身が前回と同じなら書かない。

## 何を
`sushi-calendar.json` 全体（全件。差分ではない）。UTF-8、次の形：

```json
{
 "schema": 1,
 "updated": "2026-11-23",
 "title": "JAL Fラウンジ 鮨鶴亭 週替わりネタ",
 "hours": "羽田7:00〜11:00、成田7:30〜11:30・15:00〜20:00（現行・公式ラウンジページ）",
 "sources": "JAL公式発表・公式四半期メニュー、X投稿（一次情報）、訪問記・二次記事。…",
 "items": [
  {"date": "2026-11-16", "airport": "羽田", "lounge": "鮨鶴亭（JAL Fラウンジ）",
   "detail": "本マグロ天身・のどぐろ・3品目未確認（〜11-22・2品のみ）",
   "source_url": "https://x.com/…/status/…"}
 ]
}
```

- `updated`：書いた日（日本時間、YYYY-MM-DD）。
- `items`：1行1件。`date` は提供開始日（YYYY-MM-DD）、`airport`（羽田／成田／羽田・成田／未確認）、`lounge`、`detail`（ネタと期間。分からない品は「未確認」と書く）、`source_url`（https の出典。無ければ空文字）。新しい順に並べる。
- 推測で埋めない。消す記録がある場合は理由を `sources` の末尾に書く（6件以上減ると表示側が採用しない）。

## どこへ
- リポジトリ `pplog4/sushi-calendar-data`、ブランチ `main`、ファイル `sushi-calendar.json`。
- GitHub の Contents API で上書きする。認証は Secure Vault の `custom.github-sushi`（Bearer、許可先 api.github.com）。
  1. `GET https://api.github.com/repos/pplog4/sushi-calendar-data/contents/sushi-calendar.json?ref=main` で今の `sha` を得る。
  2. `PUT` 同じURL、本文 `{"message": "update YYYY-MM-DD（n件）", "content": <base64>, "sha": <1の値>, "branch": "main"}`。
  3. 409・422（sha の食い違い）なら1から1回だけやり直す。それ以外の失敗は再送せず、会議室に1行で知らせる。
- このキーで書けるのはこのリポジトリだけ。ほかのリポジトリ・ファイルには書かない。

## 書いた後
- 2〜3分後に `https://raw.githubusercontent.com/pplog4/sushi-calendar-data/main/last-good.json` の `updated` が今日になっていれば反映済み（GitHub Actions が形を検査して合格分だけ写す）。
- ならなければ、Actions の検査で落ちています（リポジトリの Actions タブに理由）。ページは前回の表のまま「更新を確認中」と出ます。直して書き直す。
- 会議室への報告は、失敗したときだけ。
