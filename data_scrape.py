import pandas as pd
import time
import nba_api as nbp
from nba_api.stats.static import players
from nba_api.stats.endpoints import leaguedashplayerstats, playerdashptshots

league_stats = leaguedashplayerstats.LeagueDashPlayerStats().get_data_frames()[0]

#72 game season
league_stats = league_stats.loc[league_stats['GP'] > 50.4] #70% of games
league_stats = league_stats.loc[league_stats['FG3M'] >= 72] #70% of games

pids = league_stats['PLAYER_ID'].to_numpy()
tids = league_stats['TEAM_ID'].to_numpy()
names = league_stats['PLAYER_NAME'].to_numpy()
player_list = [list(i) for i in zip(pids, tids, names)]

shooting_dict = {}
for p_id, t_id, name in player_list:
    shooting_df = playerdashptshots.PlayerDashPtShots(t_id, p_id).get_data_frames()[4]
    c_make = shooting_df['FG3M'][0] + shooting_df['FG3M'][1]
    c_att = shooting_df['FG3A'][0] + shooting_df['FG3A'][1]
    o_make = shooting_df['FG3M'][2] + shooting_df['FG3M'][3]
    o_att = shooting_df['FG3A'][2] + shooting_df['FG3A'][3]
    shooting_dict[name] = [c_make, c_att, c_make/c_att, o_make, o_att, o_make/o_att]
    time.sleep(.600)
    
full_shooting_df = pd.DataFrame.from_dict(shooting_dict).transpose()
full_shooting_df.columns = ["C FG3M", 'C FG3A', 'C FG3%', "O FG3M", 'O FG3A', 'O FG3%']

full_shooting_df.to_csv("contested_shooting_data.csv")