from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Principal(Page):

	form_model = 'player'
	form_fields = ['category']



class WaitPage_1(WaitPage):

	def after_all_players_arrive(self):
 		self.subsession.set_groups()


class Hilfe(Page):

	def before_next_page(self):
		self.player.find_principals()


class Agent_1(Page):


	def vars_for_template(self):
		group = self.group.get_players()

		return {'p1_category': group[int(self.player.c_principal_1)-1].category , 'p2_category': group[int(self.player.c_principal_2)-1].category, 'p3_category': group[int(self.player.c_principal_3)-1].category, 'p4_category': group[int(self.player.c_principal_4)-1].category}

	form_model = 'player'
	form_fields = ['investment_for_p_1', 'investment_for_p_2', 'investment_for_p_3', 'investment_for_p_4']

	def before_next_page(self):
		self.player.assign_role()
		self.player.risky_asset()


class WaitPage_2(WaitPage):

	def after_all_players_arrive(self):
		self.group.determine_invested_amount()


class Hilfe_2(Page):

	def before_next_page(self):
		self.player.payments_principals()


class Results_Principal(Page):

	def is_displayed(self):
		return self.player.roles == "Principal"

	form_model = 'player'
	form_fields = ['message']


class WaitPage_3(WaitPage):
	def after_all_players_arrive(self):
		self.group.choose_principal()


class Results_Agent(Page):

	def is_displayed(self):
		return self.player.roles == "Agent"

	def vars_for_template(self):
		group = self.group.get_players()

		return {'p1_category': group[int(self.player.c_principal_1)-1].category , 'p2_category': group[int(self.player.c_principal_2)-1].category, 'p3_category': group[int(self.player.c_principal_3)-1].category, 'p4_category': group[int(self.player.c_principal_4)-1].category, 'p1_message': group[int(self.player.c_principal_1)-1].message, 'p2_message': group[int(self.player.c_principal_2)-1].message, 'p3_message': group[int(self.player.c_principal_3)-1].message, 'p4_message': group[int(self.player.c_principal_4)-1].message, 'p1_outcome': group[int(self.player.c_principal_1)-1].investment_outcome , 'p2_outcome': group[int(self.player.c_principal_2)-1].investment_outcome, 'p3_outcome': group[int(self.player.c_principal_3)-1].investment_outcome, 'p4_outcome': group[int(self.player.c_principal_4)-1].investment_outcome, 'p1_payoff': group[int(self.player.c_principal_1)-1].payoff , 'p2_payoff': group[int(self.player.c_principal_2)-1].payoff, 'p3_payoff': group[int(self.player.c_principal_3)-1].payoff, 'p4_payoff': group[int(self.player.c_principal_4)-1].payoff}

#	def before_next_page(self):
#		self.player.payments_agents()



class Questionnaire(Page):

	form_model = "player"
	form_fields = ["age", "gender", "studies", "studies2", "financial_advice", "income"]

	#returns an error message if a participant...
	def error_message(self, values):
		# ... indicates no field of studies and does not tick the box "non-student".
		if "studies" in values:
			if values["studies2"] == True:
				return "You indicated no field of studies. Are you a non-student?"
		# ... states a field of studies and claimed to be a non-student.
		else:
			if values["studies2"] == True:
				return "You stated a field of studies, but indicated that you are a non-student."

	def before_next_page(self):
		self.player.find_relevant_principal()
		self.group.determine_relevant_payoff()
		self.player.payments_agents()



class Last_Page(Page):
	pass


page_sequence = [
	Principal,
	WaitPage_1,
	Hilfe,
	Agent_1,
	WaitPage_2,
	Hilfe_2,
	Results_Principal,
	WaitPage_3,
	Results_Agent,
	Questionnaire,
	Last_Page
]
