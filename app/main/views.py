#! /usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Jack Bai'

from datetime import datetime
from flask import render_template, abort, session, redirect, url_for, current_app, flash
from .. import db
from ..models import User
from ..emails import send_email
from . import main
from .forms import NameForm

@main.route('/', methods=['GET', 'POST'])
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
            if current_app.config['MYBLOG_ADMIN']:
                send_email(current_app.config['MYBLOG_ADMIN'], 'New User', 
                    'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('.index'))
    return render_template('index.html', form=form, name=session.get('name'), 
        known=session.get('known', False), current_time=datetime.utcnow())


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)
