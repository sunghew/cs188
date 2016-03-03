# cs188
## Overview
This is a repository for our implementations of the CS 188 Spring 2016 projects. The course was instructed by Professors Pieter Abbeel and Anca Dragan. To see instructions similar to the ones we had, check out [Berkeley AI](http://ai.berkeley.edu/project_overview.html)

## Search (proj1)
We implemented DFS, BFS, UCS, and A* searches. We then created state representations for a very simple Pacman game (no ghosts) with differing goals and implemented complete and optimal heuristics that would travel to all corners or eat all the food dots. We also implemented  a suboptimal heuristic to greedily find the closest food dot.
## Multiagent (proj2)
We implemented a simple reflex agent for pacman that used a basic evaluation function which only considered the manhattan distance to ghosts and food. We also implemented an adversarial search agent that used depth-limited Minimax with Alpha-Beta Pruning optimization as well as an agent that used depth-limited Expectimax. Finally, we implemented an evaluation function on states, which took into consideration whether a ghost was scared (and if so we considered how long it would remain scared), ghost positions, power dots positions, and food dot positions.

## Reinforcement (proj3)
We implemented several variants of value iteration for a Markov Decision Problem (MDP), from which we were able to generate an offline policy. One was "Batch" Value Iteration, where we updated V<sub>k+1</sub>(s) for all states s in every iteration whereas another was Asynchronous Value Iteration, where we update only one V<sub>k+1</sub>(s) per iteration and cycle around. We finally implemented Prioritized Sweeping Value Iteration, which is described in this [paper](http://papers.nips.cc/paper/651-memory-based-reinforcement-learning-efficient-computation-with-prioritized-sweeping.pdf). 

We also implemented model-free agents for the more common situation where the MDP is unknown. We implemented a Q-Learning agent, which had an epsilon-greedy action selection for exploration. We finally implemented an Approximate Q-Learning agent, which learned weights for features of states, where states may share the same feature.