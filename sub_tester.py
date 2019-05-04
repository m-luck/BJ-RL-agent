import sub_learner as l
from typing import Dict, List

def test_winRatio(S, K, winCount, loseCount):
    res = l.genf_j(S, K, winCount, loseCount)
    print("Win ratios of",S,"are",res)
    return res

def test_bestMove(K, f):
    res = l.getMaxf_J(K, f)
    print("The index of draw of highest winRatio is", res)
    return res

def test_noBestMove(pB, T, f, J, M, g, K):
    res = l.pJ(pB, T, f, J, M, g, K)
    print("p of",J,"is",res)
    return res

def test_pB(T, f, B, M, K):
    res = l.pB(T, f, B, M, K)
    print("pB of",B,"is",res)
    return res

def test_pJ(pB, T, f, J, M, g, K):
    res = l.pJ(pB, T, f, J, M, g, K)
    print("p of",J,"is",res)
    return res

def test_stoch(K, B, probB, T, f, M, g):
    res = l.stoch(K, B, probB, T, f, M, g)
    print("We have randomly selected drawing", res, "card")
    return res

def run_trial():
    pass

def OK():
    print("OK")

def ERR():
    print("ATTENTION!")

if __name__ == "__main__":

    # Test Conditions 1
    S = (2,3,1)
    wc = {}
    lc = {}
    K = 2
    M = 4 
    print("\n## Testing win ratios...")
    if test_winRatio(S, K, wc, lc)=={0: 0.0, 1: 0.0, 2: 0.0}: OK()
    else: ERR()

    # Test Conditions 2
    print("\n##Testing pB and pJ")
    settings = (2, 4, 5, 1, 4.0, 10 ** 3)
    N, L, U, K, M, X, Y, D, f, B, g, T = l.populateTerms(settings, S, wc, lc)
    pB = test_pB(T,f,B,M,K)
    if pB == 0.5: OK()
    else: ERR()
    pJ = test_pJ(pB, T, f, 1, M, g, K)
    if pJ == 0.5: OK()
    else: ERR()

    wc = {'(2, 3, 1, 1)':1}
    print("\n## Testing with", wc)
    N, L, U, K, M, X, Y, D, f, B, g, T = l.populateTerms(settings, S, wc, lc)
    if test_bestMove(K, f)==1: OK()
    else: ERR()

    l.random.seed(0xDEADBEEF)
    if test_stoch(K, B, pB, T, f, M, g) == 1: OK()
    else: ERR()