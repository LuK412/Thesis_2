from otree.api import (
	models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
	Currency as c, currency_range
)

import random

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
	name_in_url = 'single'
	players_per_group = None
	num_rounds = 1

	category_names = ['Sehr Konservativ', 'Sicherheitsorieniert', 'Ausgeglichen', 'Wachstumsorientiert', 'Offensiv']

	endowment_principals = c(10)

	# Fixed Compensation
	fixed_payment = c(10)

	#Variable Compensation
	variable_payment = c(5)			# Fixer Anteil für die Agenten
	share = 25

class Subsession(BaseSubsession):
	
	def creating_session(self):	
		player_list = self.get_players()				
		for player in player_list:
			player.compensation = self.session.config["compensation"]
			player.participation_fee = self.session.config['participation_fee']

			player.corresponding_agent = player.id_in_group -1
			if player.corresponding_agent < 1:
				player.corresponding_agent = len(player_list)

			player.corresponding_principal = player.id_in_group + 1
			if player.corresponding_principal > len(player_list):
				player.corresponding_principal = 1


	def determine_received_categories(self):
		for player in self.get_players():
			player.get_principal_category()

	def determine_invested_amounts(self):
		for player in self.get_players():
			player.get_agent_decision()

	def determine_investment_outcome(self):
			for player in self.get_players():
				if player.id_in_group % 2 == 0:
					player.risky_asset()

	def determine_investment_outcome_for_agents(self):
		for player in self.get_players():
			player.get_principal_outcome()

	def determine_received_messages(self):
		for player in self.get_players():
			player.get_principal_message()

	def determine_payoffs_principals(self):
		for player in self.get_players():
			if player.id_in_group % 2 == 0:
				player.payments_principals()


	def determine_payoff_of_coresponding_principal(self):
		for player in self.get_players():
			player.get_principal_payoff()


	def get_payoffs_agents(self):
		for player in self.get_players():
			if player.id_in_group % 2 != 0:
				player.payments_agents()



class Group(BaseGroup):
	pass


class Player(BasePlayer):

#	Roles:
#	gerade Nummern sind Kunden
	def role(self):
		if self.id_in_group % 2 == 0:
			return "Customer"
		else:
			return "Agent"




	def get_agent_decision(self):
		agent = self.group.get_player_by_id(self.corresponding_agent)
		self.invested_amount = agent.investment_single

	def get_principal_category(self):
		principal = self.group.get_player_by_id(self.corresponding_principal)
		self.category_received = principal.category

	def get_principal_outcome(self):
		principal = self.group.get_player_by_id(self.corresponding_principal)
		self.outcome_received = principal.investment_outcome

	def get_principal_message(self):
		principal = self.group.get_player_by_id(self.corresponding_principal)
		self.message_received = principal.message

	def get_principal_payoff(self):
		principal = self.group.get_player_by_id(self.corresponding_principal)
		self.payoff_principal = principal.payoff


	corresponding_agent = models.CharField(
		doc="Returns the ID of the participants agent."
		)
	corresponding_principal = models.CharField(
		doc="Returns the ID of the participants customer."
		)






	# Part II Choosing Category:
	
	category = models.CharField(
		choices=Constants.category_names,
		widget=widgets.RadioSelect(),
		verbose_name="Bitte wählen Sie nun einen der fünf Begriffe:",
		doc="Principals choose the category which is communicated to their agent"
		)

	category_received = models.CharField(
		doc="Category that agents see (from their customers)."
		)


# Part II Investment:

	investment_single = models.CurrencyField(
		min=0,
		max=Constants.endowment_principals,
		widget=widgets.Slider(),					# Neuer Slider von Christian
		verbose_name="Ihre Investitionsentscheidung für Ihren Kunden:",
		doc="Agents investment for the principal in the risky asset."
		)
	invested_amount = models.CurrencyField(
		doc="What was invested by the corresponding agent."
		)


	# Legt fest, ob die Investition erfolgreich war (p=1/3) oder nicht (1-p=2/3):
	def risky_asset(self):
		self.random_number=random.randint(1,3)

		if self.random_number == 1:
			self.investment_outcome="Die Investition war erfolgreich."
		else:
			self.investment_outcome="Die Investition war nicht erfolgreich."



	investment_outcome = models.CharField(
		doc="Tells the customer if the investment was successfull or not successfull.")
	outcome_received = models.CharField(
		doc="Tells the agent if his investment for his customer was successfull.")


	def payments_principals(self):
		if self.id_in_group % 2 == 0: # Für Kunden
			if self.investment_outcome == "Die Investition war erfolgreich.":
				self.payoff=self.invested_amount * 3.5 + (Constants.endowment_principals - self.invested_amount)
			elif self.investment_outcome == "Die Investition war nicht erfolgreich.":
				self.payoff=Constants.endowment_principals - self.invested_amount

	def payments_agents(self):
		if self.id_in_group % 2 != 0: # Für Berater
			if self.session.config["compensation"] == "fixed":
				self.payoff=Constants.fixed_payment
			if self.session.config["compensation"] == "variable":
				self.payoff=Constants.variable_payment   + Constants.share/100 * self.payoff_principal



	payoff = models.CurrencyField()
	payoff_principal = models.CurrencyField(
		doc="Payoff of the agent's principal."
		)


# Results: Messages

	message = models.CharField(
		choices=["Ich bin sehr zufrieden mit Ihrer Entscheidung", "Ich bin zufrieden mit Ihrer Entscheidung",
		"Ich bin unzufrieden mit Ihrer Entscheidung", "Ich bin sehr unzufrieden mit Ihrer Entscheidung"],
		widget=widgets.RadioSelect(),
		verbose_name="Wählen Sie dazu eine der vorgefertigten Mitteilungen aus:",
		doc="Principals choose the message to send to the agents."
		)

	message_received = models.CharField(
		doc="Message that agents receive from their principals."
		)


	# 

	compensation = models.CharField(
		doc="Compensation scheme put in place for agents (see settings)."
		)

	participation_fee = models.CharField(
		doc="Participation Fee for all agents."
		)




# Questionnaire:

	age = models.PositiveIntegerField(
		max=100,
		verbose_name="Wie alt sind Sie?",
		doc="We ask participants for their age between 0 and 100 years"
		)

	gender = models.CharField(
		choices=["männlich", "weiblich", "anderes"],
		widget=widgets.RadioSelect(),
		verbose_name="Was ist Ihr Geschlecht?",
		doc="gender indication"
		)

	studies = models.CharField(
		blank=True,
		verbose_name="Was studieren Sie im Hauptfach?",
		doc="field of studies indication."
		)

	studies2 = models.BooleanField(
		widget=widgets.CheckboxInput(),
		verbose_name="Kein Student",
		doc="Ticking the checkbox means that the participant is a non-student.")

	financial_advice = models.CharField(
		choices=["Ja", "Nein"],
		widget=widgets.RadioSelect(),
		verbose_name="Haben Sie bereits eine Bankberatung in Anspruch genommen?",
		doc="We ask participants if they ever made use of financial advice.")

	income = models.CurrencyField(
		verbose_name="Wie viel Geld im Monat steht Ihnen frei zur Verfügung?",
		doc="We ask participants how much money they have freely available each month.")
