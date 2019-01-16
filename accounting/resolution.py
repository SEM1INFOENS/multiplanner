''' Balance and Resolution functions of a group '''

import fractions
import numpy as np
from .webScraping import get_currency_equivalence
from accounting.models import Transaction
from groups.models import Balance
from djmoney.money import Money


def balance_in_fractions(group):
    '''Computes the balance of a group in the fraction format'''
    calculated = True
    members = [m for m in group.members.all()]
    transactions = group.transactions.all()
    # check if transaction are already calculated
    for t in transactions:
        if t.calculated == False:
            calculated = False
            t.calculated = True
            t.save()
    #if not calculated, recalculate all the balance and update transactions
    if calculated == False:
        balance = [0]*len(members)
        for i in transactions:
            # beneficiaries cannot be an empty list
            amount = fractions.Fraction(i.amount.amount)
            if i.amount.currency != group.currency:
                rate = get_currency_equivalence(i.amount.currency.code, group.currency, 1)
                rate = fractions.Fraction(rate)
                amount = rate * amount 
            index = members.index(i.payer)
            balance[index] += amount

            part_transactions = Transaction.objects.get_transaction_part_with_transaction(i)
            for j in part_transactions:
                index = members.index(j.beneficiary)
                amount = fractions.Fraction(j.amount.amount)
                if i.amount.currency != group.currency:
                    amount = amount*rate
                balance[index] -= fractions.Fraction(amount)
    else :
        balance = []
    return members, balance, calculated

def get_decimals(balance2):
    ''' Gets the decimal part in a float '''
    decimals = []
    # modf seperates decimals from the integer part
    for i in balance2:
        decimals.append(np.modf(i)[0])
    return decimals

def sort (members,balances):
    balances2 = []
    for i in range(len(members)):
        for j in range(len(balances)):
            if balances[j].user == members[i]:
                balances2.append(balances[j])
    return balances2

def balance_in_floats(group):
    ''' Calculates the balance of a group in the float format '''
    members, balance1, calculated = balance_in_fractions(group)
    #get the balances from the database
    balances = Balance.objects.balancesOfGroup(group)
    #sort the balances in the order of the members in the group
    balances = sort(members,balances)

    if calculated == False:
        #calculate all the balance and update balance database
        balance2 = []
        currency = group.currency

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
                #update the database
                balances[i].amount = amount= Money(balance2[i],currency)
                balances[i].save()
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


            balances = sort(members,balances)
        for i in range(len(balance2)):
            #transform an integer to a two decimal float
            balance2[i] /= 100
            #update the database
            balances[i].amount = amount= Money(balance2[i],currency)
            balances[i].save()
    else:
        balance2 = [b.amount.amount for b in balances]

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
