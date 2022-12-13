class ToolValidator:
  # Class to add custom behavior and properties to the tool and tool parameters.

    def __init__(self):
        # set self.params for use in other function
        self.params = arcpy.GetParameterInfo()

    def initializeParameters(self):
        # Customize parameter properties. 
        # This gets called when the tool is opened.
        return

    def updateParameters(self):
        ################
        
        # Enable pyramids resampling algorithm parameter if the pyramids box is checked
        
        # Parameters:
        # -self.params[4]: Pyramids checkbox
        # -self.params[5]: Algorithm for pyramids generation
        
        ################
        
        if self.params[4].value == True:
            self.params[5].enabled = True
        else:
            self.params[5].enabled = False
        
        return

    def updateMessages(self):
        ################
        
        # Allow tool parameters to respond and interact with values and other parameters on the script.
        # Display error messages when the parameter values are different from what is expected
        
        # Parameters:
        # -self.params[0]: File path of the input raster
        # -self.params[1]: File path of the output raster
        # -self.params[2]: The new cell size
        # -self.params[5]: Algorithm for pyramids generation
        
        ################
    
    
        # Check that the input exists
        location = arcpy.da.Describe(self.params[0])['catalogPath']
        if not arcpy.Exists(location):
            self.params[0].setErrorMessage('The input raster does not exist')
            
        # Check the raster extension
        if arcpy.da.Describe(self.params[0])['extension'] != 'tif':
            self.params[0].setErrorMessage('The input is not a GTiff file')
            
        # The output must be a tif and, thus, saved outside a geodatabase
        if self.params[1].altered:
            if self.params[1].valueAsText[-4:] != '.tif':
                self.params[1].setErrorMessage('The output is not a GTiff file')  
            if '.gdb' in self.params[1].valueAsText:
                self.params[1].setErrorMessage('The output file cannot be saved in a GDB')     
           
        # Cell size must be a positive number
        if self.params[2].altered:
            if self.params[2].value <= 0:
                self.params[2].setErrorMessage('Zero or negative cell size value is invalid')
        
        # Optional parameter (Pyramids resampling algorithm) behaves as a required parameter when enabled 
        self.params[5].setIDMessage('WARNING', 530)      
        
        return