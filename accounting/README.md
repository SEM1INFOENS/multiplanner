# Resolution

- balance_in_fraction: calculates the total amount each person has to pay in fraction (TO AVOID ANY LOSS IN MONEY).
It returns a list of members and the prices they have to pay or receive ( positive = receive | negative = pay ).

- get_decimals: a sub-function for balance_in_floats that returns the decimal part of any number.

- balance_in_floats: returns the balance of the people in decimals and minimizes the loss for people.

- resolution_tuple : returns the list of transactions as tuples that has to be done from people, minimizing the number of transactions per person, and taking in consideration the amount of money received and payed compared to the original amount of money that has to be transacted.

- resolution: transforms the tuples into transactions. 
