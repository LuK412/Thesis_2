from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Principal(Page):

	form_model = 'player'
	form_fields = ['category']


class ResultsWaitPage(WaitPage):

	def after_all_players_arrive(self):
 		self.subsession.set_groups()


class Results(Page):
	pass


class Questionnaire(Page):

	form_model = "player"
	form_fields = ["age", "gender", "studies", "studies2", "financial_advice", "income"]


page_sequence = [
	Principal,
	ResultsWaitPage,
	Results,
#	Questionnaire
]
