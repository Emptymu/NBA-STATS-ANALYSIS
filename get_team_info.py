import requests
import csv

def get_team_info():
	''' GET TEAM INFO (ID AND NAME) '''
	with open('team_id.csv', 'w') as f:
		fieldnames = ['TEAM_ID', 'SEASON_YEAR', 'TEAM_CITY', 'TEAM_NAME', 'TEAM_ABBREVIATION', 'TEAM_CONFERENCE', 'W', 'L', 'PCT', 'CONF_RANK', 'MIN_YEAR', 'MAX_YEAR']
		writer = csv.DictWriter(f, fieldnames=fieldnames)
		writer.writeheader()
		builder = {}    # USE FIELDNAMES AS THE FILTER AND PASS EACH ROW INTO BUILDER

		# NBA TEAMS IDS ARE FROM 1610612737 ~ 1610612766
		for team_id in range(1610612737, 1610612767):
			respond = requests.get('http://stats.nba.com/stats/teaminfocommon?LeagueID=00&SeasonType=Regular+Season&TeamID=%d&season=2015-16' % team_id).json()

			info_list_header = respond['resultSets'][0]['headers']
			info_list = respond['resultSets'][0]['rowSet']

			for info in info_list:
				for name in fieldnames:
					builder[name] = info[info_list_header.index(name)]

				writer.writerow(builder)

get_team_info()