# Packers Schedule ICS Generator

NFL（Green Bay Packers）の全期間のスケジュールを `nflreadpy` から自動取得し、GoogleカレンダーやiOSカレンダーで購読可能な形式に公開するプロジェクトです。

## 📅 カレンダーの購読

GitHub Pages を有効化すると、以下の URL をカレンダーアプリに登録するだけで、常に最新のスケジュールが自動反映されます。

**購読用 URL:**
`https://5eto3.github.io/packers-schedule-ics/packers.ics`

### Google カレンダーへの追加方法
1. Google カレンダーを開きます。
2. 左側の「他のカレンダー」の横にある「＋」をクリックし、「URL で追加」を選択します。
3. 上記の購読用 URL を貼り付け、「カレンダーを追加」をクリックします。

---

## 🛠️ 自動同期のセットアップ方法

GitHub リポジトリ上で以下の設定を行うことで、毎週の自動更新と公開が始まります。

### 1. GitHub Actions の権限設定
1. リポジトリの **Settings > Actions > General** を開きます。
2. 下部の **Workflow permissions** を `Read and write permissions` に変更して保存（Save）します。
   - これにより、アクションがカレンダーを生成して公開用ブランチに自動保存できるようになります。

### 2. GitHub Pages の有効化
1. 修正したコードを GitHub にプッシュすると、自動的に `gh-pages` という名前のブランチが作成されます。
2. **Settings > Pages** を開きます。
3. **Build and deployment > Branch** で `gh-pages` を選択し、保存（Save）をクリックします。

### 3. 初回実行（手動）
1. **Actions** タブを選択します。
2. 左側の **Update Packers Calendar** を選択し、`Run workflow` をクリックすると即座に生成が始まります。
   - 以後は毎週月曜日の朝に自動で実行されます。

---

## 🚀 自動更新の仕組み

- **定期実行**: 毎週月曜日の朝に自動実行。
- **取得範囲**: 2000 年から現在年+1年までの全データを自動取得（1999年は時刻データなしのため除外）。
- **JST 変換**: 米国東部時間 (ET) を日本標準時 (JST) へ自動変換。

## 📦 開発・手動実行

```bash
pip install nflreadpy pandas pytz icalendar polars
python3 make_packers_calendar.py
```
実行後、`dist/` ディレクトリに `packers.ics` および `packers.csv` が生成されます。
