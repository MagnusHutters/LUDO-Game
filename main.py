import datetime
import multiprocessing

import ludopy
import numpy as np

#g = ludopy.Game(ghost_players=[1, 3])  # This will prevent players 1 and 3 from moving out of the start and thereby they are not in the game
there_is_a_winner = False
import concurrent.futures
import threading

import time
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
#plt.figure(0)  # Create a new figure


#while(1):

def doRunGames(num, player, qTable="Qtable", ):
    piece_to_move = 0
    didWin = []
    didWinTrend = []
    vTrend = 0.5
    numWins = 0
    numLosses = 0
    totalGames = 0
    winPercentage = []

    myPlayer = player

    g = ludopy.Game(ghost_players=[1, 3])  # This will prevent players 1 and 3 from moving out of the start and thereby they are not in the game

    for i in range(num):

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


def doTrain():
    for i in range(100): #Epochs
        trainingPercent=0
        evaluation=0

        player = MagnPlayer(0, training=False, exploration=0, neighborWeight=0.3)
        evaluation, _ = doRunGames(200, player=player)
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




def TrainingTestsVisualization(epochsTotal,validationWinrates, runParameterStrings):

    figure = plt.figure(1, figsize=(14, 10))
    ax = figure.add_subplot(111)

    ax.set_title("Validation Winrates")
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Winrate")
    ax.set_ylim(0,1)
    ax.set_xlim(1,epochsTotal)

    ax.grid(True)

    for i in range(len(validationWinrates)):
        xTics = np.arange(1, len(validationWinrates[i])+1, 1)
        ax.plot(xTics, validationWinrates[i], label=runParameterStrings[i], marker='o')

    ax.legend()
    plt.show()
    plt.pause(0.01)
    plt.draw()





def doPerformTrainingTests():
    neighboorWeights = [0, 0.3]
    explorations = [0.3]
    discounts = [0.5, 0.75, 0.9]
    epochs = 5
    trainingGames = 2
    validationGames = 2
    finalValidationGames = 1


    runParametersStrings = {}
    lock = threading.Lock()

    manager = multiprocessing.Manager()
    validationWinrates = manager.dict()

    #with concurrent.futures.ThreadPoolExecutor() as executor:
    results = []
    with multiprocessing.Pool() as pool:
        # Create a list to store the submitted threads


        test=0


        for neighborWeight in neighboorWeights:
            #for exploration in explorations:
            for discount in discounts:
                # print(f"Test: {test}")
                # print(f"NeighborWeight: {neighborWeight}, Discount: {discount}")
                runParameterString = f"Ngbr: {neighborWeight}, Dscnt: {discount}"

                runParametersStrings[test] = (runParameterString)

                validationWinrates[test] = manager.list()

                result=pool.apply_async(doPerformTrainingTest, (discount, epochs, finalValidationGames, neighborWeight,  test, trainingGames, validationGames, validationWinrates))
                results.append(result)
                #doPerformTrainingTest(discount, epochs, finalValidationGames, neighborWeight,  test,trainingGames, validationGames)

                test+=1


        while any(not result.ready() for result in results):
            # Do something while waiting
            pass


            TrainingTestsVisualization(epochs, validationWinrates, runParametersStrings)
            #print("Updating...")
            time.sleep(2)
        pool.close()
        pool.join()
    results = [result.get() for result in results]

    print("Saving results...")
    fileNameWithTime = f"Output/results_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"

    resultsFile= open(fileNameWithTime,"w")
    for i in range(len(results)):

        print(f"Test {i}: {runParametersStrings[i]}")
        resultsFile.write(f"Test {i}: {runParametersStrings[i]}\n")
        print(f"Final Winrate: {results[i]}")
        resultsFile.write(f"Final Winrate: {results[i]}\n")


    validationWinrates = dict(validationWinrates)
    for key in validationWinrates:
        validationWinrates[key] = list(validationWinrates[key])
    #print(validationWinrates)
    TrainingTestsVisualization(epochs, validationWinrates, runParametersStrings)


    saveFigName = f"Output/results_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_fig.png"
    fig = plt.figure(1)
    fig.savefig(saveFigName)


def doPerformTrainingTest(discount, epochs, finalValidationGames, neighborWeight, test, trainingGames, validationGames, validationWinrates):



    qTableName = f"Qtable_{test}"
    player = MagnPlayer(0, qTableName, doResetQTable=True, training=True, exploration=0.3,
                        neighborWeight=neighborWeight, learningRate=0.1, discount=discount)
    for epoch in range(epochs):
        trainingPlayer = MagnPlayer(0, qTableName, doResetQTable=False, training=True, exploration=0.3,
                                    neighborWeight=neighborWeight, learningRate=0.1, discount=discount)
        doRunGames(trainingGames, player=trainingPlayer)

        validationPlayer = MagnPlayer(0, qTableName, doResetQTable=False, training=False, exploration=0,
                                      neighborWeight=neighborWeight, learningRate=0.1, discount=discount)
        winRate = 0
        if (epoch == 0):

            winRate, _ = doRunGames(200, player=validationPlayer)
        else:
            winRate, _ = doRunGames(validationGames, player=validationPlayer)

        if (len(validationWinrates[test]) > 0):
            winRate = 0.9 * validationWinrates[test][-1] + 0.1 * winRate

            # Access and modify the shared variable
        validationWinrates[test].append(winRate)


        # print(f"Epoch: {epoch}")
        # print(validationWinrates)

    validationPlayer = MagnPlayer(0, qTableName, doResetQTable=False, training=False, exploration=0,
                                  neighborWeight=neighborWeight, learningRate=0.2, discount=discount)
    winRate, _ = doRunGames(finalValidationGames, player=validationPlayer)
    #print(f"Final Winrate: {winRate}")
    #print("")

    return winRate

doPerformTrainingTests()

#print("Saving history to numpy file")
#g.save_hist(f"game_history.npz")
#print("Saving game video")
#g.save_hist_video(f"game_video.mp4")
