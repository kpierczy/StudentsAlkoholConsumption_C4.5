from idtress.ID3 import ID3

class C45(ID3):

    def __init__(self, pruneThreshold):
        self.__pruneThreshold = pruneThreshold