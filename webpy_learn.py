#!/usr/bin/env python

import web
import sys

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

class Icon:
	def GET(self):
		return

class Index:
	def GET(self):
		return render.login()

	def POST(self):
		inp=web.input()
		myvars=dict(un=inp.username,pw=inp.password)
		user=db.select("users",where="username=$un and password=$pw", vars=myvars)
		if user:
			return render.valid(inp.username)
		else:
			return render.invalid(inp.username)

class Register:
	def GET(self):
		return render.register()

	def POST(self):
		inp=web.input()
		uid=db.insert("users",username=inp.username,password=inp.password)
		if uid:
			return "Registered"
		else:
			return "Not registered"

if __name__=="__main__":
	app=web.application(urls,globals())
	app.run()
