from numpy import argmin
from numpy import argmax


def balancing (group):
	members = group.members_set.all()
	transactions = group.transaction_set.all()

	people = []
	balance = []

	for i in members :
		people.append([i.id])
		balance.append(0)

	for i in transactions :
		#beneficiaries cannot be empty list
		amountPerPerson = i.amount/len(i.beneficiaries)

		# initialising the payer
		payer = i.payer.id
		index = people.index(payer)
		balance[index] += i.amount - amountPerPerson
		

		for j in i.beneficiaries:
			if (j.id != payer):
				index = people.index(j.id)
				balance [index] -= amountPerPerson

	return (people,balance)


def resolution (people, balance) :
	# resolution is a list of 3-tuple (a,b,amount)
	# a has to pay b the amount 
	
	resolution = []
	while people :
		maximum = argmax(balance)
		minimum = argmin (balance)
		amount = -balance[minimum]

		if (balance[maximum] == amount):
			resolution.append(people.pop(minimum),people.pop(maximum),amount)
			balance.pop(maximum)
			balance.pop(minimum)
		else :
			resolution.append(people.pop(minimum),people[maximum],amount)
			balance.pop(minimum)
			balance[maximum] -= amount

	return resolution
