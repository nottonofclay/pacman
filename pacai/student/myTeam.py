# from pacai.agents.capture import dummy
from pacai.core.directions import Directions
from pacai.agents.capture.reflex import ReflexCaptureAgent


def createTeam(firstIndex, secondIndex, isRed,
               first='pacai.student.myTeam.offenseAgent',
               second='pacai.student.myTeam.defenseAgent'):
    """
    This function should return a list of two agents that will form the capture team,
    initialized using firstIndex and secondIndex as their agent indexed.
    isRed is True if the red team is being created,
    and will be False if the blue team is being created.
    """

    firstAgent = offenseAgent
    secondAgent = defenseAgent

    return [
        firstAgent(firstIndex),
        secondAgent(secondIndex),
    ]


class defenseAgent(ReflexCaptureAgent):

    def getFeatures(self, gameState, action):
        features = {
            'numInvaders': 0,
            'onDefense': 0,
            'invaderDistance': 0,
            'stop': 0,
            'reverse': 0,
            'runAway': 0,
            'enemyDistance': 0
        }

        successor = self.getSuccessor(gameState, action)
        myState = successor.getAgentState(self.index)
        myPos = myState.getPosition()

        # Computes whether we're on defense (1) or offense (0).
        features['onDefense'] = 1
        if (myState.isPacman()):
            features['onDefense'] = 0

        # Computes distance to invaders we can see.
        enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        invaders = [a for a in enemies if a.isPacman() and a.getPosition() is not None]
        features['numInvaders'] = len(invaders)

        if (len(invaders) > 0):
            dists = []
            for enemy in invaders:
                dists.append(self.getMazeDistance(myPos, enemy.getPosition()))
            features['invaderDistance'] = min(dists)

            for enemy in invaders:
                if features['invaderDistance'] < 2 and not myState.isBraveGhost():
                    features['runAway'] = 1

        enemyDistances = []
        for enemy in enemies:
            enemyDistances.append(self.getMazeDistance(myPos, enemy.getPosition()))
        features['enemyDistance'] = min(enemyDistances)

        if (action == Directions.STOP):
            features['stop'] = 1

        rev = Directions.REVERSE[gameState.getAgentState(self.index).getDirection()]
        if (action == rev):
            features['reverse'] = 1

        return features

    def getWeights(self, gameState, action):
        return {
            'numInvaders': -1000,
            'onDefense': 100,
            'invaderDistance': -10,
            'stop': -100,
            'reverse': -2,
            'runAway': -1000,
            'enemyDistance': -5
        }

    def evaluate(self, gameState, action):
        features = self.getFeatures(gameState, action)
        weights = self.getWeights(gameState, action)
        value = 0

        for feature in features:
            value += features[feature] * weights[feature]

        return value

    def getAction(self, gameState):
        actions = gameState.getLegalActions(self.index)
        values = []
        maxValue = -float('inf')

        for action in actions:
            value = self.evaluate(gameState, action)
            values.append((value, action))
            if value > maxValue:
                maxValue = value

        for element in values:
            value, action = element
            # return action
            if value == maxValue:
                return action


class offenseAgent(ReflexCaptureAgent):

    def getFeatures(self, gameState, action):
        features = {
            'successorScore': 0,
            'distanceToFood': 0,
            'runAway': 0,
            'capsule': 0
        }

        successor = self.getSuccessor(gameState, action)
        capsules = gameState.getCapsules()
        enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        myState = successor.getAgentState(self.index)
        myPos = myState.getPosition()
        features['successorScore'] = self.getScore(successor)

        # Compute distance to the nearest food.
        foodList = self.getFood(successor).asList()

        # This should always be True, but better safe than sorry.
        if (len(foodList) > 0):
            minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
            features['distanceToFood'] = minDistance

        for enemy in enemies:
            if self.getMazeDistance(myPos, enemy.getPosition()) < 2 and myState.isPacman():
                features['runAway'] = 1

        minCapsuleDistance = min([self.getMazeDistance(myPos, capsule) for capsule in capsules])
        features['capsule'] = minCapsuleDistance

        return features
    def getWeights(self, gameState, action):
        return {
            'successorScore': 100,
            'distanceToFood': -2,
            'runAway': -100,
            'capsule': -1
        }

    def evaluate(self, gameState, action):
        features = self.getFeatures(gameState, action)
        weights = self.getWeights(gameState, action)
        value = 0

        for feature in features:
            value += features[feature] * weights[feature]

        return value

    def getAction(self, gameState):
        actions = gameState.getLegalActions(self.index)
        values = []
        maxValue = -float('inf')

        for action in actions:
            value = self.evaluate(gameState, action)
            values.append((value, action))
            if value > maxValue:
                maxValue = value

        for element in values:
            value, action = element
            # return action
            if value == maxValue:
                return action
