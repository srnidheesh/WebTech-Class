#!/usr/bin/env python

import web
import sys
from web.wsgiserver import CherryPyWSGIServer
from passlib.hash import md5_crypt

urls=(
		"/favicon.ico","Icon",
		"/","Index",
		"/register","Register",
		)

render=web.template.render("templates/");
try:
	db=web.database(dbn="mysql",db="webpydb",user="webpy",pw="webpy")
except:
	print "Unable to connect to database"
	sys.exit()

CherryPyWSGIServer.ssl_certificate="ssl/server.crt"
CherryPyWSGIServer.ssl_private_key="ssl/server.key"

class Icon:
	def GET(self):
		return

class Index:
	def GET(self):
		return render.login()

	def POST(self):
		inp=web.input()
		myvars=dict(un=inp.username)
		users=db.select("users",where="username=$un", vars=myvars)
		for user in users:
			if md5_crypt.verify(inp.password,user.password):
				return render.valid(inp.username)
		else:
			return render.invalid(inp.username)

class Register:
	def GET(self):
		return render.register()

	def POST(self):
		inp=web.input()
		pwhash=md5_crypt.encrypt(inp.password)
		uid=db.insert("users",username=inp.username,password=pwhash)
		if uid:
			return render.registered(inp.username)
		else:
			return "Not registered"

if __name__=="__main__":
	app=web.application(urls,globals())
	app.run()
