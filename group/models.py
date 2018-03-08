from otree.api import (
	models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
	Currency as c, currency_range
)
from pprint import pprint
import random

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
	name_in_url = 'group_test'
	players_per_group = None
	num_rounds = 1

	category_names = ['Sehr Konservativ', 'Sicherheitsorientiert', 'Ausgeglichen', 'Wachstumsorientiert', 'Offensiv']

	endowment_principals = c(10)

	# Fixed Compensation
	fixed_payment = c(10)

	#Variable Compensation
	variable_payment = c(5)			# Fixer Anteil für die Agenten
	share = 25

class Subsession(BaseSubsession):

	def creating_session(self):	
		player_list = self.get_players()
		random_number = random.randint(1,5)
		for player in player_list:
			player.compensation = self.session.config["compensation"]
			player.participation_fee = self.session.config['participation_fee']
			player.randomizer = random_number



	def set_groups(self):

		# Create category lists
		cat_lists = dict.fromkeys(Constants.category_names)
		for element in cat_lists:
			cat_lists[element] = []

		# sort players into category lists by their choices
		for player in self.get_players():
			for cat_name in cat_lists:
				if player.category == cat_name:
					cat_lists[cat_name].append(player)
					
		# berechne anzahl nötiger Gruppen
		# für jede Gruppe gehe durch alle categorien
		# nimm jeweils einen spieler aus jeder cat, startend bei der ersten
		# wenn keine spieler mehr in der gruppe, nimm nächste gruppe, bis gruppe voll

		total_players = len(self.get_players())
		group_size = 5
		number_groups = int(total_players / group_size)


		group_list = []
		for group in range(number_groups):
			group_members = []
			while len(group_members) < group_size:
				for cat_name in cat_lists:
					if cat_lists[cat_name]:
						group_members.append(cat_lists[cat_name].pop())

					if len(group_members) >= group_size:
						break

				print(len(group_members))
			group_list.append(group_members)

		pprint(group_list)

		self.set_group_matrix(group_list)
		
		group_matrix = self.get_group_matrix()
		for group in group_matrix:
			for player in group:
				player.my_group_id = group_matrix.index(group) + 1

class Group(BaseGroup):
	

##	def get_agent(self):
##		self.random_number=random.randint(1,5)
##
##	random_number = models.IntegerField()

	def determine_invested_amount(self):
		players = self.get_players()
		for p in players:
			if p.roles == "Agent":
				self.invested_amount_p1 = p.investment_for_p_1
				self.invested_amount_p2 = p.investment_for_p_2
				self.invested_amount_p3 = p.investment_for_p_3
				self.invested_amount_p4 = p.investment_for_p_4
		

	invested_amount_p1 = models.CurrencyField()
	invested_amount_p2 = models.CurrencyField()
	invested_amount_p3 = models.CurrencyField()
	invested_amount_p4 = models.CurrencyField()


	def choose_principal(self):
		self.random_number_principal=random.randint(1,3)

		players = self.get_players()
		for p in players:
			self.randomizer_principal = self.random_number_principal

	randomizer_principal = models.IntegerField()


	def determine_relevant_payoff(self):
		players = self.get_players()
		for p in players:
			if p.relevant_principal == 1:
				self.principals_payoff = p.payoff

	principals_payoff = models.CurrencyField()





class Player(BasePlayer):

	category = models.CharField(
		choices=Constants.category_names,
		widget=widgets.RadioSelect(),
		verbose_name="Bitte wählen Sie nun einen der fünf Begriffe:",
		doc="Principals choose the category which is communicated to their agent"
		)


