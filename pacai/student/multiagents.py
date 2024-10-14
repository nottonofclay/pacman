import random
import math

from pacai.agents.base import BaseAgent
from pacai.agents.search.multiagent import MultiAgentSearchAgent
from pacai.core import distance


class ReflexAgent(BaseAgent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.
    You are welcome to change it in any way you see fit,
    so long as you don't touch the method headers.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        `ReflexAgent.getAction` chooses among the best options according to the evaluation function.

        Just like in the previous project, this method takes a
        `pacai.core.gamestate.AbstractGameState` and returns some value from
        `pacai.core.directions.Directions`.
        """

        # Collect legal moves.
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions.
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best.

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current `pacai.bin.pacman.PacmanGameState`
        and an action, and returns a number, where higher numbers are better.
        Make sure to understand the range of different values before you combine them
        in your evaluation function.
        """
        def add_tuples(tuple1, tuple2):
            x1, y1 = tuple1
            x2, y2 = tuple2
            return (x1 + x2, y1 + y2)

        # variables
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPosition = successorGameState.getPacmanPosition()
        food = currentGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()
        curGhostPositions = [state.getPosition() for state in newGhostStates]
        possibleDirections = [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)]

        # creating possible ghost positions
        possibleGhostPositions = []
        for direction in possibleDirections:
            for ghostPosition in curGhostPositions:
                position = add_tuples(ghostPosition, direction)
                possibleGhostPositions.append(position)
        score = 0

        # avoiding ghosts
        for ghostPosition in possibleGhostPositions:
            if ghostPosition == newPosition:
                return 0

        # finding closest food
        maxFood = 99999
        for food in food:
            maxFood = min(maxFood, distance.manhattan(food, newPosition))
        if maxFood == 0:
            maxFood = 1
        score = 1 / maxFood

        return score


