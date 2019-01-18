from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, BooleanField
from wtforms.validators import DataRequired

class TradeForm(FlaskForm):
    fg_wt = DecimalField('FG')
    ft_wt = DecimalField('FT')
    tpm_wt = DecimalField('TPM')
    pts_wt = DecimalField('PTS')
    reb_wt = DecimalField('REB')
    ast_wt = DecimalField('AST')
    stl_wt = DecimalField('STL')
    blk_wt = DecimalField('BLK')
    tov_wt = DecimalField('TOV')
    cst_wt = DecimalField('CST')
    act_wt = DecimalField('ACT')
    hea_wt = DecimalField('HEA')
    give = StringField(validators=[DataRequired()])
    receive = StringField(validators=[DataRequired()])
    submit = SubmitField('Analyze')