# Part II: Investment for Group members
	
	c_principal_1 = models.CharField()
	c_principal_2 = models.CharField()
	c_principal_3 = models.CharField()
	c_principal_4 = models.CharField()

	def find_principals(self):
		# c for corresponding
		if self.id_in_group == 1:
			self.c_principal_1 = 2
			self.c_principal_2 = 3
			self.c_principal_3 = 4
			self.c_principal_4 = 5
		elif self.id_in_group == 2:
			self.c_principal_1 = 1
			self.c_principal_2 = 3
			self.c_principal_3 = 4
			self.c_principal_4 = 5
		elif self.id_in_group == 3:
			self.c_principal_1 = 1
			self.c_principal_2 = 2
			self.c_principal_3 = 4
			self.c_principal_4 = 5
		elif self.id_in_group == 4:
			self.c_principal_1 = 1
			self.c_principal_2 = 2
			self.c_principal_3 = 3
			self.c_principal_4 = 5
		elif self.id_in_group == 5:
			self.c_principal_1 = 1
			self.c_principal_2 = 2
			self.c_principal_3 = 3
			self.c_principal_4 = 4


	investment_for_p_1 = models.CurrencyField(
		min=0,
		max=Constants.endowment_principals,
		widget=widgets.Slider(),					# Neuer Slider von Christian
		verbose_name="Ihre Investitionsentscheidung für Ihren Kunden:",
		doc="Agents investment for the principal in the risky asset."
		)
		
	investment_for_p_2 = models.CurrencyField(
		min=0,
		max=Constants.endowment_principals,
		widget=widgets.Slider(),					# Neuer Slider von Christian
		verbose_name="Ihre Investitionsentscheidung für Ihren Kunden:",
		doc="Agents investment for the principal in the risky asset."
		)

	investment_for_p_3 = models.CurrencyField(
		min=0,
		max=Constants.endowment_principals,
		widget=widgets.Slider(),					# Neuer Slider von Christian
		verbose_name="Ihre Investitionsentscheidung für Ihren Kunden:",
		doc="Agents investment for the principal in the risky asset."
		)

	investment_for_p_4 = models.CurrencyField(
		min=0,
		max=Constants.endowment_principals,
		widget=widgets.Slider(),					# Neuer Slider von Christian
		verbose_name="Ihre Investitionsentscheidung für Ihren Kunden:",
		doc="Agents investment for the principal in the risky asset."
		)


