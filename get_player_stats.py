import requests
import csv
import webbrowser
import time

# PAST 20 SEASONS
seasons = ['1996-97', '1997-98', '1998-99', '1999-00', '2000-01', '2001-02', '2002-03', '2003-04', '2004-05', '2005-06', '2006-07', '2007-08', '2008-09', '2009-10', '2010-11', '2011-12', '2012-13', '2013-14', '2014-15', '2015-16']

# PLAYER ID LIST
player_list = []

# player_list_new = [] USE WHEN GET PLAYERS STATS BY TEAM

def get_player_list(team_name):
    ''' GET PLAYER ID LIST '''
    PLAYER_STATS = './nba_data/player_list/%s_player_list.csv' % team_name
    FULL_LIST = 'player_stats.csv'
    with open(PLAYER_STATS, 'r') as f:
        for line in f.readlines():
            player = line.strip().split(',')
            if player[-1] != 'PLAYER_ID' and player[-1] not in player_list and player[-1] not in current_players:
                player_list.append(player[-1])
        print(len(player_list))

def get_player_stats_by_year():
    '''' GET PLAYER STATS BY YEAR '''
    for season in seasons:
        with open(season + '_player_stats_by_year.csv', 'w') as f:
            fieldnames = ['SEASON_ID', 'PLAYER_NAME', 'TEAM_ABBREVIATION', 'GP', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS' ,'PLAYER_ID']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            builder = {}    # USE FIELDNAMES AS THE FILTER AND PASS EACH ROW INTO BUILDER
        
            respond = requests.get('http://stats.nba.com/stats/leaguedashplayerstats?' + 
                'College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&' +
                'DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&' + 
                'Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&' +
                'PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&' +
                'PlusMinus=N&Rank=N&Season=%s&SeasonSegment=&SeasonType=Regular+Season&' % season + 
                'ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight=').json()

            player_stats_header = respond['resultSets'][0]['headers']
            player_stats = respond['resultSets'][0]['rowSet']

            for stats in player_stats:
                builder[fieldnames[0]] = season

                for name in fieldnames:
                     builder[name] = stats[player_stats_header.index(name)]

                writer.writerow(builder)

def access():
    ''' GET ACCESS TO NBA STATS '''
    for season in seasons:
        respond = requests.get('http://stats.nba.com/stats/leaguedashplayerstats?' + 
                'College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&' +
                'DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&' + 
                'Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&' +
                'PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&' +
                'PlusMinus=N&Rank=N&Season=%s&SeasonSegment=&SeasonType=Regular+Season&' % season + 
                'ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight=')
        
        if respond.status_code !=200:    # AUTOMATICALY OPEN WEB PAGES TO GET ACCESS
            webbrowser.open_new_tab('http://stats.nba.com/league/player/#!/?Season=%s&SeasonType=Regular%s20Season&PerMode=Totals&sort=TEAM_ABBREVIATION&dir=1' % (season, '%'))
            time.sleep(8)
        print(respond, season)


access()
get_player_stats_by_year()
