from qLearningMagn.State import State
import numpy as np



class GameInterp:
    _quarterGameSize = 13
    _starPositions = np.array([5, 12, 18, 25, 31, 38, 44, 51])
    _globePositionsGlobal = np.array([9, 22, 35, 48])
    _homeStars = np.array([51,12,25,38])
    #"_globePositionsLocal = np.array([1])
    #"_globePositionsEnemyLocal = np.array([])
    #_dangerPositionsLocal = np.array([14, 27, 40])
    def __init__(self):

        self.globalEnemyLocations = np.array([])
        self.glboalPlayerPositions = np.array([])


        self.reward = 0
        self.previousScore = 0
        self.previousHavens = 0
    def getState(self, player):
        return State.State(0,0,0,0,0,0,0,0,0,0)

    def interp(self, dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner, there_is_a_winner,currentPlayer):
        self.playerIndex=currentPlayer
        self.enemyIndexes = [x for x in [0, 1, 2, 3] if x != self.playerIndex]
        self.dice=dice

        self._dangerPositionsGlobal = [x for x in [1, 14, 27, 40] if x != (self.playerIndex*13)+1]
        self.movePieces = move_pieces
        self.playerPieces = player_pieces
        self.enemyPieces = enemy_pieces
        self.findEnemyLocations(enemy_pieces)
        self.findPlayerLocations(player_pieces)


        self._updateReward()







    def findPlayerLocations(self, player_pieces):

        self.globalPlayerPieces=[]

        for playerPieceIndex in range(4):
            playerPiece = player_pieces[playerPieceIndex]
            globalPlayerPiece=self._GetGlobalPosition(self.playerIndex,playerPiece)

            if(globalPlayerPiece<=51 and globalPlayerPiece>0) :
                self.globalPlayerPieces.append(globalPlayerPiece)
        self.globalPlayerPieces=np.array(self.globalPlayerPieces)
    def findEnemyLocations(self, enemy_pieces):

        self.globalEnemyLocations=[]

        for enemyListIndex in range(len(enemy_pieces)):
            for enemyPieceIndex in range(4):
                enemyPiece = enemy_pieces[enemyListIndex,enemyPieceIndex]
                globalEnemyPiece=self._GetGlobalPosition(self.enemyIndexes[enemyListIndex],enemyPiece)

                if(globalEnemyPiece<=51 and globalEnemyPiece>0) :
                    self.globalEnemyLocations.append(globalEnemyPiece)
        self.globalEnemyLocations = np.array(self.globalEnemyLocations)
    def _GetGlobalPosition(self, playerIdx, localPosition):
        if (localPosition == 0):
            return 0
        elif (localPosition == 59):
            return 59
        elif (localPosition>51):
            return localPosition
        else:
            return (localPosition + (self._quarterGameSize * playerIdx)) % 52





    def checkThreat(self, location):

        closeThreat=0
        farThreat=0
        #if location in self._starPositions: #Check if on star

        index = np.where(location == self._starPositions)[0]  # If star position: check next star instead
        if len(index) > 0:
            # If the target value is found in the array
            index_before = index - 1
            location = self._starPositions[index_before]

        for i in range(-6,0):
            testPos = i+location
            if(location<0): testPos = testPos+52
            if testPos in self.globalEnemyLocations:
                closeThreat+=1
        for i in range(-12,-6):
            testPos = i+location
            if(location<0): testPos = testPos+52
            if testPos in self.globalEnemyLocations:
                farThreat+=1

        if closeThreat>1:
            return 3
        elif closeThreat==1:
            return 2
        elif farThreat:
            return 1
        else:
            return 0

    def checkWouldThreaten(self, location):
        index = np.where(location == self._starPositions)[0]  # If star position: check next star instead
        if len(index) > 0:
            # If the target value is found in the array
            index_before = index + 1
            if (index_before >= self._starPositions.size): index_before -= self._starPositions.size
            location = self._starPositions[index_before]

        for i in range(1,7):
            testPos = i+location
            if(location>=52): testPos = testPos-52
            #print(self.globalEnemyLocations)
            enemyLocation=[]
            for enemy in self.globalEnemyLocations: enemyLocation.append(enemy)

            enemyIndices = np.where(self.globalEnemyLocations == testPos)[0]
            if len(enemyIndices) == 1:
                if (testPos not in self._globePositionsGlobal) and (testPos not in self._dangerPositionsGlobal):
                    return 1
        return 0

    def checkHaven(self, pieceIndex, addLocalPieceLocation=0, requiredForSafety=1):
        closeThreat = 0

        location = self._GetGlobalPosition(self.playerIndex, self.playerPieces[pieceIndex])+addLocalPieceLocation
        enemyIndices = np.where(self.globalEnemyLocations == location)[0]
        if self.playerPieces[pieceIndex] + addLocalPieceLocation >= 52:



            if self.playerPieces[pieceIndex]+addLocalPieceLocation<57:
                return 1
            elif self.playerPieces[pieceIndex] + addLocalPieceLocation == 57:
                return 2
            elif self.playerPieces[pieceIndex] + addLocalPieceLocation > 57:
                toSubtract = self.playerPieces[pieceIndex] + addLocalPieceLocation-57
                if self.playerPieces[pieceIndex] - toSubtract >=52:
                    return 1
                else:
                    return 0

        if location == self._homeStars[self.playerIndex]: #If landing on home star
            return 2

        index = np.where(location == self._starPositions)[0]  # If star position: check next star instead
        if len(index) > 0:
            # If the target value is found in the array
            index_before = index + 1
            if (index_before >= self._starPositions.size): index_before -= self._starPositions.size
            location = self._starPositions[index_before]


        if (enemyIndices.size == 2): #If 2 enemies not safe
            return 0
        if location in self._globePositionsGlobal: # if is globe
            if (enemyIndices.size == 0): #and no enemies
                return 1
            if (enemyIndices.size == 1): #and with enemy
                return 0
        if location in self._dangerPositionsGlobal:
            return 0
        friendIndices = np.where(self.globalPlayerPieces == location)[0]
        if friendIndices.size == requiredForSafety:
            return 1
        return 0
    def checkEnemyInPos(self, location):

        index = np.where(location == self._starPositions)[0] #If star position: check next star instead
        if len(index) > 0:
            # If the target value is found in the array
            index_before = index + 1
            if(index_before>=self._starPositions.size): index_before-=self._starPositions.size
            location = self._starPositions[index_before]


        if (location in self._globePositionsGlobal or location in self._dangerPositionsGlobal):  # Dont return enemies if on a globe or homebase
            return 0
        enemyIndices = np.where(self.globalEnemyLocations == location)[0]


        numberEnemies = np.clip(enemyIndices.size,0,2)
        return numberEnemies

    def getSection(self, pieceIndex):
        section = int(np.clip(np.floor(self.playerPieces[pieceIndex]/13),0,3))
        return section
    def isStar(self, location):
        return 1 if location in self._starPositions else 0

    def getScore(self):
        playerScore = np.sum(self.playerPieces)
        enemyScores = np.sum(self.enemyPieces,1)
        self.score = playerScore-np.max(enemyScores)
        return self.score
    def getScoreStateValue(self):
        score = self.getScore()
        if score <= -30 : return 0
        if score <= -10: return 1
        if score <  10: return 2
        if score <  30: return 3
        return 4


    def getState(self, pieceIndex):
        pieceLocation = self._GetGlobalPosition(self.playerIndex,self.playerPieces[pieceIndex])
        dice = self.dice
        prospectiveLocation = pieceLocation + dice

        section = self.getSection(pieceIndex)# section 4
        wouldHitEnemy = self.checkEnemyInPos(prospectiveLocation)# would take 2
        doesThreaten = self.checkWouldThreaten(pieceLocation)
        wouldThreaten = self.checkWouldThreaten(prospectiveLocation)# would threaten 2
        threat = self.checkThreat(pieceLocation)# threat 4
        wouldBeThreat = self.checkThreat(prospectiveLocation)# would be in threat 4
        wouldBeHaven = self.checkHaven(pieceIndex, addLocalPieceLocation=dice)# would be haven 2
        inHaven = self.checkHaven(pieceIndex, requiredForSafety=2)# is in haven 2
        is6 = 1 if dice == 6 else 0 # is 6: 2
        isStar=self.isStar(prospectiveLocation)
        score =self.getScoreStateValue() # current score 5

        return State(section,wouldHitEnemy,doesThreaten,wouldThreaten,threat,wouldBeThreat,wouldBeHaven,inHaven,is6,isStar,score)


    def getStates(self):
        states=[]
        for i in range(4):
            if i not in self.movePieces:
                states.append(None)
            else:
                states.append(self.getState(i))
        return states


    def _updateReward(self):
        currentScore = self.getScore()
        currentHavens=0
        for piece in range(4):
            currentHavens+=self.checkHaven(piece,requiredForSafety=2)
        #self.reward = currentScore - self.previousScore


        scoreReward = currentScore - self.previousScore
        if (scoreReward<=6 and scoreReward >=-6): scoreReward = 0

        havenReward = (currentHavens-self.previousHavens) * 10





        self.reward = scoreReward + havenReward

        self.previousHavens=currentHavens
        self.previousScore = currentScore
    def getCurrentReward(self):
        return self.reward












