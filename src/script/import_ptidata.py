'''
Created on 22 jan 2016

@author: fragom
'''

import sys, os
from domainlayer.stream.streampti import InputChannelOUT
from actionlayer.streamcimh5 import StreamCIMH5

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
    
def outToH5(self, outfile= '.out', binpath= './'):
    PSSE_PATH= binpath
    sys.path.append(PSSE_PATH)
    os.environ['PATH']+= ';'+ PSSE_PATH
    
    ''' .out files resulting from psse dynamic simulations '''
    sourceout= InputChannelOUT(outfile)
    sourceout.load_outputData()
    selectedOutput= self.selectData(sourceout.ch_id, "Select the data to import, in pairs:")
    sourceout.save_channelID(selectedOutput)
    sourceout.load_channelData()
#         print 'signal: ', sourceout.signals
    networkname= outfile.split('.')[1].split('/')[-1]
    h5name= networkname + '.h5'
    samples= magnitudes= []
    dbh5= StreamCIMH5(['./db/measurements', h5name], 'psse')
    dbh5.open(h5name)
    for component in sourceout.signals.keys():
        dbh5.add_PowerSystemResource(component) 
        dbh5.add_AnalogMeasurement(sourceout.selectedId[component])
        for aValue in sourceout.signals[component].getAnalogValues():
            samples.append(aValue.timestamp)
            magnitudes.append(aValue.value)
        dbh5.add_AnalogValue(samples, magnitudes)
    dbh5.close()

if __name__ == '__main__':  
    outToH5(sys.argv[1])
