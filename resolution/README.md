
# Resolution
The algorithm of optimising the graph is based on 4 steps.
It optimises the graph to the max by optimising the total number of transactions, and the number of transactions per person.

## Notes
While optimising the number of transactions per person, it is prefered that the graph has a form such that:
- a person with no transfers to do in the initial graph can have maximum one transfer;
- a person with plenty of transactions to do in the initial graph can have a much smaller number of transfers to do in the graph (theorically one transfer to do).

Note also that the algorithm is not optimised in term of time: it is estimated to have a complexity of O(n^3) but this can be solved later on with some heuristics or optimisations in practice.

### STEP 1 : FIND CYCLES in the oriented graph O(n^3)
1. Finding a  cycle in the graph is just doing the Depth-First Search of each connected part of the graph while 	coloring the nodes (with three colors) and conseving the parent.
2. Once the cycle is found take the arc with the minimum weight on it and delete it.
3. Subtract this value of each arc in the cycle and delete the arcs that have value 0
4. Repeat the 3 first steps till no cycles are found 

### STEP 2 : FIND CYCLES in the non-oriented graph O(n^2) or less
1. Calculate the TOPOLOGICAL sort of the graph.
2. Find cycles with a depth-first search and a graph coloring.
3. Deduce the node (in the cycle) with two arcs in the cycle using the topological order.
4.	Combine the two arcs with the arc that leads to a parent in the cycle (using topological sort).
5.	Update the arcs in the cycle by adding the value to the arc off the weight of the deleted arc.
6.	Repeat the 5 first steps until no cycles are found.

### STEP 3: FIND THE PARENTS  p with the most children
1. Chose one of the nodes with the most children.
2. Chose an arbitrary leaf l.
3. Create an arc from the leaf to one of the children of the p that DO NOT lead to l.
4. Update all the arcs from the root to l with adding the weight of (p, p.child)
5. Delete (p, p.child)
6. Repeat until no nodes with more than one child

### STEP 4: MAXIMUM OPTIMIZATION
From the root to the leaf check if two successives arcs a_i a_(i+1) have weights such that w(a_i) < w(a_(i+1)).
If so delete a_i and update a_(i+1) s.t. w(a_(i+1)) := w(a_(i+1)) - w(a_i)

DONE !
It is hard to implement and the algorithm might work till n = 30 people in a group with each one having a transaction with all the others.
