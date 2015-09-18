Emma Montross
CSCI 3202 Into to AI
Programming Assignment #2

To run program:
python2 assignment2.py <filename> <heuristic number>

Filename: text file that contains the world or maze to perform the A* search on
	In this case, World1.txt or World2.txt
Heuristic Number: 1 if Manhattan, 2 for other

Heuristic Equation: sqrt( (x - endx)^2 + (y - endy)^2 )
	This is the straight-line distance formula. 
	I thought it would produce a good solution because it calculates the straight distance from the current square to the ending square, instead of just doing horizontal and verticle moves.
	So the distance it calculates is usually shorter than the Manhattan distance, but both heuristics come up with the same results. The same number of nodes are evaluated, the cost is the same, 
	and the path is exactly the same as well. So both heuristics work equally well.
