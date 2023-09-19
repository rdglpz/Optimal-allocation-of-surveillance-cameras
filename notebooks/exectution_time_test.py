from timeit import default_timer as timer

T =list([])

K = aptitude.gkern(L*2 + 1, 2)

for i in range(1000):
    

    start = timer()

    i = L
    j = L

    si = (i, j)
    S_sub = np.copy(S[si[0]-L:si[0]+L+1, si[1]-L:si[1]+L+1])
    CD_sub = np.copy(CD[si[0]-L:si[0]+L+1, si[1]-L:si[1]+L+1])

    #es la operacion mas costosa
    mask = aptitude.isovista(S_sub)


    p = np.sum(CD_sub*K*mask)

    end = timer()

    #print((end - start))
    T.append((end - start))