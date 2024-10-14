"""
In this file, you will implement generic search algorithms which are called by Pacman agents.
"""

from pacai.util.stack import Stack
from pacai.util.priorityQueue import PriorityQueue
from pacai.util.queue import Queue 

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first [p 85].

    Your search algorithm needs to return a list of actions that reaches the goal.
    Make sure to implement a graph search algorithm [Fig. 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
        ```
    print("Start: %s" % (str(problem.startingState())))
    ((coord), 'direction', value)
    print("Is the start a goal?: %s" % (problem.isGoal(problem.startingState())))
    print("Start's successors: %s" % (problem.successorStates(problem.startingState())))
    ```
    """
    
    stack = Stack() 
    visited = set()
    stack.push((problem.startingState(), [], 0))
    # result = 0
    while not stack.isEmpty():
        node = stack.pop()
        if problem.isGoal(node[0]):
            # path = [item[1] for item in stack.list]
            return node[1]

        if node[0] not in visited:
            visited.add(node[0])
            for child in problem.successorStates(node[0]):
                stack.push((child[0], node[1]+[child[1]], node[2]+child[2]))
    return 0;


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    """

    queue = Queue()
    visited = set()
    queue.push((problem.startingState(), [], 0))
    # result = 0
    while not queue.isEmpty():
        node = queue.pop()
        if problem.isGoal(node[0]):
            # path = [item[1] for item in stack.list]
            return node[1]

        if node[0] not in visited:
            visited.add(node[0])
            for child in problem.successorStates(node[0]):
                queue.push((child[0], node[1]+[child[1]], node[2]+child[2]))
    return 0;



def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """

    # *** Your Code Here ***
    prioqueue = PriorityQueue()
    visited = set()
    prioqueue.push((problem.startingState(), [], 0) ,0)
    # result = 0
    while not prioqueue.isEmpty():
        node = prioqueue.pop()
        if problem.isGoal(node[0]):
            # path = [item[1] for item in stack.list]
            return node[1]

        if node[0] not in visited:
            visited.add(node[0])
            for child in problem.successorStates(node[0]):
                prioqueue.push((child[0], node[1]+[child[1]], node[2]+child[2]), node[2]+child[2])
    return 0;


def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    prioqueue = PriorityQueue()
    visited = set()
    prioqueue.push((problem.startingState(), [], 0) ,0)
    # result = 0
    while not prioqueue.isEmpty():
        node = prioqueue.pop()
        if problem.isGoal(node[0]):
            # path = [item[1] for item in stack.list]
            return node[1]

        if node[0] not in visited:
            visited.add(node[0])
            for child in problem.successorStates(node[0]):
                prioqueue.push((child[0], node[1]+[child[1]], heuristic(node[0], problem)), heuristic(node[0], problem))
    return 0;


    # *** Your Code Here ***
