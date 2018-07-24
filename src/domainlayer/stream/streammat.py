'''
Created on 28 jan 2016

@author: fragom
'''

from modelicares import SimRes

class ChannelMAT(object):
    '''
    classdocs
    '''
    _resultFile= None
    _compiler= ''
    
    def __init__(self, params):
        '''
        Constructor
        '''
        self._resultFile= SimRes(params[0])
        print self._resultFile
        self._compiler= params[1]
    
class InputChannelMAT(ChannelMAT):
    '''
    classdocs
    '''
    __components= {} 
    __variables= []
    __senyal= {}
    
    def __init__(self, matfile, compiler= 'openmodelica'):
        super(InputChannelMAT,self).__init__([matfile, compiler])
        
    @property
    def senyal(self, variablename):
        return self.__senyal[variablename]

    def get_variables(self):
        return self.__variables

    def set_variables(self, value):
        self.__variables = value

    def del_variables(self):
        del self.__variables

    @property
    def components(self):
        return self.__components
        
        
    def load_components(self):
        ''' from the object file, loads the name of the components of the network '''
        self.__components= sorted(self._resultFile.nametree().keys())
    
    def load_variables(self, componentes):
        '''
        components
        '''
        #TODO improve the importer to show variable names
        for component in componentes:
            self.__variables.append(self._resultFile.nametree()[component].keys())
        
    def load_subvariables(self, component, variable):
        '''
        component
        variables
        '''
        idx= self._resultFile.nametree()[component].keys().index(variable)
        self.__variables= self._resultFile.nametree()[component].values()[idx].keys()
        
    def load_signals(self, component, variables):
        '''
        components, is an array
        variables, is an array
        '''
        if self._compiler== 'openmodelica': 
            nameVarTime= 'time' 
        else: 
            nameVarTime= "Time"
        self.__senyal['sampletime']= self._resultFile[nameVarTime].times().tolist()
        for var in variables:
            variableName= component+ '.'+ var
            self.__senyal[variableName]= self._resultFile[variableName].values().tolist()
#         print self.__signalData
            
    def clear_signals(self):
        self.__senyal= {}
    
    variables = property(get_variables, set_variables, del_variables, "variables's docstring")
