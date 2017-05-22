import csv

# PAST 12 SEASONS
seasons = ['2004-05', '2005-06', '2006-07', '2007-08', '2008-09', '2009-10', '2010-11', '2011-12', '2012-13', '2013-14', '2014-15', '2015-16']

# NBA TEAM NAME LIST
team_name_list = ['76ers', 'Bucks', 'Bulls', 'Cavaliers', 'Celtics', 'Clippers', 'Grizzlies', 'Hawks', 'Heat', 'Hornets', 'Jazz', 'Kings', 'Knicks', 'Lakers', 'Magic', 'Mavericks', 'Nets', 'Nuggets', 'Pacers', 'Pelicans', 'Pistons', 'Raptors', 'Rockets', 'Spurs', 'Suns', 'Thunder', 'Timberwolves', 'TrailBlazers', 'Warriors', 'Wizards']

team_id = {}        # {'TEAM_ID': 'TEAM_NAME'}
id_team = {}        # {'TEAM_NAME': 'TEAM_ID'}
player_list = []    # PLAYER ID LIST
#player_name = {}   # {'PLAYER_NAME': 'PLAYER_ID'}
team_list = []      # TEAM ID LIST
TER = 0
per = []            # INDIVIDULE PLAYER PER LIST



def get_player_list(team_name, season_year):
    ''' GET PLAYER LIST AND PLAYER NAME DICTIONARY'''
    PLAYER_LIST = './nba_data/player_list/%s_player_list.csv' % team_name
    with open(PLAYER_LIST, 'r') as f:
    	for line in f.readlines():
    		player = line.strip().split(',')
    		if player[-1] != 'PLAYER_ID' and player[-1] not in player_list and player[0] == season_year:
    			player_list.append(player[-1])
    			#player_name[player[-1]] = player[2]    # GENERAGE PLAYER NAME LIST

def get_team_list():
    '''  GET TEAM ID DICTIONARY, ID TEAM DICTIONARY AND TEAM ID LIST'''
	TEAM_LIST = './nba_data/team/team_id.csv'
	with open(TEAM_LIST, 'r') as f:
		for line in f.readlines():
			team = line.strip().split(',')
			if team[0] != 'TEAM_ID':
				team_list.append(team[0])
				team_id[team[3]] = team[0]
				id_team[team[0]] = team[3]

