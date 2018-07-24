'''
Created on 17 Jul 2018

@author: fran_jo
'''
from actionlayer.parsers.hdf5Parser import HDF5Parser
from domainlayer.stream.streammat import InputChannelMAT
from modelicares import SimRes

class MATParser(HDF5Parser):
    
    def __init__(self, matFile=".mat", targetlocation="", compiler=""):
        self.sourcemat= InputChannelMAT(matFile, compiler)
        self.sourcemat.load_components()
        super(MATParser, self).__init__(targetlocation, matFile)
    
    def export_hdf5(self):
        componentsName= self.selectData(self.sourcemat.components, 'Select which component data to import: ')
        self.sourcemat.load_variables(componentsName)
        componentsSignals= zip(componentsName,self.sourcemat.variables)
        for componentname, componentSignal in componentsSignals:
            newVariablesName= []
            variablesName= self.selectData(componentSignal, 'Select which signals from '+ componentname+ ' to import: ')
            try:
                self.sourcemat.load_signals(componentname, variablesName)
            except LookupError:
                for variablename in variablesName:
                    self.sourcemat.load_subvariables(componentname, variablename)
                    subvariableNames= self.selectData(self.sourcemat.variables, 
                                                 'Select which signals from '+ componentname+'.'+variablename+' to import: ')
                    for subvariablename in subvariableNames:
                        newVariablesName.append(variablename+ '.'+ subvariablename)
                variablesName= newVariablesName
                self.sourcemat.load_signals(componentname, variablesName)
            if not self.outh5.exist_PowerSystemResource(componentname):
                self.outh5.add_PowerSystemResource(componentname)
            else:
                self.outh5.update_PowerSystemResource(componentname,componentname)
            for variable in variablesName:
                paramName= componentname+ '.'+ variable
                if not self.outh5.exist_AnalogMeasurement(variable):
                    self.outh5.add_AnalogMeasurement(variable)
                    self.outh5.add_AnalogValue(self.sourcemat.senyal['sampletime'], 
                                         self.sourcemat.senyal[paramName])
                else:
                    self.outh5.update_AnalogMeasurement(variable)
                    self.outh5.update_AnalogValue(variable,self.sourcemat.senyal['sampletime'], 
                                         self.sourcemat.senyal[paramName])
            self.sourcemat.clear_signals()
        self.outh5.close()
        
    def exportAll_hdf5(self):
        self.sourcemat.load_variables(self.sourcemat.components)
        componentsSignals= zip(self.sourcemat.components,self.sourcemat.variables)
        for componentname, componentSignal in componentsSignals:
            newVariablesName= []
            variablesName= self.selectData(componentSignal, 'Select which signals from '+ componentname+ ' to import: ')
            try:
                self.sourcemat.load_signals(componentname, variablesName)
            except LookupError:
                for variablename in variablesName:
                    self.sourcemat.load_subvariables(componentname, variablename)
                    subvariableNames= self.selectData(self.sourcemat.variables, 
                                                 'Select which signals from '+ componentname+'.'+variablename+' to import: ')
                    for subvariablename in subvariableNames:
                        newVariablesName.append(variablename+ '.'+ subvariablename)
                variablesName= newVariablesName
                self.sourcemat.load_signals(componentname, variablesName)
            if not self.outh5.exist_PowerSystemResource(componentname):
                self.outh5.add_PowerSystemResource(componentname)
            else:
                self.outh5.update_PowerSystemResource(componentname,componentname)
            for variable in variablesName:
                paramName= componentname+ '.'+ variable
                if not self.outh5.exist_AnalogMeasurement(variable):
                    self.outh5.add_AnalogMeasurement(variable)
                    self.outh5.add_AnalogValue(self.sourcemat.senyal['sampletime'], 
                                         self.sourcemat.senyal[paramName])
                else:
                    self.outh5.update_AnalogMeasurement(variable)
                    self.outh5.update_AnalogValue(variable,self.sourcemat.senyal['sampletime'], 
                                         self.sourcemat.senyal[paramName])
            self.sourcemat.clear_signals()
        self.outh5.close()
    