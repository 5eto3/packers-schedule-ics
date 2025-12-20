import datetime
import os
import sys
import pandas as pd
import pytz
import nflreadpy
from icalendar import Calendar, Event
import polars as pl
 
OUTPUT_DIR = "dist"

def fetch_schedule(seasons):
    """nflreadpyを使用してスケジュールを取得し、GBの試合のみにフィルタリングする"""
    print(f"Fetching schedules for {seasons}...")
    try:
        schedules = nflreadpy.load_schedules(seasons=seasons)
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

def generate_ics(df, seasons_str, filename):
    """カレンダー登録用のICSを生成する"""
    cal = Calendar()
    cal.add('prodid', '-//GB Schedule Generator//mxm.dk//')
    cal.add('version', '2.0')
    cal.add('x-wr-calname', f"Packers Schedule ({seasons_str})")

    for _, row in df.iterrows():
        if pd.isna(row['start_jst']):
            continue

        start_dt = row['start_jst']
        end_dt = start_dt + datetime.timedelta(hours=3)

        event = Event()
        
        # Summary format: GB 24-21 vs DET (Week X) or GB @ DET (Week X)
        is_home = row['home_team'] == 'GB'
        connector = "vs" if is_home else "@"
        opponent = row['away_team'] if is_home else row['home_team']
        
        score_str = ""
        if not pd.isna(row['home_score']) and not pd.isna(row['away_score']):
            gb_score = row['home_score'] if is_home else row['away_score']
            opp_score = row['away_score'] if is_home else row['home_score']
            score_str = f" {int(gb_score)}-{int(opp_score)}"
            
        summary = f"GB {connector} {opponent}{score_str} (Week {row['week']})"
        
        event.add('summary', summary)
        event.add('dtstart', start_dt)
        event.add('dtend', end_dt)
        event.add('dtstamp', datetime.datetime.now(pytz.utc))
        
        # Unique ID based on season and week
        uid = f"GB-{row['season']}-{row['game_type']}-{row['week']}@packers-schedule"
        event.add('uid', uid)

        cal.add_component(event)

    with open(filename, 'wb') as f:
        f.write(cal.to_ical())
    print(f"ICS generated: {filename}")

def main():
    # Default: 2000 to current year + 1
    current_year = datetime.datetime.now().year
    start_year = 2000
    end_year = current_year + 1
    seasons = list(range(start_year, end_year + 1))
    seasons_str = f"{start_year}-{end_year}"

    # Fetch data
    gb_games = fetch_schedule(seasons)

    if gb_games.empty:
        print(f"No games found for seasons {seasons}.")
        return

    # Process times
    gb_games['start_jst'] = gb_games.apply(convert_to_jst, axis=1)
    
    # Sort by time
    gb_games = gb_games.sort_values(['season', 'week', 'gameday'])

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Generate files (Fixed names for subscription)
    csv_filename = os.path.join(OUTPUT_DIR, "packers.csv")
    ics_filename = os.path.join(OUTPUT_DIR, "packers.ics")

    generate_csv(gb_games, seasons_str, csv_filename)
    generate_ics(gb_games, seasons_str, ics_filename)

if __name__ == "__main__":
    main()
