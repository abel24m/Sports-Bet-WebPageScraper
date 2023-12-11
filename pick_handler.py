from difflib import SequenceMatcher
from enum import Enum


class League(Enum):
    NBA = 0
    NFL = 1
    NHL = 2
    NCAAB = 3
    NCAAF = 4

class Pick_Handler:

    
    SIMILARITY_STANDARD = .80


    def print_ncaab(self):
        for pick in self.ncaab_picks:
            print(pick, end="\n")

    def print_nba(self):
        for pick in self.nba_picks:
            print(pick, end="\n")
    
    def print_nfl(self):
        for pick in self.nfl_picks:
            print(pick, end="\n")

    def print_nhl(self):
        for pick in self.nhl_picks:
            print(pick, end="\n")

    def print_ncaaf(self):
        for pick in self.ncaaf_picks:
            print(pick, end="\n")

    def group_picks_ncaab(self):
        grouped_picks = []
        for pick in self.ncaab_picks:
            away_team_stripped = pick[0].strip()
            home_team_stripped = pick[1].strip()
            game_existed = False
            for index in range(len(grouped_picks)) :
                away_team_similarity = SequenceMatcher(None, away_team_stripped, grouped_picks[index][0]).ratio()
                home_team_similarity = SequenceMatcher(None, home_team_stripped, grouped_picks[index][1]).ratio()
                if away_team_similarity > self.SIMILARITY_STANDARD or home_team_similarity > self.SIMILARITY_STANDARD:
                    grouped_picks[index].append(pick[2])
                    game_existed = True
                    break
            if (not game_existed):
                grouped_picks.append(pick)
        
        self.ncaab_picks = grouped_picks

    def group_picks_nba(self):
        grouped_picks = []
        for pick in self.nba_picks:
            away_team_split = pick[0].split(" ")
            away_team_last_word = away_team_split[-1]
            game_existed = False
            for index in range(len(grouped_picks)) :
                other_away_team_last_word = grouped_picks[index][0].split(" ")[-1]
                similarity = SequenceMatcher(None, away_team_last_word, other_away_team_last_word).ratio()
                if similarity > self.SIMILARITY_STANDARD:
                    grouped_picks[index].append(pick[2])
                    game_existed = True
                    break
            if (not game_existed):
                grouped_picks.append(pick)        
        self.nba_picks = grouped_picks

    def group_picks_nfl(self):
        grouped_picks = []
        for pick in self.nfl_picks:
            away_team_split = pick[0].split(" ")
            away_team_last_word = away_team_split[-1]
            game_existed = False
            for index in range(len(grouped_picks)) :
                other_away_team_last_word = grouped_picks[index][0].split(" ")[-1]
                similarity = SequenceMatcher(None, away_team_last_word, other_away_team_last_word).ratio()
                if similarity > self.SIMILARITY_STANDARD:
                    grouped_picks[index].append(pick[2])
                    game_existed = True
                    break
            if (not game_existed):
                grouped_picks.append(pick)        
        self.nfl_picks = grouped_picks

    def group_picks_ncaaf(self):
        grouped_picks = []
        for pick in self.ncaaf_picks:
            away_team_stripped = pick[0].strip()
            home_team_stripped = pick[1].strip()
            game_existed = False
            for index in range(len(grouped_picks)) :
                away_team_similarity = SequenceMatcher(None, away_team_stripped, grouped_picks[index][0]).ratio()
                home_team_similarity =  SequenceMatcher(None, home_team_stripped, grouped_picks[index][1]).ratio()
                if away_team_similarity > self.SIMILARITY_STANDARD or home_team_similarity > self.SIMILARITY_STANDARD:
                    grouped_picks[index].append(pick[2])
                    game_existed = True
                    break
            if (not game_existed):
                grouped_picks.append(pick)
        
        self.ncaaf_picks = grouped_picks

    def group_picks_nhl(self):
        grouped_picks = []
        for pick in self.nhl_picks:
            away_team_split = pick[0].split(" ")
            away_team_last_word = away_team_split[-1]
            game_existed = False
            for index in range(len(grouped_picks)) :
                other_away_team_last_word = grouped_picks[index][0].split(" ")[-1]
                similarity = SequenceMatcher(None, away_team_last_word, other_away_team_last_word).ratio()
                if similarity > self.SIMILARITY_STANDARD:
                    grouped_picks[index].append(pick[2])
                    game_existed = True
                    break
            if (not game_existed):
                grouped_picks.append(pick)        
        self.nhl_picks = grouped_picks


                    
                


            





    


    def __init__(self) -> None:
        self.nba_picks = []
        self.nfl_picks = []
        self.nhl_picks = []
        self.ncaab_picks = []
        self.ncaaf_picks = []



