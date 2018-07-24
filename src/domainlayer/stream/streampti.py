'''
Created on 10 feb 2016

@author: fragom
'''

from data import signal
from itertools import izip
import psspy, dyntools
from CIM16.IEC61970.Base.Meas import Analog, AnalogValue
from CIM16.IEC61970.Base.Core import PowerSystemResource

class ChannelOUT(object):
    '''
    classdocs
    '''

    _chnfobj = None
    
    def __init__(self, params):
        '''
        Constructor
        '''
        self._chnfobj = dyntools.CHNF([params[0]])

class InputChannelOUT(ChannelOUT): 
    '''
    classdocs
    '''
    __outid= []
    __outdata= []
    __selectedId= {}
    __signals= {}

    def __init__(self, psseoutfile):
        super(InputChannelOUT, self).__init__([psseoutfile])

    def get_selected_id(self):
        return self.__selectedId

    def set_selected_id(self, value):
        self.__selectedId = value

    def del_selected_id(self):
        del self.__selectedId

    def get_outid(self):
        return self.__outid.values()

    def set_outid(self, value):
        self.__outid = value

    def del_outid(self):
        del self.__outid

    def get_signals(self):
        return self.__signals

    def set_signals(self, value):
        self.__signals = value

    def del_signals(self):
        del self.__signals
    
    
    def save_channelID(self, selectedOutput):
        i= 0
        while (i< len(selectedOutput)):
#             print selectedOutput[i]
            cn= selectedOutput[i].split(' ')[2:]
            a= cn[0][1:]
            b= cn[1][:-1]
            component= a+ '_'+ b
#             cn= selectedOutput[i].split('_')[:-1]
#             component= cn[0]+ '_'+ cn[1]
            self.__selectedId[component]= (selectedOutput[i], selectedOutput[i+1])
            i= i+ 2
#         print len(self.__selectedId)
       
    def load_outputData(self):
        sh_ttl, self.__outid, self.__outdata= self._chnfobj.get_data()
    
    def load_channelData(self):
        manyAValues= []
        channels = [self.__outid[index] for index in range(1, len(self.__outid))]
        for component, valor in self.__selectedId.iteritems():
            iclau= channels.index(valor[0])+ 1
            ivalor= channels.index(valor[1])+ 1
            '''TODO use Measurement-> Analog '''
            aMeas= Analog(mRID= 'psse_measurement', name= component,
                      UUID= 'uuid'+ str(valor[1]))
            '''TODO use MeasurementValue-> AnalogValue'''
            for eachSample, eachValue in zip(self.__outdata['time'],self.__outdata[iclau]):
                localmRID= 'analogValue_'+ str(eachSample)
                aValue= AnalogValue(value= eachValue, timeStamp= eachSample,
                                mRID= localmRID, UUID= localmRID)
                manyAValues.append(aValue)
#             senyal.set_signal(self.__outdata['time'], self.__outdata[iclau], self.__outdata[ivalor])
            aMeas.setAnalogValues(manyAValues)
            self.__signals[component]= aMeas
#         print len(self.__signals)
        
    signals = property(get_signals, set_signals, del_signals, "signals's docstring")
    ch_id = property(get_outid, set_outid, del_outid, "ch_id's docstring")
    selectedId = property(get_selected_id, set_selected_id, del_selected_id, "selectedId's docstring")
    
    