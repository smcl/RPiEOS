import cherrypy
from cherrypy.lib import static
from cherrypy.lib.static import serve_file
from datetime import datetime
import json
import os
import sys
import sqlite3
from mako.template import Template
from mako.lookup import TemplateLookup
from threading import Thread
from threading import Event

#import RPi.GPIO as GPIO
import time

import signal


class PictureTaker(Thread):
    def __init__(self, event, seconds):
            Thread.__init__(self)
            self.stopped = event
            self.seconds = seconds
            self.counter = 0
            
    def run(self):
            while not self.stopped.wait(self.seconds):
                    self.takePic()


    def takePic(self):
            #GPIO.setmode(GPIO.BOARD)
            #GPIO.setup(12, GPIO.OUT)
            
            #GPIO.output(12, GPIO.HIGH)
            #time.sleep(0.1)
            #GPIO.output(12, GPIO.LOW)
            self.counter += 1
            print "Pic!!" # TODO: fire the GPIO event
            
    def updateSeconds(self, seconds):
    	    self.seconds = seconds

class RPiEOS:
	def __init__(self, filenames, picThread, stopFlag):
		self.AppName = "RPiEOS"
                self.picThread = picThread
                self.stopFlag = stopFlag
                self.picThread.start()
		
	@cherrypy.expose
	def index(self, **args):
		db = self.initDB()
		cur = db.cursor()    
		cur.execute('SELECT * from Widgets')
		widgets = cur.fetchall()

		return self.dynamic("index", model=widgets)

	@cherrypy.expose
	def about(self, **args):
		return self.dynamic("about")

	@cherrypy.expose
	def snap(self):
                self.picThread.takePic()
                raise cherrypy.HTTPRedirect("/")

        @cherrypy.expose
        def updateTimer(self, seconds):
                self.picThread.updateSeconds(int(seconds))

                raise cherrypy.HTTPRedirect("/")

        # for debugging
        @cherrypy.expose
        def stopTimer(self):
                self.stopFlag.set()
        
	@cherrypy.expose
	def static(self,filename):
		return static.serve_file(os.path.join(current_dir,'static',filename))
	
	def dynamic(self, pageName, model=object()):
		header = self.makoLookup.get_template("boilerplate/header.mako")
		body = self.makoLookup.get_template(os.path.join("pages", pageName + ".mako"))
		footer = self.makoLookup.get_template("boilerplate/footer.mako")

		return "\n".join([
			header.render_unicode(app=self, page=pageName, model=model),
			body.render_unicode(app=self, page=pageName, model=model), 
			footer.render_unicode(app=self, page=pageName, model=model),
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


def stopit():
        app.picThread.stopped.set()
stopit.priority = 10

   
if __name__ == "__main__":
	current_dir = os.path.dirname(os.path.abspath(__file__))

	if len(sys.argv) > 1:
		port = int(sys.argv[1])
	else:
		port = 8080

        # start the picture taking thread, default = 10 secs
        seconds = 10
        stopFlag = Event()
        thread = PictureTaker(stopFlag, seconds)

        # start the app thread
	app = RPiEOS(sys.argv[1:], thread, stopFlag)
        app.current_dir = current_dir
	app.makoLookup = TemplateLookup(directories=['./ui'], module_directory='./.ui-modules', input_encoding='utf-8', output_encoding='utf-8', )

	cherrypy.config.update( {
		'server.socket_host':"0.0.0.0", 
		'server.socket_port': port,
		'request.error_response': blank_error_page,
		'error_page.404': "./static/404",
		"tools.proxy.on": True,
		"tools.proxy.local": "Host",
		"tools.proxy.remote": "X-Forwarded-For",
	})

        # stop the pic timer
        cherrypy.engine.subscribe('stop', stopit)
        
	cherrypy.quickstart(app)			
