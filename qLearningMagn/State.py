


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
        2,  # Max wouldTake,
        2,  # Max wouldThreaten,
        4,  # Max threat,
        4,  # Max wouldBeInThreat,
        2,  # Max wouldBeInHaven,
        2,  # Max isInHaven,
        2,  # Max rolled6,
        5  # Max currentScore
    ], int)



    doGroupNeighboor = np.array([
        1,  # Group neighboor section,
        0,  # Group neighboor wouldTake,
        0,  # Group neighboor wouldThreaten,
        1,  # Group neighboor threat,
        1,  # Group neighboor wouldBeInThreat,
        0,  # Group neighboor wouldBeInHaven,
        0,  # Group neighboor isInHaven,
        0,  # Group neighboor rolled6,
        1  # Group neighboor currentScore
    ], int)

    def __init__(self, section, wouldTake, wouldThreaten, threat, wouldBeInThreat, wouldBeInHaven, isInHaven, rolled6, currentScore):



        self.state = np.array([
            section,
            wouldTake,
            wouldThreaten,
            threat,
            wouldBeInThreat,
            wouldBeInHaven,
            isInHaven,
            rolled6,
            currentScore
        ],int)


        #self.state=np.clip(self._state,0,self._stateMax-1)
        self.Qindex=np.ravel_multi_index(self.state,self._stateMax)

        print(self.Qindex)
