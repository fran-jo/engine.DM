'''
Created on 17 Jul 2018

@author: fran_jo
'''
from csvParser import CSVParser
from matParser import MATParser

class FactoryParser(object):
    '''
    classdocs
    '''
    
    def make_CSVParser(self, sourceFile=".csv", delimiter= ',', sourceSignal="simulation"):
        if (sourceSignal= "simulation"):
            targetlocation= "/db/simulation"
        if (sourceSignal= "measurement"):
            targetlocation= "/db/measurement"
        return CSVParser(sourceFile, delimiter, targetlocation)
    
    def make_MATParser(self, sourceFile=".mat", sourceSignal="simulation", compiler="omc"):
        if (sourceSignal= "simulation"):
            targetlocation= "/db/simulation"
        if (sourceSignal= "measurement"):
            targetlocation= "/db/measurement"
        return MATParser(sourceFile, targetlocation, compiler)
    
        