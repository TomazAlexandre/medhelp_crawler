class Question:
	title = None
	user_id = None
	user_link = None
	question = None
	timestamp = None
	answers = []
	def __init__(self, title, user_id, user_link, question, answers, timestamp):
		self.title = title
		self.user_id = user_id
		self.user_link = user_link
		self.question = question
		self.answers = answers
		self.timestamp = timestamp

class Answer:
	user_id = None
	user_link = None
	answer = None
	timestamp = None
	votes = None
	def __init__(self, user_id, user_link, answer, timestamp, votes):
		self.user_id = user_id
		self.user_link = user_link
		self.answer = answer
		self.timestamp = timestamp
		self.votes = votes