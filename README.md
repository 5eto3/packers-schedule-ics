# Packers Schedule ICS Generator

NFL（Green Bay Packers）の全期間のスケジュールを `nflreadpy` から自動取得し、GoogleカレンダーやiOSカレンダーで購読可能な形式に公開するプロジェクトです。

## 📅 カレンダーの購読（推奨）

このプロジェクトを GitHub Pages で公開している場合、以下の URL をカレンダーアプリに登録するだけで、常に最新（2000年〜最新シーズン）のスケジュールが自動的に反映されます。

**購読用 URL:**
`https://[あなたのユーザー名].github.io/packers-schedule-ics/packers.ics`

### Google カレンダーへの追加方法
1. Google カレンダーを開きます。
2. 左側の「他のカレンダー」の横にある「＋」をクリックし、「URL で追加」を選択します。
3. 上記の購読用 URL を貼り付け、「カレンダーを追加」をクリックします。

---

## 🚀 自動更新の仕組み

- **GitHub Actions**: 毎週月曜日の朝に自動的にスクリプトが実行され、最新の試合結果や予定（日時の確定など）が更新されます。
- **全期間取得**: 実行時に 2000 年から現在年+1年までの全データを自動取得し、1つのカレンダーに統合します。
- **JST 変換**: 米国東部時間 (ET) は自動的に日本標準時 (JST) へ変換されます。

## 🛠️ 開発・手動実行

自分自身でカレンダーファイルを生成したい場合：

### セットアップ
```bash
pip install nflreadpy pandas pytz icalendar polars
```

### 実行
```bash
python3 make_packers_calendar.py
```
実行後、`dist/` ディレクトリに `packers.ics` および `packers.csv` が生成されます。

## 📦 ソース管理 (Git) について

- **スクリプト本体**: Gitで管理されています。
- **自動同期設定**: `.github/workflows/update_calendar.yml` で制御されています。
- **生成物 (`dist/`)**: `gh-pages` ブランチにのみデプロイされ、`main` ブランチの履歴は汚さないよう設定されています。

## ⚠️ 注意事項
- 試合開始時刻が未確定（TBD）の場合はデータに含まれないことがあります。公式のスケジュールが確定次第、毎週の自動更新で反映されます。
