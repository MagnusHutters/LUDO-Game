


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
    _stateMax = np.array([
        4,  # Max section,
        3,  # Max isEnemy,
        2,  # Does Threaten
        2,  # Max wouldThreaten,
        4,  # Max threat,
        4,  # Max wouldBeInThreat,
        2,  # Max wouldBeInHaven,
        2,  # Max isInHaven,
        2,  # Max rolled6,
        2,  # Max isStar
        5  # Max currentScore
    ], int)
    stateNames = [
        "sec",
        "eny",
        "trtn",
        "wtrtn",
        "trt",
        "wtrt",
        "whav",
        "hav",
        "is6",
        "isS",
        "sco"
    ]



    doGroupNeighboor = np.array([
        1,  # Group neighboor section,
        0,  # Group neighboor isEnemy,
        1,  # Group neighboor Does Threaten
        1,  # Group neighboor wouldThreaten,
        1,  # Group neighboor threat,
        1,  # Group neighboor wouldBeInThreat,
        0,  # Group neighboor wouldBeInHaven,
        0,  # Group neighboor isInHaven,
        1,  # Group neighboor rolled6,
        0,  # Group neighboor is star,
        1  # Group neighboor currentScore
    ], int)

    def __init__(self, section, isEnemy, doesThreaten, wouldThreaten, threat, wouldBeInThreat, wouldBeInHaven, isInHaven, rolled6, isStar, currentScore):



        self.state = np.array([
            section,
            isEnemy,
            doesThreaten,
            wouldThreaten,
            threat,
            wouldBeInThreat,
            wouldBeInHaven,
            isInHaven,
            rolled6,
            isStar,
            currentScore
        ],int)


        #self.state=np.clip(self._state,0,self._stateMax-1)
        self.Qindex=np.ravel_multi_index(self.state,self._stateMax)

        #print(self.Qindex)


    def fromState(self, stateArray):
        return State(
            stateArray[0],
            stateArray[1],
            stateArray[2],
            stateArray[3],
            stateArray[4],
            stateArray[5],
            stateArray[6],
            stateArray[7],
            stateArray[8],
            stateArray[9],
            stateArray[10],
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
