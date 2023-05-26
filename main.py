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