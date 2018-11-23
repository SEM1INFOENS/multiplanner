import numpy as np
import fractions
import models

def balance_in_fractions (group):
	members = [m for m in group.members.all()]
	transactions = [t for t in group.transactions.all()]

	balance = [0]*len(members)

	totalMoney = 0
	for i in transactions :
		# beneficiaries cannot be empty list
		beneficiaries = [b for b in i.beneficiaries.all()]

		amount = fractions.Fraction(str(i.amount))
		index = members.index(i.payer)
		balance[index] += amount

		for j in beneficiaries :
			index = members.index(j)
			balance[index] -= fractions.Fraction(amount,len(beneficiaries))

	return members,balance

def get_decimals (balance2) :
	decimals = []
	# modf seperates decimals from the integer part
	for i in balance2:
		decimals.append(np.modf(i)[0])
	return decimals




def balance_in_floats (group):
	members,balance1 = balance_in_fractions (group)
	balance2 = []

	#transform the euros fractions into centimes floats
	for i in range(len(balance1)):
		balance1[i] = float(100*balance1[i])
		balance2.append(np.floor (balance1[i]))

	moneyPutOnTable = 0
	moneyTakenFromTable = 0

	for i in balance2:
		if i>0 :
			moneyTakenFromTable += i
		else :
			moneyPutOnTable -= i

	if moneyTakenFromTable == moneyPutOnTable:
		return balance2

	exceedingMoneyOnTable = moneyPutOnTable - moneyTakenFromTable
	decimals = get_decimals(balance1)

	#redistributing the money
	#chosing the people who spent the most in the exceeding operation
	i1 = np.argmax (decimals)
	i2 = np.argmin (decimals)
	while (exceedingMoneyOnTable>0):
		exceedingMoneyOnTable -= 1
		if (decimals[i1]>1+decimals[i2]):
			balance2 [i1] +=1
			decimals[i1] = 0
			i1 = np.argmax (decimals)
		else :

			balance2 [i2] +=1
			decimals[i2] = 0
			i2 = np.argmin (decimals)


	#transform centimes to euros
	for i in range(len(balance2)):
		balance2[i] /=100
	return balance2

def resolution_tuple (group, balance) :
	# resolution_tuple is a list of 3-tuple (a,b,amount)
	# a has to pay b the amount
	# takes the person 'a' that has to be payed the most,
	# takes the person 'b' that has to pay the most;
	# transacts all the money from  b to a. Repeats.
	members = [m for m in group.members.all()]
	resolution = []
	while members :
		maximum = np.argmax(balance)
		minimum = np.argmin (balance)
		amount = -balance[minimum]
		if (maximum == minimum):
			return resolution
		if (balance[maximum] == amount):
			balance.pop(maximum)
			m = members.pop(maximum)
			if maximum<minimum:
				resolution.append((members.pop(minimum-1),m,amount))
				balance.pop(minimum-1)
			else :
				resolution.append((members.pop(minimum),m,amount))
				balance.pop(minimum)

		else :
			resolution.append((members.pop(minimum),members[maximum],amount))
			balance.pop(minimum)
			balance[maximum] -= amount

	return resolution


def resolution (group, balance):
	# returns the transactions that has to be done after the resolution
	tupRes = resolution_tuple(group, balance)
	transaction =[]
	for i in len(tupRes):
		(a,b,amount) = tupRes[i]
		t = Transaction.create_new(
			motive = "Transaction " + str(i),
			payer = a,
			amount = amount,
			beneficiaries = b
		)
		transaction.append(t)
	return transaction
