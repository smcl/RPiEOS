import cherrypy
from cherrypy.lib import static
from datetime import datetime
import json
import os
import sys
import sqlite3
from mako.template import Template
from mako.lookup import TemplateLookup

class AppSkeleton:
	def __init__(self, filenames):
		self.AppName = "AppSkeleton"
		
	@cherrypy.expose
	def index(self, **args):
		db = self.initDB()
		cur = db.cursor()    
		cur.execute('SELECT * from Widgets')
		widgets = cur.fetchall()

		return self.dynamic("index.mako", model=widgets)

	@cherrypy.expose
	def about(self, **args):
		return self.dynamic("about.mako")

	@cherrypy.expose
	def datetime(self, **args):
		return json.dumps({
			"utcnow" : str(datetime.utcnow()),
			"now" : str(datetime.now())
		})

	@cherrypy.expose
	def static(self,filename):
		return static.serve_file(os.path.join(current_dir,'static',filename))
	
	def dynamic(self, pageName, model=object()):
		header = self.makoLookup.get_template("boilerplate/header.mako")
		body = self.makoLookup.get_template(os.path.join("pages", pageName))
		footer = self.makoLookup.get_template("boilerplate/footer.mako")

		return "\n".join([
			header.render_unicode(app=self, model=model),
			body.render_unicode(app=self, model=model), 
			footer.render_unicode(app=self, model=model),
		])

	def initDB(self, create=False):
		appDB = os.path.join(current_dir, "db", "app.db")
		appSQL = os.path.join(current_dir, "db", "app.sql")

		if not os.path.isfile(appDB):
			# ./db/app.db doesn't exist, initialise from ./db/app.sql
			# note: this is nasty
			os.system("sqlite3 {0} < {1}".format(appDB, appSQL))

		try:
			return sqlite3.connect(appDB)
		except:
			return None


def blank_error_page():
    cherrypy.response.status = 500
    cherrypy.response.body = "500"

if __name__ == "__main__":
	current_dir = os.path.dirname(os.path.abspath(__file__))

	if len(sys.argv) > 1:
		port = int(sys.argv[1])
	else:
		port = 8080
	
	app = AppSkeleton(sys.argv[1:])
	app.makoLookup = TemplateLookup(directories=['./ui'], module_directory='./.ui-modules', input_encoding='utf-8', output_encoding='utf-8', )

	cherrypy.config.update( {
		'server.socket_host':"0.0.0.0", 
		'server.socket_port': port,
		'request.error_response': blank_error_page,
		'error_page.404': "./static/404",
		"tools.proxy.on": True,
		"tools.proxy.local": "X-Forwarded-Host",
		"tools.proxy.remote": "X-Forwarded-For",
	})
	cherrypy.quickstart(app)			