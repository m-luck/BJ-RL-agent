from typing import Dict, List
# Size X x Y x D/P x K 
winCount = {}
loseCount = {}

def run_trial():
    pass

def genf_j(K: int, winCount: Dict, loseCount: Dict):
    f = {}
    for J in range(0,K+1):
        wc, ls = winCount[(X,Y,D,J)], loseCount[(X,Y,D,J)]
        denom = wc + lc
        denom = denom if denom != 0 else 0.5
        f[J] = wc/denom
    return f


def getMaxf_J(K: int, f: Dict):
    valB = 0
    B = 0
    for J in range(0,K+1):
        if f[J] > valB:
            B = J
            valB = f[J]
    return B

def sumOver_f_J_notB(B: int, f: Dict):
    total = 0
    for J, f_J in enumerate(f):
        if J != B: total += f_J 

def sumSeenInTrajectory(S: List, K: int, winCount: Dict, loseCount: Dict):
    total = 0
    X, Y, D = *S
    for J in range(0,K+1):
        total += winCount[(X,Y,D,J)] + loseCount[(X,Y,D,J)]
    return total

def choose(S: List, settings: List):
    X, Y, D = *S
    L, U, K = *settings
    f = genf_j(K, winCount, loseCount)
    B = getMaxf_J(K, f)
    g = sumOver_f_J_notB(B, f)
    T = sumSeenInTrajectory(S, K, winCount, loseCount)
    


def update_policy():
    pass