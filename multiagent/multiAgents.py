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

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
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

    def evaluationFunction(self, currentGameState, action):
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
        count, score = 0, 0
        for ghost in newGhostStates:
            GhostPosition = ghost.getPosition()
            if manhattanDistance(newPos, GhostPosition) <= 2:
                return -float('inf')

        for FoodPosition in newFood.asList():
            count += (1.0 / manhattanDistance(newPos, FoodPosition))
          
        return successorGameState.getScore() + count

def scoreEvaluationFunction(currentGameState):
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

    def getAction(self, gameState):
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
        v, action = -float('inf'), None
        for a in gameState.getLegalActions(self.index):
            successor = gameState.generateSuccessor(self.index, a)
            result = self.value(successor, self.index, 0)
            v = max(v, result)
            if v == result:
                action = a

        return action

    def max_value(self, state, index, depth):
        v = -float('inf')
        for a in state.getLegalActions(index):
            successor = state.generateSuccessor(index, a)
            v = max(v, self.value(successor, index, depth))
        return v

    def min_value(self, state, index, depth):
        v = float('inf')
        for a in state.getLegalActions(index):
            successor = state.generateSuccessor(index, a)
            v = min(v, self.value(successor, index, depth))
        return v
        

    def value(self, state, index, depth):
        index = (index+1) % state.getNumAgents()

        if depth == self.depth or state.isWin() or state.isLose():
            return self.evaluationFunction(state)
        elif index == self.index:
            return self.max_value(state, index, depth)
        else:
            return self.min_value(state, index, depth + (index+1)/state.getNumAgents())

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        v, action = -float('inf'), None
        alpha, beta = -float('inf'), float('inf')
        for a in gameState.getLegalActions(self.index):
            successor = gameState.generateSuccessor(self.index, a)
            result = self.value(successor, self.index, 0, alpha, beta)
            v = max(v, result)
            if v == result:
                action = a
            if v > beta:
                return v
            alpha = max(alpha, v)

        return action

    def max_value(self, state, index, depth, alpha, beta):
        v = -float('inf')
        for a in state.getLegalActions(index):
            successor = state.generateSuccessor(index, a)
            v = max(v, self.value(successor, index, depth, alpha, beta))
            if v > beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(self, state, index, depth, alpha, beta):
        v = float('inf')
        for a in state.getLegalActions(index):
            successor = state.generateSuccessor(index, a)
            v = min(v, self.value(successor, index, depth, alpha, beta))
            if v < alpha:
                return v
            beta = min(beta, v)
        return v

    def value(self, state, index, depth, alpha, beta):
        index = (index+1) % state.getNumAgents()

        if depth == self.depth or state.isWin() or state.isLose():
            return self.evaluationFunction(state)
        elif index == self.index:
            return self.max_value(state, index, depth, alpha, beta)
        else:
            return self.min_value(state, index, depth + (index+1)/state.getNumAgents(), alpha, beta)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        v, action = -float('inf'), None
        for a in gameState.getLegalActions(self.index):
            successor = gameState.generateSuccessor(self.index, a)
            result = self.value(successor, self.index, 0)
            v = max(v, result)
            if v == result:
                action = a

        return action

    def value(self, state, index, depth):
        index = (index+1) % state.getNumAgents()

        if depth == self.depth or state.isWin() or state.isLose():
            return self.evaluationFunction(state)
        elif index == self.index:
            return self.max_value(state, index, depth)
        else:
            return self.exp_value(state, index, depth + (index+1)/state.getNumAgents())


    def max_value(self, state, index, depth):
        v = -float('inf')
        for a in state.getLegalActions(index):
            successor = state.generateSuccessor(index, a)
            v = max(v, self.value(successor, index, depth))
        return v


    def exp_value(self, state, index, depth):
        v, actions = 0, state.getLegalActions(index)
        for a in actions:
            successor = state.generateSuccessor(index, a)
            v += self.value(successor, index, depth)
        return v / float(len(actions))

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: check ghost first since you might die.
                   check food now
                   check power
                   if scare time is really low, then ghost is scary, so i make ghost level high, also power is important
                   if scaretime is plenty, then ghost is not even a problem and food is important


    """
    "*** YOUR CODE HERE ***"
    ghost_level = 0
    food_level = 0
    power_level = 0
    counter = 0
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newGhostPosition = currentGameState.getGhostPositions()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    newPower = currentGameState.getCapsules()

    for ghosts in newGhostPosition:
        ghost_dis = manhattanDistance(newPos, ghosts)
        if ghost_dis <= 5:
            if ghosts[0] != newPos[0] or ghosts[1] != newPos[1]:
                ghost_level += -50
            else:
                ghost_level += -80
        else:
            ghost_level += -ghost_dis

    for food in newFood.asList():
        food_dis = manhattanDistance(newPos, food)
        if food_dis != 0:
            food_level += 1.0/food_dis
    for power in newPower:
        power_dis = manhattanDistance(newPos, power)
        if power_dis != 0:
            power_level += 1.0/power_dis

    for t in newScaredTimes:
        if t<1:
            score = 50*currentGameState.getScore()+70*ghost_level+60*food_level+20*power_level
            # print("food level: ")
            # print(food_level)
            # print("ghost level: ")
            # print(ghost_level)
            # print("normal: ")
            # print(score)
            return score
    return 50*currentGameState.getScore()+50*food_level
# Abbreviation
better = betterEvaluationFunction

