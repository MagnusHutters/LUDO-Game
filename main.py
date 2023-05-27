import ludopy
import numpy as np

g = ludopy.Game(ghost_players=[1, 3])  # This will prevent players 1 and 3 from moving out of the start and thereby they are not in the game
there_is_a_winner = False


#State
#Dice 6
#Pieces section 4*4=16
#Pieces isInThreat 4*2=8
#Pieces wouldBeInTreat 4*2=8
#Piece canTake 4*2=8
#piece active 4*2=8

from qLearningMagn.State import State

#print(np.ravel_multi_index(((2,0),(1,1)), (3,3)))
#print(np.ravel_multi_index(((3,0),(0,0)), (7,6)))
State(0,0,0,0,0,0,0,0,0)
exit()





while not there_is_a_winner:
    (dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner, there_is_a_winner), player_i = g.get_observation()
    print(f"{player_i}")
    print(f"{dice}, {move_pieces}")
    print(f"{player_pieces}")
    a = input("")
    if len(move_pieces):
        piece_to_move = move_pieces[np.random.randint(0, len(move_pieces))]
    else:
        piece_to_move = -1

    _, _, _, _, _, there_is_a_winner = g.answer_observation(piece_to_move)

print("Saving history to numpy file")
g.save_hist(f"game_history.npz")
print("Saving game video")
g.save_hist_video(f"game_video.mp4")