''' Balance and Resolution functions of a group '''

import fractions
import numpy as np

def balance_in_fractions(group):
    '''Computes the balance of a group in the fraction format'''
    members = [m for m in group.members.all()]
    transactions = group.transactions.all()

    balance = [0]*len(members)
    for i in transactions:
        # beneficiaries cannot be an empty list
        beneficiaries = [b for b in i.get_beneficiaries()]

        amount = fractions.Fraction(str(i.amount.amount))
        index = members.index(i.payer)
        balance[index] += amount

        for j in beneficiaries:
            index = members.index(j)
            balance[index] -= fractions.Fraction(amount, len(beneficiaries))

    return members, balance

def get_decimals(balance2):
    ''' Gets the decimal part in a float '''
    decimals = []
    # modf seperates decimals from the integer part
    for i in balance2:
        decimals.append(np.modf(i)[0])
    return decimals




def balance_in_floats(group):
    ''' Calculates the balance of a group in the float format '''
    members, balance1 = balance_in_fractions(group)
    balance2 = []

    # transform the euros fractions into centimes floats
    for i in range(len(balance1)):
        # multiply by 100 to avoid float non-precision with operations
        balance1[i] = float(100*balance1[i])
        balance2.append(np.floor(balance1[i]))

    moneyPutOnTable = 0
    moneyTakenFromTable = 0

    for i in balance2:
        if i > 0:
            moneyTakenFromTable += i
        else:
            moneyPutOnTable -= i

    if moneyTakenFromTable == moneyPutOnTable:
        for i in range(len(balance2)):
            #transform centimes to euros
            balance2[i] /= 100
        return balance2

    exceedingMoneyOnTable = moneyPutOnTable - moneyTakenFromTable
    decimals = get_decimals(balance1)

    # redistributing the money
    # chosing the people who spent the most in the exceeding operation
    i1 = np.argmax(decimals)
    i2 = np.argmin(decimals)
    while exceedingMoneyOnTable > 0:
        exceedingMoneyOnTable -= 1
        if decimals[i1] > 1 + decimals[i2]:
            balance2[i1] += 1
            decimals[i1] = 0
            i1 = np.argmax(decimals)
        else:

            balance2[i2] += 1
            decimals[i2] = 0
            i2 = np.argmin(decimals)


    #transform an integer to a two decimal float to  (100 centimes is 1.00 euros)
    for i in range(len(balance2)):
        balance2[i] /= 100
    return balance2

def resolution_tuple(group, balance):
    ''' Returns the resolution of a group as a list of 3-tuples '''
    # resolution_tuple is a list of 3-tuple (a,b,amount)
    # a has to pay b the amount
    # takes the person 'a' that has to be payed the most,
    # takes the person 'b' that has to pay the most;
    # transacts all the money from  b to a. Repeats.
    members = [m for m in group.members.all()]
    resolution = []
    for i in range(len(balance)):
        balance[i] *= 100

    while members:
        maximum = np.argmax(balance)
        minimum = np.argmin(balance)
        amount = -balance[minimum]
        if maximum == minimum:
            return resolution
        if balance[maximum] == amount:
            balance.pop(maximum)
            m = members.pop(maximum)
            if maximum < minimum:
                resolution.append((members.pop(minimum-1), m, amount/100))
                balance.pop(minimum-1)
            else:
                resolution.append((members.pop(minimum), m, amount/100))
                balance.pop(minimum)

        else:
            if minimum > maximum:
                resolution.append((members.pop(minimum), members[maximum], amount/100))
                balance.pop(minimum)
                balance[maximum] = balance[maximum] - amount
            else:
                resolution.append((members.pop(minimum), members[maximum-1], amount/100))
                balance.pop(minimum)
                balance[maximum-1] = balance[maximum-1] - amount
    return resolution
