import os
import json
import sqlite3
from database import get_connection, init_db

RAW_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "raw")

def populate_database():
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    
    # We will track processed players to avoid redundant inserts
    processed_players = set()
    
    files = [f for f in os.listdir(RAW_DATA_DIR) if f.endswith('.json')]
    print(f"Found {len(files)} JSON files. Starting ingestion...")
    
    for i, filename in enumerate(files):
        if i > 0 and i % 100 == 0:
            print(f"Processed {i}/{len(files)} files...")
            conn.commit() # Commit periodically

        filepath = os.path.join(RAW_DATA_DIR, filename)
        match_id = filename.split('.')[0]
        
        with open(filepath, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print(f"Error reading {filename}. Skipping.")
                continue
                
        info = data.get('info', {})
        
        # 1. Insert Match
        date = info.get('dates', [''])[0] if info.get('dates') else None
        venue = info.get('venue')
        teams = info.get('teams', [])
        team1 = teams[0] if len(teams) > 0 else None
        team2 = teams[1] if len(teams) > 1 else None
        
        toss_winner = info.get('toss', {}).get('winner')
        toss_decision = info.get('toss', {}).get('decision')
        winner = info.get('outcome', {}).get('winner')
        
        cursor.execute('''
            INSERT OR IGNORE INTO matches 
            (match_id, date, venue, team1, team2, toss_winner, toss_decision, winner)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (match_id, date, venue, team1, team2, toss_winner, toss_decision, winner))
        
        # 2. Insert Players
        registry = info.get('registry', {}).get('people', {})
        for player_name, player_id in registry.items():
            if player_id not in processed_players:
                cursor.execute('''
                    INSERT OR IGNORE INTO players (player_id, player_name)
                    VALUES (?, ?)
                ''', (player_id, player_name))
                processed_players.add(player_id)
        
        # 3. Insert Ball by Ball
        innings = data.get('innings', [])
        ball_records = []
        for inning_idx, inning in enumerate(innings):
            inning_num = inning_idx + 1
            overs = inning.get('overs', [])
            for over in overs:
                over_num = over.get('over')
                deliveries = over.get('deliveries', [])
                for del_idx, delivery in enumerate(deliveries):
                    actual_delivery = delivery.get('actual_delivery', f"{over_num}.{del_idx + 1}")
                    
                    batter = delivery.get('batter')
                    bowler = delivery.get('bowler')
                    non_striker = delivery.get('non_striker')
                    
                    runs = delivery.get('runs', {})
                    runs_batter = runs.get('batter', 0)
                    runs_extras = runs.get('extras', 0)
                    runs_total = runs.get('total', 0)
                    
                    wickets = delivery.get('wickets', [])
                    wicket_type = wickets[0].get('kind') if wickets else None
                    player_dismissed = wickets[0].get('player_out') if wickets else None
                    
                    ball_records.append((
                        match_id,
                        inning_num,
                        over_num,
                        str(actual_delivery),
                        batter,
                        bowler,
                        non_striker,
                        runs_batter,
                        runs_extras,
                        runs_total,
                        wicket_type,
                        player_dismissed
                    ))
                    
        if ball_records:
            cursor.executemany('''
                INSERT INTO ball_by_ball 
                (match_id, inning, over, delivery, batter, bowler, non_striker, runs_batter, runs_extras, runs_total, wicket_type, player_dismissed)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', ball_records)
            
    conn.commit()
    conn.close()
    print("Database population complete.")

if __name__ == "__main__":
    populate_database()
