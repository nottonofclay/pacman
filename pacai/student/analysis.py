"""
Analysis question.
Change these default values to obtain the specified policies through value iteration.
If any question is not possible, return just the constant NOT_POSSIBLE:
```
return NOT_POSSIBLE
```
"""

NOT_POSSIBLE = None

def question2():
    """
    I decreased the noise to 0, this made it so that the
    agent would always take the optimal action instead of
    killing itself.
    """

    answerDiscount = 0.9
    answerNoise = 0

    return answerDiscount, answerNoise


def question3a():
    """
    I decreased the discount so that the agent
    took the closer route to the goal and increased the
    living reward so that the agent would be more willing
    to take risks I also decreased the noise so that the
    agent would try the quickest solution to the goal.
    """

    answerDiscount = 0.4
    answerNoise = 0.1
    answerLivingReward = -3.5

    return answerDiscount, answerNoise, answerLivingReward


def question3b():
    """
    I again decreased the discount so that the agent
    took the closer exit and kept the living reward and
    noise the same as the defaults as those avoided the cliffs.
    """

    answerDiscount = 0.1
    answerNoise = 0.1
    answerLivingReward = 0

    return answerDiscount, answerNoise, answerLivingReward


def question3c():
    """
    Kept most of the defaults, increased the discount
    and decreased the noise so that the agent wouldn't
    walk around aimlessly too much.
    """

    answerDiscount = 0.9
    answerNoise = 0.1
    answerLivingReward = -0.5

    return answerDiscount, answerNoise, answerLivingReward


def question3d():
    """
    Decreased discount so that the agent would take fewer
    steps to the goal and increased the noise so that the
    agent would take a more optimal route to the goal. Kept
    the discount higher than trying to get to the closest
    exit because it allowed for more moves.
    """

    answerDiscount = 0.9
    answerNoise = 0.2
    answerLivingReward = 0.0

    return answerDiscount, answerNoise, answerLivingReward


def question3e():
    """
    Significantly increased the living reward so that the
    agent would avoid the cliffs. Increased the discount
    by a lot so that the agent would be willing to make
    a lot of moves and turned the noise to 0 so that it
    wouldn't explore options once it reached the optimal
    spot.
    """

    answerDiscount = 0.99
    answerNoise = 0.0
    answerLivingReward = 99999

    return answerDiscount, answerNoise, answerLivingReward


def question6():
    """
    Increased the epsilon so that the agent would explore
    further pathways
    """

    # answerEpsilon = 0.5
    # answerLearningRate = 10

    return NOT_POSSIBLE


if __name__ == '__main__':
    questions = [
        question2,
        question3a,
        question3b,
        question3c,
        question3d,
        question3e,
        question6,
    ]

    print('Answers to analysis questions:')
    for question in questions:
        response = question()
        print('    Question %-10s:\t%s' % (question.__name__, str(response)))
