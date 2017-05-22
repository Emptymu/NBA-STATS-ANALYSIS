import requests
import csv
import webbrowser
import time

# PAST 20 SEASONS
seasons = ['1996-97', '1997-98', '1998-99', '1999-00', '2000-01', '2001-02', '2002-03', '2003-04', '2004-05', '2005-06', '2006-07', '2007-08', '2008-09', '2009-10', '2010-11', '2011-12', '2012-13', '2013-14', '2014-15', '2015-16']

# TEAM ID LIST
team_list = []

def get_team_list():
	''' GET TEAM ID LIST '''
	TEAM_LIST = './team_id.csv'
	with open(TEAM_LIST, 'r') as f:
		for line in f.readlines():
			team = line.strip().split(',')
			if team[0] != 'TEAM_ID':
				team_list.append(team[0])

def get_team_stats():
	''' GET TEAM BASIC STATS BY YEAR '''
	with open('team_stats.csv', 'w') as f:
		fieldnames = ['SEASON', 'TEAM_NAME', 'GP', 'W', 'L', 'W_PCT', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'TOV', 'STL', 'BLK', 'BLKA', 'PF', 'PFD', 'PTS', 'PLUS_MINUS', 'TEAM_ID']
		writer = csv.DictWriter(f, fieldnames=fieldnames)
		writer.writeheader()
		builder = {}

		for season in seasons:
			respond = requests.get('http://stats.nba.com/stats/leaguedashteamstats?' + 
				                   'Conference=&DateFrom=&DateTo=&Division=&GameScope=&' + 
				                   'GameSegment=&LastNGames=0&LeagueID=00&Location=&' + 
				                   'MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&' + 
				                   'PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&' + 
				                   'PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&' + 
				                   'Season=%s&SeasonSegment=&SeasonType=Regular+Season&' % season +
				                   'ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=').json()
			#print(respond)

			team_stats_header = respond['resultSets'][0]['headers']
			team_stats_list = respond['resultSets'][0]['rowSet']

			for team in team_stats_list:
				builder[fieldnames[0]] = season
				builder[fieldnames[28]] = team[0]

				for i in range(1, 28):
					builder[fieldnames[i]] = team[i]
				
				writer.writerow(builder)

def get_team_advanced_data(season):
	''' GET TEAM ADVANCED DATA BY YEAR '''
	get_team_list()
	with open('get_%s_team_advanced_data.csv' % season, 'w') as f:
		fieldnames = ['SEASON_YEAR', 'OFF_RATING', 'DEF_RATING', 'NET_RATING', 'AST_PCT', 'AST_TO', 'AST_RATIO', 'OREB_PCT', 'DREB_PCT', 'REB_PCT', 'TM_TOV_PCT', 'EFG_PCT', 'TS_PCT', 'PACE', 'PIE', 'TEAM_ID']
		writer = csv.DictWriter(f, fieldnames=fieldnames)
		writer.writeheader()
		builder = {}    # USE FIELDNAMES AS THE FILTER AND PASS EACH ROW INTO BUILDER

		for team in team_list:
			respond = requests.get('http://stats.nba.com/stats/teamdashboardbygeneralsplits?' + 
				'DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Advanced' + 
				'&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&' + 
				'PlusMinus=N&Rank=N&Season=%s&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=' % season + 
				'&TeamID=%s&VsConference=&VsDivision=' % team).json()

			team_stats_header = respond['resultSets'][0]['headers']
			team_advanced_stats = respond['resultSets'][0]['rowSet']

			for stats in team_advanced_stats:
				for i in range(0, 15):
					builder[fieldnames[i]] = stats[team_stats_header.index(fieldnames[i])]

				builder[fieldnames[15]] = team
				writer.writerow(builder)
			

def access():
	''' GET ACCESS TO NBA STATS '''
	get_team_list()
	for season in seasons:
		respond = requests.get('http://stats.nba.com/stats/leaguedashteamstats?' + 
			'Conference=&DateFrom=&DateTo=&Division=&GameScope=&' + 
			'GameSegment=&LastNGames=0&LeagueID=00&Location=&' + 
			'MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&' + 
			'PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&' + 
			'PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&' + 
			'Season=%s&SeasonSegment=&SeasonType=Regular+Season&' % season +
			'ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=')

		if respond.status_code != 200:    # AUTOMATICALY OPEN WEB PAGES TO GET ACCESS
			webbrowser.open_new_tab('http://stats.nba.com/league/team/#!/?Season=%s&SeasonType=Regular%s20Season&PerMode=Totals' % (season, '%'))
			time.sleep(5)
		print(respond)
    team_list = []


access()
get_team_stats()
