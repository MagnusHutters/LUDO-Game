import ludopy
import numpy as np

g = ludopy.Game(ghost_players=[1, 3])  # This will prevent players 1 and 3 from moving out of the start and thereby they are not in the game
there_is_a_winner = False


import matplotlib.pyplot as plt

#State
#Dice 6
#Pieces section 4*4=16
#Pieces isInThreat 4*2=8
#Pieces wouldBeInTreat 4*2=8
#Piece canTake 4*2=8
#piece active 4*2=8

from qLearningMagn.State import State
from qLearningMagn.MagnPlayer import MagnPlayer

#print(np.ravel_multi_index(((2,0),(1,1)), (3,3)))
#print(np.ravel_multi_index(((3,0),(0,0)), (7,6)))
#State(0,0,0,0,0,0,0,0,0)
#exit()






plt.ion()  # Turn on interactive mode
plt.figure(0)  # Create a new figure


#while(1):

def doRunGames(num, training = False, exploration = 0, learningRate=0.02, discount = 0.70, neighborWeight=0.30):
    piece_to_move = 0
    didWin = []
    didWinTrend = []
    vTrend = 0.5
    numWins = 0
    numLosses = 0
    totalGames = 0
    winPercentage = []

    myPlayer = MagnPlayer(0, training=training, exploration=exploration, neighborWeight=neighborWeight, learningRate=learningRate,discount=discount)
    for i in range(num):

        g = ludopy.Game()
        there_is_a_winner = False
        g.reset()
        while not there_is_a_winner:
            (dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner, there_is_a_winner), player_i = g.get_observation()



            if(player_i==0): #My player

                piece_to_move = myPlayer.update(
                    (dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner, there_is_a_winner), player_i)


                #a = input("")
            else: #Opponent


                if len(move_pieces):
                    piece_to_move = move_pieces[np.random.randint(0, len(move_pieces))]
                else:
                    piece_to_move = -1

            _, _, _, _, _, there_is_a_winner = g.answer_observation(piece_to_move)
            if(there_is_a_winner):
                if(player_i==0):
                    numWins+=1
                else:
                    numLosses+=1
                totalGames+=1
                v = 1.0 if player_i==0 else 0.0

                percent=numWins/totalGames
                winPercentage.append(percent)
                didWin.append(v)
                #vTrend = 0.995*vTrend + 0.005 * v

                vTrend= np.average(didWin[max(0,len(didWin)-200):-1])
                didWinTrend.append(vTrend)

    myPlayer.qTable.doSave()
    return (numWins/totalGames, didWin)


    #print("Game")



evaluations=[]
trainings=[]

for i in range(100): #Epochs
    trainingPercent=0
    evaluation=0
    evaluation, _ = doRunGames(1000, training=False, exploration=0, neighborWeight=0.3)
    #trainingPercent, _ = doRunGames(100,training=True,exploration=0.25,learningRate=0.2,discount=0.7,neighborWeight=0.3)



    evaluations.append(evaluation)
    trainings.append(trainingPercent)



    plt.clf()  # Clear the previous plot

    print(f"Epoch: {i} \t Training Winrate: {trainingPercent}\t Evaluations Winrate: {evaluation}")
    plt.plot(evaluations)  # Plot the updated data
    #plt.plot(trainings)
    plt.pause(0.01)
    plt.draw()  # Redraw the plot
    plt.show()  # Show the empty plot window










print("Saving history to numpy file")
g.save_hist(f"game_history.npz")
print("Saving game video")
g.save_hist_video(f"game_video.mp4")