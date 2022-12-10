# Checkers AI

## Some suggestions to get started
- Right now we have a way to estimate the value of a board as simple how many pieces and kings we control, however checkers is an advanced game, and we can estimate the value of a board in more sophisticated manners, check out section 5 of this link for ideas: https://www.cs.huji.ac.il/w~ai/projects/old/English-Draughts.pdf
- A fairly simple yet effective way to play turn based games is a minimax algorithm, we've made one in the ai3.py file, but it's slow, try adding alpha beta pruning to make it faster and look further
    - Minimax: https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-1-introduction/
    - Alpha-beta pruning: https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/
        - To give context on why alpha beta pruning is good, mike's minimax alone can only go to a depth of 4 on our laptops (look 4 moves ahead) before it gets unreasonably slow, however an implementation of alpha beta pruning can look ahead 128 moves almost instantaniously.
    

