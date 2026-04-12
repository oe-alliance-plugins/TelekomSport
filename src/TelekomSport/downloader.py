from Tools.BoundFunction import boundFunction

from twisted.web.client import Agent, BrowserLikeRedirectAgent, ResponseDone
from twisted.internet.defer import Deferred
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.web.http_headers import Headers


class TelekomSportFileSaver(Protocol):

	def __init__(self, finished, callback, errorCallback, filename):
		self.finished = finished
		self.callback = callback
		self.errorCallback = errorCallback
		self.filename = filename
		self.f = open(filename, 'wb')

	def dataReceived(self, bytes):
		self.f.write(bytes)

	def connectionLost(self, reason):
		self.f.close()
		if reason.check(ResponseDone):
			self.callback()
		else:
			self.errorCallback(reason.getErrorMessage())


class TelekomSportFileDownloader:

	def __init__(self):
		self.agent = BrowserLikeRedirectAgent(Agent(reactor))

	def start(self, url, filename, callback, errorCallback):
		self.filename = filename
		d = self.agent.request(b'GET', url, Headers({'user-agent': ['Twisted']}))
		d.addCallback(boundFunction(self.handleResponse, callback, errorCallback))
		d.addErrback(errorCallback)

	def handleResponse(self, callback, errorCallback, response):
		finished = Deferred()
		response.deliverBody(TelekomSportFileSaver(finished, callback, errorCallback, self.filename))
		return finished
