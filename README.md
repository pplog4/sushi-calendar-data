# sushi-calendar-data

PPログ（powerplatformnikki.com）の JAL ページに出す「JAL Fラウンジ 鮨鶴亭 週替わりネタ」のデータです。

- `sushi-calendar.json`：Muse（メイン）が更新する最新データ。手順は MUSE-UPDATE.md。
- `last-good.json`：GitHub Actions（validate-and-promote）が形を検査し、合格した版だけを写したもの。
- `validate.py`：形の検査（Actions と同じ）。
- 表示部品：https://pplog4.github.io/sushi-calendar/embed.js（両方のファイルを読み、最新が壊れていれば last-good を表示して「更新を確認中」と出す）。

出典は各行の source_url と、`sources` の説明のとおり。2026年分は X 投稿が出典で、3品目が分からない週があります。ご利用前に JAL 公式サイトでご確認ください。
