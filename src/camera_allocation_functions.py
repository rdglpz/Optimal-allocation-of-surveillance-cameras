import numpy as np
import scipy.stats as st

def gkern(kernlen=101, nsig=2):

    """Returns a 2D Gaussian kernel."""

    x = np.linspace(-nsig, nsig, kernlen+1)
    kern1d = np.diff(st.norm.cdf(x))
    kern2d = np.outer(kern1d, kern1d)
    return kern2d/kern2d.sum()


def perimeter(img):
    '''
    
    '''
    perimeter = list([])
    
    for i in range(0, img.shape[1]):
        perimeter.append((0, i))

    for i in range(0, img.shape[1]):
        perimeter.append((img.shape[0]-1, i))
    
    for i in range(0, img.shape[0]):
        perimeter.append((i, 0))

    for i in range(0, img.shape[0]):
        perimeter.append((i, img.shape[1]-1))
        
    return perimeter


def isovista(img):
    
    from skimage.draw import line
    
    #it works only if the shape is odd in length
    si = (int(img.shape[0]/2), int(img.shape[0]/2))
    
    mask = np.ones(img.shape)
    
    #we get all the coordinates of the img perimeter 
    corner = perimeter(img)
    
    #we draw a line from the center to the edge 
    for x in corner:
        
        rr, cc = line(si[0], si[1], x[0], x[1])
        
        ray = img[rr, cc]
        
        ix = np.argwhere(ray==1)

        if len(ix)!=0:

            ixw = ix[0][0]

            mask[rr[ixw:], cc[ixw:]] = 0 
    
    return mask
    
    
def F(X, S, Walls, CD, L = 50, K = gkern(50*2+1, 4)):
    
    X = X.astype(int)
    
    alpha = 1.0
    
    X_resh = X.reshape(-1, 2)
    
    n_sensors = int(len(X_resh))
    
    COVERS = np.zeros((n_sensors+1, S.shape[0], S.shape[1]))
    
    K = gkern(L*2+1, 4)

    for i, x in enumerate(X_resh):

        #esto me lo puedo ahorrar
        si = tuple(x)

        S_sub = np.copy(S[si[0]-L:si[0]+L+1, si[1]-L:si[1]+L+1])
        
        CD_sub = np.copy(CD[si[0]-L:si[0]+L+1, si[1]-L:si[1]+L+1])

        mask = isovista(S_sub)

        COVERS[i+1, si[0]-L : si[0] + L + 1, si[1]-L:si[1]+L+1] = CD_sub*K*mask

    max_covers = np.sum(np.max(COVERS, axis=0))
    
    cercania_pared = np.sum(Walls[X_resh[:, 0], X_resh[:, 1]])
    
    return -(alpha*max_covers + (1-alpha)*cercania_pared)




#COVERS = np.zeros((n_sensors+1, S.shape[0], S.shape[1]))


def show_surveillance_coverage(X, L, S, CD):


    X_resh = X.reshape(-1,2).astype(int)
    
    

    for i, x in enumerate(X_resh):

        si = tuple(x)
        print(si)

        Z = np.zeros((L*2+1, L*2+1))
        Z[(L, L)] = 1

        S_sub = np.copy(S[si[0]-L:si[0]+L+1, si[1]-L:si[1]+L+1])
        CD_sub = np.copy(CD[si[0]-L:si[0]+L+1, si[1]-L:si[1]+L+1])


        mask = isovista(S_sub)
        K = gkern(L*2+1, 4)


        fig, axs = plt.subplots(1, 5, figsize=(12, 3), sharey=True)

        axs[0].imshow(S_sub+Z)
        axs[1].imshow(mask+Z)
        axs[1].title.set_text("Isovista")
        axs[2].imshow(mask*K)
        axs[2].title.set_text("Isovista ponderada")

        axs[3].imshow(CD_sub*mask)
        axs[3].title.set_text("Densidad Crimen")

        axs[4].imshow(CD_sub*K*mask+Z*np.max(CD_sub*mask))
        axs[4].title.set_text("IV ponderada x Dens Delic: = \n"+str(np.sum(CD_sub*K*mask)))

        COVERS[i+1, si[0]-L : si[0] + L + 1, si[1]-L:si[1]+L+1] = CD_sub*K*mask


    #    plt.imshow(mask*CD_sub)


        #plt.imshow(mask*3+S_sub+Z)
        plt.show()

#    max_covers = np.max(COVERS, axis=0)


#taken from this StackOverflow answer: https://stackoverflow.com/a/39225039
import requests

