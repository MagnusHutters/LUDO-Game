
import numpy as np
import os
class QTable:

    changesBeforeAutosave=1000
    qTableFolder="qLearningMagn/QTables/"
    qTableFileExtension=".npy"
    def __init__(self, stateSpaceSize, actionSize, qTable = "qTable", doResetQTable = False):

        self.qTablePath = self.qTableFolder+qTable+self.qTableFileExtension


        self.stateSpaceSize=stateSpaceSize
        self.actionSize=actionSize

        self.qTable=np.zeros((np.prod(stateSpaceSize),actionSize),float)
        self.changes = 0


        if os.path.isfile(self.qTablePath) and not doResetQTable:
            loadedArray = np.load(self.qTablePath)
            if(loadedArray.shape == self.qTable.shape):
                self.qTable=loadedArray
        self.doSave()
    def doSave(self):
        np.save(self.qTablePath,self.qTable)

    def doReset(self,qTableFile = "qLearningMagn/QTables/qTable.npy"):
        self.qTable = np.zeros((np.prod(self.stateSpaceSize), self.actionSize), float)
    def __getitem__(self, indices):
        #if isinstance(indices, tuple):
        #    row, col = indices
        #    return self.qTable[row][col]
        #else:
            return self.qTable[indices]

    def __setitem__(self, indices, value):
        #if isinstance(indices, tuple):
        #    row, col = indices
        #    self.qTable[row][col] = value
        #else:
        self.qTable[indices] = value
        self.changes+=1;
        if(self.changes>=self.changesBeforeAutosave):
            self.doSave()
            self.changes=0