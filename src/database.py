import psycopg2 as psql
from psycopg2 import sql
from psycopg2.extras import execute_batch

from config import config

class database():
	def __init__(self):
		c = config()
		self._databaseConf = c.getDatabaseConfig()
		self._sources = c.getSourcesList()

	def connect(self):
		try:
			self._connection = psql.connect(dbname=self._databaseConf[2], user=self._databaseConf[0], password=self._databaseConf[1])
			self._connection.set_session(autocommit=True)
			self._cursor = self._connection.cursor()
		except psql.DatabaseError as e:
			print e

	def cursor(self):
		return self._cursor

	def sources(self):
		return self._sources
		
	def submit(self, d):
	    for k in d.keys():
		cmd = sql.SQL("insert into {} values(%s, %s, %s, %s, %s, %s, %s)").format(sql.Identifier(k.lower()))
		try:
		    execute_batch(self._cursor, cmd, d[k])
		except psql.DatabaseError as e:
		    print e

	def tables(self, d):
		for key in d.keys():
			cmd = sql.SQL("SELECT to_regclass('{}')").format(sql.Identifier(key.lower()))
			self._cursor.execute(cmd)
			ret = self._cursor.fetchone()[0]

			if ret is None:
				try:
					ctable = sql.SQL("CREATE TABLE {} (timestamp int not null, value varchar(150), host varchar(150), ip varchar(150), tn float8, tmax float8, dmax float8)").format(sql.Identifier(key.lower()))
					self._cursor.execute(ctable)
				except psql.DatabaseError as e:
					raise e
			else:
				pass

	def __del__(self):
		self._connection.close()
		self._cursor = None