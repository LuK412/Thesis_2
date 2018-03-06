from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Principal(Page):
	
	form_model = "player"
	form_fields = ["category"]


class WaitPage_1(WaitPage):

	def after_all_players_arrive(self):
		self.subsession.determine_received_categories()


class Agent(Page):
	
	form_model = "player"
	form_fields = ["investment_single"]



class ResultsWaitPage(WaitPage):

	def after_all_players_arrive(self):
		self.subsession.determine_invested_amounts()
		self.subsession.determine_investment_outcome()
		self.subsession.determine_investment_outcome_for_agents()
		self.subsession.determine_payoffs_principals()
		self.subsession.determine_payoff_of_coresponding_principal()
		self.subsession.get_payoffs_agents()


class Results_Principal(Page):

	def is_displayed(self):
		return self.player.role() == "Customer"

	form_model = "player"
	form_fields = ["message"]


class WaitPage_2(WaitPage):

	def after_all_players_arrive(self):
		self.subsession.determine_received_messages()


class Results_Agent(Page):

	def is_displayed(self):
		return self.player.role() == "Agent"


class Questionnaire(Page):

	form_model = "player"
	form_fields = ["age", "gender", "studies", "studies2", "financial_advice", "income"]

class Last_Page(Page):
	pass



page_sequence = [
	Principal,
	WaitPage_1,
	Agent,
	ResultsWaitPage,
	Results_Principal,
	WaitPage_2,
	Results_Agent,
	Questionnaire,
	Last_Page
]
