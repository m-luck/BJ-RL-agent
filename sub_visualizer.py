from typing import Dict
def printPolicyGrid(policy: Dict,K,L,axes):
    '''
    Prints the policy grid as specified.
    '''
    full = ""
    if axes:
        full += "X/Y"
        for Y in range(0,L):
            full += str(Y) + " "
    for X in range(0,L):
        row = ""
        if axes: row += str(X) + " "
        for Y in range(0,L):
            total_of_D = 0
            state_str = str((X, Y, 1))
            if Y == 0: state_str = str((X, Y, 0))
            total_of_D += policy.get(state_str, 0)
            # res = total_of_D / (K)
            res = total_of_D
            row += " " + str(res)
        full += "\n" + row  
    print(full)

def printProbabilityGrid(policy, wc, lc, L, axes):
    '''
    Prints the Probability grid as specified. 
    '''
    full = ""
    if axes:
        full += "X\Y"
        for Y in range(0,L):
            full += str(Y) + "      "
    for X in range(0,L):
        row = ""
        if axes: row += str(X) + " "
        for Y in range(0,L):
            state = (X, Y, 1)
            if Y == 0: 
                state = (X, Y, 0)
            state_str = str(state)
            optimal_move = policy.get(state_str, 0)
            move_tuple = str((*state, optimal_move)) 
            w = wc.get(move_tuple, 0)
            l = lc.get(move_tuple, 0)
            denom = w + l if w + l != 0 else 0.5
            prob = "{0:.4f}".format(w / denom)
            row += " " + str(prob)
        full += "\n" + row  
    print(full)
    # print("W")
    # for w in wc:
    #     print(w, wc[w])
    # print("L")
    # for l in lc:
    #     print(l, lc[l])
        
