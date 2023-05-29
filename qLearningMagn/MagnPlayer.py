



from qLearningMagn.GameInterpretor import GameInterp
from qLearningMagn.QTable import QTable
from qLearningMagn.State import State
import numpy as np
import random

class MagnPlayer:






    def __init__(self,playerId=0, training = False, exploration = 0, learningRate=0.02, discount = 0.70, neighborWeight=0.30):

        self.exploration = exploration
        self.learningRate=learningRate
        self.discount=discount
        self.neighborWeight=neighborWeight
        self.training=training
        self.myPlayerId=playerId

        self.enermyIndex = [x for x in [0,1,2,3] if x != self.myPlayerId] # filter out player id. indice for others
        self.gameInterp = GameInterp()

        self.previousStates = []
        self.previousActions= []

        self.qTable=QTable(State._stateMax,4)




    def update(self, obs, currentPlayer):

        dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner, there_is_a_winner=obs
        if(currentPlayer!=self.myPlayerId):
            print("Not my turn")
            return

        self.gameInterp.interp(dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner, there_is_a_winner, currentPlayer)

        currentStates = self.gameInterp.getStates()
        if(self.training):
            reward = self.gameInterp.getCurrentReward()
            self.rewardStates(self.previousStates, currentStates,self.previousActions, reward, updateNeigboors=True)



        currentActions = self.chooseActions(currentStates) #Return a list of actions - eg a list of priorities to choose that piece

        piece_to_move = self.selectPiece(currentActions, move_pieces)

        self.previousStates = currentStates
        self.previousActions = currentActions

        return piece_to_move

    def selectPiece(self, currentActions, move_pieces):
        piece_to_move = -1
        to_move_pieces = np.where(currentActions == np.max(currentActions))[0]
        #print(currentActions)
        if to_move_pieces.size >= 1 and len(move_pieces):
            #print(np.random.randint(0, move_pieces.size))
            rand=np.random.randint(0, to_move_pieces.size)
            #print(move_pieces,rand)
            piece_to_move = to_move_pieces[rand]
        if (piece_to_move not in move_pieces):
            if len(move_pieces):
                piece_to_move = move_pieces[np.random.randint(0, len(move_pieces))]
            else:
                piece_to_move = -1

        return piece_to_move

    def rewardStates(self, prevousStates, currentStates, previousAction, reward, updateNeigboors):
        count = prevousStates.count(None)
        if count >=3:
            return

        for i in range(len(prevousStates)):
            state=prevousStates[i]
            currentState = currentStates[i]

            if(currentState==None):
                currentState=self.gameInterp.getState(i)


            action=previousAction[i]
            if state != None:


                self.qTable[state.Qindex,action] = \
                    self.qTable[state.Qindex,action] + self.learningRate * (
                        reward + self.discount * np.max(self.qTable[currentState.Qindex]) - self.qTable[state.Qindex,action]
                    )

                #Q(s, a) = Q(s, a) + α * [R + γ * max(Q(s', a')) - Q(s, a)]



    def chooseActions(self, currentStates, doExplore=True):

        priorities = []
        for state in currentStates:
            if state == None:
                priorities.append(-1)
            else:
                qOwnEntry = self.qTable[state.Qindex]
                qEntries=[]
                neighboors = state.getNeigboors()
                for neighboor in neighboors:
                    qEntries.append(self.qTable[neighboor.Qindex])
                neigboorQEntry = np.average(qEntries,0)

                qEntry = self.neighborWeight*neigboorQEntry + (1-self.neighborWeight)*qOwnEntry;

                action = np.argmax(qEntry)
                if (random.random()<self.exploration) and self.training:
                    action=np.random.randint(0, 4)
                priorities.append(action)

        return priorities










