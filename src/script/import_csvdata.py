'''
Created on 19 Sep 2017

@author: fran_jo
'''
import sys
from actionlayer.parsers.factoryparser import FactoryParser
    
if __name__ == '__main__':
    '''
    parseador= FactoryParser.make_MATParser(
                    "./viladelpingui/File_1.csv"
                    ",",
                    "measurement")
    '''
    parseador= FactoryParser.make_CSVParser(sys.argv[1], sys.argv[2], sys.argv[3])
    parseador.export_hdf5()