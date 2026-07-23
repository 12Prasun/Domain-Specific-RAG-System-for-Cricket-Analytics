import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "cricket.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def get_batting_stats(player_name: str) -> dict:
    """Calculates batting statistics for a given player."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Runs Scored and Balls Faced
    cursor.execute('''
        SELECT SUM(runs_batter), COUNT(id)
        FROM ball_by_ball
        WHERE batter = ?
    ''', (player_name,))
    runs, balls = cursor.fetchone()
    runs = runs or 0
    balls = balls or 0
    
    # Times Dismissed
    cursor.execute('''
        SELECT COUNT(id)
        FROM ball_by_ball
        WHERE player_dismissed = ?
    ''', (player_name,))
    dismissals = cursor.fetchone()[0]
    
    conn.close()
    
    batting_average = runs / dismissals if dismissals > 0 else runs if runs > 0 else 0.0
    strike_rate = (runs / balls * 100) if balls > 0 else 0.0
    
    return {
        "Player": player_name,
        "Runs Scored": runs,
        "Balls Faced": balls,
        "Times Dismissed": dismissals,
        "Batting Average": round(batting_average, 2),
        "Strike Rate": round(strike_rate, 2)
    }

def get_bowling_stats(player_name: str) -> dict:
    """Calculates bowling statistics for a given player."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Runs Conceded (Total Runs off the bowler)
    cursor.execute('''
        SELECT SUM(runs_total), COUNT(id)
        FROM ball_by_ball
        WHERE bowler = ?
    ''', (player_name,))
    runs_conceded, balls_bowled = cursor.fetchone()
    runs_conceded = runs_conceded or 0
    balls_bowled = balls_bowled or 0
    
    # Wickets Taken
    cursor.execute('''
        SELECT COUNT(id)
        FROM ball_by_ball
        WHERE bowler = ? AND player_dismissed IS NOT NULL AND wicket_type != 'run out'
    ''', (player_name,))
    wickets = cursor.fetchone()[0]
    
    conn.close()
    
    overs_bowled = balls_bowled / 6.0
    economy_rate = (runs_conceded / overs_bowled) if overs_bowled > 0 else 0.0
    bowling_average = (runs_conceded / wickets) if wickets > 0 else 0.0
    
    return {
        "Player": player_name,
        "Runs Conceded": runs_conceded,
        "Balls Bowled": balls_bowled,
        "Overs Bowled": round(overs_bowled, 1),
        "Wickets": wickets,
        "Economy Rate": round(economy_rate, 2),
        "Bowling Average": round(bowling_average, 2)
    }

def get_team_stats(team_name: str) -> dict:
    """Calculates basic team statistics."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT COUNT(match_id)
        FROM matches
        WHERE team1 = ? OR team2 = ?
    ''', (team_name, team_name))
    matches_played = cursor.fetchone()[0]
    
    cursor.execute('''
        SELECT COUNT(match_id)
        FROM matches
        WHERE winner = ?
    ''', (team_name,))
    matches_won = cursor.fetchone()[0]
    
    conn.close()
    
    win_percentage = (matches_won / matches_played * 100) if matches_played > 0 else 0.0
    
    return {
        "Team": team_name,
        "Matches Played": matches_played,
        "Matches Won": matches_won,
        "Win Percentage": round(win_percentage, 2)
    }

def calculate_custom_metrics(entities: dict) -> dict:
    """
    Takes an entities dictionary (from ner.py) and calculates 
    metrics for each recognized player and team.
    """
    results = {}
    
    if "players" in entities and entities["players"]:
        results["players"] = {}
        for player in entities["players"]:
            batting = get_batting_stats(player)
            bowling = get_bowling_stats(player)
            
            # Include if they have played
            if batting["Balls Faced"] > 0 or bowling["Balls Bowled"] > 0:
                results["players"][player] = {
                    "Batting": batting,
                    "Bowling": bowling
                }
                
    if "teams" in entities and entities["teams"]:
        results["teams"] = {}
        for team in entities["teams"]:
            team_stats = get_team_stats(team)
            if team_stats["Matches Played"] > 0:
                results["teams"][team] = team_stats
                
    return results

if __name__ == "__main__":
    # Test block
    print("Testing Custom Metrics Calculation...")
    
    # We use common player names that might be in the IPL dataset 
    # to see if it grabs any stats.
    sample_entities = {
        "players": ["V Kohli", "JJ Bumrah", "MS Dhoni", "Rashid Khan"],
        "teams": ["Chennai Super Kings", "Mumbai Indians", "India"]
    }
    
    metrics = calculate_custom_metrics(sample_entities)
    
    import json
    print(json.dumps(metrics, indent=2))
