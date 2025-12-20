import argparse
import datetime
import sys
import pandas as pd
import pytz
import nflreadpy
from icalendar import Calendar, Event
import polars as pl

def fetch_schedule(season):
    """nflreadpyを使用してスケジュールを取得し、GBの試合のみにフィルタリングする"""
    print(f"Fetching schedule for {season}...")
    try:
        schedules = nflreadpy.load_schedules(seasons=[season])
    except Exception as e:
        print(f"Error loading schedules: {e}")
        sys.exit(1)

    # Polars DataFrame or Pandas DataFrame handling
    if isinstance(schedules, pl.DataFrame):
        df = schedules.to_pandas()
    else:
        df = pd.DataFrame(schedules)

    # Filter for Green Bay Packers (GB)
    gb_games = df[(df['home_team'] == 'GB') | (df['away_team'] == 'GB')].copy()
    return gb_games

def convert_to_jst(row):
    """gamedayとgametimeを組み合わせてJSTに変換する"""
    gameday = row['gameday'] # YYYY-MM-DD
    gametime = row['gametime'] # HH:MM (ET)

    if pd.isna(gametime) or gametime == "" or gametime is None:
        return None

    # ET timezone (handles DST automatically)
    et_tz = pytz.timezone('US/Eastern')
    jst_tz = pytz.timezone('Asia/Tokyo')

    try:
        # Combine day and time
        dt_str = f"{gameday} {gametime}"
        et_dt = et_tz.localize(datetime.datetime.strptime(dt_str, '%Y-%m-%d %H:%M'))
        jst_dt = et_dt.astimezone(jst_tz)
        return jst_dt
    except Exception as e:
        print(f"Error converting time for {gameday} {gametime}: {e}")
        return None

def generate_csv(df, season, filename):
    """確認用のCSVを生成する"""
    output_df = pd.DataFrame()
    output_df['start_jst'] = df['start_jst'].dt.strftime('%Y-%m-%d %H:%M')
    output_df['home_away'] = df.apply(lambda r: 'home' if r['home_team'] == 'GB' else 'away', axis=1)
    output_df['opponent'] = df.apply(lambda r: r['away_team'] if r['home_team'] == 'GB' else r['home_team'], axis=1)
    output_df['week'] = df['week']
    output_df['season_type'] = df['game_type']

    output_df.to_csv(filename, index=False)
    print(f"CSV generated: {filename}")

def generate_ics(df, season, filename):
    """カレンダー登録用のICSを生成する"""
    cal = Calendar()
    cal.add('prodid', '-//GB Schedule Generator//mxm.dk//')
    cal.add('version', '2.0')

    for _, row in df.iterrows():
        if pd.isna(row['start_jst']):
            continue

        start_dt = row['start_jst']
        end_dt = start_dt + datetime.timedelta(hours=3)

        event = Event()
        
        # Summary format: 🏈 Packers vs Opponent (Week X) or 🏈 Packers @ Opponent (Week X)
        is_home = row['home_team'] == 'GB'
        connector = "vs" if is_home else "@"
        opponent = row['away_team'] if is_home else row['home_team']
        summary = f"GB {connector} {opponent} (Week {row['week']})"
        
        event.add('summary', summary)
        event.add('dtstart', start_dt)
        event.add('dtend', end_dt)
        event.add('dtstamp', datetime.datetime.now(pytz.utc))
        
        # Unique ID based on season and week
        uid = f"GB-{season}-{row['game_type']}-{row['week']}@packers-schedule"
        event.add('uid', uid)

        cal.add_component(event)

    with open(filename, 'wb') as f:
        f.write(cal.to_ical())
    print(f"ICS generated: {filename}")

def main():
    parser = argparse.ArgumentParser(description='Generate Packers schedule CSV and ICS')
    parser.add_argument('season', type=int, help='Season year (e.g. 2025)')
    args = parser.parse_args()

    # Fetch data
    gb_games = fetch_schedule(args.season)

    if gb_games.empty:
        print(f"No games found for season {args.season}.")
        return

    # Process times
    gb_games['start_jst'] = gb_games.apply(convert_to_jst, axis=1)
    
    # Sort by time
    gb_games = gb_games.sort_values('gameday')

    # Generate files
    csv_filename = f"packers_{args.season}.csv"
    ics_filename = f"packers_{args.season}.ics"

    generate_csv(gb_games, args.season, csv_filename)
    generate_ics(gb_games, args.season, ics_filename)

if __name__ == "__main__":
    main()
