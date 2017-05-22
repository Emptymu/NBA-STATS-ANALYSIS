import requests
import csv
import time
import webbrowser

#PAST 12 SEASONS
seasons = ['2004-05', '2005-06', '2006-07', '2007-08', '2008-09', '2009-10', '2010-11', '2011-12', '2012-13', '2013-14', '2014-15', '2015-16']


def get_player_list(team, team_id):
	''' GET PLAYER ID LIST '''
	with open(team + '_player_list.csv', 'w') as f:
		fieldnames = ['SEASON', 'TEAM', 'PLAYER', 'NUM', 'POSITION', 'HEIGHT', 'WEIGHT', 'BIRTH_DATE', 'AGE', 'EXP', 'PLAYER_ID']
		writer = csv.DictWriter(f, fieldnames=fieldnames)
		writer.writeheader()
		builder = {}     # USE FIELDNAMES AS THE FILTER AND PASS EACH ROW INTO BUILDER

		for season in seasons:
			respond = requests.get('http://stats.nba.com/stats/commonteamroster?LeagueID=00&Season=%s&TeamID=%d' % (season, team_id)).json()

			player_list_header = respond['resultSets'][0]['headers']
			player_list = respond['resultSets'][0]['rowSet']

			for player in player_list:
				builder['SEASON'] = season
				builder['TEAM'] = team
				for i in range(2, 11):
					builder[fieldnames[i]] = player[player_list_header.index(fieldnames[i])]

				writer.writerow(builder)

def access(team_id):
	''' GET ACCESS TO NBA STATS '''
	for season in seasons:
		respond = requests.get('http://stats.nba.com/stats/commonteamroster?LeagueID=00&Season=%s&TeamID=%d' % (season, team_id))
		if respond.status_code != 200:
			webbrowser.open_new_tab('http://stats.nba.com/team/#!/%s/?Season=%s' % (team_id, season))
			time.sleep(5)
		print(respond, season)
    


access(1610612759)
get_player_list('Spur', 1610612759)
