'''
Created on 23 Jul 2018

@author: fran_jo
'''

from hdf5Formatter import HDF5Formatter
from CIM16.IEC61970.Base.Meas import Analog, AnalogValue
from CIM16.IEC61970.Base.Core import PowerSystemResource

class CIMFormatter(HDF5Formatter):
    '''
    classdocs
    '''
    def __init__(self, sourcelocation="/db", signalfile=".xml", ):
        '''
        Constructor
        '''
        self.__componentID= "id"
        self.__componentName= "name"
        self.__component= None
        self.__signalID= "signal_id"
        self.__signalName= "signal_name"
        self.__signal= []
        super(CIMFormatter, self).__init__(sourcelocation, signalfile)
        
    @property
    def power_system_component(self):
        self.__component= PowerSystemResource(mRID= self.__componentID, 
                                       name= self.__componentName,
                                       UUID= self.__componentID)
        return self.__component
    
    @property
    def measurement(self):
        ''' property of type Analog - contains array of AnalogValue '''
        self.__aSignal= Analog(mRID= self.__signalID, 
                               name= self.__signalname,
                               UUID= self.__signalID)
        self.__aSignal.setAnalogValues(self.__signal)
        return self.__aSignal
    
    def import_hdf5(self, psComponent='', psSignal=''):
        ''' component '''
        if (self.inh5.exist_PowerSystemResource(psComponent)):
            self.__componentName= self.__gPowerSystemResource.name
        ''' signal associated to component '''
        if (self.inh5.exist_AnalogMeasurement(psComponent, psSignal)):
            signalValues= self.inh5.select_AnalogMeasurement(psSignal)
            self.__signalName= psSignal
            for sample, valor in zip(signalValues['sampleTime'],
                             signalValues['magnitude']):
                aValue= AnalogValue(value= valor, timeStamp= sample,
                                    mRID= sample, UUID= sample)
                self.__signal.append(aValue)
