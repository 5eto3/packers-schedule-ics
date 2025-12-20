# Packers Schedule ICS Generator

Green Bay Packers の試合スケジュールを `nflreadpy` から取得し、日本標準時 (JST) に変換して CSV と ICS ファイルを生成するツールです。

## 特徴
- **NFL公式系データ**: `nflreadpy` ライブラリを使用して信頼性の高いスケジュールを取得。
- **JST変換**: 米国東部時間 (ET) を自動的に日本標準時 (JST) へ変換。
- **カレンダー対応**: Google / iOS カレンダーへインポート可能な ICS ファイルを出力。
- **確認用ファイル**: 生成内容を目視で確認するための CSV ファイルも同時出力。

## セットアップ

このプロジェクトでは Python 3.10 以上が必要です。便利ツールの `uv` を使用したセットアップ例を以下に示します。

```bash
# 仮想環境の作成とライブラリのインストール
uv venv .venv
source .venv/bin/activate
uv pip install nflreadpy pandas pytz icalendar pyarrow
```

## 使い方

仮想環境を有効にした状態で、対象のシーズン（年）を指定してスクリプトを実行します。

```bash
source .venv/bin/activate
python3 make_packers_calendar.py 2025
```

### 出力ファイル
- `packers_2025.csv`: 試合開始日時（JST）、ホーム/アウェイ、対戦相手などの一覧。
- `packers_2025.ics`: カレンダーアプリにインポートして使用。

## 運用ルール
- 毎年、新シーズンのスケジュールが公開されたタイミングで実行してください。
- 試合開始時刻が未確定（TBD）の場合はデータに含まれないか、空になる可能性があります。スケジュール確定後に再実行してください。
