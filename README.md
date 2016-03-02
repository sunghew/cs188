# cs188
## Overview
This is a repository for our implementations of the CS 188 Spring 2016 projects. To see instructions similar to the ones we had, check out [berkeley ai](http://ai.berkeley.edu/project_overview.html)
## Search (proj1)
We implemented DFS, BFS, UCS, and A* searches. We then created state representations for a very simple Pacman game (no ghosts) with differing goals and implemented complete and optimal heuristics that would travel to all corners or eat all the food dots. We also implemented  a suboptimal heuristic to greedily find the closest food dot.
## Multiagent (proj2)
We implemented a simple reflex agent for pacman that used a basic evaluation function which only considered the manhattan distance to ghosts and food. We also implemented an adversarial search agent that used depth-limited Minimax with Alpha-Beta Pruning optimization as well as an agent that used depth-limited Expectimax. Finally, we implemented an evaluation function on states, which took into consideration whether a ghost was scared (and if so we considered how long it would remain scared), ghost positions, power dots positions, and food dot positions.
