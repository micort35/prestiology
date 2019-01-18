from flask import render_template, request
from flaskr import app
from flaskr.forms import TradeForm
from flaskr.models import LeagueRoster, GameLogs

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render-template('500.html'), 500

@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    #get form and validate    
    form = TradeForm()
    give = receive = delta = None
    if form.validate_on_submit():
        #add all weights to dict
        cat_weights = {}
        for fieldname, value in form.data.items():
            if fieldname is 'give':
                break
            cat_weights[fieldname] = value

        #get players, stat differentials
        stddevs = LeagueRoster.get_stddevs()
        means = LeagueRoster.get_means()

        give = LeagueRoster.wrap(LeagueRoster.query.filter_by(name=request.form['give']).first())
        zscores = LeagueRoster.get_zscores(give, stddevs, means)
        LeagueRoster.evaluate(give, zscores, cat_weights)

        receive = LeagueRoster.wrap(LeagueRoster.query.filter_by(name=request.form['receive']).first())
        zscores = LeagueRoster.get_zscores(receive, stddevs, means)
        LeagueRoster.evaluate(receive, zscores, cat_weights)

        delta = LeagueRoster.delta(give, receive)
        
    return render_template('index.html', form=form, give=give, receive=receive, delta=delta)