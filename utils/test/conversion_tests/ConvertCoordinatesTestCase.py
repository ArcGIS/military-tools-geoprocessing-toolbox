# coding: utf-8
'''
-----------------------------------------------------------------------------
Copyright 2016 Esri
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-----------------------------------------------------------------------------

==================================================
ConvertCoordinatesTestCase.py
--------------------------------------------------
requirements:
* ArcGIS Desktop 10.X+ or ArcGIS Pro 1.X+
* Python 2.7 or Python 3.4

author: ArcGIS Solutions
company: Esri

==================================================
history:
5/11/2016 - JH - initial creation
5/27/2016 - MF - change unittest fail pattern to catch tool errors
==================================================
'''

import unittest
import arcpy
import os
import UnitTestUtilities
import Configuration

class ConvertCoordinatesTestCase(unittest.TestCase):
    ''' Test all tools and methods related to the Convert Coordinates tool
    in the Military Tools toolbox'''
    
    inputTable = None
    outputConvert = None
    
    def setUp(self):
        if Configuration.DEBUG == True: print(".....ConvertCoordinatesTestCase.setUp")    
        
        UnitTestUtilities.checkArcPy()
        if(Configuration.militaryScratchGDB == None) or (not arcpy.Exists(Configuration.militaryScratchGDB)):
            Configuration.militaryScratchGDB = UnitTestUtilities.createScratch(Configuration.militaryDataPath)

        self.inputTable = os.path.join(Configuration.militaryInputDataGDB, "SigActs")
        self.outputConvert = os.path.join(Configuration.militaryScratchGDB, "outputConvert")
        
    def tearDown(self):
        if Configuration.DEBUG == True: print(".....ConvertCoordinatesTestCase.tearDown")
        UnitTestUtilities.deleteScratch(Configuration.militaryScratchGDB)
    
    def test_convert_coordinates_desktop(self):
        ''' Test Convert Coordinates in ArcGIS Desktop '''
        try:
            runToolMessage = ".....ConvertCoordinatesTestCase.test_convert_coordinates_desktop"
            arcpy.ImportToolbox(Configuration.military_DesktopToolboxPath, "mt")
            print(runToolMessage)
            Configuration.Logger.info(runToolMessage)
            
            arcpy.ConvertCoordinates_mt(self.inputTable, "DD_2", "Location_X", "Location_Y", self.outputConvert)
            
            self.assertTrue(arcpy.Exists(self.outputConvert), "Output points do not exist")
            
            featureCount = int(arcpy.GetCount_management(self.outputConvert).getOutput(0))
            expectedNumFeats = int(288)
            self.assertEqual(featureCount, expectedNumFeats, "Expected %s points but got %s" % (str(expectedNumFeats), str(featureCount)))

        except arcpy.ExecuteError:
            UnitTestUtilities.handleArcPyError()

    def test_convert_coordinates_pro(self):
        ''' Test Convert Coordinates in ArcGIS Pro '''
        try:
            runToolMessage = ".....ConvertCoordinatesTestCase.test_convert_coordinates_pro"
            arcpy.ImportToolbox(Configuration.military_ProToolboxPath, "mt")
            print(runToolMessage)
            Configuration.Logger.info(runToolMessage)
            
            arcpy.ConvertCoordinates_mt(self.inputTable, "DD_2", "Location_X", "Location_Y", self.outputConvert)
            
            self.assertTrue(arcpy.Exists(self.outputConvert), "Output points do not exist")
            
            featureCount = int(arcpy.GetCount_management(self.outputConvert).getOutput(0))
            expectedNumFeats = int(288)
            self.assertEqual(featureCount, expectedNumFeats, "Expected %s points but got %s" % (str(expectedNumFeats), str(featureCount)))

        except arcpy.ExecuteError:
            UnitTestUtilities.handleArcPyError()
        