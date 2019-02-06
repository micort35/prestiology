from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID, TEXT, INTEGER, NUMERIC, DATE
from flaskr import db

class LeagueRoster(db.Model):
    __tablename__ = 'league_roster'

    player_id = db.Column(UUID, primary_key=True, server_default=func.uuid_generate_v4())
    name = db.Column(TEXT)
    team = db.Column(TEXT)
    gp = db.Column(INTEGER)
    mins = db.Column(NUMERIC)
    mins_sd = db.Column(NUMERIC)
    fg = db.Column(NUMERIC)
    fg_sd = db.Column(NUMERIC)
    fga = db.Column(NUMERIC)
    fga_sd = db.Column(NUMERIC)
    ft = db.Column(NUMERIC)
    ft_sd = db.Column(NUMERIC)
    fta = db.Column(NUMERIC)
    fta_sd = db.Column(NUMERIC)
    tpm = db.Column(NUMERIC)
    tpm_sd = db.Column(NUMERIC)
    pts = db.Column(NUMERIC)
    pts_sd = db.Column(NUMERIC)
    reb = db.Column(NUMERIC)
    reb_sd = db.Column(NUMERIC)
    ast = db.Column(NUMERIC)
    ast_sd = db.Column(NUMERIC)
    stl = db.Column(NUMERIC)
    stl_sd = db.Column(NUMERIC)
    blk = db.Column(NUMERIC)
    blk_sd = db.Column(NUMERIC)
    tov = db.Column(NUMERIC)
    tov_sd = db.Column(NUMERIC)

    def __repr__(self):
        return '<Player {}>'.format(self.name)

    def get_stddevs():
        stddevs = {
            'fg': ((db.session.query(func.stddev(LeagueRoster.fg))).all())[0][0],
            'ft': ((db.session.query(func.stddev(LeagueRoster.ft))).all())[0][0],
            'tpm': ((db.session.query(func.stddev(LeagueRoster.tpm))).all())[0][0],
            'pts': ((db.session.query(func.stddev(LeagueRoster.pts))).all())[0][0],
            'reb': ((db.session.query(func.stddev(LeagueRoster.reb))).all())[0][0],
            'ast': ((db.session.query(func.stddev(LeagueRoster.ast))).all())[0][0],
            'stl': ((db.session.query(func.stddev(LeagueRoster.stl))).all())[0][0],
            'blk': ((db.session.query(func.stddev(LeagueRoster.blk))).all())[0][0],
            'tov': ((db.session.query(func.stddev(LeagueRoster.tov))).all())[0][0]
        }
        return stddevs

    def get_means():
        means = {
            'fg': ((db.session.query(func.avg(LeagueRoster.fg))).all())[0][0],
            'ft': ((db.session.query(func.avg(LeagueRoster.ft))).all())[0][0],
            'tpm': ((db.session.query(func.avg(LeagueRoster.tpm))).all())[0][0],
            'pts': ((db.session.query(func.avg(LeagueRoster.pts))).all())[0][0],
            'reb': ((db.session.query(func.avg(LeagueRoster.reb))).all())[0][0],
            'ast': ((db.session.query(func.avg(LeagueRoster.ast))).all())[0][0],
            'stl': ((db.session.query(func.avg(LeagueRoster.stl))).all())[0][0],
            'blk': ((db.session.query(func.avg(LeagueRoster.blk))).all())[0][0],
            'tov': ((db.session.query(func.avg(LeagueRoster.tov))).all())[0][0]
        }
        return means

    def get_zscores(player, stddevs, means):
        scores = {mean:((player.get(mean) - means.get(mean))/stddevs.get(mean)) for mean in means}
        return scores

    def wrap(row):
        player = {
          'name': row.name,
          'team': 'OKC', #placeholder until abbreviation function is written
          'gp': row.gp,
          'mins': round(row.mins, 2),
          'fg': round(row.fg, 2),
          'fga': round(row.fga, 2),
          'ft': round(row.ft, 2),
          'fta': round(row.fta, 2),
          'tpm': round(row.tpm, 2),
          'pts': round(row.pts, 2),
          'reb': round(row.reb, 2),
          'ast': round(row.ast, 2),
          'stl': round(row.stl, 2),
          'blk': round(row.blk, 2),
          'tov': round(row.tov, 2)
        }
        return player
    
    def evaluate(player, zscores, weights):
        player['value'] = 0
        zscores.update(tov = -zscores.get('tov'))
        for key, val in zscores.items():
            if key == 'fg':
                player['vfg'] = (round((val*weights.get('fg_wt')*player.get('fga')/5), 2))
                player.update(value = player.get('value') + round((val*weights.get('fg_wt')), 2))
            elif key == 'ft':
                player['vft'] = (round((val*weights.get('ft_wt')*player.get('fta')/2), 2))
                player.update(value = player.get('value') + round((val*weights.get('ft_wt')), 2))
            else:
                player['v'+key] = round(val*weights.get(key+'_wt'), 2)
                player.update(value = player.get('value') + round((val*weights.get(key+'_wt')), 2))

    def delta(give, receive):
        delta = give.copy()
        for key in delta.keys():
            if key == 'name':
                delta[key] = u'Δ'
            elif (key == 'team') or (key == 'gp'):
                delta[key] = ""
            else:
                delta[key] = (give.get(key) - receive.get(key))
        return delta

class GameLogs(db.Model):
    __tablename__ = 'game_logs'

    player_id = db.Column(UUID, db.ForeignKey('league_roster.player_id'), primary_key=True)
    name = db.Column(TEXT, index=True)
    date = db.Column(DATE, primary_key=True)
    mins = db.Column(NUMERIC)
    fgm = db.Column(INTEGER)
    fga= db.Column(INTEGER)
    fg = db.Column(NUMERIC)
    ftm = db.Column(INTEGER)
    fta = db.Column(INTEGER)
    ft = db.Column(NUMERIC)
    tpm = db.Column(INTEGER)
    pts = db.Column(INTEGER)
    reb = db.Column(INTEGER)
    ast = db.Column(INTEGER)
    stl = db.Column(INTEGER)
    blk = db.Column(INTEGER)
    tov = db.Column(INTEGER)

    def __repr__(self):
        return '<Player {}, Date {}>'.format(self.name, self.date)