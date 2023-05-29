


#Dice
#section 4
#would take 2
#would threaten 2
#threat 4
#would be in threat 4
#would be haven 2
#is in haven 2
#is 6: 2
#current score 5

import numpy as np




class State:


    #Special Tile: none, star, haven, home, goal, danger, death
    _stateMax = np.array([
        4,  # Max section,
        7,  # Max tileFeature,
        2,  # Max isEnemy,
        4,  # Max threat,
        4,  # Max wouldBeInThreat,
        2,  # Does Threaten
        2,  # Max wouldThreaten,
        2,  # Max isSafe,
        2,  # Max rolled6,
        5   # Max currentScore
    ], int)


    stateNames = [
        "sec",
        "feat",
        "enmy",
        "trt",
        "wtrt",
        "trtn",
        "wtrtn",
        "safe",
        "is6",
        "sco"
    ]



    doGroupNeighboor = np.array([
        1,  # Group neighboor section,
        0,  # Group neighboor tileFeature,
        0,  # Group neighboor isEnemy,
        1,  # Group neighboor threat,
        1,  # Group neighboor wouldBeInThreat,
        0,  # Group neighboor Threaten
        0,  # Group neighboor wouldThreaten,
        0,  # Group neighboor isSafe,
        1,  # Group neighboor rolled6,
        1,  # Group neighboor currentScore

    ], int)

    def __init__(self, array):



        self.state = np.array(array
        ,int)


        #self.state=np.clip(self._state,0,self._stateMax-1)
        self.Qindex=np.ravel_multi_index(self.state,self._stateMax)

        #print(self.Qindex)


    def fromState(self, stateArray):
        return State(stateArray
        )
    def getNeigboors(self):
        neighbors=[]
        for i in range(len(self.state)):
            if(self.doGroupNeighboor[i]):
                for delta in [-1, 1]:
                    new_state = np.copy(self.state)
                    new_state[i] += delta
                    if( new_state[i] >=0 and new_state[i] <self._stateMax[i]):

                        neighbors.append(self.fromState(new_state))
        return neighbors
