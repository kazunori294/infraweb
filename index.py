# -*- coding: utf-8 -*-

import sys
sys.path.append('libs')

from bottle import route, static_file, default_app, run
from app.controllers import *

@route('/stat/<filepath:path>')
def server_static(filepath):
	return static_file(filepath, root='./stat/')

run(host='0.0.0.0', port=80, debug=True, reloader=True)

#if you use gunicorn
#app = default_app()
