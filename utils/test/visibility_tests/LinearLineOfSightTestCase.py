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
TableToPointTestCase.py
--------------------------------------------------
requirements:
* ArcGIS Desktop 10.X+ or ArcGIS Pro 1.X+
* Python 2.7 or Python 3.4

author: ArcGIS Solutions
company: Esri

==================================================
history:
5/18/2016 - DJH - initial creation
5/24/2016 - MF - update for parameter changes in Pro
5/27/2016 - MF - change unittest fail pattern to catch tool errors
==================================================
'''

import unittest
import arcpy
import os
import UnitTestUtilities
import Configuration

class LinearLineOfSightTestCase(unittest.TestCase):
    ''' Test all tools and methods related to the Linear Line Of Sight tool
    in the Military Tools toolbox'''

    inputTable = None
    outputPoints = None

    def setUp(self):
        if Configuration.DEBUG == True: print(".....LinearLineOfSightTestCase.setUp")

        UnitTestUtilities.checkArcPy()
        if(Configuration.militaryScratchGDB == None) or (not arcpy.Exists(Configuration.militaryScratchGDB)):
            Configuration.militaryScratchGDB = UnitTestUtilities.createScratch(Configuration.militaryDataPath)

        self.observers = os.path.join(Configuration.militaryInputDataGDB, "LLOS_Observers_ArcMap")
        self.targets = os.path.join(Configuration.militaryInputDataGDB, "LLOS_Targets_ArcMap")
        self.inputSurface = os.path.join(Configuration.militaryInputDataGDB, "ElevationUTM_Zone10")
        self.outputLOS = os.path.join(Configuration.militaryScratchGDB, "outputLinearLineOfSight")
        self.outputSightLines = os.path.join(Configuration.militaryScratchGDB, "outputSightLines")

        if arcpy.CheckExtension("Spatial") == "Available":
            arcpy.CheckOutExtension("Spatial")
            if Configuration.DEBUG == True: print(".....Spatial checked out")
        if arcpy.CheckExtension("3D") == "Available":
            arcpy.CheckOutExtension("3D")
            if Configuration.DEBUG == True: print(".....3D checked out")

    def tearDown(self):
        if Configuration.DEBUG == True: print(".....LinearLineOfSightTestCase.tearDown")
        arcpy.CheckInExtension("Spatial");
        UnitTestUtilities.deleteScratch(Configuration.militaryScratchGDB)

    def test_linear_line_of_sight_desktop(self):
        ''' Test Linear Line of Sight for ArcGIS Desktop '''
        try:
            runToolMessage = ".....LinearLineOfSightTestCase.test_linear_line_of_sight_desktop"
            arcpy.ImportToolbox(Configuration.military_DesktopToolboxPath, "mt")
            print(runToolMessage)
            Configuration.Logger.info(runToolMessage)

            arcpy.LinearLineOfSight_mt(self.observers, self.targets, self.inputSurface, self.outputLOS)
            self.assertTrue(arcpy.Exists(self.outputLOS), "Output lines do not exist")

            featureCount = int(arcpy.GetCount_management(self.outputLOS).getOutput(0))
            expectedNumFeats = int(32)
            self.assertEqual(featureCount, expectedNumFeats, "Expected %s lines but got %s" % (str(expectedNumFeats), str(featureCount)))

        except arcpy.ExecuteError:
            failMsg = runToolMessage + "/n" + str(arcpy.GetMessages())
            self.fail(failMsg)
            Configuration.Logger.error(failMsg)

    def test_linear_line_of_sight_pro(self):
        ''' Test Linear Line of Sight for ArcGIS Pro '''
        try:
            runToolMessage = ".....LinearLineOfSightTestCase.test_linear_line_of_sight_pro"
            arcpy.ImportToolbox(Configuration.military_ProToolboxPath, "mt")
            print(runToolMessage)
            Configuration.Logger.info(runToolMessage)

            #
            arcpy.LinearLineOfSight_mt(self.observers, self.targets, self.inputSurface, self.outputLOS, self.outputSightLines)
            self.assertTrue(arcpy.Exists(self.outputLOS), "Output LOS lines do not exist")
            self.assertTrue(arcpy.Exists(self.outputSightLines), "Output sight lines do not exist")

            featureCount = int(arcpy.GetCount_management(self.outputLOS).getOutput(0))
            expectedLOS = int(32)
            self.assertEqual(featureCount, expectedLOS, "Expected %s point but got %s" % (str(expectedLOS), str(featureCount)))
            
            featureCountSightLines = int(arcpy.GetCount_management(self.outputSightLines).getOutput(0))
            expectedSightLines = int(16)
            self.assertEqual(featureCountSightLines, expectedSightLines, "Expected %s point but got %s" % (str(expectedSightLines), str(featureCountSightLines)))

        except arcpy.ExecuteError:
            failMsg = runToolMessage + "/n" + str(arcpy.GetMessages())
            self.fail(failMsg)
            Configuration.Logger.error(failMsg)
