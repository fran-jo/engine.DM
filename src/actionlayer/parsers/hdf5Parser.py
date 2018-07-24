'''
Created on 17 Jul 2018

@author: fran_jo
'''

from domainlayer.stream.streamhdf5 import OutputChannelHDF5

class HDF5Parser():

    def __init__(self, targetlocation, sourcefile):
        self.h5name= sourcefile.split('.')[1].split('/')[-1]
        self.outh5= OutputChannelHDF5(targetlocation, self.h5name)
    
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

    def export_hdf5(self):
        pass
