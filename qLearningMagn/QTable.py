
import numpy as np
import os
class QTable:
    qTableFile = "/qTable.npy"
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
            return self.data[row][col]
        else:
            return self.data[indices]

    def __setitem__(self, indices, value):
        if isinstance(indices, tuple):
            row, col = indices
            self.data[row][col] = value
        else:
            self.data[indices] = value
        self.changes+=1;
        if(self.changes>=self.changesBeforeAutoSave):
            self.doSave()
            self.changes=0