import numpy as np
import pandas as pd

def load_players(file_path):
    return pd.read_csv("C:\\Users\\Ascendion\\Downloads\\cricket_players_analysis (1)\\cricket_players_analysis\\data\\players.csv")


def load_matches(file_path):
    return pd.read_csv("C:\\Users\\Ascendion\\Downloads\\cricket_players_analysis (1)\\cricket_players_analysis\\data\\matches.csv")

def merge_players_matches(players_df, matches_df):
    merged = pd.merge(players_df, matches_df, on='PlayerID', how='inner')
    expected_order = ['PlayerID', 'Name', 'Team', 'Role', 'Age', 'MatchID', 'Runs', 'Balls',
                      'Fours', 'Sixes', 'Wickets', 'Catches', 'Date']
    merged = merged[expected_order]
    return merged

def total_runs_per_team(merged_df):
    return merged_df.groupby('Team', as_index=False)['Runs'].sum()

def calculate_strike_rate(merged_df):
    merged_df = merged_df.copy()
    merged_df['StrikeRate'] = (merged_df['Runs'] / merged_df['Balls']) * 100
    return merged_df[['PlayerID', 'Name', 'Runs', 'Balls', 'StrikeRate']]

def runs_agg_per_player(merged_df):
    agg_df = merged_df.groupby(['PlayerID', 'Name'], as_index=False).agg(
        mean=('Runs', 'mean'),
        max=('Runs', 'max'),
        min=('Runs', 'min')
    )
    return agg_df

def avg_age_by_role(players_df):
    return players_df.groupby('Role', as_index=False)['Age'].mean()

def total_matches_per_player(matches_df):
    matches_count = matches_df.groupby('PlayerID')['MatchID'].nunique().reset_index()
    matches_count = matches_count.rename(columns={'MatchID': 'MatchCount'})
    return matches_count

def top_wicket_takers(merged_df):
    wickets_df = merged_df.groupby(['PlayerID', 'Name'], as_index=False)['Wickets'].sum()
    wickets_df = wickets_df.sort_values('Wickets', ascending=False).head(3).reset_index(drop=True)
    return wickets_df

def avg_strike_rate_per_team(merged_df):
    merged_df = merged_df.copy()
    merged_df['StrikeRate'] = (merged_df['Runs'] / merged_df['Balls']) * 100
    return merged_df.groupby('Team', as_index=False)['StrikeRate'].mean()

def catch_to_match_ratio(merged_df):
    catches = merged_df.groupby('PlayerID', as_index=False)['Catches'].sum()
    matches = merged_df.groupby('PlayerID')['MatchID'].nunique().reset_index()
    matches = matches.rename(columns={'MatchID': 'Matches'})
    ratio_df = pd.merge(catches, matches, on='PlayerID')
    ratio_df['CatchToMatchRatio'] = ratio_df['Catches'] / ratio_df['Matches']
    return ratio_df[['PlayerID', 'CatchToMatchRatio']]

