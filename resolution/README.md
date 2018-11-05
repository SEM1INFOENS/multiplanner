# Balance

The Balance function returns the list of people and the amount they should pay (negative amount) or recieve (positive amount)

A small problem might occur if there are three people a,b,c:

	** a pays 1 euro for b and c

	** b and c have each an amount of -0.333333333

This problem will be resolved between the people themselves (who will lose one centime)

# Resolution

The Resolution function returns a list of the final transactions that should be made. Each transaction is a 3-tuple (a,b,amount) which means that a should pay b a sum of amount.
Finally this function directly optimises the total number of transactions and the number of transaction made by person. 



Note: these two functions return the ID of the Users not the whole Users
