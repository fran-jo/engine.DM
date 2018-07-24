'''
Created on 17 Jul 2018

@author: fran_jo
'''
from domainlayer.stream.streamcsv import InputChannelCSV
from hdf5Parser  import HDF5Parser

class CSVParser(HDF5Parser):
    '''
    class
    '''
    
    def __init__(self, csvFile='.csv', delimiter= ',', targetlocation='/db'):
        self.sourcecsv= InputChannelCSV(csvFile, delimiter)
        self.sourcecsv.load_csvHeader() 
        super(CSVParser, self).__init__(targetlocation, csvFile)
    
    def export_hdf5(self):
        self.outh5.open(self.h5name, 'w')
        measname= self.selectData(self.sourcecsv.header, 'Select which component data to import: ')
        for selectedMeas in measname:
            nameSplit= selectedMeas.split(':')
            componentname= nameSplit[0]
            signalName= nameSplit[1]
            self.sourcecsv.load_csvValues(selectedMeas)
            if not self.outh5.exist_PowerSystemResource(componentname):
                self.outh5.add_PowerSystemResource(componentname)
            if not self.outh5.exist_AnalogMeasurement(signalName):
                self.outh5.add_AnalogMeasurement(signalName)
            self.outh5.add_AnalogValue(self.sourcecsv.timestamp2sample(
                                self.sourcecsv.senyal['sampletime']), 
                                self.sourcecsv.senyal['magnitude'])
        self.outh5.close()
    
    def exportAll_hdf5(self):
        self.outh5.open(self._h5name, 'w')
        for i, meas in enumerate(self.sourcecsv.header):
            if (meas!= "Timestamp"):
                nameSplit= meas.split(':')
                if (len(nameSplit)> 2):
                    componentname= nameSplit[0]
                    signalname= nameSplit[1]+':'+nameSplit[2]
                else:
                    componentname= nameSplit[0]
                    signalname= nameSplit[1]
                self.sourcecsv.load_csvValues(meas) 
                ''' correct sourcecsv object, cause it contains duplicated data '''
                if not self.outh5.exist_PowerSystemResource(componentname):
                    self.outh5.add_PowerSystemResource(componentname)
                if not self.outh5.exist_AnalogMeasurement(componentname, signalname):
                    self.outh5.add_AnalogMeasurement(signalname)
                self.outh5.add_AnalogValue(self.sourcecsv.timestamp2sample(
                                    self.sourcecsv.senyal['sampletime']), 
                                    self.sourcecsv.senyal['magnitude'])
        self.outh5.close()
    
    def import_hdf5(self, fileformat='.txt'):
        pass
