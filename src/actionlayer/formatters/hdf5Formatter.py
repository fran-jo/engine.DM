'''
Created on 17 Jul 2018

@author: fran_jo
'''

from domainlayer.stream.streamhdf5 import InputChannelHDF5

class HDF5Formatter():

    def __init__(self, sourcelocation, sourcefile):
        self.h5name= sourcefile.split('.')[1].split('/')[-1]
        self.inh5= InputChannelHDF5(sourcelocation, self.h5name)
    
    def selectData(self, arrayQualquiera, mensaje):
        count= 0
        indexMapping={}
        for i, meas in enumerate(arrayQualquiera):
            print '[%d] %s' % (i, meas)
            indexMapping[count]= i
            count+= 1
        try:
            value= raw_input(mensaje)
            lindex = value.split()
        except ValueError:
            print "Wrong choice ...!" 
        values= []
        for idx in lindex:  
            idx= int(idx)
            values.append(arrayQualquiera[indexMapping[idx]])
        return values
    
    @property
    def power_system_component(self):
        self.__component= None
        
    def import_hdf5(self, fileformat='.txt'):
        pass
