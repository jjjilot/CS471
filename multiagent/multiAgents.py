# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
    
        foods = currentGameState.getFood().asList()
        distance = []

        # never run into ghost
        for ghost in newGhostStates:
            if ghost.getPosition() == newPos:
                # if ghost in path make return value as bad as possible
                return -float("inf")
        # sum distance from foods (make negative so lower dist is better)
        for food in foods:
            distance.append(-1 * util.manhattanDistance(newPos, food))

        return max(distance)

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
       
        def maxFunc(gameState, depth):
            # default return
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState)

            max_sofar = -float("inf")
            # for each possible action move to min agent layer
            actions = gameState.getLegalActions(agentIndex = 0)
            for action in actions:
                max_sofar = max(max_sofar, minFunc(gameState.generateSuccessor(0, action),depth, 1))

            # track best score
            return max_sofar

        def minFunc(gameState, depth, ghost_num):
            # default return
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState)
            
            min_sofar = float("inf")
            # if there are more ghosts continue running on min agent layer
            actions = gameState.getLegalActions(agentIndex = ghost_num)
            if ghost_num != gameState.getNumAgents() - 1:                
                for action in actions:
                    min_sofar = min(min_sofar, minFunc(gameState.generateSuccessor(ghost_num, action), depth, ghost_num + 1))
            # otherwise move to max agent layer
            else:                    
                for action in actions:
                    min_sofar = min(min_sofar, maxFunc(gameState.generateSuccessor(gameState.getNumAgents() - 1, action), depth - 1))

            return min_sofar

        # main
        actions = gameState.getLegalActions()
        winner = Directions.STOP

        score = -float("inf")
        max_score = -float("inf")
        # begin on first layer (max agent)
        for action in actions:
            max_score = score
            score = max(score, minFunc(gameState.generateSuccessor(0, action), self.depth, 1))

            # track best score among branches
            if score > max_score:
                max_score = score
                winner = action

        return winner

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # same as minimax but add alpha/beta pruning

        def maxFunc(gameState, depth, alpha, beta):
            # default return
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState)

            max_sofar = -float("inf")
            # for each possible action move to min agent layer
            actions = gameState.getLegalActions(agentIndex = 0)
            for action in actions:
                max_sofar = max(max_sofar, minFunc(gameState.generateSuccessor(0, action),depth, 1, alpha, beta))
                #alpha time
                if beta < max_sofar:
                    return max_sofar
                alpha = max(alpha, max_sofar)
            # track best score
            return max_sofar

        def minFunc(gameState, depth, ghost_num, alpha, beta):
            # default return
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState)
            
            min_sofar = float("inf")
            # if there are more ghosts continue running on min agent layer
            actions = gameState.getLegalActions(agentIndex = ghost_num)
            if ghost_num != gameState.getNumAgents() - 1:                
                for action in actions:
                    min_sofar = min(min_sofar, minFunc(gameState.generateSuccessor(ghost_num, action), depth, ghost_num + 1, alpha, beta))
                    #beta time
                    if alpha > min_sofar:
                        return min_sofar
                    beta = min(beta, min_sofar)
            # otherwise move to max agent layer
            else:                    
                for action in actions:
                    min_sofar = min(min_sofar, maxFunc(gameState.generateSuccessor(gameState.getNumAgents() - 1, action), depth - 1, alpha, beta))
                    #beta time (2)
                    if alpha > min_sofar:
                        return min_sofar
                    beta = min(beta, min_sofar)
            return min_sofar

        # main
        actions = gameState.getLegalActions()
        winner = Directions.STOP
        alpha = -float("inf")
        beta = float("inf")
        score = -float("inf")
        max_score = -float("inf")

        # begin on first layer (max agent)
        for action in actions:
            max_score = score
            score = max(score, minFunc(gameState.generateSuccessor(0, action), self.depth, 1, alpha, beta))

            # track best score among branches
            if score > max_score:
                max_score = score
                winner = action
            # alpha/beta time
            if beta < score:
                return winner
            alpha = max(alpha, max_score)

        return winner


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        # same as minimax but with expecti

        def maxFunc(gameState, depth):
            # default return
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState)

            max_sofar = -float("inf")
            # for each possible action move to min agent layer
            actions = gameState.getLegalActions(agentIndex = 0)
            for action in actions:
                max_sofar = max(max_sofar, expectFunc(gameState.generateSuccessor(0, action),depth, 1))

            # track best score
            return max_sofar

        def expectFunc(gameState, depth, ghost_num):
            # default return
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState)
            
            expect_val = 0
            # if there are more ghosts continue running on expect agent layer
            actions = gameState.getLegalActions(agentIndex = ghost_num)
            # new value for calculating avg later
            length = len(actions)
            if ghost_num != gameState.getNumAgents() - 1:                
                for action in actions:
                    expect_val += expectFunc(gameState.generateSuccessor(ghost_num, action), depth, ghost_num + 1)
            # otherwise move to max agent layer
            else:                    
                for action in actions:
                    expect_val += maxFunc(gameState.generateSuccessor(gameState.getNumAgents() - 1, action), depth - 1)

            avg = expect_val / length
            return avg

        # main
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        
        actions = gameState.getLegalActions()
        winner = Directions.STOP

        score = -float("inf")
        max_score = -float("inf")
        # begin on first layer (max agent)
        for action in actions:
            max_score = score
            score = max(score, expectFunc(gameState.generateSuccessor(0, action), self.depth, 1))

            # track best score among branches
            if score > max_score:
                max_score = score
                winner = action

        return winner

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    # useful vals
    pos = currentGameState.getPacmanPosition()
    foods = currentGameState.getFood()
    food_list = foods.asList()    
    capsules = currentGameState.getCapsules()

    # find closest food
    min_dist = -1
    for food in food_list:
        min_dist = min(min_dist, util.manhattanDistance(pos, food))
        if min_dist == -1:
            min_dist =  util.manhattanDistance(pos, food)

    # find avg ghost dist
    ghost_dist = 1
    for ghost in currentGameState.getGhostPositions():
        ghost_dist += util.manhattanDistance(pos, ghost)
    
    # combine reciprocals with appropriate signs
    return currentGameState.getScore() + (1 / min_dist) - (1 / ghost_dist) - len(capsules)

# Abbreviation
better = betterEvaluationFunction
