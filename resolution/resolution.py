# Transaction:
#	motive = char
#	date = date
#	expeditor = User		// User : name ; pass ; email
#	amount = float
#	group = Group


%inline pylab


def transaction_matrix (transactions, members, groups):
	# number of groups = number of transactions
	M = zeros((len(participants), len(members))) 

	for i in range(len(transactions)):
		expIndex = members.index(transaction[i].expeditor)
		grouplen  = len(transaction.group)
		amount = transaction[i].amount / grouplen #grouplen != 0 
		for j in range(grouplen):
			benefIndex = members.index(groups[i][j])
			M[expIndex][benefIndex] +=  amount

	 

def balance (transaction_matrix):


