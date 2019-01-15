# Resolution

The algorithm only optimises the number of transactions per person. This means that each person will do maximum 1 final transaction. This implies that sometimes some people with no transactions to do will have to make 1 transaction with this algorithm.

- balance_in_fraction: calculates the total amount each person has to pay in fraction (TO AVOID ANY LOSS OF MONEY).
It returns a list of members and the prices they have to pay or receive ( positive = receive | negative = pay ).

- get_decimals: a sub-function for balance_in_floats that returns the decimal part of any number.

- balance_in_floats: returns the balance of the people in decimals and minimizes the loss for people. This function forces everyone to pay a rounded up of the price he/she has to pay (if it's 101.1 centimes then he/she pays 102 centimes). Next it distributes the a rounded down of sums for the people that should get paid (if it's 101.1 centimes then he/she receives 101 centimes). Finally, the rest of the centimes are distributed such that the person who lost the most in this operation will take one centime, and then the second most ... until no centimes are left.

- resolution_tuple : returns the list of transactions as tuples that has to be done from people, minimizing the number of transactions per person, and taking in consideration the amount of money received and payed compared to the original amount of money that has to be transacted.
