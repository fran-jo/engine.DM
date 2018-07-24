'''
Created on 22 jan 2016

@author: fragom
'''

import sys
from actionlayer.parsers.factoryparser import FactoryParser

if __name__ == '__main__':  
    '''
    parseador= FactoryParser.make_MATParser(
                    "./viladelpingui/File_1.mat"
                    "simulation",
                    "openmodelica")
    '''
    parseador= FactoryParser.make_MATParser(sys.argv[1], sys.argv[2], sys.argv[3])
    parseador.export_hdf5()