def get_ter(team_name, season_year):
    ''' GET TEAM EFFICENCY RATING '''
    PLAYER_STATS = './nba_data/player_stats_by_year/%s_player_stats_by_year.csv' % season_year
    TEAM_STATS =  './nba_data/team/team_stats.csv'
    TEAM_ADVANCED_STATS = './nba_data/team_advanced_stats/get_%s_team_advanced_data.csv' % season_year

    MIN = 0
    FGM = 0
    FGA = 0
    FG3M = 0
    FTM = 0
    FTA = 0
    AST = 0
    STL = 0
    BLK = 0
    DREB_PCT = 0
    OREB = 0	
    REB = 0
    PF = 0
    TOV = 0
    TEAM_MIN = 0
    TEAM_GP = 0
    TEAM_AST = 0
    TEAM_FGM = 0
    TEAM_FGA = 0
    TEAM_PACE = 0
    TER = 0
    LG_FGM = 0
    LG_FGA = 0
    LG_FTM = 0
    LG_FTA = 0
    LG_AST = 0
    LG_PTS = 0
    LG_OREB = 0
    LG_REB = 0
    LG_TOV = 0
    LG_PF = 0
    TOTAL_LG_PACE = 0
    LG_PACE = 0

    # GENERATE LISTS AND DICTIONARIES SET IN THE BEGGINING
    get_player_list(team_name, season_year)
    get_team_list()
    
    # CALCULATE TEAM BASIC STATS
    with open(TEAM_STATS, 'r') as f:
    	for line in f.readlines():
    		team_stats = line.strip().split(',')
    		if team_stats[0] == 'SEASON':
    			team_stats_header = team_stats
    		elif team_stats[0] == season_year and team_stats[-1] == team_id[team_name]:
    			TEAM_GP = float(team_stats[team_stats_header.index('GP')])
    			TEAM_AST = float(team_stats[team_stats_header.index('AST')])
    			TEAM_FGM = float(team_stats[team_stats_header.index('FGM')])
    			TEAM_FGA = float(team_stats[team_stats_header.index('FGA')])
    
    # CALCULATE LEAGUE STATS
    for team in team_list:
    	with open(TEAM_STATS, 'r') as f:
    		for line in f.readlines():
    			team_stats = line.strip().split(',')
    			if team_stats[0] == 'SEASON':
    				team_stats_header = team_stats
    			elif team_stats[0] == season_year and team_stats[-1] == team:
    				LG_FGM += float(team_stats[team_stats_header.index('FGM')])
    				LG_FGA += float(team_stats[team_stats_header.index('FGA')])
    				LG_FTM += float(team_stats[team_stats_header.index('FTM')])
    				LG_FTA += float(team_stats[team_stats_header.index('FTA')])
    				LG_AST += float(team_stats[team_stats_header.index('AST')])
    				LG_PTS += float(team_stats[team_stats_header.index('PTS')])
    				LG_OREB += float(team_stats[team_stats_header.index('OREB')])
    				LG_REB += float(team_stats[team_stats_header.index('REB')])
    				LG_TOV += float(team_stats[team_stats_header.index('TOV')])
    				LG_PF += float(team_stats[team_stats_header.index('PF')])	
    	
    # CALCULATE TEAM PACE AND LEAGUE PACE
    with open(TEAM_ADVANCED_STATS, 'r') as f:
    	for line in f.readlines():
    		team_advanced_stats = line.strip().split(',')
    		if team_advanced_stats[0] == season_year and team_advanced_stats[-1] == team_id[team_name]:
    			TEAM_PACE = float(team_advanced_stats[-3])

    for team in team_list:
    	with open(TEAM_ADVANCED_STATS, 'r') as f:
    		for line in f.readlines():
    			team_advanced_stats = line.strip().split(',')
    			if team_advanced_stats[0] == season_year and team_advanced_stats[-1] == team:
    				TOTAL_LG_PACE += float(team_advanced_stats[-3])

    LG_PACE = TOTAL_LG_PACE / len(team_list)
    factor = (2/3) - (0.5 * (LG_AST /LG_FGM)) / (2 * (LG_FGM / LG_FTM))
    VOP = LG_PTS / (LG_FGA - LG_OREB + LG_TOV + 0.44 * LG_FTA)
    DREB_PCT = (LG_REB - LG_OREB) / LG_REB
    PACE_ADJUSTMENT = LG_PACE / TEAM_PACE

    # GET PLAYER STATS TO CALCULATE PER
    for player in player_list:
    	with open(PLAYER_STATS, 'r') as f:
    		for line in f.readlines():
    			player_stats = line.strip().split(',')
    			if player_stats[0] == 'SEASON_ID':
    				player_stats_header = player_stats
    			elif player_stats[0] == season_year:
    				if player_stats[-1] == player:
    					MIN = float(player_stats[player_stats_header.index('MIN')])
    					FGM = float(player_stats[player_stats_header.index('FGM')])
    					FGA = float(player_stats[player_stats_header.index('FGA')])
    					FG3M = float(player_stats[player_stats_header.index('FG3M')])
    					FTM = float(player_stats[player_stats_header.index('FTM')])
    					FTA = float(player_stats[player_stats_header.index('FTA')])
    					AST = float(player_stats[player_stats_header.index('AST')])
    					STL = float(player_stats[player_stats_header.index('STL')])
    					BLK = float(player_stats[player_stats_header.index('BLK')])
    					OREB = float(player_stats[player_stats_header.index('OREB')])
    					REB = float(player_stats[player_stats_header.index('REB')])
    					PF = float(player_stats[player_stats_header.index('PF')])
    					TOV = float(player_stats[player_stats_header.index('TOV')])
    					TEAM_MIN += MIN

    	uPER = (1 / MIN) * (FG3M + (3/2) * AST + (2 - factor * (TEAM_AST / TEAM_FGM)) * FGM + (FTM * 0.5 * (1 + (1- (TEAM_AST / TEAM_FGM)) + (2/3) * (TEAM_AST / TEAM_FGM))) - VOP * TOV - VOP * DREB_PCT * (FGA - FGM) - VOP * 0.44 * (0.44 + (0.56 * DREB_PCT)) + VOP * (1 - DREB_PCT) * (REB - OREB) + VOP * DREB_PCT * OREB + VOP * STL + VOP * DREB_PCT * BLK - PF * ((LG_FTM / LG_PF) - 0.44 * (LG_FTA / LG_PF) * VOP))

    	aPER = PACE_ADJUSTMENT * uPER    	
    	per.append(aPER * MIN)

    # THERE IS A BUG. IN SOME TEAMS' STATS, THERE WILL BE TWO SAME PERS BELONGS TO ONE PERSON. THE REASON IS THAT THERE IS A PLAYER DIDN'T
    # PLAY AT ALL IN THAT SEASON BUT THAT PLAYER EXISTS IN PLAYER ID LIST.
    # ELIMINATE DUPLICATED DATA
    for i in range(0, len(per)):
    	m = i + 1
    	if m == len(per):
    		m = 0
    	if per[i] != per[m]:
    		TER += per[i]
    		
    TER = TER / TEAM_MIN
    return TER


# OUTPUT
TEAM_STATS = './nba_data/team/team_stats.csv'
with open('all_ters.csv', 'w') as f:
	fieldnames = ['SEASON_ID', 'TEAM_NAME', 'TER', 'W_PCT']
	writer = csv.DictWriter(f, fieldnames=fieldnames)
	writer.writeheader()
	builder = {}

	for season in seasons:
		for team in team_name_list:
			ters = get_ter(team, season)
			builder['SEASON_ID'] = season
			builder['TEAM_NAME'] = team
			builder['TER'] = ters

			with open(TEAM_STATS, 'r') as f:
				for line in f.readlines():
					team_stats = line.strip().split(',')
					if team_stats[-1] == team_id[team] and team_stats[0] == season:
						builder['W_PCT'] = team_stats[5]
			writer.writerow(builder)
			team_list = []
			player_list = []
			per = []
			print(team, season, ters)