import ConfigParser

class config():
	def __init__(self):
		self.config = ConfigParser.ConfigParser()
		self.config.read("/path/to/config.cfg")

		self._sections = [x for x in self.config.sections()]
		print self._sections
		
	def getDatabaseConfig(self):
		user, password, database = [self.config.get(self._sections[0], x) for x in self.config.options(self._sections[0])]
		databaseConfigList = [user, password, database]
		return databaseConfigList

	def getSourcesList(self):
		sourcesList = [self.config.get(self._sections[1], x) for x in self.config.options(self._sections[1])]
		return sourcesList