# -*- coding:utf-8 -*-

import sys
sys.path.append('libs')

from bottle import route, post, request, redirect, jinja2_template as template, response

import app.models.infra
model = app.models.infra.Infra()




#overview page

@route('/')
def index():
    result = model.load()
    return template('index', result = result)


@route('/reg_api')
def reg_api():
    host = {}
    host["hostname"] = request.query.getall('hostname')
    host["ipaddress"] = request.query.getall('ipaddress')

    model.reg(host)
    return

@route('/get_hostname')
def get_hostname():
    ipaddress = request.query.get('ipaddress')
    host = model.get_hostname(ipaddress)

    return '%s' % host["hostname"]


@route('/edit/<id>')
def edit_host(id):
    result = model.edit(id)
    return template('edit', i = result)


@post('/done')
def done():
    post_data = {}
    post_data["hostname"] = request.forms.get('hostname')
    post_data["ipaddress"] = request.forms.get('ipaddress')
    post_data["comment"] = request.forms.get('comment')
    post_data["id"] = request.forms.get('id')
    post_data["del"] = request.forms.get('del')

    model.done(post_data)

    redirect("/")

@route('/reg_dns/<id>')
def reg_dns(id):
    model.reg_dns(id)
    redirect("/")


#http://10.1.0.106/hello?name=kazu&test=1
@route('/hello')
def hello():
    name = None
    names = request.query.getall('name')
    if names:
        name = names[0]
    return '<h1>Hello %s</h1>' % name
