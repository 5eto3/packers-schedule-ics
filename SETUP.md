# Repository Setup & Maintenance Guide

このファイルは、リポジトリの所有者が GitHub Actions と GitHub Pages を使用してカレンダーの自動更新をセットアップ・保守するためのガイドです。

## 🛠️ 自動同期のセットアップ方法

GitHub リポジトリ上で以下の設定を行うことで、毎週の自動更新と公開が始まります。

### 1. GitHub Actions の権限設定
1. リポジトリの **Settings > Actions > General** を開きます。
2. 下部の **Workflow permissions** を `Read and write permissions` に変更して保存（Save）します。
   - これにより、アクションがカレンダーを生成して公開用ブランチに自動保存できるようになります。

### 2. GitHub Pages の有効化
1. **GitHub Actions を手動で一度実行する**ことで、自動的に `gh-pages` という名前のブランチが作成されます（詳細は「3. 初回実行」を参照）。
2. ブランチ作成後、**Settings > Pages** を開きます。
3. **Build and deployment > Source** で `Deploy from a branch` を選択します（デフォルトでこれになっているはずです）。
4. **Build and deployment > Branch** で `gh-pages` および `/(root)` を選択し、保存（Save）をクリックします。

### 3. 初回・手動実行方法
1. リポジトリ上部の **Actions** タブを選択します。
2. 左側の **Update Packers Calendar** を選択します。
3. `Run workflow` ボタンをクリックすると、スクリプトが実行され、カレンダーファイルが生成・デプロイされます。
   - 数分待つと `gh-pages` ブランチが作成され、URL でアクセスできるようになります。
   - 以後は毎週月曜日の朝に自動で実行されます。

---

## 🚀 更新の仕組み

- **定期実行**: 毎週月曜日の朝（JST）に自動実行されるように `.github/workflows/update_calendar.yml` で設定されています。
- **データ取得**: 2000 年から「実行時の年 + 1」までの全データを自動的に取得し、1つの統合されたプロジェクト（Packers Schedule）として出力します。
- **タイムゾーン**: `make_packers_calendar.py` 内で米国東部時間を日本標準時に変換しています。
