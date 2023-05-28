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



myPlayer = MagnPlayer(0)
piece_to_move=0

didWin=[]
didWinTrend=[]
vTrend=0.5
numWins=0
numLosses=0
totalGames=0

winPercentage=[]

plt.ion()  # Turn on interactive mode
plt.figure()  # Create a new figure
plt.show()  # Show the empty plot window

while(1):
#for i in range(1):

    g = ludopy.Game(ghost_players=[1, 3])
    there_is_a_winner = False
    g.reset()
    while not there_is_a_winner:
        (dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner, there_is_a_winner), player_i = g.get_observation()



        if(player_i==0): #My player

            piece_to_move = myPlayer.update(
                (dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner, there_is_a_winner)
                , player_i, doExplore=False, training=False)


            #a = input("")
        if(player_i==2): #Opponent


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




    #print("Game")

    plt.clf()  # Clear the previous plot
    plt.plot(didWinTrend)  # Plot the updated data
    plt.draw()  # Redraw the plot
    plt.pause(0.001)




print("Saving history to numpy file")
g.save_hist(f"game_history.npz")
print("Saving game video")
g.save_hist_video(f"game_video.mp4")