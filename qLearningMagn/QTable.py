
import numpy as np
import os
class QTable:
    qTableFile = "qLearningMagn/QTables/qTable.npy"
    changesBeforeAutosave=100
    def __init__(self, stateSpaceSize, actionSize):
        self.qTable=np.zeros((np.prod(stateSpaceSize),actionSize),float)
        self.changes = 0

        if os.path.isfile(self.qTableFile):
            loadedArray = np.load(self.qTableFile)
            if(loadedArray.shape == self.qTable.shape):
                self.qTable=loadedArray
        self.doSave()
    def doSave(self):
        np.save(self.qTableFile,self.qTable)

    def __getitem__(self, indices):
        if isinstance(indices, tuple):
            row, col = indices
            return self.qTable[row][col]
        else:
            return self.qTable[indices]

    def __setitem__(self, indices, value):
        if isinstance(indices, tuple):
            row, col = indices
            self.qTable[row][col] = value
        else:
            self.qTable[indices] = value
        self.changes+=1;
        if(self.changes>=self.changesBeforeAutosave):
            self.doSave()
            self.changes=0