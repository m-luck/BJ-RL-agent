from typing import Dict
def printPolicyGrid(policy: Dict,K,L,axes):
    '''
    Prints the grid as specified. Also has a more detailed default option. Use --concise for simple grid.
    '''
    full = ""
    if axes:
        full += "  "
        for Y in range(L-1,-1,-1):
            full += " " + str(Y)
    for X in range(L-1,-1,-1):
        row = ""
        if axes: row += str(X) + " "
        for Y in range(L-1,-1,-1):
            total_of_D = 0
            state_str = str((X, Y, 1))
            total_of_D += policy.get(state_str, 0)
            # res = total_of_D / (K)
            res = total_of_D
            row += " " + str(res)
        full += "\n" + row  
    print(full)

def printProbabilityGrid(policy, wc, lc, L, axes):
    '''
    Prints the grid as specified. Also has a more detailed default option. Use --concise for simple grid.
    '''
    full = ""
    if axes:
        full += "  "
        for Y in range(L-1,-1,-1):
            full += " " + str(Y)
    for X in range(L-1,-1,-1):
        row = ""
        if axes: row += str(X) + " "
        for Y in range(L-1,-1,-1):
            state = (X, Y, 1)
            state_str = str(state)
            optimal_move = policy.get(state_str, 0)
            move_tuple = str((*state, optimal_move)) 
            w = wc.get(move_tuple, 0)
            l = lc.get(move_tuple, 0)
            denom = w + l if w + l != 0 else 0.5
            prob = "{0:.3f}".format(w / denom)
            row += " " + str(prob)
        full += "\n" + row  
    print(full)
