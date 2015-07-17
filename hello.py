#! /usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Baidong'

import os
from datetime import datetime
from flask import Flask, render_template, session, request, make_response, redirect, url_for, flash
from flask.ext.script import Manager, Shell
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.mail import Mail, Message
from threading import Thread
# from sqlalchemy import create_engine


app = Flask(__name__)
app.config['SECRET_KEY'] = 'CaNYoUSeEMeNoW'
# this method to create "SQLAlchemy object" by using "mysql-connector-python" module
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/test_flask'
# 为 True 时,每次请求结束后都会自动提交数据库中的变动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MYBLOG_MAIL_SUBJECT_PREFIX'] = '[MYBLOG INFO]'
app.config['MYBLOG_MAIL_SENDER'] = os.environ.get('MAIL_USERNAME')
app.config['MYBLOG_ADMIN'] = os.environ.get('MYBLOG_ADMIN') # admin of the blog ,mail reciever


manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
# use create_engine() to create "engine object"
# engine = create_engine('mysql+mysqlconnector://root:11235813@localhost:3306/test_flask')
migrate = Migrate(app, db)
mail = Mail(app)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


class NameForm(Form):
    name = StringField('What\'s your name?', validators=[Required()])
    submit = SubmitField('Submit')


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_mail(to, subject, template, **kw):
    msg = Message(app.config['MYBLOG_MAIL_SUBJECT_PREFIX'] + ' ' + subject, 
        sender=app.config['MYBLOG_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kw)
    msg.html = render_template(template + '.html', **kw)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


def make_shell_context():
    return dict(app=app, db=db, Role=Role, User=User)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('You have changed your name.')
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            if app.config['MYBLOG_ADMIN']:
                send_mail(app.config['MYBLOG_ADMIN'], 'New User', 
                    'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), 
        known=session.get('known', False), current_time=datetime.utcnow())


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

if __name__ == '__main__':
    # db.create_all()
    manager.run()
