# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from util import *

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    # define lists and stacks to track progress
    start_state = problem.getStartState()
    fringe = Stack()
    path_curr = Stack()
    visited_list = []
    outp = []

    # leave the start state and begin DFS
    fringe.push(start_state)
    state = fringe.pop()

    # DFS code from lecture (and like three previous classes)
    while not problem.isGoalState(state):
        if state not in visited_list:
            successor_list = problem.getSuccessors(state)
            visited_list.append(state)
            # update fringe and current path lists
            for child, direction, cost in successor_list:   # have to include cost even though is not used
                tmp = outp[:]
                tmp.append(direction)
                path_curr.push(tmp)
                fringe.push(child)
        state = fringe.pop()
        outp = path_curr.pop()
        
    return outp


def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # exactly the same as DFS but with queue instead of stack
    
    # define lists and queues to track progress
    start_state = problem.getStartState()
    fringe = Queue()
    path_curr = Queue()
    visited_list = []
    outp = []

    # leave the start state and begin BFS
    fringe.push(start_state)
    state = fringe.pop()

    # BFS code from lecture (and like three previous classes)
    while not problem.isGoalState(state):
        if state not in visited_list:
            successor_list = problem.getSuccessors(state)
            visited_list.append(state)
            # update fringe and current path lists
            for child, direction, cost in successor_list:   # have to include cost even though is not used
                tmp = outp[:]
                tmp.append(direction)
                path_curr.push(tmp)
                fringe.push(child)
        state = fringe.pop()
        outp = path_curr.pop()
        
    return outp

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # same as previous two but now we care about cost so we use a priority queue

    start_state = problem.getStartState()
    fringe = PriorityQueue()
    path_curr = PriorityQueue()
    visited_list = []
    outp = []

    # leave the start state and begin UCS
    fringe.push(start_state, 0)
    state = fringe.pop()

    # UCS code from lecture
    while not problem.isGoalState(state):
        if state not in visited_list:
            successor_list = problem.getSuccessors(state)
            visited_list.append(state)
            # update fringe and current path lists
            for child, direction, cost in successor_list:   # we still don't use cost :(
                tmp = outp[:]
                tmp.append(direction)
                # don't forget about cost
                path_cost = problem.getCostOfActions(tmp)
                if child not in visited_list:    
                    path_curr.push(tmp, path_cost)
                    fringe.push(child, path_cost)
        state = fringe.pop()
        outp = path_curr.pop()
        
    return outp

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # same as UCS but add heuristic value to cost (null means no change)

    start_state = problem.getStartState()
    fringe = PriorityQueue()
    path_curr = PriorityQueue()
    visited_list = []
    outp = []

    # leave the start state and begin UCS
    fringe.push(start_state, 0)
    state = fringe.pop()

    # UCS code from lecture
    while not problem.isGoalState(state):
        if state not in visited_list:
            successor_list = problem.getSuccessors(state)
            visited_list.append(state)
            # update fringe and current path lists
            for child, direction, cost in successor_list:   # we still don't use cost :(
                tmp = outp[:]
                tmp.append(direction)
                # don't forget about cost
                path_cost = problem.getCostOfActions(tmp) + heuristic(child, problem)   # + heuristic this time
                if child not in visited_list:    
                    path_curr.push(tmp, path_cost)
                    fringe.push(child, path_cost)
        state = fringe.pop()
        outp = path_curr.pop()
        
    return outp


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
