from flask import Flask
from werkzeug.utils import *
from flask_restplus import Api

class Server():
	def __init__(self, ):
		self.app = Flask(__name__)
		self.api = Api(self.app, version='1.0',title = 'Lenovo Laptop API',description='A lenovo laptop API',doc='/docs')

	def run(self,):
		self.app.run()

server = Server()