### some notes

potential applications:
 - sorting
 - btrees
 - pathfinding
 - matrix multiplication
 - more?

Elements:
 - Optimizer
   - Can set value function: time, memory or arbitrary function on solution
 - Feature Extractor
   - Eg for sorting: orderdness, length, etc
   - Goal is to balance time to extract features and usefullness of features
 - Data Generator
   - Generates "training set" of problems (eg unsorted lists, graphs, matrices)
   - Alternatively could just pass in training set
 - Bag of solutions
   - Includes call to subproblem and reduction
   - Can have parameters, changed by optimizer