class MinimaxAgent(MultiAgentSearchAgent):
    """
    A minimax agent.

    Here are some method calls that might be useful when implementing minimax.

    `pacai.core.gamestate.AbstractGameState.getNumAgents()`:
    Get the total number of agents in the game

    `pacai.core.gamestate.AbstractGameState.getLegalActions`:
    Returns a list of legal actions for an agent.
    Pacman is always at index 0, and ghosts are >= 1.

    `pacai.core.gamestate.AbstractGameState.generateSuccessor`:
    Get the successor game state after an agent takes an action.

    `pacai.core.directions.Directions.STOP`:
    The stop direction, which is always legal, but you may not want to include in your search.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction.
        """
        legalMoves = gameState.getLegalActions()
        # agent 0 is pacman
        sucStates = [gameState.generateSuccessor(self.index, action) for action in legalMoves]
        # agent 1 is first ghost, 0 is starting depth
        scores = [self.min_value(state, 1, 0) for state in sucStates]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)

        return legalMoves[chosenIndex]

    def min_value(self, gameState, ghostIndex, depth):
        # if game over
        if gameState.isOver():
            return self.getEvaluationFunction()(gameState)
        # if depth reached and on last ghost
        elif (depth >= self.getTreeDepth()) and (ghostIndex == gameState.getNumAgents() - 1):
            return self.evaluationFunction()(gameState)

        # generate ghost moves
        v = math.inf
        ghostSucStates = []
        for action in gameState.getLegalActions(ghostIndex):
            ghostSucStates.append(gameState.generateSuccessor(ghostIndex, action))

        # constructing tree of moves
        ghostScores = []
        for state in ghostSucStates:
            # recursing for each ghost
            if not ghostIndex == gameState.getNumAgents() - 1:
                ghostScores.append(self.min_value(state, ghostIndex + 1, depth))
            # last ghost, go down in depth, move on to pacman
            else:
                ghostScores.append(self.max_value(state, 0, depth + 1))
        v = min(ghostScores)
        return v

    def max_value(self, gameState, ghostIndex, depth):
        # if game over
        if gameState.isOver():
            return self.getEvaluationFunction()(gameState)
        # if depth reached
        elif (depth >= self.getTreeDepth()):
            return self.getEvaluationFunction()(gameState)

        # generate pacman moves
        v = -math.inf
        pacSucStates = []
        for action in gameState.getLegalActions(self.index):
            pacSucStates.append(gameState.generateSuccessor(ghostIndex, action))

        pacScores = []
        # generating ghost reponses to moves
        for state in pacSucStates:
            pacScores.append(self.min_value(state, 1, depth))

        v = max(pacScores)
        return v


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    A minimax agent with alpha-beta pruning.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction.
        """
        legalMoves = gameState.getLegalActions()
        # agent 0 is pacman
        sucStates = [gameState.generateSuccessor(self.index, action) for action in legalMoves]
        # agent 1 is first ghost, 0 is starting depth
        alpha = -math.inf
        beta = math.inf
        scores = [self.min_value(state, 1, 0, alpha, beta) for state in sucStates]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)

        return legalMoves[chosenIndex]

    def min_value(self, gameState, ghostIndex, depth, alpha, beta):
        # if game over
        if gameState.isOver():
            return self.getEvaluationFunction()(gameState)
        # if depth reached and on last ghost
        elif (depth >= self.getTreeDepth()) and (ghostIndex == gameState.getNumAgents() - 1):
            return self.evaluationFunction()(gameState)

        # generate ghost moves
        v = math.inf
        ghostSucStates = []
        for action in gameState.getLegalActions(ghostIndex):
            ghostSucStates.append(gameState.generateSuccessor(ghostIndex, action))

        # constructing tree of moves
        ghostScores = []
        for state in ghostSucStates:
            # recursing for each ghost
            if not ghostIndex == gameState.getNumAgents() - 1:
                ghostScores.append(self.min_value(state, ghostIndex + 1, depth, alpha, beta))
            # last ghost, go down in depth, move on to pacman
            else:
                ghostScores.append(self.max_value(state, 0, depth + 1, alpha, beta))

        # might not work fast enough
        v = min(ghostScores)
        if v <= alpha:
            return v
        beta = min(beta, v)

        return v

    def max_value(self, gameState, ghostIndex, depth, alpha, beta):
        # if game over
        if gameState.isOver():
            return self.getEvaluationFunction()(gameState)
        # if depth reached
        elif (depth >= self.getTreeDepth()):
            return self.getEvaluationFunction()(gameState)

        # generate pacman moves
        v = -math.inf
        pacSucStates = []
        for action in gameState.getLegalActions(self.index):
            pacSucStates.append(gameState.generateSuccessor(ghostIndex, action))

        pacScores = []
        # generating ghost reponses to moves
        for state in pacSucStates:
            pacScores.append(self.min_value(state, 1, depth, alpha, beta))

        v = max(pacScores)
        if v >= beta:
            return v
        alpha = max(alpha, v)

        return v


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    An expectimax agent.

    All ghosts should be modeled as choosing uniformly at random from their legal moves.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the expectimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction.
        """
        legalMoves = gameState.getLegalActions()
        # agent 0 is pacman
        sucStates = [gameState.generateSuccessor(self.index, action) for action in legalMoves]
        # agent 1 is first ghost, 0 is starting depth
        alpha = -math.inf
        beta = math.inf
        scores = [self.min_value(state, 1, 0, alpha, beta) for state in sucStates]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)

        return legalMoves[chosenIndex]

    def min_value(self, gameState, ghostIndex, depth, alpha, beta):
        # if game over
        if gameState.isOver():
            return self.getEvaluationFunction()(gameState)
        # if depth reached and on last ghost
        elif (depth >= self.getTreeDepth()) and (ghostIndex == gameState.getNumAgents() - 1):
            return self.evaluationFunction()(gameState)

        # generate ghost moves
        v = math.inf
        ghostSucStates = []
        for action in gameState.getLegalActions(ghostIndex):
            ghostSucStates.append(gameState.generateSuccessor(ghostIndex, action))

        # constructing tree of moves
        ghostScores = []
        for state in ghostSucStates:
            # recursing for each ghost
            if not ghostIndex == gameState.getNumAgents() - 1:
                ghostScores.append(self.min_value(state, ghostIndex + 1, depth, alpha, beta))
            # last ghost, go down in depth, move on to pacman
            else:
                ghostScores.append(self.max_value(state, 0, depth + 1, alpha, beta))

        # might not work fast enough
        v = sum(ghostScores) / len(ghostScores)
        if v <= alpha:
            return v
        beta = min(beta, v)

        return v

    def max_value(self, gameState, ghostIndex, depth, alpha, beta):
        # if game over
        if gameState.isOver():
            return self.getEvaluationFunction()(gameState)
        # if depth reached
        elif (depth >= self.getTreeDepth()):
            return self.getEvaluationFunction()(gameState)

        # generate pacman moves
        v = -math.inf
        pacSucStates = []
        for action in gameState.getLegalActions(self.index):
            pacSucStates.append(gameState.generateSuccessor(ghostIndex, action))

        pacScores = []
        # generating ghost reponses to moves
        for state in pacSucStates:
            pacScores.append(self.min_value(state, 1, depth, alpha, beta))

        v = max(pacScores)
        if v >= beta:
            return v
        alpha = max(alpha, v)

        return v


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable evaluation function.

    DESCRIPTION: <write something here so we know what you did>
    """

    return currentGameState.getScore()


class ContestAgent(MultiAgentSearchAgent):
    """
    Your agent for the mini-contest.

    You can use any method you want and search to any depth you want.
    Just remember that the mini-contest is timed, so you have to trade off speed and computation.

    Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
    just make a beeline straight towards Pacman (or away if they're scared!)

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
