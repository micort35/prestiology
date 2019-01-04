#!usr/bin/env/python
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
        self.min = round(((score.get('seconds_played'))/60), 2)
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
        query = 'SELECT id FROM league_roster WHERE name = %s;'
        cur.execute(query, (self.name,))
        player_id = cur.fetchone()
        #returns as tuple so index required
        return player_id[0]

    def update_season_measures(self, p_id, cur):
        #update games played
        ct_query = 'SELECT COUNT(id) FROM {}'
        cur.execute(sql.SQL(ct_query).format(sql.Identifier(self.name)))
        res = cur.fetchone()
        update_gp = 'UPDATE league_roster SET {} = %s WHERE id = %s'.format('gp')
        cur.execute(update_gp, (res[0], p_id))

        #update avgs and std devs
        avg_vars = ('min', 'fg', 'ft', 'tpm', 'pts', 'reb', 'ast', 'stl', 'blk', 'tov')
        sd_vars = [var + '_sd' for var in avg_vars]
        for avg, sd in zip(avg_vars, sd_vars):
            #avg
            avg_query = 'SELECT AVG({}) FROM "{}"'.format(avg, self.name)
            cur.execute(avg_query)
            res = (cur.fetchone())[0]
            if res is not None:
                res = round(res, 4)
            update_avg = 'UPDATE league_roster SET {} = %s WHERE id = %s'.format(avg)
            cur.execute(update_avg, (res, p_id))
            #stddev
            sd_query = 'SELECT STDDEV({}) FROM "{}"'.format(avg, self.name)
            cur.execute(sd_query)
            res = (cur.fetchone())[0]
            if res is not None:
                res = round(res, 4)
            update_sd = 'UPDATE league_roster SET {} = %s WHERE id = %s'.format(sd)
            cur.execute(update_sd, (res, p_id))

    def ins_log(self, p_id, cur):
        ins = 'INSERT INTO "%s"(id, date, min, fgm, fga, ftm, fta, tpm, pts, reb, ast, stl, blk, tov) \
        VALUES(\'%s\', \'%s\', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)' % (self.name,
        p_id, self.date, self.min, self.fgm, self.fga, self.ftm, self.fta,
        self.tpm, self.pts, self.reb, self.ast, self.stl, self.blk, self.tov)
        cur.execute(ins)
        #INSERT statement breaks with None values, use update for fields where possible
        update = 'UPDATE "{}" SET fg = %s, ft = %s WHERE date = \'{}\''.format(self.name, self.date)
        cur.execute(update, (self.fg, self.ft))
        Log.update_season_measures(self, p_id, cur)

    def add_player(self, cur):
        #add player to roster
        ins = 'INSERT INTO league_roster(name, team) VALUES(%s, %s);'
        cur.execute(ins, (self.name, self.team))
        #create game log table
        create = 'CREATE TABLE {}(\
                id UUID, date date, min decimal, fgm int, fga int, fg decimal, ftm int, fta int,\
                ft decimal, tpm int, pts int, reb int, ast int, stl int, blk int, tov int,\
                FOREIGN KEY(id) REFERENCES league_roster(id));'
        cur.execute(sql.SQL(create).format(sql.Identifier(self.name)))
        p_id = self.get_pid(cur)
        #add game to game log
        Log.ins_log(self, p_id, cur)