# Results: Messages
	
	message = models.CharField(
		choices=["Ich bin sehr zufrieden mit Ihrer Entscheidung", "Ich bin zufrieden mit Ihrer Entscheidung",
		"Ich bin unzufrieden mit Ihrer Entscheidung", "Ich bin sehr unzufrieden mit Ihrer Entscheidung"],
		widget=widgets.RadioSelect(),
		verbose_name="Wählen Sie dazu eine der vorgefertigten Mitteilungen aus:",
		doc="Principals choose the message to send to the agents."
		)





	randomizer = models.IntegerField()


	def assign_role(self):
		if self.id_in_group == self.randomizer:
			self.roles="Agent"
		else:
			self.roles="Principal"


	roles = models.CharField()


	# Legt fest, ob die Investition erfolgreich war (p=1/3) oder nicht (1-p=2/3):
	def risky_asset(self):
		self.random_number=random.randint(1,3)

		if self.random_number == 1:
			self.investment_outcome="Die Investition war erfolgreich."
		else:
			self.investment_outcome="Die Investition war nicht erfolgreich."

	investment_outcome = models.CharField(
		doc="Tells the customer if the investment was successfull or not successfull.")


	def payments_principals(self):

		if self.roles == "Principal":
			if self.randomizer == 1:
				if self.id_in_group == 2:
					if self.investment_outcome == "Die Investition war erfolgreich.":
						self.payoff=self.group.invested_amount_p1 * 3.5 + (Constants.endowment_principals - self.group.invested_amount_p1)
					elif self.investment_outcome == "Die Investition war nicht erfolgreich.":
						self.payoff=Constants.endowment_principals - self.group.invested_amount_p1
				elif self.id_in_group == 3:
					if self.investment_outcome == "Die Investition war erfolgreich.":
						self.payoff=self.group.invested_amount_p2 * 3.5 + (Constants.endowment_principals - self.group.invested_amount_p2)
					elif self.investment_outcome == "Die Investition war nicht erfolgreich.":
						self.payoff=Constants.endowment_principals - self.group.invested_amount_p2
				elif self.id_in_group == 4:
					if self.investment_outcome == "Die Investition war erfolgreich.":
						self.payoff=self.group.invested_amount_p3 * 3.5 + (Constants.endowment_principals - self.group.invested_amount_p3)
					elif self.investment_outcome == "Die Investition war nicht erfolgreich.":
						self.payoff=Constants.endowment_principals - self.group.invested_amount_p3
				elif self.id_in_group == 5:
					if self.investment_outcome == "Die Investition war erfolgreich.":
						self.payoff=self.group.invested_amount_p4 * 3.5 + (Constants.endowment_principals - self.group.invested_amount_p4)
					elif self.investment_outcome == "Die Investition war nicht erfolgreich.":
						self.payoff=Constants.endowment_principals - self.group.invested_amount_p4

			elif self.randomizer == 2:
				if self.id_in_group == 1:
					if self.investment_outcome == "Die Investition war erfolgreich.":
						self.payoff=self.group.invested_amount_p1 * 3.5 + (Constants.endowment_principals - self.group.invested_amount_p1)
					elif self.investment_outcome == "Die Investition war nicht erfolgreich.":
						self.payoff=Constants.endowment_principals - self.group.invested_amount_p1
				elif self.id_in_group == 3:
					if self.investment_outcome == "Die Investition war erfolgreich.":
						self.payoff=self.group.invested_amount_p2 * 3.5 + (Constants.endowment_principals - self.group.invested_amount_p2)
					elif self.investment_outcome == "Die Investition war nicht erfolgreich.":
						self.payoff=Constants.endowment_principals - self.group.invested_amount_p2
				elif self.id_in_group == 4:
					if self.investment_outcome == "Die Investition war erfolgreich.":
						self.payoff=self.group.invested_amount_p3 * 3.5 + (Constants.endowment_principals - self.group.invested_amount_p3)
					elif self.investment_outcome == "Die Investition war nicht erfolgreich.":
						self.payoff=Constants.endowment_principals - self.group.invested_amount_p3
				elif self.id_in_group == 5:
					if self.investment_outcome == "Die Investition war erfolgreich.":
						self.payoff=self.group.invested_amount_p4 * 3.5 + (Constants.endowment_principals - self.group.invested_amount_p4)
					elif self.investment_outcome == "Die Investition war nicht erfolgreich.":
						self.payoff=Constants.endowment_principals - self.group.invested_amount_p4

			elif self.randomizer == 3:
				if self.id_in_group == 1:
					if self.investment_outcome == "Die Investition war erfolgreich.":
						self.payoff=self.group.invested_amount_p1 * 3.5 + (Constants.endowment_principals - self.group.invested_amount_p1)
					elif self.investment_outcome == "Die Investition war nicht erfolgreich.":
						self.payoff=Constants.endowment_principals - self.group.invested_amount_p1
				elif self.id_in_group == 2:
					if self.investment_outcome == "Die Investition war erfolgreich.":
						self.payoff=self.group.invested_amount_p2 * 3.5 + (Constants.endowment_principals - self.group.invested_amount_p2)
					elif self.investment_outcome == "Die Investition war nicht erfolgreich.":
						self.payoff=Constants.endowment_principals - self.group.invested_amount_p2
				elif self.id_in_group == 4:
					if self.investment_outcome == "Die Investition war erfolgreich.":
						self.payoff=self.group.invested_amount_p3 * 3.5 + (Constants.endowment_principals - self.group.invested_amount_p3)
					elif self.investment_outcome == "Die Investition war nicht erfolgreich.":
						self.payoff=Constants.endowment_principals - self.group.invested_amount_p3
				elif self.id_in_group == 5:
					if self.investment_outcome == "Die Investition war erfolgreich.":
						self.payoff=self.group.invested_amount_p4 * 3.5 + (Constants.endowment_principals - self.group.invested_amount_p4)
					elif self.investment_outcome == "Die Investition war nicht erfolgreich.":
						self.payoff=Constants.endowment_principals - self.group.invested_amount_p4

			elif self.randomizer == 4:
				if self.id_in_group == 1:
					if self.investment_outcome == "Die Investition war erfolgreich.":
						self.payoff=self.group.invested_amount_p1 * 3.5 + (Constants.endowment_principals - self.group.invested_amount_p1)
					elif self.investment_outcome == "Die Investition war nicht erfolgreich.":
						self.payoff=Constants.endowment_principals - self.group.invested_amount_p1
				elif self.id_in_group == 2:
					if self.investment_outcome == "Die Investition war erfolgreich.":
						self.payoff=self.group.invested_amount_p2 * 3.5 + (Constants.endowment_principals - self.group.invested_amount_p2)
					elif self.investment_outcome == "Die Investition war nicht erfolgreich.":
						self.payoff=Constants.endowment_principals - self.group.invested_amount_p2
				elif self.id_in_group == 3:
					if self.investment_outcome == "Die Investition war erfolgreich.":
						self.payoff=self.group.invested_amount_p3 * 3.5 + (Constants.endowment_principals - self.group.invested_amount_p3)
					elif self.investment_outcome == "Die Investition war nicht erfolgreich.":
						self.payoff=Constants.endowment_principals - self.group.invested_amount_p3
				elif self.id_in_group == 5:
					if self.investment_outcome == "Die Investition war erfolgreich.":
						self.payoff=self.group.invested_amount_p4 * 3.5 + (Constants.endowment_principals - self.group.invested_amount_p4)
					elif self.investment_outcome == "Die Investition war nicht erfolgreich.":
						self.payoff=Constants.endowment_principals - self.group.invested_amount_p4

			elif self.randomizer == 5:
				if self.id_in_group == 1:
					if self.investment_outcome == "Die Investition war erfolgreich.":
						self.payoff=self.group.invested_amount_p1 * 3.5 + (Constants.endowment_principals - self.group.invested_amount_p1)
					elif self.investment_outcome == "Die Investition war nicht erfolgreich.":
						self.payoff=Constants.endowment_principals - self.group.invested_amount_p1
				elif self.id_in_group == 2:
					if self.investment_outcome == "Die Investition war erfolgreich.":
						self.payoff=self.group.invested_amount_p2 * 3.5 + (Constants.endowment_principals - self.group.invested_amount_p2)
					elif self.investment_outcome == "Die Investition war nicht erfolgreich.":
						self.payoff=Constants.endowment_principals - self.group.invested_amount_p2
				elif self.id_in_group == 3:
					if self.investment_outcome == "Die Investition war erfolgreich.":
						self.payoff=self.group.invested_amount_p3 * 3.5 + (Constants.endowment_principals - self.group.invested_amount_p3)
					elif self.investment_outcome == "Die Investition war nicht erfolgreich.":
						self.payoff=Constants.endowment_principals - self.group.invested_amount_p3
				elif self.id_in_group == 4:
					if self.investment_outcome == "Die Investition war erfolgreich.":
						self.payoff=self.group.invested_amount_p4 * 3.5 + (Constants.endowment_principals - self.group.invested_amount_p4)
					elif self.investment_outcome == "Die Investition war nicht erfolgreich.":
						self.payoff=Constants.endowment_principals - self.group.invested_amount_p4




	def payments_agents(self):

		if self.roles == "Agent":
			if self.compensation == "fixed":
				self.payoff=Constants.fixed_payment
			if self.compensation == "variable":
				self.payoff=Constants.variable_payment + Constants.share/100 * self.group.principals_payoff



	def find_relevant_principal(self):

		if self.group.randomizer_principal == self.id_in_group:
			self.relevant_principal = 1
		elif self.group.randomizer_principal != self.id_in_group:
			self.relevant_principal = 0

	relevant_principal = models.IntegerField()





	payoff = models.CurrencyField()






	my_group_id = models.IntegerField()

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
