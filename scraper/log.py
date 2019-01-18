import statistics
from datetime import date
import psycopg2
from psycopg2 import sql

class Log:

    def __init__(self, score, gameday):
        #gather player data
        self.name = score.get('name')
        self.team = (score.get('team')).name
        self.date = gameday
        self.mins = round(((score.get('seconds_played'))/60), 2)
        self.fgm = score.get('made_field_goals')
        self.fga = score.get('attempted_field_goals')
        if self.fga is 0:
            self.fg = None
        else:
            self.fg = round((self.fgm/self.fga), 4)
        self.ftm = score.get('made_free_throws')
        self.fta = score.get('attempted_free_throws')
        if self.fta is 0:
            self.ft = None
        else:
            self.ft = round((self.ftm/self.fta), 4)
        self.tpm = score.get('made_three_point_field_goals')
        self.pts = ((self.fgm - self.tpm)*2) + (self.tpm*3) + (self.ftm*1)
        self.reb = score.get('offensive_rebounds') + score.get('defensive_rebounds')
        self.ast = score.get('assists')
        self.stl = score.get('steals')
        self.blk = score.get('blocks')
        self.tov = score.get('turnovers')

    def exists(self, cur):
        #check if return is empty for given player
        SQL = 'SELECT * FROM league_roster WHERE name = %s;'
        cur.execute(SQL, (self.name,))
        ans = cur.fetchone()
        if ans is None:
            return 0
        else:
            return 1

    def get_pid(self, cur):
        query = 'SELECT player_id FROM league_roster WHERE name = %s;'
        cur.execute(query, (self.name,))
        player_id = cur.fetchone()
        return player_id[0]

    def update_season_measures(self, p_id, cur):
        #update games played
        ct_query = 'SELECT COUNT(player_id) FROM game_logs WHERE player_id = %s'
        cur.execute(ct_query, (p_id,))
        res = (cur.fetchone())[0]
        update_gp = 'UPDATE league_roster SET gp = %s WHERE player_id = %s'
        cur.execute(update_gp, (res, p_id))

        #update avgs and std devs
        avg_vars = ('mins', 'fg', 'fga', 'ft', 'fta', 'tpm', 'pts', 'reb', 'ast', 'stl', 'blk', 'tov')
        sd_vars = [var + '_sd' for var in avg_vars]
        for avg, sd in zip(avg_vars, sd_vars):
            #avg
            avg_query = "SELECT AVG({}) FROM game_logs WHERE player_id = '{}'".format(avg, p_id)
            cur.execute(avg_query)
            res = (cur.fetchone())[0]
            if res is not None:
                res = round(res, 4)
            update_avg = "UPDATE league_roster SET {} = %s WHERE player_id = '{}'".format(avg, p_id)
            cur.execute(update_avg, (res,))
            #stddev
            sd_query = "SELECT STDDEV({}) FROM game_logs WHERE player_id = '{}'".format(avg, p_id)
            cur.execute(sd_query)
            res = (cur.fetchone())[0]
            if res is not None:
                res = round(res, 4)
            update_sd = "UPDATE league_roster SET {} = %s WHERE player_id = '{}'".format(sd, p_id)
            cur.execute(update_sd, (res,))

    def ins_log(self, p_id, cur):
        #Add game to logs
        ins = 'INSERT INTO game_logs(player_id, name, date, mins, fgm, fga, ftm, fta, tpm, pts, reb, ast, stl, blk, tov)\
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        ins_args = (p_id, self.name, self.date, self.mins, self.fgm, self.fga, self.ftm, self.fta, self.tpm, 
        self.pts, self.reb, self.ast, self.stl, self.blk, self.tov)
        cur.execute(ins, ins_args)

        #INSERT statement breaks with None values, use update for fields where possible
        update = 'UPDATE game_logs SET fg = %s, ft = %s WHERE date = %s AND name = %s'
        cur.execute(update, (self.fg, self.ft, self.date, self.name))
        Log.update_season_measures(self, p_id, cur)

    def add_player(self, cur):
        #add player to roster
        ins = 'INSERT INTO league_roster(name, team) VALUES(%s, %s);'
        cur.execute(ins, (self.name, self.team))

        #add game to game log
        p_id = self.get_pid(cur)
        Log.ins_log(self, p_id, cur)