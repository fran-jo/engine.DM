'''
Created on 17 Jul 2018

@author: fran_jo
'''
from cimFormatter import CIMFormatter

class FactoryFormatter(object):
    '''
    classdocs
    '''
    
    def make_CIMFormatter(self, sourcelocation="/db", sourcefile='.h5'):
        return CIMFormatter(sourcelocation, sourcefile)
    
        