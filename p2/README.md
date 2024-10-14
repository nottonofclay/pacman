    For example, Sammy Slug would have a `config.json` for P1 that looks like:

```json
    {
        "course": "CSE140-S24",
        "assignment": "p2",
        "server": "http://lighthouse.soe.ucsc.edu",
        "user": "sslug@ucsc.edu",
        "pass": "1234567890"
    }
```

When you are ready to submit,
    you can do so using the command:

```sh
    python3 -m autograder.cli.submit pacai/student/multiagents.py
```

#### Question 1 (3 points)

Improve the [ReflexAgent](https://ucsc-cse-140.github.io/student/multiagents.html#pacai.student.multiagents.ReflexAgent) to play respectably.
               Reflex agent provides some helpful methods that call into [GameState](https://ucsc-cse-140.github.io/core/gamestate.html#pacai.core.gamestate.AbstractGameState) for information.
               A capable reflex agent will have to consider both food locations and ghost locations to perform well.
               Your agent should easily and reliably clear the `testClassic` layout:

`
               python3 -m pacai.bin.pacman --pacman ReflexAgent --layout testClassic
            `

Try out your reflex agent on the default `mediumClassic` layout with one and two ghosts:

`
               python3 -m pacai.bin.pacman --pacman ReflexAgent --num-ghosts 1
            `

`
               python3 -m pacai.bin.pacman --pacman ReflexAgent --num-ghosts 2
            `

How does your agent fare?
               It will likely often die with 2 ghosts on the default board,
               unless your evaluation function is quite good.

_Notes:_

* You can never have more than two ghosts on `mediumClassic`.
* As features, try the reciprocal of important values (such as distance to food) rather than just the values themselves.
* The evaluation function you're writing is evaluating state-action pairs; in later parts of the project, you'll be evaluating states.

_Options:_
Default ghosts are random;
               you can also play for fun with slightly smarter directional ghosts using `--ghosts DirectionalGhost`.
               If the randomness is preventing you from telling whether your agent is improving, you can use `--seed [NUMBER]` to run with a seed.
               You can also play multiple games in a row with `--num-games [NUMBER]`.
               Turn off graphics with `--null-graphics` to run lots of games quickly.

The autograder will check that your agent can rapidly clear the
               `openClassic` layout ten times without dying more than twice or thrashing around infinitely
               (i.e. repeatedly moving back and forth between two positions, making no progress).

`
               python3 -m pacai.bin.pacman --pacman ReflexAgent --layout openClassic --num-games 10 --null-graphics
            `

Don't spend too much time on this question, though, as the meat of the project lies ahead.

#### Question 2 (5 points)

Now you will write an adversarial search agent in [pacai.student.multiagents.MinimaxAgent](https://ucsc-cse-140.github.io/student/multiagents.html#pacai.student.multiagents.MinimaxAgent).
               Your minimax agent should work with any number of ghosts.
               This means you will have to write an algorithm that is slightly more general than what appears in the textbook.
               In particular, your minimax tree will have multiple min layers (one for each ghost) for every max layer.

Your code should also expand the game tree to an arbitrary depth.
               Score the leaves of your minimax tree with the evaluation function supplied by the parent class: [MultiAgentSearchAgent.getEvaluationFunction()](https://ucsc-cse-140.github.io/agents/search/multiagent.html#pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction).
               You can invoke it like: `self.getEvaluationFunction()(state)`.

_Important:_
A single search **ply** is considered to be one Pac-Man move and all the ghosts' responses, so depth 2 search will involve Pac-Man and each ghost moving two times.

##### Hints and Observations:

* The evaluation function in this part is already written.
                     You shouldn't change this function, but recognize that now we're evaluating **states** rather than actions, as we were for the reflex agent.
                     Look-ahead agents evaluate future states whereas reflex agents evaluate actions from the current state.
* The minimax values of the initial state in the `minimaxClassic` layout are 9, 8, 7, and -492 for depths 1, 2, 3, and 4 respectively.
                     Note that your minimax agent will often win (665/1000 games for us) despite the dire prediction of depth 4 minimax. `
                     python3 -m pacai.bin.pacman --pacman MinimaxAgent --layout minimaxClassic --agent-args depth=4
                  `
* To increase the search depth achievable by your agent,
                     remove the [Directions.STOP](https://ucsc-cse-140.github.io/core/directions.html#pacai.core.directions.Directions.STOP) action from Pac-Man's list of possible actions.
                     Depth 2 should be pretty quick, but depth 3 or 4 will be slow.
                     Don't worry, the next question will speed up the search somewhat.
* Pac-Man is always agent 0, and the agents move in order of increasing agent index.
* All states in minimax should be a [PacmanGameState](https://ucsc-cse-140.github.io/bin/pacman.html#pacai.bin.pacman.PacmanGameState).
                     They are either passed in to [MinimaxAgent.getAction](https://ucsc-cse-140.github.io/student/multiagents.html#pacai.student.multiagents.MinimaxAgent)
                     or generated via [PacmanGameState.generateSuccessor](https://ucsc-cse-140.github.io/bin/pacman.html#pacai.bin.pacman.PacmanGameState.generateSuccessor).
                     In this project, you will not be abstracting to simplified states.
* On larger boards such as `openClassic` and `mediumClassic`, you'll find Pac-Man to be good at not dying, but quite bad at winning.
                     He'll often thrash around without making progress.
                     He might even thrash around right next to a dot without eating it because he doesn't know where he'd go after eating that dot.
                     Don't worry if you see this behavior, question 5 will clean up all of these issues.
* When Pac-Man believes that death is unavoidable,
                     they will try to end the game as soon as possible because of the constant penalty for living.
                     Sometimes, this is the wrong thing to do with random ghosts, but minimax agents always assume the worst: `
                     python3 -m pacai.bin.pacman --pacman MinimaxAgent --layout trappedClassic --agent-args depth=3
                  ` Make sure you understand why Pac-Man rushes the closest ghost in this case.

#### Question 3 (4 points)

Make a new agent that uses alpha-beta pruning to more efficiently explore the minimax tree in [pacai.student.multiagents.AlphaBetaAgent](https://ucsc-cse-140.github.io/student/multiagents.html#pacai.student.multiagents.AlphaBetaAgent).
               Again, your algorithm will be slightly more general than the pseudo-code in the textbook.
               Part of the challenge is to extend the alpha-beta pruning logic appropriately to multiple minimizer agents.

You should see a speed-up (perhaps depth 3 alpha-beta will run as fast as depth 2 minimax).
               Ideally, depth 3 on `smallClassic` should run in just a few seconds per move or faster.

`
               python3 -m pacai.bin.pacman --pacman AlphaBetaAgent --agent-args depth=3 --layout smallClassic
            `

The [AlphaBetaAgent](https://ucsc-cse-140.github.io/student/multiagents.html#pacai.student.multiagents.AlphaBetaAgent) minimax values should be identical to the [MinimaxAgent](https://ucsc-cse-140.github.io/student/multiagents.html#pacai.student.multiagents.MinimaxAgent) minimax values.
               Although the actions it selects can vary because of different tie-breaking behavior.
               Again, the minimax values of the initial state in the `minimaxClassic` layout are 9, 8, 7, and -492 for depths 1, 2, 3, and 4 respectively.

#### Question 4 (4 points)

Random ghosts are of course not optimal minimax agents, and so modeling them with minimax search may not be appropriate.
               Fill in [pacai.student.multiagents.ExpectimaxAgent](https://ucsc-cse-140.github.io/student/multiagents.html#pacai.student.multiagents.ExpectimaxAgent),
               where the expectation is according to your agent's model of how the ghosts act.
               To simplify your code, assume you will only be running against a [RandomGhost](https://ucsc-cse-140.github.io/agents/ghost/random.html#pacai.agents.ghost.random.RandomGhost).
               These ghosts choose amongst their legal actions uniformly at random.

You should now observe a more cavalier approach in close quarters with ghosts.
               In particular, if Pac-Man perceives that he could be trapped but might escape to grab a few more pieces of food, he'll at least try.
               Investigate the results of these two scenarios:

`
               python3 -m pacai.bin.pacman --pacman AlphaBetaAgent --layout trappedClassic --agent-args depth=3 --null-graphics --num-games 10
            `

`
               python3 -m pacai.bin.pacman --pacman ExpectimaxAgent --layout trappedClassic --agent-args depth=3 --null-graphics --num-games 10
            `

You should find that your [ExpectimaxAgent](https://ucsc-cse-140.github.io/student/multiagents.html#pacai.student.multiagents.ExpectimaxAgent) wins about half the time,
               while your [AlphaBetaAgent](https://ucsc-cse-140.github.io/student/multiagents.html#pacai.student.multiagents.AlphaBetaAgent) always loses.
               Make sure you understand why the behavior here differs from the minimax case.

#### Question 5 (4 points)

Write a better evaluation function for pacman in the provided function [pacai.student.multiagents.betterEvaluationFunction](https://ucsc-cse-140.github.io/student/multiagents.html#pacai.student.multiagents.betterEvaluationFunction).
               The evaluation function should evaluate states, rather than actions like your reflex agent evaluation function did.
               You may use any tools at your disposal for evaluation, including your search code from the last project.
               With depth 2 search, your evaluation function should clear the `smallClassic` layout with two random ghosts more than half the time and still run at a reasonable rate.
               To get full credit, Pac-Man should be averaging around 1000 points when he's winning.

`
               python3 -m pacai.bin.pacman --layout smallClassic --pacman ExpectimaxAgent --agent-args evalFn=pacai.student.multiagents.betterEvaluationFunction --null-graphics --num-games 10
            `

Document your evaluation function!
               We're very curious about what great ideas you have, so don't be shy.
               We reserve the right to reward bonus points for clever solutions and show demonstrations in class.

##### Hints and Observations:

* As for your reflex agent evaluation function, you may want to use the reciprocal of important values (such as distance to food) rather than the values themselves.
* One way you might want to write your evaluation function is to use a linear combination of features.
                     That is, compute values for features about the state that you think are important.
                     Then combine those features by multiplying them by different values and adding the results together.
                     You might decide what to multiply each feature by based on how important you think it is.

#### Mini Contest (3 points extra credit)

Pac-Man's been doing well so far, but things are about to get a bit more challenging.
               This time, we'll pit Pac-Man against smarter foes in a trickier maze.
               In particular, the ghosts will actively chase Pac-Man instead of wandering around randomly and the maze features more twists and dead-ends!
               Extra pellets are given to give Pac-Man a fighting chance.
               You're free to have Pac-Man use any search procedure, search depth, and evaluation function you like.
               The only limit is that games can last a maximum of 3 minutes (with graphics off), so be sure to use your computation wisely.
               We'll run the contest with the following command:

`
               python3 -m pacai.bin.pacman --layout contestClassic --pacman ContestAgent --ghosts DirectionalGhost --null-graphics --num-games 10
            `

The three students with the highest score will receive 3, 2, and 1 extra credit points respectively and can look on with pride as their Pac-Man agents are shown off in class.
               Details: we run 10 games, games longer than 3 minutes get score 0, lowest and highest 2 scores discarded, the rest averaged.
               Be sure to document what your agent is doing, as we may award additional extra credit to creative solutions even if they're not in the top 3.

_Project 2 is done.
                  Go Pac-Man!_
