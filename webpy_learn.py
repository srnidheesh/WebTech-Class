#!/usr/bin/env python

import web
from web.wsgiserver import CherryPyWSGIServer
from passlib.hash import md5_crypt
from uuid import uuid4

CherryPyWSGIServer.ssl_certificate="ssl/server.crt"
CherryPyWSGIServer.ssl_private_key="ssl/server.key"

urls=(
		"/favicon.ico","Icon",
		"/","Index",
		"/register","Register",
		)


db=web.database(dbn="mysql",db="webpydb",user="webpy",pw="webpy")

app=web.application(urls,globals())
if web.config.get('_session') is None:
	session = web.session.Session(app, web.session.DiskStore('sessions'))
	web.config._session = session
else:
	session = web.config._session

def csrf_token():
	if not session.has_key("csrf_token"):
		session.csrf_token=uuid4().hex
	return session.csrf_token

def csrf_protected(fun):
	def decorated(*args,**kwargs):
		inp=web.input()
		if not (inp.has_key("csrf_token") and inp.csrf_token==session.pop("csrf_token",None)):
			raise web.HTTPError(
					"400 Bad request",
					{"content-type":"text/html"},
					"<h2>Cross site request forgery attempt (or stale browser form). <a href=''>Back to form</a>.<h2>")
		return fun(*args,**kwargs)
	return decorated

render=web.template.render("templates/",globals={"csrf_token":csrf_token});

class Icon:
	def GET(self):
		return

class Index:
	def GET(self):
		return render.login()

	@csrf_protected
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

	@csrf_protected
	def POST(self):
		inp=web.input()
		pwhash=md5_crypt.encrypt(inp.password)
		uid=db.insert("users",username=inp.username,password=pwhash)
		if uid:
			return render.registered(inp.username)
		else:
			return "Not registered"

if __name__=="__main__":
	app.run()
