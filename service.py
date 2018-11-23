import logging, time, socket

from src.database import database
from src.parser import parser
from daemon import runner

class App():
	def __init__(self):
		self.stdin_path = '/dev/null'
		self.stdout_path = '/dev/tty'
		self.stderr_path = '/dev/tty'
		self.pidfile_path = '/var/run/daemon.pid'
		self.pidfile_timeout = 5

	def data(self, socket):
		self.d = {}
		p = parser()
		s1 = p.recvAll(socket, 4096)
		self.d = p.parse(s1)

	def run(self):
		db = database()
		db.connect()
		cursor = db.cursor()

		while True:
			sources = db.sources()

			for source in sources:
				host, port = source.split(':')
				logger.info('Opening socket for host %s and port %s' % (host, port))

				sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				sock.connect((host, int(port)))

				self.data(sock)
				#db.tables(self.d)
				db.submit(self.d)
				del sock
			time.sleep(15)

if __name__ == "__main__":
	app = App()
	logger = logging.getLogger('daemonlog')
	logger.setLevel(logging.INFO)
	formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
	handler = logging.FileHandler("/var/log/daemon.log")
	handler.setFormatter(formatter)
	logger.addHandler(handler)
	daemon_runner = runner.DaemonRunner(app)
	daemon_runner.daemon_context.files_preserve = [handler.stream]
	daemon_runner.do_action()
