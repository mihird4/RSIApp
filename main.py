from flask import Flask, render_template, jsonify, json, request, send_from_directory, redirect, url_for
from flask_wtf import Form
from wtforms import StringField, PasswordField, RadioField, SubmitField
from wtforms.validators import InputRequired
from getrsimod import getRSI
from config import *
from pathlib import Path


app = Flask(__name__)
app.config.from_object('config.ProdConfig')
Path(app.config['DOWNLOAD']).mkdir(parents=True, exist_ok=True)


class DeviceInfo(Form):
    mgmtip = StringField('Hostname', validators=[InputRequired()])
    user = StringField('Username', validators=[InputRequired()])
    passwd = PasswordField('Password', validators=[InputRequired()])
    downloads = RadioField('Download', choices=[(
        'RSI', 'RSI'), ('varlog', 'VARLOG'), ('both', 'RSI+VARLOG')])
    btn = SubmitField('Collect Support Information')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = DeviceInfo()
    form.validate_on_submit()
    return render_template('app.html', form=form)


@app.route('/_getrsi', methods=['GET', 'POST'])
def _getrsi():
    mgmtip = request.get_json()['mgmtipid']
    user = request.get_json()['userid']
    password = request.get_json()['passwordid']
    rsi = request.get_json()['rsi']
    varlog = request.get_json()['varlog']
    both = request.get_json()['both']
    try:
        results = getRSI(mgmtip, user, password,
                         app.config['DOWNLOAD'], rsi, varlog, both)
        if results[1]:
            return jsonify({'successmsg': 'Success!', 'filename': results[0], 'coredump': 'True', 'rpcreply': results[2]})
        else:
            return jsonify({'successmsg': 'Success!', 'filename': results[0]})

    except Exception as err:
        return jsonify({'errormsg': str(err)})


@app.route('/_sendf/<path:fname>', methods=['GET', 'POST'])
def _sendf(fname):
    print(fname)
    return send_from_directory(app.config['DOWNLOAD'], fname, as_attachment=True)
