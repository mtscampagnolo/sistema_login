from bottle import Bottle
from bottle.ext import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import bottle_session


Base = declarative_base()
engine = create_engine('sqlite:///database.db', echo=True)


app = Bottle()
plugin = sqlalchemy.Plugin(
	engine,
	Base.metadata,
	keyword='db',
	create=True,
	commit=True,
	use_kwargs=False
)
plugin_session = bottle_session.SessionPlugin(cookie_lifetime=300)
app.install(plugin)
app.install(plugin_session)
from app.controllers import default
from app.models import default

