
import uuid

class Observer:
	def __init__(self):
		self.subscription = None

	def onEvent(self, event):
		raise NotImplementedError()

	def set_subscription(self, subscription, observable):
		self.subscription = (subscription, observable)

	def get_subscription(self):
		return self.subscription


class Observable:
	def __init__(self):
		self.subscribers = {}

	def subscribe(self, *arg):
		for observer in arg:
			subscription = str(uuid.uuid1())
			observer.set_subscription(subscription, self)
			self.subscribers[subscription] = observer
			return subscription

	def unsubscribe(self, subscription):
		del self.subscribers[subscription]

	def notifySubscribers(self, event):
		for subscription in self.subscribers:
			self.subscribers[subscription].onEvent(event)

	def clear(self):
		self.subscribers = {}

class KeyboardStream(Observable):
	def __init__(self):
		Observable.__init__(self)

	def notifySubscribers(self, event, game):
		for subscription in self.subscribers:
			self.subscribers[subscription].onEvent(event, game)
