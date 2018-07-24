'''
Created on 17 Jul 2018

@author: fran_jo
'''

import h5py
import collections

class ChannelHDF5(object):
    '''
    classdocs
    '''
    _h5namefile= ""
    _h5file= None
    _gmodel= None
    
    def __init__(self, resultFile=".mat", resFilelocation='/'):
        '''
        Constructor
        dblocation= folder where to locate h5 files
        resultFile= instances of a SimRes object with result file
        '''
        if '.' in resultFile:
            self._h5namefile= resFilelocation+ '/'+ resultFile
        else:
            self._h5namefile= resFilelocation+ '/'+ resultFile+ '.h5'
        
    def open(self, networkname= '', mode= 'r'):
        ''' h5name is name of the model '''
        if '.' in networkname:
            networkname= networkname.split('.')[0]
        self._h5file= h5py.File(self._h5namefile, mode)
        if not networkname in self._h5file:
            self._gmodel= self._h5file.create_group(networkname)
        else:
            self._gmodel= self._h5file[networkname]

    def close(self):
        self._h5file.close()
        
class InputChannelHDF5(ChannelHDF5):
    '''
    classdocs
    '''
    
    def __init__(self, resultFile=".mat", resFilelocation='/'):
        '''
        Constructor
        '''
        self.__gPowerSystemResource= None
        self.__gAnalogMeasurement= None
        super(InputChannelHDF5, self).__init__(resultFile, resFilelocation)
        
    def exist_PowerSystemResource(self, component):
        if not component in self._gmodel:
            return False
        else:
            return True
    
    def exist_AnalogMeasurement(self, component, variable):
        self.__gPowerSystemResource= self._gmodel[component]
        if not variable in self.__gPowerSystemResource:
            return False
        else:
            return True
    
    def select_arrayMeasurements(self):
        ''' network name is the name of the h5 file '''
        signalNames= []
        for psres in self.__gmodel.keys():
            self.__gPowerSystemResource= self.__gmodel[psres]
            for meas in self.__gPowerSystemResource.keys():
                signalFullName= psres+ '.'+ meas
                signalNames.append(signalFullName)
        return signalNames
    
    def select_treeMeasurements(self):
        ''' build a dictionary with the name of the groups '''
        arbol = {}
        senyals= []
        for psres in self.__gmodel.keys():
            self.__gPowerSystemResource= self.__gmodel[psres]
            for meas in self.__gPowerSystemResource.keys():
                senyals.append(meas)
            arbol[psres]= senyals
            senyals= []
        arbol= collections.OrderedDict(sorted(arbol.items()))
        return arbol
    
    def select_AnalogMeasurement(self, variable):
        analogMeas= {}
        self.__gAnalogMeasurement= self.__gPowerSystemResource[variable]
        analogMeas['sampleTime']= self.__gAnalogMeasurement['AnalogValue'][:,0]
        analogMeas['magnitude']= self.__gAnalogMeasurement['AnalogValue'][:,1]
        return analogMeas
    
class OutputChannelHDF5(ChannelHDF5):
    '''
    classdocs
    '''
    
    def __init__(self, resultFile=".mat", resFilelocation='/'):
        '''
        Constructor
        '''
        self.__gPowerSystemResource= None
        self.__gAnalogMeasurement= None
        self.__dAnalogValue= None
        super(OutputChannelHDF5, self).__init__(resultFile, resFilelocation)
        
    def exist_PowerSystemResource(self, component):
        if not component in self._gmodel:
            return False
        else:
            return True
    
    def exist_AnalogMeasurement(self, component, variable):
        self.__gPowerSystemResource= self._gmodel[component]
        if not variable in self.__gPowerSystemResource:
            return False
        else:
            return True
        
    def add_PowerSystemResource(self, resource):
        ''' resource is the name of the component '''
        self.__gPowerSystemResource= self._gmodel.create_group(resource)
    
    
    def add_AnalogMeasurement(self, variable, unisymb= 'unit', 
                              unitmultipl= 'multiplier', measType= 'AnalogMeasurement'):
        ''' variable is the name of the variable signal
        add a new group and add attributes '''
        self.__gAnalogMeasurement= self.__gPowerSystemResource.create_group(variable)
        self.__gAnalogMeasurement.attrs['unitSymbol']= unisymb
        self.__gAnalogMeasurement.attrs['unitMultiplier']= unitmultipl
        self.__gAnalogMeasurement.attrs['measurementType']= measType
        
    def add_AnalogValue (self, sampleTime, measValues):
        ''' add to the dataset an entire signal (sampletime,magnitude) at once'''
        self.__dAnalogValue= self.__gAnalogMeasurement.create_dataset('AnalogValue', 
                                    (len(sampleTime),2), chunks=(100,2))
        self.__dAnalogValue[:,0]= sampleTime
        self.__dAnalogValue[:,1]= measValues
        
    def update_PowerSystemResource(self, resource, resourceNew):
        self.__gPowerSystemResource= self._gmodel[resource]
        
    def update_AnalogMeasurement(self, variable, unisymb= 'unitSymbol', 
                              unitmultipl= 'unitMultiplier', measType= 'measurementType'):
        self.__gAnalogMeasurement= self.__gPowerSystemResource[variable]
        self.__gAnalogMeasurement.attrs['unitSymbol']= unisymb
        self.__gAnalogMeasurement.attrs['unitMultiplier']= unitmultipl
        self.__gAnalogMeasurement.attrs['measurementType']= measType
        
    def update_AnalogValue(self, sampleTime, measValues):
        self.__dAnalogValue= self.__gAnalogMeasurement['AnalogValue']
        self.__dAnalogValue[:,0]= sampleTime
        self.__dAnalogValue[:,1]= measValues