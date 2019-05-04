from typing import Dict
def printPolicyGrid(policy: Dict,K,L):
    '''
    Prints the grid as specified. Also has a more detailed default option. Use --concise for simple grid.
    '''
    for X in range(0,L-1):
        row = ""
        for Y in range(0,L-1):
            total_of_D = 0
            for D in range(0,K+1):
                state_str = str((X, Y, D))
                total_of_D += policy.get(state_str, 0)
            row += " " + str(total_of_D)
        print(row)
            
