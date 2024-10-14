from pacai.agents.learning.value import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
    A value iteration agent.

    Make sure to read `pacai.agents.learning` before working on this class.

    A `ValueIterationAgent` takes a `pacai.core.mdp.MarkovDecisionProcess` on initialization,
    and runs value iteration for a given number of iterations using the supplied discount factor.

    Some useful mdp methods you will use:
    `pacai.core.mdp.MarkovDecisionProcess.getStates`,
    `pacai.core.mdp.MarkovDecisionProcess.getPossibleActions`,
    `pacai.core.mdp.MarkovDecisionProcess.getTransitionStatesAndProbs`,
    `pacai.core.mdp.MarkovDecisionProcess.getReward`.

    Additional methods to implement:

    `pacai.agents.learning.value.ValueEstimationAgent.getQValue`:
    The q-value of the state action pair (after the indicated number of value iteration passes).
    Note that value iteration does not necessarily create this quantity,
    and you may have to derive it on the fly.

    `pacai.agents.learning.value.ValueEstimationAgent.getPolicy`:
    The policy is the best action in the given state
    according to the values computed by value iteration.
    You may break ties any way you see fit.
    Note that if there are no legal actions, which is the case at the terminal state,
    you should return None.
    """

    def __init__(self, index, mdp, discountRate = 0.9, iters = 100, **kwargs):
        super().__init__(index, **kwargs)

        self.mdp = mdp
        self.discountRate = discountRate
        self.iters = iters
        self.values = {}  # A dictionary which holds the q-values for each state.

        # Compute the values here.

        for state in mdp.getStates():
            # self.values[state] = self.getValue(state)
            self.values[state] = 0
        for i in range(self.iters):
            next_values = {}
            for state in mdp.getStates():
                q_values = []
                for action in self.mdp.getPossibleActions(state):
                    q_values.append(self.getQValue(state, action))
                init_val = self.values.get(state, 0)
                next_values[state] = max(q_values, default=init_val)
            self.values = next_values

    def getValue(self, state):
        """
        Return the value of the state (computed in __init__).
        """

        return self.values.get(state, 0.0)

    def getAction(self, state):
        """
        Returns the policy at the state (no exploration).
        """

        return self.getPolicy(state)

    def getQValue(self, state, action):
        """
        Returns the q-value of the state action pair.
        """
        probilities = self.mdp.getTransitionStatesAndProbs(state, action)
        q_value = 0
        for probility in probilities:
            state_prob, prob = probility
            reward = self.mdp.getReward(state, action, state_prob)
            value = self.values.get(state_prob, 0.0)
            q_value += prob * (reward + (self.discountRate * value))
        return q_value

    def getPolicy(self, state):
        """
        Returns the policy at the state (no exploration).
        """

        if state == "TERMINAL_STATE":
            return None
        value = ("", -float('inf'))
        for action in self.mdp.getPossibleActions(state):
            temp = max(value[1], self.getQValue(state, action))
            if temp > value[1]:
                value = (action, temp)
        return value[0]
