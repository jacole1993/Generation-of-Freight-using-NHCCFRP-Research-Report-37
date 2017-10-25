import arcpy, numpy as np
arcpy.AddMessage("-----------------")
arcpy.AddMessage("Task I: Initialize Input Data")

Establishments = arcpy.GetParameterAsText(0)  # Point Feature Layer (geodatabase)
NAICSField = arcpy.GetParameterAsText(1)  # Name of NAICS field in Establishments layer
EmploymentField = arcpy.GetParameterAsText(2)  # Name of Employment field in Establishments layer
SICField = arcpy.GetParameterAsText(3)
if not SICField:
    SICField=0
ALLFreight = arcpy.GetParameterAsText(5)
Metrics = arcpy.GetParameterAsText(6)
Metrics = Metrics.split(";")
Models = arcpy.GetParameterAsText(7)
if Models:
    Models = Models.split(";")
CFS=arcpy.GetParameterAsText(9)
if CFS:
    CFS = CFS.split(";")
Out = arcpy.GetParameterAsText(10) # Output folder where aggregated model estimates will be exported




arcpy.CreateFileGDB_management(Out, "FTG_Geodatabase.gdb")
OutFolder = Out + "/FTG_Geodatabase.gdb"

arcpy.AddMessage("Done With Task I")
arcpy.AddMessage("---------------")
arcpy.AddMessage("Task II: Inputing Field Data")

# DEFINE TABLE DICTIONARY
ModMetDictionary = {'FTA linear models: Table 9NYC and CR': 'Table_9_Both', 'FTA linear models: Table 9NYC': 'Table_9_NYC', 'FTA linear models: Table 9CR': 'Table_9_CR', 'FTA non-linear models: Table 10NYC and CR': 'Table_10_Both', 'FTA non-linear models: Table 10NYC': 'Table_10_NYC', 'FTA non-linear models: Table 10CR': 'Table_10_CR',
                    'FTP linear models: Table 11NYC and CR': 'Table_11_Both', 'FTP linear models: Table 11NYC': 'Table_11_NYC', 'FTP linear models: Table 11CR': 'Table_11_CR', 'FTP non-linear models: Table 12NYC and CR': 'Table_12_Both', 'FTP non-linear models: Table 12NYC': 'Table_12_NYC', 'FTP non-linear models: Table 12CR': 'Table_12_CR',
                    'STA linear models: Table 14NYC and CR': 'Table_14_Both', 'STA linear models: Table 14NYC': 'Table_14_NYC', 'STA linear models: Table 14CR': 'Table_14_CR', 'STA non-linear models: Table 15NYC and CR': 'Table_15_Both', 'STA non-linear models: Table 15NYC': 'Table_15_NYC', 'STA non-linear models: Table 15CR': 'Table_15_CR',
                    'FA linear models: Table 16NYC and CR': 'Table_16_Both', 'FA linear models: Table 16NYC': 'Table_16_NYC', 'FA linear models: Table 16CR': 'Table_16_CR', 'FA non-linear models: Table 17NYC and CR': 'Table_17_Both', 'FA non-linear models: Table 17NYC': 'Table_17_NYC', 'FA non-linear models: Table 17CR': 'Table_17_CR',
                    'FP linear models: Table 18NYC and CR': 'Table_18_Both', 'FP linear models: Table 18NYC': 'Table_18_NYC', 'FP linear models: Table 18CR': 'Table_18_CR', 'FP non-linear models: Table 19NYC and CR': 'Table_19_Both','FP non-linear models: Table 19NYC': 'Table_19_NYC', 'FP non-linear models: Table 19CR': 'Table_19_CR',}


FTGDictionary = {'FTG rates models: Table 13': 'Table_13'}

FADictionary={'Relationship between FA and FTA linear models: Table 20': 'Table_20_Both', 'Relationship between FTA and FA non-linear models: Table 21': 'Table_21_Both', 'Relationship between FP and FTP linear models: Table 22': 'Table_22_Both', 'FTP as a function of FP non-linear models: Table 23': 'Table_23_Both'}


FPDictionary = {'2-digit NAICS All modes Linear Model New York State: Table 24': 'Table_24_CFS', '3-digit NAICS All modes Linear Model New York State: Table 25': 'Table_25_CFS', '2-digit NAICS Road modes Linear Model New York State: Table 26': 'Table_26_CFS', '3-digit NAICS Road modes Linear Model New York State: Table 27': 'Table_27_CFS', '2-digit NAICS All modes Lin-Log Model New York State: Table 28': 'Table_28_CFS', '2-digit NAICS All modes Log-Log Model New York State: Table 29': 'Table_29_CFS', '2-digit NAICS All modes Log-Lin Model New York State: Table 30': 'Table_30_CFS', '3-digit NAICS All modes Lin-Log Model New York State: Table 31': 'Table_31_CFS', '3-digit NAICS All modes Log-Log Model New York State: Table 32': 'Table_32_CFS', '3-digit NAICS All modes Log-Lin Model New York State: Table 33': 'Table_33_CFS', '2-digit NAICS Road modes Lin-Log Model New York State: Table 34': 'Table_34_CFS', '2-digit NAICS Road modes Log-Log Model New York State: Table 35': 'Table_35_CFS', '2-digit NAICS Road modes Log-Lin Model New York State: Table 36': 'Table_36_CFS', '3-digit NAICS Road modes Lin-Log Model New York State: Table 37': 'Table_37_CFS', '3-digit NAICS Road modes Log-Log Model New York State: Table 38': 'Table_38_CFS', '3-digit NAICS Road modes Log-Lin Model New York State: Table 39': 'Table_39_CFS',
                 '2-digit NAICS All modes Linear Model California: Table 40': 'Table_40_CFS', '3-digit NAICS All modes Linear Model California: Table 41': 'Table_41_CFS', '2-digit NAICS Road modes Linear Model California: Table 42': 'Table_42_CFS', '3-digit NAICS Road modes Linear Model California: Table 43': 'Table_43_CFS', '2-digit NAICS All modes Lin-Log Model California: Table 44': 'Table_44_CFS', '2-digit NAICS All modes Log-Log Model California: Table 45': 'Table_45_CFS', '2-digit NAICS All modes Log-Lin Model California: Table 46': 'Table_46_CFS', '3-digit NAICS All modes Lin-Log Model California: Table 47': 'Table_47_CFS', '3-digit NAICS All modes Log-Log Model California: Table 48': 'Table_48_CFS', '3-digit NAICS All modes Log-Lin Model California: Table 49': 'Table_49_CFS', '2-digit NAICS Road modes Lin-Log Model California: Table 50': 'Table_50_CFS', '2-digit NAICS Road modes Log-Log Model California: Table 51': 'Table_51_CFS', '2-digit NAICS Road modes Log-Lin Model California: Table 52': 'Table_52_CFS', '3-digit NAICS Road modes Lin-Log Model California: Table 53': 'Table_53_CFS', '3-digit NAICS Road modes Log-Log Model California: Table 54': 'Table_54_CFS', '3-digit NAICS Road modes Log-Lin Model California: Table 55': 'Table_55_CFS',
                 '2-digit NAICS All modes Linear Model Texas: Table 56': 'Table_56_CFS', '3-digit NAICS All modes Linear Model Texas: Table 57': 'Table_57_CFS', '2-digit NAICS Road modes Linear Model Texas: Table 58': 'Table_58_CFS', '3-digit NAICS Road modes Linear Model Texas: Table 59': 'Table_59_CFS', '2-digit NAICS All modes Lin-Log Model Texas: Table 60': 'Table_60_CFS', '2-digit NAICS All modes Log-Log Model Texas: Table 61': 'Table_61_CFS', '2-digit NAICS All modes Log-Lin Model Texas: Table 62': 'Table_62_CFS', '3-digit NAICS All modes Lin-Log Model Texas: Table 63': 'Table_63_CFS', '3-digit NAICS All modes Log-Log Model Texas: Table 64': 'Table_64_CFS', '3-digit NAICS All modes Log-Lin Model Texas: Table 65': 'Table_65_CFS', '2-digit NAICS Road modes Lin-Log Model Texas: Table 66': 'Table_66_CFS', '2-digit NAICS Road modes Log-Log Model Texas: Table 67': 'Table_67_CFS', '2-digit NAICS Road modes Log-Lin Model Texas: Table 68': 'Table_68_CFS', '3-digit NAICS Road modes Lin-Log Model Texas: Table 69': 'Table_69_CFS', '3-digit NAICS Road modes Log-Log Model Texas: Table 70': 'Table_70_CFS', '3-digit NAICS Road modes Log-Lin Model Texas: Table 71': 'Table_71_CFS',
                 '2-digit NAICS All modes Linear Model Wyoming: Table 72': 'Table_72_CFS', '3-digit NAICS All modes Linear Model Wyoming: Table 73': 'Table_73_CFS', '2-digit NAICS Road modes Linear Model Wyoming: Table 74': 'Table_74_CFS', '3-digit NAICS Road modes Linear Model Wyoming: Table 75': 'Table_75_CFS', '2-digit NAICS All modes Lin-Log Model Wyoming: Table 76': 'Table_76_CFS', '2-digit NAICS All modes Log-Log Model Wyoming: Table 77': 'Table_77_CFS', '2-digit NAICS All modes Log-Lin Model Wyoming: Table 78': 'Table_78_CFS', '3-digit NAICS All modes Lin-Log Model Wyoming: Table 79': 'Table_79_CFS', '3-digit NAICS All modes Log-Log Model Wyoming: Table 80': 'Table_80_CFS', '3-digit NAICS All modes Log-Lin Model Wyoming: Table 81': 'Table_81_CFS', '2-digit NAICS Road modes Lin-Log Model Wyoming: Table 82': 'Table_82_CFS', '2-digit NAICS Road modes Log-Log Model Wyoming: Table 83': 'Table_83_CFS', '2-digit NAICS Road modes Log-Lin Model Wyoming: Table 84': 'Table_84_CFS', '3-digit NAICS Road modes Lin-Log Model Wyoming: Table 85': 'Table_85_CFS', '3-digit NAICS Road modes Log-Log Model Wyoming: Table 86': 'Table_86_CFS', '3-digit NAICS Road modes Log-Lin Model Wyoming: Table 87': 'Table_87_CFS',
                 '2-digit NAICS All modes Linear Model Ohio: Table 88': 'Table_88_CFS', '3-digit NAICS All modes Linear Model Ohio: Table 89': 'Table_89_CFS', '2-digit NAICS Road modes Linear Model Ohio: Table 90': 'Table_90_CFS', '3-digit NAICS Road modes Linear Model Ohio: Table 91': 'Table_91_CFS', '2-digit NAICS All modes Lin-Log Model Ohio: Table 92': 'Table_92_CFS', '2-digit NAICS All modes Log-Log Model Ohio: Table 93': 'Table_93_CFS', '2-digit NAICS All modes Log-Lin Model Ohio: Table 94': 'Table_94_CFS', '3-digit NAICS All modes Lin-Log Model Ohio: Table 95': 'Table_95_CFS', '3-digit NAICS All modes Log-Log Model Ohio: Table 96': 'Table_96_CFS', '3-digit NAICS All modes Log-Lin Model Ohio: Table 97': 'Table_97_CFS', '2-digit NAICS Road modes Lin-Log Model Ohio: Table 98': 'Table_98_CFS', '2-digit NAICS Road modes Log-Log Model Ohio: Table 99': 'Table_99_CFS', '2-digit NAICS Road modes Log-Lin Model Ohio: Table 100': 'Table_100_CFS', '3-digit NAICS Road modes Lin-Log Model Ohio: Table 101': 'Table_101_CFS', '3-digit NAICS Road modes Log-Log Model Ohio: Table 102': 'Table_102_CFS', '3-digit NAICS Road modes Log-Lin Model Ohio: Table 103': 'Table_103_CFS',
                 '2-digit NAICS All modes Linear Model United States: Table 104': 'Table_104_CFS', '3-digit NAICS All modes Linear Model United States: Table 105': 'Table_105_CFS', '2-digit NAICS Road modes Linear Model United States: Table 106': 'Table_106_CFS', '3-digit NAICS Road modes Linear Model United States: Table 107': 'Table_107_CFS', '2-digit NAICS All modes Lin-Log Model United States: Table 108': 'Table_108_CFS', '2-digit NAICS All modes Log-Log Model United States: Table 109': 'Table_109_CFS', '2-digit NAICS All modes Log-Lin Model United States: Table 110': 'Table_110_CFS', '3-digit NAICS All modes Lin-Log Model United States: Table 111': 'Table_111_CFS', '3-digit NAICS All modes Log-Log Model United States: Table 112': 'Table_112_CFS', '3-digit NAICS All modes Log-Lin Model United States: Table 113': 'Table_113_CFS', '2-digit NAICS Road modes Lin-Log Model United States: Table 114': 'Table_114_CFS', '2-digit NAICS Road modes Log-Log Model United States: Table 115': 'Table_115_CFS', '2-digit NAICS Road modes Log-Lin Model United States: Table 116': 'Table_116_CFS', '3-digit NAICS Road modes Lin-Log Model United States: Table 117': 'Table_117_CFS', '3-digit NAICS Road modes Log-Log Model United States: Table 118': 'Table_118_CFS', '3-digit NAICS Road modes Log-Lin Model United States: Table 119': 'Table_119_CFS'}

OutFeatureClass = OutFolder + "/FreightGenerationOutput"
arcpy.CopyFeatures_management(Establishments, OutFeatureClass)


arcpy.AddField_management(Establishments, 'NAICS2D', 'DOUBLE')
exp = """int(str(!%s!)[:2])""" % NAICSField
arcpy.CalculateField_management(Establishments, 'NAICS2D', exp,  "PYTHON_9.3")

arcpy.AddField_management(Establishments, 'NAICS3D', 'DOUBLE')
exp = """int(str(!%s!)[:3])""" % NAICSField
arcpy.CalculateField_management(Establishments, 'NAICS3D', exp,  "PYTHON_9.3")

arcpy.AddField_management(Establishments, 'Employment', 'DOUBLE')
exp = """!%s!""" % EmploymentField
arcpy.CalculateField_management(Establishments, 'Employment', exp,  "PYTHON_9.3")
arcpy.AddMessage("-----------------")


if SICField:
    arcpy.AddField_management(Establishments, 'SIC2D', 'DOUBLE')
    exp = """int(str(!%s!)[:2])""" % SICField
    arcpy.CalculateField_management(Establishments, 'SIC2D', exp,  "PYTHON_9.3")
    arcpy.AddMessage("-----------------")
    array = arcpy.da.FeatureClassToNumPyArray(Establishments, ["OBJECTID", 'SIC2D', 'NAICS2D', 'Employment', 'NAICS3D'])
    uniqueSIC = np.unique(array['SIC2D'])

else:
    array = arcpy.da.FeatureClassToNumPyArray(Establishments, ["OBJECTID", 'NAICS2D', 'Employment', 'NAICS3D'])

# GET UNIQUE NAICS 2D, 3D AND SIC VALUES
uniqueNAICS = np.unique(array['NAICS2D'])
unique3DNAICS = np.unique(array['NAICS3D'])



# STORED NCHRP 37 TABLES
Table_9_Both = np.array([(23, 2.132, 0.059), (31, 1.825, 0.032), (32, 0, 0.153), (33, 2.276, 0.075), (42, 3.669, 0.081), (44, 2.793, 0.143), (45, 3.375, 0.0), (48, 10.157, 0.0), (72, 1.918, 0.07)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_9_Both_ALL = np.array([(3.061, 0.079)], dtype=[('alpha', '<f8'), ('beta', '<f8')])
Table_9_NYC = np.array([(23, 2.168, 0.059), (31, 1.705, 0.035), (32, 0, 0.157), (33, 2.056, 0.082), (42, 3.91, 0.079), (44, 2.97, 0.144), (45, 3.4, 0.0), (48, 11.291, 0.0), (72, 2.081, 0.069)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_9_NYC_ALL = np.array([(3.072, 0.078)], dtype=[('alpha', '<f8'), ('beta', '<f8')])
Table_9_CR = np.array([(23, 2.789, 0), (31, 3.4, 0), (32, 3.315, 0), (33, 0, 0.07), (42, 3.282, 0), (44, 2.042, 0.105), (45, 0, 0.262), (72, 1.141, 0)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_9_CR_ALL = np.array([(2.932, 0.093)], dtype=[('alpha', '<f8'), ('beta', '<f8')])
Table_10_Both = np.array([(23, 1.565, 0.275), (31, 1.169, 0.298), (32, 0.517, 0.603), (33, 0.803, 0.54), (42, 1.142, 0.539), (44, 1.571, 0.465), (45, 1.541, 0.316), (48, 2.463, 0.47), (72, 0.918, 0.477)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_10_Both_ALL = np.array([(1.389, 0.428)], dtype=[('alpha', '<f8'), ('beta', '<f8')])
Table_10_NYC = np.array([(23, 1.574, 0.28), (31, 1.183, 0.292), (32, 0.767, 0.606), (33, 0.801, 0.54), (42, 1.182, 0.538), (44, 1.566, 0.477), (45, 1.568, 0.307), (48, 3.154, 0.448), (72, 1.449, 0.342)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_10_NYC_ALL = np.array([(1.607, 0.38)], dtype=[('alpha', '<f8'), ('beta', '<f8')])
Table_10_CR = np.array([(23, 1.576, 0.23), (31, 1.033, 0.346), (32, 1.585, 0.304), (33, 1.769, 0.345), (42, 1.511, 0.338), (44, 1.59, 0.372), (45, 1.163, 0.467), (72, 0.335, 0.521)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_10_CR_ALL = np.array([(0.749, 0.639)], dtype=[('alpha', '<f8'), ('beta', '<f8')])
Table_11_Both= np.array([(23, 0, 0.092), (31, 0, 0.117), (32, 5.511, 0.135), (33, 5.769, 0.021), (42, 6.455, 0), (44, 0, 0.321), (45, 3.956, 0.179), (48, 8.5, 0), (72, 0, 0.114)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_11_Both_ALL= np.array([(3.8, 0.085)], dtype=[('alpha', '<f8'), ('beta', '<f8')])
Table_11_NYC=np.array([(23, 0, 0.091), (31, 0, 0.11), (32, 7.394, 0.126), (33, 6.612, 0), (42, 6.021, 0), (44, 0, 0.295), (45, 3.49, 0.186), (48, 7.667, 0), (72, 0, 0.115)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_11_NYC_ALL = np.array([(3.386, 0.087)], dtype=[('alpha', '<f8'), ('beta', '<f8')])
Table_11_CR=np.array([(32, 2.564, 0.14), (33, 6.041, 0.037), (42, 7.25, 0),  (44, 0, 0.418)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_11_CR_ALL = np.array([(5.189, 0.09)], dtype=[('alpha', '<f8'), ('beta', '<f8')])
Table_12_Both= np.array([(23, 0.276, 0.896), (31, 1.581, 0.369), (32, 2.201, 0.572), (33, 2.133, 0.385), (42, 6.804, 0), (44, 0.806, 0.762), (45, 1.689, 0.603), (48, 9.714, 0), (72, 0.508, 0.706)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_12_Both_ALL= np.array([(1.348, 0.544)], dtype=[('alpha', '<f8'), ('beta', '<f8')])
Table_12_NYC= np.array([(23, 0.0, 0.639), (31, 1.607, 0.337), (32, 2.03, 0.608), (33, 1.782, 0.379), (42, 6.286, 0),  (44, 1.959, 0.404), (45, 1.651, 0.583), (48, 1.717, 0.413), (72, 1.468, 0.421)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_12_NYC_ALL= np.array([(1.122, 0.557)], dtype=[('alpha', '<f8'), ('beta', '<f8')])
Table_12_CR= np.array([(32, 2.623, 0.466), (33, 3.661, 0.403), (42, 2.007, 0.644), (44, 1.415, 0.628)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_12_CR_ALL= np.array([(2.659, 0.499)], dtype=[('alpha', '<f8'), ('beta', '<f8')])
Table_13 = np.array([(13.0, 0.097, 0.097, 0.097, 0.097, 0.097, 0.097), (15.0, 0.295, 0.255, 0.255, 0.255, 0.255, 0.255), (16.0, 0.206, 0.297, 0.206, 0.206, 0.206, 0.206), (17.0, 0.308, 0.644, 0.378, 0.51, 0.51, 0.51), (20.0, 0.124, 0.124, 0.124, 0.124, 0.02, 0.124), (24.0, 0.154, 0.154, 0.154, 0.154, 0.154, 0.154), (25.0, 0.052, 0.052, 0.052, 0.052, 0.052, 0.052), (27.0, 0.38, 0.575, 0.38, 0.039, 0.38, 0.38), (30.0, 0.884, 0.884, 0.884, 0.884, 0.884, 0.884), (33.0, 0.127, 0.127, 0.127, 0.127, 0.127, 0.127), (34.0, 0.317, 0.358, 0.298, 0.317, 0.317, 0.317), (35.0, 1.149, 1.149, 1.775, 1.149, 1.149, 1.149), (36.0, 0.117, 0.117, 0.117, 0.117, 0.117, 0.117), (37.0, 0.249, 0.249, 0.249, 0.249, 0.249, 0.249), (38.0, 2.092, 2.092, 2.092, 2.092, 2.092, 2.092), (39.0, 0.664, 0.664, 0.664, 0.664, 0.664, 0.664), (41.0, 0.028, 0.028, 0.028, 0.028, 0.028, 0.028), (42.0, 1.341, 1.341, 1.341, 1.341, 1.341, 1.341), (47.0, 0.051, 0.051, 0.051, 0.051, 0.051, 0.051), (48.0, 0.225, 0.225, 0.225, 0.225, 0.225, 0.225), (49.0, 0.045, 0.045, 0.045, 0.045, 0.045, 0.045), (50.0, 1.117, 0.382, 0.27, 0.027, 0.021, 0.542), (51.0, 1.03, 0.911, 0.075, 0.211, 0.124, 0.911), (52.0, 0.264, 0.509, 0.264, 0.07, 0.264, 0.264), (53.0, 0.078, 0.078, 0.078, 0.015, 0.078, 0.078), (54.0, 0.071, 0.071, 0.05, 0.071, 0.071, 0.071), (55.0, 0.279, 0.311, 0.279, 0.279, 0.279, 0.279), (56.0, 0.617, 0.617, 0.617, 0.617, 0.617, 0.617), (57.0, 0.215, 0.067, 0.215, 0.022, 0.215, 0.215), (58.0, 0.159, 0.057, 0.053, 0.159, 0.159, 0.159), (59.0, 0.344, 0.233, 0.344, 0.344, 0.344, 0.344), (60.0, 0.084, 0.084, 0.084, 0.084, 0.084, 0.084), (61.0, 0.183, 0.114, 0.114, 0.114, 0.114, 0.114), (62.0, 0.588, 0.588, 0.588, 0.588, 0.588, 0.588), (64.0, 0.067, 0.067, 0.067, 0.014, 0.067, 0.067), (65.0, 0.404, 0.364, 0.342, 0.342, 0.342, 0.342), (67.0, 0.088, 0.088, 0.088, 0.088, 0.088, 0.088), (70.0, 0.041, 0.041, 0.041, 0.042, 0.017, 0.041), (73.0, 0.439, 0.133, 0.086, 0.158, 0.223, 0.223), (76.0, 1.067, 1.067, 1.067, 1.067, 1.067, 1.067), (79.0, 0.435, 0.219, 0.219, 0.219, 0.03, 0.219), (80.0, 0.135, 0.102, 0.042, 0.101, 0.018, 0.056), (81.0, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3), (82.0, 0.028, 0.028, 0.032, 0.03, 0.007, 0.028), (83.0, 0.347, 0.171, 0.027, 0.171, 0.171, 0.171), (87.0, 1.515, 0.129, 0.117, 0.089, 0.359, 0.359), (91.0, 0.846, 0.846, 0.846, 0.017, 0.846, 0.846), (99.0, 0.403, 0.156, 0.052, 0.156, 0.156, 0.156)], dtype=[('SIC2D', '<i4'), ('F10', '<f8'), ('F40', '<f8'), ('F149', '<f8'), ('F999', '<f8'), ('F1000', '<f8'), ('AVG', '<f8')])
Table_13_ALL = np.array((100, 0.638, 0.45, 0.194, 0.073, 0.097, 0.313), dtype=[('SIC2D', '<i4'), ('F10', '<f8'), ('F40', '<f8'), ('F149', '<f8'), ('F999', '<f8'), ('F1000', '<f8'), ('AVG', '<f8')])
Table_14_Both =np.array([(23, 0, 4.07E-03), (31, 0.197, 0), (32, 0.251, 0),(33, 0.23, 0), (42, 0.304, 0), (44, 0, 0.012), (45, 0.174, 0), (48, 0, 9.30E-03), (51, 0.595, 0), (52, 0.85, 0), (53, 0, 9.23E-04), (54, 0.391, 7.99E-04), (56, 0.291, 0), (61, 0.439, 0), (62, 1.179, 0), (71, 0.763, 0), (72, 0, 0.022), (81, 0.571, 0)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_14_Both_ALL= np.array([(0.408, 1.09E-03)], dtype=[('alpha', '<f8'), ('beta', '<f8')])
Table_14_NYC= np.array([(23, 0, 3.92E-03), (31, 0.167, 0), (32, 0.233, 0), (33, 0.298, 0), (42, 0.266, 0), (44, 0.295, 0), (45, 0.091, 0), (48, 0, 9.25E-03), (51, 0.804, 0), (52, 0.428, 3.22E-04), (53, 0, 9.15E-04), (54, 0, 1.10E-03), (56, 0.393, 0), (61, 0, 2.77E-03), (62, 1.126, 0), (71, 0.879, 0), (72, 0, 0.017), (81, 0.571, 0)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_14_NYC_ALL= np.array([ (0.42, 4.10E-04)], dtype=[('alpha', '<f8'), ('beta', '<f8')])
Table_14_CR= np.array([(23, 0.258, 0), (31, 0.227, 0), (32, 0.284, 0), (33, 0.123, 0), (42, 0, 0.021), (44, 0, 0.018), (45, 0, 0.017), (51, 0, 0.013), (53, 0.08, 0), (54, 0.5, 0), (56, 0.19, 0), (61, 0, 0.036), (62, 0.466, 8.53E-03), (72, 0, 0.054)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_14_CR_ALL= np.array([ (0.184, 0.012)], dtype=[('alpha', '<f8'), ('beta', '<f8')])
Table_15_Both =np.array([(23, 0.309, 0), (31, 0.222, 0), (32, 0.256, 0), (33, 0.058, 0.347), (42, 0.134, 0.263), (44, 0.312, 0), (45, 0.197, 0), (48, 0.007, 1.073), (51, 0.044, 0.582), (52, 1.173, 0), (53, 0.279, 0), (54, 0.635, 0), (56, 0.077, 0.362), (61, 0.45, 0), (62, 1.632, 0), (71, 1.003, 0), (72, 0.08, 0.697), (81, 0.596, 0)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_15_Both_ALL=  np.array([(0.137, 0.362)], dtype=[('alpha', '<f8'), ('beta', '<f8')])
Table_15_NYC= np.array([ (23, 0.326, 0), (31, 0.201, 0), (32, 0.247, 0), (33, 0.322, 0), (42, 0.302, 0), (44, 0.339, 0), (45, 0.099, 0), (48, 0.003, 1.278), (51, 0.887, 0), (52, 0.897, 0), (53, 0.012, 0.567), (54, 0.884, 0), (56, 0.46, 0), (61, 0.021, 0.592), (62, 1.689, 0), (71, 1.22, 0), (72, 0.64, 0), (81, 0.596, 0)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_15_NYC_ALL= np.array([  ( 0.518, 0)], dtype=[('alpha', '<f8'), ('beta', '<f8')])
Table_15_CR= np.array([ (23, 0.359, 0), (31, 0.304, 0), (32, 0.298, 0), (33, 0.036, 0.433), (42, 0.05, 0.742), (44, 0.018, 0.96), (45, 0.374, 0), (51, 0.026, 0.749), (53, 0.082, 0), (54, 0.556, 0), (56, 0.183, 0), (61, 0.036, 1.198), (62, 0.111, 0.602), (72, 0.016, 1.546)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_15_CR_ALL=  np.array([ (0.037, 0.846)], dtype=[('alpha', '<f8'), ('beta', '<f8')])
Table_16_Both= np.array([ (31-33, 46.492), (31, 109.978), (33, 25.427), (42, 431.221), (44, 100.519), (72, 8.853)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_16_NYC= np.array([ (31, 137.905), (42, 351.038), (44, 87.484), (72, 8.135)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_16_CR= np.array([ (23, 153.338), (32, 818.186), (42, 3089.543), (44, 248.448), (72, 26.734)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_17_Both=np.array([(23, 50.149, 1.626536), (31, 68.341, 1.645), (32, 4274.54, 0.982), (33, 87.103, 1.029), (42, 11500.09, 0.802), (44, 1266.153, 0.733), (72, 21.716, 1.69)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_17_Both_ALL=np.array([(4420.138, 0.452)], dtype=[('alpha', '<i4'), ('beta', '<f8')])
Table_17_CR=np.array([(23, 7.986, 2.270933), (31, 56.714, 1.701), (32, 9.348, 2.664), (33, 61.151, 0.947), (42, 5219.031, 1.304), (44, 261.045, 1.169), (45, 73.831, 3.96), (72, 5.736, 2.091)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_17_CR_ALL=np.array([(1625.239, 0.913)], dtype=[('alpha', '<i4'), ('beta', '<f8')])
Table_17_NYC=np.array([ (23, 58.93, 1.484038), (31, 218.448, 1.615), (32, 441.517, 1.867), (33, 158.637, 1.031), (44, 80.449, 1.559), (45, 251.826, 1.342), (72, 26.272, 1.64)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_17_NYC_ALL=np.array([(2522.368, 0.532)], dtype=[('alpha', '<i4'), ('beta', '<f8')])
Table_18_Both= np.array([(31, 216.084), (32, 119.151), (33, 9.993), (44, 91.439), (72, 1.855)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_18_NYC= np.array([(31, 212.291), (32, 88.971), (42, 229.101), (72, 1.867)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_18_CR= np.array([(23, 16.302), (32, 698.234), (42, 4442.041) , (44, 125.219) ,(45, 1588.257)], dtype=[('NAICS', '<i4'),  ('beta', '<f8')])
Table_19_NYC= np.array([(23, 2.331, 0.93), (31, 19.404, 1.84), (32, 7144.925, 1.98), (33, 7.5, 1.32), (42, 142.334, 1.91), (44, 636.783, 1.47), (72, 6.927, 0.65)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_19_NYC_ALL= np.array([( 128.22, 1.11)], dtype=[('alpha', '<i4'), ('beta', '<f8')])
Table_19_Both= np.array([(23, 4.922, 1.06), (31, 19.284, 1.92), (32, 771.387, 2.19), (33, 10.255, 1.37), (42, 14746.32, 0.67), (44, 43.384, 1.7), (72, 5.995, 0.69)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_19_Both_ALL= np.array([(3561.123, 0.65)], dtype=[('alpha', '<i4'), ('beta', '<f8')])
Table_19_CR= np.array([(23, 3.355, 1.89), (31, 46.372, 2.16), (32, 495.567, 1.35), (33, 18.054, 1.48), (42, 5126.014, 1.39), (44, 10.087, 1.93), (45, 3.016, 4.64)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_19_CR_ALL= np.array([(3592.825, 0.7)], dtype=[('alpha', '<i4'), ('beta', '<f8')])
Table_20_Both = np.array([(23, 4.24E-04), (31, 4.11E-04), (33, 6.90E-04), (44, 5.55E-04), (48, 8.40E-05), (72, 3.66E-03)], dtype=[('NAICS', '<i4'),  ('lamb', '<f8')])
Table_20_Both_ALL =3.15E-05
Table_21_Both = np.array([(23, 1.439, 0.184), (31, 1.343, 0.207), (32, 2.034, 0.18), (33, 1.81, 0.272), (44, 1.665, 0.208),(45, 2.161, 0.17), (48, 1.227, 0.227), (72, 1.632, 0.193)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('lamb', '<f8')])
Table_21_Both_ALL =np.array( [(1.731, 0.194)], dtype=[('alpha', '<i4'),  ('lamb', '<f8')])
Table_22_Both = np.array([(31, 1.93E-03), (32, 3.36E-04), (33, 9.68E-04), (42, 8.45E-05), (48, 1.55E-04)], dtype=[('NAICS', '<i4'),  ('lamb', '<f8')])
Table_22_Both_ALL = 1.02E-04
Table_23_Both = np.array([(31, 2.193, 0.347), (32, 3.236, 0.231), (33, 2.926, 0.28), (42, 1.583, 0.235), (44, 2.248, 0.319), (48, 1.274, 0.24), (72, 1.683, 0.398)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('lamb', '<f8')])
Table_23_Both_ALL = np.array([(4.915, 0.16)], dtype=[('alpha', '<i4'),  ('lamb', '<f8')])
Table_24_CFS=np.array([(21.0, 26126448.0), (31.0, 876226.0), (32.0, 62289.0), (33.0, 48081.0), (42.0, 565253.0), (45.0, 266125.0), (49.0, 838638.0), (51.0, 39166.0), (55.0, 231546.0)], dtype=[('NAICS', '<i4'),  ('beta', '<f8')])
Table_25_CFS=np.array([(212.0, 26126448.0), (311.0, 736479.0), (312.0, 2178828.0), (313.0, 35721.0), (314.0, 39006.0), (315.0, 5359.0), (321.0, 652905.0), (322.0, 703119.0), (323.0, 332054.0), (324.0, 17085653.0), (325.0, 17968.0), (326.0, 144649.0), (327.0, 1074852.0), (331.0, 628500.0), (332.0, 60080.0), (333.0, 40849.0), (334.0, 1669.0), (335.0, 10610.0), (336.0, 109445.0), (337.0, 27090.0), (339.0, 6579.0), (423.0, 240429.0), (424.0, 723241.0), (454.0, 266125.0), (493.0, 838638.0), (511.0, 39166.0), (551.0, 231546.0)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_26_CFS=np.array([(21.0, 25335647.0), (31.0, 856281.0), (32.0, 53399.0), (33.0, 37748.0), (42.0, 548908.0), (45.0, 255977.0), (51.0, 39140.0), (55.0, 231297.0)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_27_CFS=np.array([(212.0, 25335647.0), (311.0, 722970.0), (312.0, 2115619.0), (314.0, 38337.0), (321.0, 640232.0), (322.0, 591017.0), (323.0, 323522.0), (325.0, 11948.0), (327.0, 1044915.0), (331.0, 520289.0), (332.0, 59649.0), (333.0, 35581.0), (335.0, 10050.0), (336.0, 76299.0), (337.0, 26976.0), (423.0, 206510.0), (424.0, 715443.0), (454.0, 255977.0), (511.0, 39140.0), (551.0, 231297.0)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_28_CFS=np.array([(21.0, 246867379.0), (31.0, 16281311.0), (32.0, 20645218.0), (33.0, 2401143.0), (42.0, 8529135.0), (45.0, 6315305.0), (49.0, 25309371.0), (51.0, 1594972.0), (55.0, 10991421.0)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_29_CFS=np.array([(21.0, 1.70E+08, 1.28), (31.0, 224173, 1.4), (32.0, 25650878, 1.12), (33.0, 14200, 1.35), (42.0, 6143087, 1.06), (45.0, 8661789, 1.144), (49.0, 49897518, 0.642), (51.0, 4652, 1.344), (55.0, 51527, 4.1)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_30_CFS=np.array([(21.0, 1.43E+09, 0.049), (31.0, 5368605, 0.024), (32.0, 946011717, 0.002), (33.0, 1246411, 0.006), (42.0, 34011548, 0.029), (45.0, 147124041, 0.014), (49.0, 91821538, 0.01), (51.0, 205784, 0.01), (55.0, 4.04E+09, 0.009)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_31_CFS=np.array([(212.0, 246867379.0), (311.0, 20865881.0), (312.0, 37826939.0), (313.0, 419055.0), (314.0, 468595.0), (315.0, 178778.0), (321.0, 6033498.0), (322.0, 20232004.0), (323.0, 2634454.0), (324.0, 180043872.0), (325.0, 11510364.0), (326.0, 3146431.0), (327.0, 30485284.0), (331.0, 18595964.0), (332.0, 1412150.0), (333.0, 964732.0), (334.0, 153129.0), (335.0, 335552.0), (336.0, 5384491.0), (337.0, 701716.0), (339.0, 328636.0), (423.0, 2798542.0), (424.0, 16085108.0), (454.0, 6315305.0), (493.0, 25309371.0), (511.0, 1594972.0), (551.0, 10991421.0)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_32_CFS=np.array([(212.0, 169688897.0, 1.28), (311.0, 81344.0, 1.76), (312.0, 1243252.0, 1.13), (313.0, 54408.0, 0.84), (314.0, 1744.0, 1.66), (315.0, 8039.0, 0.97), (321.0, 119417.0, 1.86), (322.0, 35012.0, 1.71), (323.0, 6691.0, 1.48), (324.0, 0.0, 9.08), (325.0, 59106.0, 1.57), (326.0, 1503.0, 2.09), (327.0, 275040184.0, 0.59), (331.0, 119355.0, 1.4), (332.0, 73368.0, 1.19), (333.0, 4773.0, 1.31), (334.0, 2189.0, 1.06), (335.0, 9485.0, 1.12), (336.0, 85317.0, 0.96), (337.0, 3975.0, 1.49), (339.0, 6462.0, 1.39), (423.0, 2085726.0, 1.21), (424.0, 3986660.0, 0.97), (454.0, 8661789.0, 1.14), (493.0, 0.0, 5.33), (511.0, 4652.0, 1.34), (551.0, 51527.0, 4.1)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_33_CFS=np.array([(212.0, 1430291766, 0.049), (311.0, 24994127, 0.02), (312.0, 9883289, 0.02), (313.0, 186660, 0.029), (314.0, 96032, 0.034), (315.0, 8.51E+18, 0.083), (321.0, 6908406, 0.074), (322.0, 20682599, 0.013), (323.0, 224407, 0.023), (324.0, 1.96E+59, 0.638), (325.0, 20804687, 0.001), (326.0, 3755021, 0.018), (327.0, 1.98E+45, 0.141), (331.0, 12666016, 0.012), (332.0, 1540908, 0.017), (333.0, 279542, 0.01), (334.0, 41253, 0.003), (335.0, 125519, 0.01), (336.0, 1435495, 0.005), (337.0, 351232, 0.015), (339.0, 205476, 0.012), (423.0, 13933033, 0.045), (424.0, 20115663, 0.021), (454.0, 147124041, 0.014), (493.0, 91821538, 0.01), (511.0, 205784, 0.01), (551.0, 4040975454, 0.009)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_34_CFS=np.array([(21.0, 235396875.0), (31.0, 15786981.0), (32.0, 18982265.0), (33.0, 2007680.0), (42.0, 8006293.0), (45.0, 6132574.0), (51.0, 1590763.0), (55.0, 10981410.0)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_35_CFS=np.array([(21.0, 167820623.0, 1.26), (31.0, 204792.0, 1.41), (32.0, 27471096.0, 1.11), (33.0, 15082.0, 1.34), (42.0, 5598338.0, 1.04), (45.0, 11536835.0, 1.111), (51.0, 4177.0, 1.359), (55.0, 45121.0, 4.08)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_36_CFS=np.array([(21.0, 1.43E+09, 0.049), (31.0, 4887278, 0.024), (32.0, 955591459, 0.002), (33.0, 1255454, 0.006), (42.0, 29330047, 0.029), (45.0, 175137309, 0.014), (51.0, 186841, 0.01), (55.0, 3.81E+09, 0.009)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_37_CFS=np.array([(212.0, 235396875.0), (311.0, 20343134.0), (312.0, 36277995.0), (314.0, 462165.0), (321.0, 5896322.0), (322.0, 17231624.0), (323.0, 2562800.0), (325.0, 6318337.0), (327.0, 29737028.0), (331.0, 15281532.0), (332.0, 1396123.0), (333.0, 881285.0), (335.0, 323614.0), (336.0, 3715722.0), (337.0, 696881.0), (423.0, 2456332.0), (424.0, 15324097.0), (454.0, 6132574.0), (511.0, 1590763.0), (551.0, 10981410.0)], dtype=[('NAICS', '<i4'),  ('beta', '<f8')])
Table_38_CFS=np.array([(212.0, 167820623.0, 1.26), (311.0, 83167.0, 1.75), (312.0, 1236020.0, 1.13), (314.0, 1756.0, 1.66), (321.0, 118825.0, 1.85), (322.0, 36996.0, 1.69), (323.0, 6735.0, 1.46), (325.0, 61351.0, 1.54), (327.0, 0.0, 5.45), (331.0, 152037.0, 1.37), (332.0, 74568.0, 1.17), (333.0, 5356.0, 1.27), (335.0, 9884.0, 1.09), (336.0, 105514.0, 0.88), (337.0, 5047.0, 1.43), (423.0, 1880746.0, 1.2), (424.0, 3370818.0, 0.94), (454.0, 11536835.0, 1.11), (511.0, 4177.0, 1.36), (551.0, 45121.0, 4.08)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_39_CFS=np.array([(212.0, 151748280.0, 0.048), (311.0, 1963482.0, 0.02), (312.0, 2034542.0, 0.02), (314.0, 78784.0, 0.034), (321.0, 958188.0, 0.073), (322.0, 7777389.0, 0.013), (323.0, 71291.0, 0.023), (325.0, 815494.0, 0.001), (327.0, 1350.0, 0.14), (331.0, 3245717.0, 0.012), (332.0, 169578.0, 0.017), (333.0, 86960.0, 0.009), (335.0, 59669.0, 0.01), (336.0, 398960.0, 0.005), (337.0, 170149.0, 0.014), (423.0, 237918.0, 0.044), (424.0, 2280188.0, 0.02), (454.0, 3024844.0, 0.014), (511.0, 16743.0, 0.01), (551.0, 276550.0, 0.009)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_40_CFS=np.array([(21.0, 31294508.0), (31.0, 590798.0), (32.0, 551889.0), (33.0, 42751.0), (42.0, 610208.0), (45.0, 65478.0), (49.0, 962702.0), (51.0, 126226.0), (55.0, 212740.0)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_41_CFS=np.array([(212.0, 31294508.0), (311.0, 526756.0), (312.0, 1350394.0), (313.0, 21340.0), (314.0, 109208.0), (315.0, 10790.0), (316.0, 2921.0), (321.0, 713111.0), (322.0, 689784.0), (323.0, 180576.0), (324.0, 9622939.0), (325.0, 31388.0), (326.0, 117861.0), (327.0, 3393056.0), (331.0, 1961209.0), (332.0, 88210.0), (333.0, 18939.0), (334.0, 1913.0), (335.0, 55085.0), (336.0, 30664.0), (337.0, 89697.0), (339.0, 3444.0), (423.0, 293427.0), (424.0, 852945.0), (454.0, 65478.0), (493.0, 962702.0), (511.0, 126226.0), (551.0, 212740.0)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_42_CFS=np.array([(21.0, 22824611.0), (31.0, 523136.0), (32.0, 282044.0), (33.0, 27392.0), (42.0, 569334.0), (49.0, 952758.0), (51.0, 126123.0), (55.0, 202911.0)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_43_CFS=np.array([(212.0, 22824611.0), (311.0, 465422.0), (312.0, 1200033.0), (313.0, 21301.0), (314.0, 104372.0), (315.0, 9366.0), (321.0, 590528.0), (322.0, 644367.0), (323.0, 178115.0), (324.0, 3187020.0), (325.0, 21700.0), (326.0, 108286.0), (327.0, 2955178.0), (332.0, 78014.0), (333.0, 17012.0), (334.0, 1489.0), (335.0, 47240.0), (336.0, 25276.0), (337.0, 78845.0), (339.0, 2795.0), (423.0, 270730.0), (424.0, 798142.0), (493.0, 952758.0), (511.0, 126123.0), (551.0, 202911.0)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_44_CFS=np.array([(21.0, 424606800.0), (31.0, 23567728.0), (32.0, 60417115.0), (33.0, 2347140.0), (42.0, 14215616.0), (45.0, 1069771.0), (49.0, 35170984.0), (51.0, 3831102.0), (55.0, 27776524.0)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_45_CFS=np.array([(21.0, 39153022.0, 1.29), (31.0, 539826.0, 1.55), (32.0, 909592631.0, 0.94), (33.0, 10924.0, 1.32), (42.0, 2169296.0, 1.3), (45.0, 64420.0, 1.82), (49.0, 50964839.69, 0.29), (51.0, 11326.89, 1.27), (55.0, 5.5E+20, 5.06)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_46_CFS=np.array([(21.0, 688538046, 0.036), (31.0, 179205213, 0.01), (32.0, 1.16E+50, 0.024), (33.0, 1008544, 0.005), (42.0, 37926079, 0.023), (45.0, 3676540, 0.032), (49.0, 75799546, 0.006), (51.0, 210257, 0.009), (55.0, 8.66E+50, 0.031)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_47_CFS=np.array([(212.0, 424606800.0), (311.0, 29286811.0), (312.0, 39038842.0), (313.0, 455842.0), (314.0, 2048024.0), (315.0, 313203.0), (316.0, 81061.0), (321.0, 13875575.0), (322.0, 15858188.0), (323.0, 63243.0), (324.0, 299851573.0), (325.0, 13397054.0), (326.0, 4263735.0), (327.0, 103187661.0), (331.0, 23286173.0), (332.0, 2189669.0), (333.0, 471154.0), (334.0, 159577.0), (335.0, 1394323.0), (336.0, 3002591.0), (337.0, 2124498.0), (339.0, 267461.0), (423.0, 5556032.0), (424.0, 26492275.0), (454.0, 1069771.0), (493.0, 35170984.0), (511.0, 3831102.0), (551.0, 27776524.0)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_48_CFS=np.array([(212.0, 39153022.0, 1.29), (311.0, 1218533.0, 1.31), (312.0, 41628.0, 1.77), (313.0, 16424.0, 1.2), (314.0, 158293.0, 0.89), (315.0, 1193.0, 1.87), (316.0, 1038.0, 1.48), (321.0, 322252.0, 1.69), (322.0, 212028.0, 1.37), (323.0, 4760.0, 1.66), (324.0, 0.0, 8.75), (325.0, 666465.0, 1.61), (326.0, 11276.0, 1.97), (327.0, 0.0, 5.52), (331.0, 36458.0, 1.71), (332.0, 13086.0, 1.48), (333.0, 4477.0, 1.24), (334.0, 3199.0, 1.07), (335.0, 4286.0, 1.47), (336.0, 34691.0, 1.11), (337.0, 22063.0, 1.29), (339.0, 2767.0, 1.25), (423.0, 400385.0, 1.43), (424.0, 9727884.0, 1.09), (454.0, 64420.0, 1.82), (493.0, 50964840.0, 0.29), (511.0, 11327.0, 1.27), (551.0, 5.5E+20, 5.06)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_49_CFS=np.array([(212.0, 688538046, 0.036), (311.0, 200141034, 0.006), (312.0, 22008269, 0.015), (313.0, 579819, 0.01), (314.0, 1269000, 0.015), (315.0, 544819, 0.016), (316.0, 6.51E+15, 0.103), (321.0, 48422963, 0.025), (322.0, 20535666, 0.014), (323.0, 208535, 0.029), (324.0, 1873289492, 0.006), (325.0, 1.92E+42, 0.007), (326.0, 31966463, 0.012), (327.0, 36648177981, 0.012), (331.0, 11456743, 0.013), (332.0, 656081, 0.024), (333.0, 105301, 0.011), (334.0, 133690, 0.004), (335.0, 234480, 0.016), (336.0, 2789199, 0.003), (337.0, 694810, 0.019), (339.0, 72677, 0.006), (423.0, 9621223, 0.027), (424.0, 104914020, 0.017), (454.0, 3676540, 0.032), (493.0, 75799546, 0.006), (511.0, 210257, 0.009), (551.0, 8.66323E+50, 0.031)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_50_CFS=np.array([(21.0, 285150949.0), (31.0, 21286700.0), (32.0, 48684193.0), (33.0, 1780223.0), (42.0, 13291802.0), (49.0, 34563636.0), (51.0, 3821957.0), (55.0, 26140670.0)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_51_CFS=np.array([(21.0, 40515715, 1.22), (31.0, 457894, 1.57), (32.0, 800715035, 0.83), (33.0, 12636, 1.27), (42.0, 2160985, 1.3), (49.0, 50400999, 0.29), (51.0, 7553, 1.32), (55.0, 5.50E+20, 5.06)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_52_CFS=np.array([(21.0, 599926026, 0.034), (31.0, 169294022, 0.01), (32.0, 1.51E+49, 0.024), (33.0, 966684, 0.005), (42.0, 37690540, 0.023), (49.0, 74475722, 0.006), (51.0, 146922, 0.009), (55.0, 2.54E+50, 0.03)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_53_CFS=np.array([(212.0, 285150949.0), (311.0, 26372867.0), (312.0, 35594221.0), (313.0, 453417.0), (314.0, 1797942.0), (315.0, 288476.0), (321.0, 11795379.0), (322.0, 14775129.0), (323.0, 1989216.0), (324.0, 227781426.0), (325.0, 10766630.0), (326.0, 4012883.0), (327.0, 89408739.0), (332.0, 2033204.0), (333.0, 416752.0), (334.0, 132651.0), (335.0, 1207746.0), (336.0, 2584437.0), (337.0, 1625375.0), (339.0, 215948.0), (423.0, 5019491.0), (424.0, 25019426.0), (493.0, 34563636.0), (511.0, 3821957.0), (551.0, 26140670.0)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_54_CFS=np.array([(212.0, 40515715.0, 1.22), (311.0, 1124369.0, 1.29), (312.0, 33312.0, 1.81), (313.0, 16569.0, 1.19), (314.0, 98651.0, 0.99), (315.0, 962.0, 1.91), (321.0, 323906.0, 1.67), (322.0, 219471.0, 1.35), (323.0, 5748.0, 1.53), (324.0, 451123557.0, 0.74), (325.0, 640743.0, 1.58), (326.0, 11222.0, 1.99), (327.0, 9047178128.0, 0.63), (332.0, 13624.0, 1.46), (333.0, 4985.0, 1.2), (334.0, 3611.0, 0.99), (335.0, 4857.0, 1.42), (336.0, 49571.0, 1.02), (337.0, 25736.0, 1.29), (339.0, 2819.0, 1.18), (423.0, 358077.0, 1.44), (424.0, 9979572.0, 1.1), (493.0, 50400999.0, 0.29), (511.0, 7553.0, 1.32), (551.0, 5.5E+20, 5.06)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_55_CFS=np.array([(212.0, 599926026.0, 0.034), (311.0, 166760319.0, 0.006), (312.0, 24198696.0, 0.015), (313.0, 574277.0, 0.01), (314.0, 1172765.0, 0.015), (315.0, 536007.0, 0.016), (321.0, 44811236.0, 0.025), (322.0, 20237464.0, 0.014), (323.0, 158547.0, 0.027), (324.0, 1761324633.0, 0.004), (325.0, 212239428.0, 0.001), (326.0, 38947270.0, 0.012), (327.0, 34364831433.0, 0.011), (332.0, 660247.0, 0.023), (333.0, 106423.0, 0.011), (334.0, 111189.0, 0.003), (335.0, 220703.0, 0.016), (336.0, 2787997.0, 0.002), (337.0, 752072.0, 0.019), (339.0, 60058.0, 0.005), (423.0, 9108737.0, 0.027), (424.0, 107541102.0, 0.018), (493.0, 74475722.0, 0.006), (511.0, 146922.0, 0.009), (551.0, 2.54E+50, 0.03)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_56_CFS=np.array([(21.0, 48689606.0), (31.0, 580353.0), (32.0, 4371744.0), (33.0, 64431.0), (42.0, 757778.0), (45.0, 37277.0), (49.0, 1329914.0), (51.0, 42013.0)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_57_CFS=np.array([(212.0, 48689606.0), (311.0, 429910.0), (312.0, 3736219.0), (314.0, 65915.0), (315.0, 40207.0), (321.0, 913417.0), (322.0, 1352247.0), (323.0, 168462.0), (324.0, 23145410.0), (325.0, 1473751.0), (326.0, 288629.0), (327.0, 3725196.0), (331.0, 973844.0), (332.0, 155994.0), (333.0, 93585.0), (334.0, 6505.0), (335.0, 51356.0), (336.0, 48289.0), (337.0, 98524.0), (339.0, 37210.0), (423.0, 409823.0), (424.0, 1080614.0), (454.0, 37277.0), (493.0, 1329914.0), (511.0, 42013.0)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_58_CFS=np.array([(21.0, 31516621.0), (31.0, 539411.0), (32.0, 719978.0), (33.0, 47611.0), (42.0, 588205.0), (49.0, 1325751.0), (51.0, 41393.0)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_59_CFS=np.array([(212.0, 31516621.0), (311.0, 385644.0), (321.0, 769736.0), (322.0, 809648.0), (323.0, 166740.0), (324.0, 1413470.0), (325.0, 298897.0), (326.0, 265060.0), (327.0, 3459746.0), (331.0, 638526.0), (332.0, 152537.0), (333.0, 89553.0), (334.0, 6456.0), (335.0, 50557.0), (336.0, 22877.0), (339.0, 26335.0), (423.0, 368432.0), (424.0, 792114.0), (493.0, 1325751.0), (511.0, 41393.0)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_60_CFS=np.array([(21.0, 522087613.0), (31.0, 28930812.0), (32.0, 103692655.0), (33.0, 5554549.0), (42.0, 21107112.0), (45.0, 799771.0), (49.0, 30201083.0), (51.0, 1273006.0), (55.0, 58485178.0)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_61_CFS=np.array([(21.0, 94467304.0, 1.3), (31.0, 398834.0, 1.55), (32.0, 42964256.0, 1.18), (33.0, 35811.0, 1.38), (42.0, 10847010.0, 1.17), (45.0, 126031.0, 1.52), (49.0, 34802449.0, 0.54), (51.0, 9978.0, 1.19), (55.0, 4.57E+18, 5.22)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_62_CFS=np.array([(21.0, 922158839.0, 0.055), (31.0, 173997212.0, 0.007), (32.0, 1130395413.0, 0.01), (33.0, 9958536.0, 0.003), (42.0, 157826503.0, 0.016), (45.0, 3067530.0, 0.027), (49.0, 83965253.0, 0.008), (51.0, 153948.0, 0.012), (55.0, 1.042E+51, 0.018)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_63_CFS=np.array([(212.0, 522087613.0), (311.0, 26101350.0), (312.0, 96413378.0), (314.0, 929959.0), (315.0, 1067738.0), (321.0, 16340824.0), (322.0, 31730237.0), (323.0, 1887651.0), (324.0, 657510948.0), (325.0, 75026632.0), (326.0, 6805859.0), (327.0, 114875348.0), (331.0, 39519914.0), (332.0, 4397262.0), (333.0, 2889300.0), (334.0, 707755.0), (335.0, 2389584.0), (336.0, 3672614.0), (337.0, 1939961.0), (339.0, 983396.0), (423.0, 9157917.0), (424.0, 39588964.0), (454.0, 799771.0), (493.0, 30201083.0), (511.0, 1273006.0), (551.0, 58485178.0)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_64_CFS=np.array([(212.0, 94467304.0, 1.3), (311.0, 449285.0, 1.35), (312.0, 50417.0, 2.09), (314.0, 38973.0, 0.97), (315.0, 8920.0, 1.43), (321.0, 20665.0, 1.99), (322.0, 49966.0, 1.77), (323.0, 8701.0, 1.27), (324.0, 23508399.0, 1.46), (325.0, 4539987.0, 1.26), (326.0, 29823.0, 1.56), (327.0, 1292730909.0, 0.71), (331.0, 4712.0, 2.08), (332.0, 49577.0, 1.48), (333.0, 6993.0, 1.5), (334.0, 2336.0, 1.3), (335.0, 107288.0, 1.01), (336.0, 26142.0, 1.03), (337.0, 13442.0, 1.37), (339.0, 14616.0, 1.11), (423.0, 2584289.0, 1.24), (424.0, 27881018.0, 1.16), (454.0, 126031.0, 1.52), (493.0, 34802449.0, 0.54), (511.0, 9978.0, 1.19), (551.0, 4.57E+18, 5.22)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_65_CFS=np.array([(212.0, 922158839.0, 0.055), (311.0, 91693916.0, 0.005), (312.0, 284744377.0, 0.011), (314.0, 183109.0, 0.022), (315.0, 490937.0, 0.017), (321.0, 3351094.0, 0.032), (322.0, 51205633.0, 0.012), (323.0, 89898.0, 0.027), (324.0, 718145079.0, 0.01), (325.0, 289556202.0, 0.007), (326.0, 11321834.0, 0.01), (327.0, 6123672708.0, 0.011), (331.0, 72112874.0, 0.012), (332.0, 3734653.0, 0.016), (333.0, 2418955.0, 0.01), (334.0, 730574.0, 0.001), (335.0, 1712671.0, 0.01), (336.0, 996716.0, 0.003), (337.0, 464811.0, 0.019), (339.0, 155461.0, 0.016), (423.0, 48778394.0, 0.016), (424.0, 393807458.0, 0.014), (454.0, 3067530.0, 0.027), (493.0, 83965253.0, 0.008), (511.0, 153948.0, 0.012), (551.0, 1.042E+51, 0.018)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_66_CFS=np.array([(21.0, 359883900.0), (31.0, 26970714.0), (32.0, 40781501.0), (33.0, 4360175.0), (42.0, 14769009.0), (49.0, 30027564.0), (51.0, 1218385.0), (55.0, 58169092.0)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_67_CFS=np.array([(21.0, 102785401, 1.16), (31.0, 402732, 1.55), (32.0, 45002445, 1.12), (33.0, 37193, 1.36), (42.0, 9339931, 1.13), (49.0, 23011651, 0.68), (51.0, 3767, 1.41), (55.0, 2.19E+18, 5.17)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_68_CFS=np.array([(21.0, 699546594, 0.053), (31.0, 176110888, 0.007), (32.0, 1028883496, 0.008), (33.0, 9319545, 0.003), (42.0, 118079027, 0.015), (49.0, 78873919, 0.008), (51.0, 164520, 0.011), (55.0, 1.23E+50, 0.018)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_69_CFS=np.array([(212.0, 359883900.0), (311.0, 23451751.0), (321.0, 13693827.0), (322.0, 22038050.0), (323.0, 1859197.0), (324.0, 105971020.0), (325.0, 16667414.0), (326.0, 6293540.0), (327.0, 108866091.0), (331.0, 26114569.0), (332.0, 4288540.0), (333.0, 2771366.0), (334.0, 698155.0), (335.0, 2346465.0), (336.0, 2266513.0), (339.0, 761226.0), (423.0, 8310361.0), (424.0, 24758619.0), (493.0, 30027564.0), (511.0, 1218385.0), (551.0, 58169092.0)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_70_CFS=np.array([(212.0, 102785401.0, 1.16), (311.0, 447775.0, 1.34), (321.0, 21275.0, 1.96), (322.0, 45363.0, 1.77), (323.0, 13657.0, 1.24), (324.0, 39325164.0, 1.19), (325.0, 2746979.0, 1.19), (326.0, 20849.0, 1.59), (327.0, 1342484521.0, 0.69), (331.0, 4830.0, 2.01), (332.0, 51956.0, 1.46), (333.0, 6999.0, 1.49), (334.0, 2504.0, 1.29), (335.0, 112819.0, 0.99), (336.0, 29914.0, 1.0), (339.0, 14737.0, 1.1), (423.0, 2588922.0, 1.22), (424.0, 18856872.0, 1.08), (493.0, 23011651.0, 0.68), (511.0, 3767.0, 1.41), (551.0, 2.19E+18, 5.17)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_71_CFS=np.array([(212.0, 699546594.0, 0.053), (311.0, 86385156.0, 0.005), (321.0, 3233715.0, 0.031), (322.0, 50918448.0, 0.011), (323.0, 110290.0, 0.028), (324.0, 698807153.0, 0.006), (325.0, 131469881.0, 0.005), (326.0, 8618854.0, 0.01), (327.0, 6055357455.0, 0.01), (331.0, 53784754.0, 0.011), (332.0, 3603157.0, 0.016), (333.0, 2259754.0, 0.01), (334.0, 653775.0, 0.001), (335.0, 1682920.0, 0.01), (336.0, 1017399.0, 0.003), (339.0, 157543.0, 0.016), (423.0, 46085010.0, 0.015), (424.0, 205830914.0, 0.014), (493.0, 78873919.0, 0.008), (511.0, 164520.0, 0.011), (551.0, 1.23E+50, 0.018)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_72_CFS=np.array([(21.0, 153230056.0), (32.0, 8166167.0), (33.0, 50544.0), (42.0, 428427.0)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_73_CFS=np.array([(212.0, 153230056.0), (332.0, 129651.0), (423.0, 206047.0), (424.0, 660248.0)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_74_CFS=np.array([(21.0, 1289196.0), (32.0, 3329018.0), (42.0, 409019.0)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_75_CFS=np.array([(212.0, 1289196.0), (423.0, 173152.0)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_76_CFS=np.array([(21.0, 5104333216.0), (32.0, 101518191.0), (33.0, 1003926.0), (42.0, 2882665.0)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_77_CFS=np.array([(21.0, 740830598.0, 1.53), (32.0, 254462711.0, 1.1), (33.0, 60010.0, 1.34), (42.0, 5339064756.0, 6.58)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_78_CFS=np.array([(21.0, 148312541348.0, 0.02), (32.0, 1205000027.0, 0.04), (33.0, 848541.0, 0.03), (42.0, 18949698.0, 0.06)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_79_CFS=np.array([(212.0, 5104333216.0), (332.0, 2158712.0), (423.0, 1404805.0), (424.0, 4678188.0)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_80_CFS=np.array([(212.0, 740830598, 1.53), (332.0, 620232, 0.88), (423.0, 5413965, 6.08), (424.0, 5.64E+12, 7.19)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_81_CFS=np.array([(212.0, 148312541348, 0.02), (332.0, 1794685, 0.03), (423.0, 6281929, 0.08), (424.0, 1.50E+29, 0.83)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_82_CFS=np.array([(21.0, 94326921.0), (32.0, 51872206.0), (42.0, 2765512.0)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_83_CFS=np.array([(21.0, 96777091.0, 0.36), (32.0, 262026868.0, 1.02), (42.0, 6745053865.0, 6.5)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_84_CFS=np.array([(21.0, 174342140, 0.004), (32.0, 1250222485, 0.032), (42.0, 8.77E+22, 0.789)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_85_CFS=np.array([(212.0, 94326921.0), (423.0, 1255856.0)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_86_CFS=np.array([(212.0, 96777091.0, 0.36), (423.0, 6967018.0, 5.91)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_87_CFS=np.array([(212.0, 174342140, 0.004), (423.0, 6.34E+17, 0.753)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_88_CFS=np.array([(21.0, 37433995.0), (31.0, 960538.0), (32.0, 733006.0), (33.0, 287457.0), (42.0, 1204735.0), (45.0, 21156.0), (49.0, 1046450.0), (51.0, 79478.0), (55.0, 446118.0)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_89_CFS=np.array([(212.0, 37433995.0), (311.0, 746513.0), (312.0, 4050008.0), (321.0, 264828.0), (322.0, 523207.0), (323.0, 137411.0), (324.0, 15587655.0), (325.0, 741631.0), (326.0, 150044.0), (327.0, 680959.0), (331.0, 1511607.0), (332.0, 107167.0), (333.0, 249092.0), (334.0, 10081.0), (335.0, 160615.0), (336.0, 218796.0), (337.0, 57970.0), (339.0, 49377.0), (423.0, 840489.0), (424.0, 1657872.0), (454.0, 21156.0), (493.0, 1046450.0), (511.0, 79478.0), (551.0, 446118.0)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_90_CFS=np.array([(21.0, 17710145.0), (31.0, 888331.0), (32.0, 423773.0), (33.0, 160857.0), (42.0, 855584.0), (45.0, 21053.0), (49.0, 1040823.0)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_91_CFS=np.array([(212.0, 17710145.0), (311.0, 669639.0), (321.0, 250766.0), (322.0, 514322.0), (323.0, 136961.0), (324.0, 2759436.0), (325.0, 586343.0), (326.0, 147403.0), (327.0, 609653.0), (331.0, 645007.0), (332.0, 90393.0), (333.0, 219023.0), (334.0, 8751.0), (336.0, 119734.0), (339.0, 47467.0), (423.0, 405279.0), (424.0, 1415782.0), (454.0, 21053.0), (493.0, 1040823.0), (551.0, 445052.0)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_92_CFS=np.array([(21.0, 437239086.0), (31.0, 45968090.0), (32.0, 26087617.0), (33.0, 12291675.0), (42.0, 40977856.0), (45.0, 1991229.0), (49.0, 37221805.0), (51.0, 3781415.0), (55.0, 28878334.0)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_93_CFS=np.array([(21.0, 114459571, 1.15), (31.0, 2383452, 1.27), (32.0, 11209680, 1.07), (33.0, 47729, 1.38), (42.0, 17285209, 1.1), (45.0, 1.40E+14, 5.33), (49.0, 3.10E+21, 4.95), (51.0, 73721, 1.57), (55.0, 2.71E+18, 4.65)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_94_CFS=np.array([(21.0, 1056642075.0, 0.029), (31.0, 221718215.0, 0.008), (32.0, 251033410.0, 0.011), (33.0, 12560516.0, 0.005), (42.0, 205704435.0, 0.021), (45.0, 9759193.0, 0.003), (49.0, 70547893.0, 0.006), (51.0, 14633400.0, 0.006), (55.0, 7.61E+50, 0.033)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_95_CFS=np.array([(212.0, 437239086.0), (311.0, 47359757.0), (312.0, 75432014.0), (321.0, 4369943.0), (322.0, 16770038.0), (323.0, 2510261.0), (324.0, 214026130.0), (325.0, 29741427.0), (326.0, 4743365.0), (327.0, 32051613.0), (331.0, 52192746.0), (332.0, 7404703.0), (333.0, 4185654.0), (334.0, 447342.0), (335.0, 8397457.0), (336.0, 14917454.0), (337.0, 3617000.0), (339.0, 1059820.0), (423.0, 38025405.0), (424.0, 45701387.0), (454.0, 1991229.0), (493.0, 37221805.0), (511.0, 3781415.0), (551.0, 28878334.0)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_96_CFS=np.array([(212.0, 114459571, 1.15), (311.0, 1344421, 1.33), (312.0, 951233, 1.62), (321.0, 257042, 1.28), (322.0, 59846, 1.51), (323.0, 4427, 1.54), (324.0, 9.75E+27, 7.57), (325.0, 3275582, 1.18), (326.0, 37493, 1.49), (327.0, 2837260, 1.61), (331.0, 56033, 1.59), (332.0, 56212, 1.4), (333.0, 11991, 1.27), (334.0, 8033, 0.98), (335.0, 34244, 1.15), (336.0, 32336, 1.35), (337.0, 172678, 0.78), (339.0, 2991, 1.83), (423.0, 1202986, 1.33), (424.0, 148557762, 0.68), (454.0, 1.40E+14, 5.33), (493.0, 3.10E+21, 4.95), (511.0, 73721, 1.57), (551.0, 2.71E+18, 4.65)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_97_CFS=np.array([(212.0, 1056642075, 0.029), (311.0, 322047497, 0.006), (312.0, 68110697, 0.016), (321.0, 3572284, 0.041), (322.0, 18104272, 0.012), (323.0, 392048, 0.015), (324.0, 3.25E+68, 0.124), (325.0, 229922408, 0.009), (326.0, 13017950, 0.011), (327.0, 521723610, 0.012), (331.0, 49660989, 0.007), (332.0, 10897324, 0.006), (333.0, 1102321, 0.007), (334.0, 194139, 0.007), (335.0, 4334602, 0.003), (336.0, 16494171, 0.003), (337.0, 1171394, 0.003), (339.0, 961311, 0.024), (423.0, 28027892, 0.027), (424.0, 596683597, 0.013), (454.0, 9759193, 0.003), (493.0, 70547893, 0.006), (511.0, 14633400, 0.006), (551.0, 7.61E+50, 0.033)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_98_CFS=np.array([(21.0, 334763266.0), (31.0, 38278592.0), (32.0, 19214095.0), (33.0, 7957992.0), (42.0, 16870788.0), (45.0, 1977430.0), (49.0, 36788653.0), (55.0, 28618067.8)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_99_CFS=np.array([(21.0, 99246911, 1.11), (31.0, 2388019, 1.27), (32.0, 11178918, 1.04), (33.0, 50631, 1.37), (42.0, 8881110, 1.09), (45.0, 1.48E+14, 5.32), (49.0, 3.21E+21, 4.95), (55.0, 3.18E+18, 4.62)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_100_CFS=np.array([(21.0, 920429626, 0.025), (31.0, 208632582, 0.008), (32.0, 215648109, 0.01), (33.0, 12695153, 0.005), (42.0, 98117414, 0.022), (45.0, 9666491, 0.003), (49.0, 70904907, 0.006), (55.0, 3.76E+50, 0.033)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_101_CFS=np.array([(212.0, 334763266.0), (311.0, 37033322.0), (321.0, 4158012.0), (322.0, 16435129.0), (323.0, 2498985.0), (324.0, 115068182.0), (325.0, 21863075.0), (326.0, 4626915.0), (327.0, 29417743.0), (331.0, 25651462.0), (332.0, 6356113.0), (333.0, 3747734.0), (334.0, 409188.0), (336.0, 10126744.0), (339.0, 991311.0), (423.0, 6943331.0), (424.0, 32753402.0), (454.0, 1977430.0), (493.0, 36788653.0), (551.0, 28618068.0)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_102_CFS=np.array([(212.0, 99246911, 1.11), (311.0, 1196188, 1.34), (321.0, 260368, 1.26), (322.0, 62709, 1.49), (323.0, 3060, 1.64), (324.0, 8.69E+27, 7.64), (325.0, 1909687, 1.21), (326.0, 36961, 1.49), (327.0, 3600178, 1.61), (331.0, 73890, 1.5), (332.0, 55145, 1.4), (333.0, 12342, 1.26), (334.0, 9164, 0.93), (336.0, 38920, 1.31), (339.0, 2701, 1.86), (423.0, 730667, 1.39), (424.0, 66140782, 0.47), (454.0, 1.48E+14, 5.32), (493.0, 3.21E+21, 4.95), (551.0, 3.18E+18, 4.62)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_103_CFS=np.array([(212.0, 920429626, 0.025), (311.0, 300907755, 0.006), (321.0, 3578829, 0.04), (322.0, 17337210, 0.012), (323.0, 407586, 0.014), (324.0, 3.06E+68, 0.118), (325.0, 155488145, 0.009), (326.0, 12619957, 0.011), (327.0, 636135771, 0.012), (331.0, 50259157, 0.006), (332.0, 10407126, 0.006), (333.0, 1054333, 0.007), (334.0, 179918, 0.007), (336.0, 16389868, 0.003), (339.0, 1105807, 0.024), (423.0, 20530513, 0.028), (424.0, 147941861, 0.012), (454.0, 9666491, 0.003), (493.0, 70904907, 0.006), (551.0, 3.76E+50, 0.033)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_104_CFS=np.array([(21.0, 30950434), (31.0, 506712), (32.0, 12171), (33.0, 153426), (42.0, 787685), (45.0, 55970), (49.0, 792551), (51.0, 50498), (55.0, 187803)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_105_CFS=np.array([(212.0, 30950434.0), (311.0, 479233.0), (312.0, 1247982.0), (313.0, 121735.0), (314.0, 156603.0), (315.0, 13069.0), (316.0, 26298.0), (321.0, 535798.0), (322.0, 983715.0), (323.0, 206843.0), (324.0, 21353264.0), (325.0, 331190.0), (326.0, 173722.0), (327.0, 2324909.0), (331.0, 1344674.0), (332.0, 124851.0), (333.0, 93915.0), (334.0, 5551.0), (335.0, 124671.0), (336.0, 91317.0), (337.0, 79134.0), (339.0, 20208.0), (423.0, 463162.0), (424.0, 1004441.0), (454.0, 55970.0), (493.0, 792551.0), (511.0, 50498.0), (551.0, 187803.0)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_106_CFS=np.array([(21.0, 7745393.0), (31.0, 438112.0), (32.0, 400204.0), (33.0, 96430.0), (42.0, 634793.0), (45.0, 55162.0), (49.0, 776337.0), (51.0, 50264.0), (55.0, 131126.0)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_107_CFS=np.array([(212.0, 7745393.0), (311.0, 407308.0), (312.0, 1141177.0), (313.0, 107003.0), (314.0, 149057.0), (315.0, 12406.0), (316.0, 14818.0), (321.0, 442228.0), (322.0, 681290.0), (323.0, 199029.0), (324.0, 3049815.0), (325.0, 140199.0), (326.0, 165006.0), (327.0, 2071737.0), (331.0, 688961.0), (332.0, 116781.0), (333.0, 79544.0), (334.0, 5068.0), (335.0, 109183.0), (336.0, 62432.0), (337.0, 78062.0), (339.0, 18846.0), (423.0, 364029.0), (424.0, 815641.0), (454.0, 55162.0), (493.0, 776337.0), (511.0, 50264.0), (551.0, 131126.0)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_108_CFS=np.array([(21.0, 429983087.0), (31.0, 31333710.0), (32.0, 47847304.0), (33.0, 6476103.0), (42.0, 22315863.0), (45.0, 3395976.0), (49.0, 35471262.0), (51.0, 2334908.0), (55.0, 45286940.0)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_109_CFS=np.array([(21.0, 102966643.0, 1.04), (31.0, 468066.0, 1.6), (32.0, 53474643.0, 1.09), (33.0, 26863.0, 1.44), (42.0, 13820918.0, 1.03), (45.0, 3506710.0, 1.079), (49.0, 55234357.0, 0.384), (51.0, 18122.0, 1.221), (55.0, 1.30E19, 5.27)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_110_CFS=np.array([(21.0, 1199901388.0, 0.013), (31.0, 326892029.0, 0.007), (32.0, 1487452490.0, 0.006), (33.0, 7567683.0, 0.005), (42.0, 122367091.0, 0.017), (45.0, 34579096.0, 0.005), (49.0, 101248238.0, 0.005), (51.0, 638169.0, 0.006), (55.0, 7.52E52, 0.018)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_111_CFS=np.array([(212.0, 429983087.0), (311.0, 37931394.0), (312.0, 57115808.0), (313.0, 3450167.0), (314.0, 3225652.0), (315.0, 377710.0), (316.0, 839479.0), (321.0, 16779809.0), (322.0, 29828941.0), (323.0, 3131831.0), (324.0, 319927314.0), (325.0, 38833673.0), (326.0, 5098086.0), (327.0, 69302012.0), (331.0, 43046210.0), (332.0, 4391241.0), (333.0, 2571528.0), (334.0, 420467.0), (335.0, 4105737.0), (336.0, 8370088.0), (337.0, 2020253.0), (339.0, 767475.0), (423.0, 11144484.0), (424.0, 37457598.0), (454.0, 3395976.0), (493.0, 35471262.0), (511.0, 2334908.0), (551.0, 45286940.0)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_112_CFS=np.array([(212.0, 102966643.0, 1.04), (311.0, 1041245.0, 1.39), (312.0, 688916.0, 1.46), (313.0, 36487.0, 1.28), (314.0, 7960.0, 1.51), (315.0, 4037.0, 1.4), (316.0, 12208.0, 1.29), (321.0, 694425.0, 1.35), (322.0, 83322.0, 1.57), (323.0, 7131.0, 1.49), (324.0, 515913515.0, 0.63), (325.0, 2044183.0, 1.45), (326.0, 31214.0, 1.53), (327.0, 203230866.0, 0.99), (331.0, 52303.0, 1.69), (332.0, 47856.0, 1.5), (333.0, 10987.0, 1.45), (334.0, 5393.0, 1.07), (335.0, 5733.0, 1.54), (336.0, 23124.0, 1.4), (337.0, 18220.0, 1.27), (339.0, 5837.0, 1.43), (423.0, 1862995.0, 1.25), (424.0, 39048068.0, 0.85), (454.0, 3506710.0, 1.08), (493.0, 55234357.0, 0.38), (511.0, 18122.0, 1.22), (551.0, 1.30E+19, 5.27)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_113_CFS=np.array([(212.0, 1199901388.0, 0.013), (311.0, 375169495.0, 0.005), (312.0, 94574636.0, 0.008), (313.0, 2228393.0, 0.011), (314.0, 398747.0, 0.015), (315.0, 231302.0, 0.014), (316.0, 269358.0, 0.02), (321.0, 37582650.0, 0.015), (322.0, 47435340.0, 0.011), (323.0, 283656.0, 0.019), (324.0, 1409085570.0, 0.009), (325.0, 554139014.0, 0.003), (326.0, 9675381.0, 0.011), (327.0, 2352689371.0, 0.013), (331.0, 162668499.0, 0.007), (332.0, 5879730.0, 0.014), (333.0, 2626627.0, 0.008), (334.0, 265544.0, 0.003), (335.0, 2002370.0, 0.007), (336.0, 18410870.0, 0.003), (337.0, 851389.0, 0.008), (339.0, 447156.0, 0.009), (423.0, 30415674.0, 0.024), (424.0, 218477972.0, 0.012), (454.0, 34579096.0, 0.005), (493.0, 101248238.0, 0.005), (511.0, 638169.0, 0.006), (551.0, 7.52E+52, 0.018)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_114_CFS=np.array([(21.0, 282432192.0), (31.0, 26039527.0), (32.0, 31515922.0), (33.0, 4777409.0), (42.0, 16109203.0), (45.0, 3344522.0), (49.0, 32568847.0), (51.0, 2302358.0), (55.0, 27154413.0)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_115_CFS=np.array([(21.0, 112096301.0, 0.96), (31.0, 432129.0, 1.6), (32.0, 55617478.0, 1.05), (33.0, 28786.0, 1.43), (42.0, 10850958.0, 1.01), (45.0, 3660418.0, 1.08), (49.0, 43493667.0, 0.41), (51.0, 14244.0, 1.25), (55.0, 1.10E18, 5.19)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_116_CFS=np.array([(21.0, 1060968078.0, 0.011), (31.0, 284051672.0, 0.007), (32.0, 1325290816.0, 0.006), (33.0, 7183053.0, 0.005), (42.0, 89493563.0, 0.017), (45.0, 35653332.0, 0.005), (49.0, 83685705.0, 0.005), (51.0, 543866.0, 0.006), (55.0, 2.11E50, 0.018)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_117_CFS=np.array([(212.0, 282432192.0), (311.0, 30186424.0), (312.0, 55070117.0), (313.0, 3236767.0), (314.0, 3100576.0), (315.0, 360950.0), (316.0, 452518.0), (321.0, 14202550.0), (322.0, 22255566.0), (323.0, 3034954.0), (324.0, 148268574.0), (325.0, 18347836.0), (326.0, 4918655.0), (327.0, 64152503.0), (331.0, 25910905.0), (332.0, 4085332.0), (333.0, 2346774.0), (334.0, 388738.0), (335.0, 3422187.0), (336.0, 6425835.0), (337.0, 1974956.0), (339.0, 718824.0), (423.0, 7321444.0), (424.0, 28020169.0), (454.0, 3344522.0), (493.0, 32568847.0), (511.0, 2302358.0), (551.0, 27154413.0)], dtype=[('NAICS', '<i4'), ('beta', '<f8')])
Table_118_CFS=np.array([(212.0, 112096301.0, 0.96), (311.0, 922466.0, 1.39), (312.0, 668480.0, 1.47), (313.0, 36636.0, 1.27), (314.0, 7343.0, 1.58), (315.0, 3324.0, 1.43), (316.0, 11815.0, 1.25), (321.0, 694240.0, 1.32), (322.0, 86482.0, 1.54), (323.0, 6771.0, 1.52), (324.0, 628206677.0, 0.51), (325.0, 1616289.0, 1.4), (326.0, 30572.0, 1.53), (327.0, 213404854.0, 0.97), (331.0, 53094.0, 1.66), (332.0, 48237.0, 1.49), (333.0, 10940.0, 1.44), (334.0, 5783.0, 1.06), (335.0, 6738.0, 1.5), (336.0, 25131.0, 1.37), (337.0, 17983.0, 1.28), (339.0, 6346.0, 1.41), (423.0, 1689523.0, 1.23), (424.0, 26846992.0, 0.83), (454.0, 3660418.0, 1.08), (493.0, 43493667.0, 0.41), (511.0, 14244.0, 1.25), (551.0, 1.10E+18, 5.19)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])
Table_119_CFS=np.array([(212.0, 1060968078.0, 0.011), (311.0, 318001220.0, 0.005), (312.0, 95152870.0, 0.008), (313.0, 2177178.0, 0.011), (314.0, 490646.0, 0.015), (315.0, 219800.0, 0.014), (316.0, 223977.0, 0.02), (321.0, 34288321.0, 0.014), (322.0, 45453085.0, 0.01), (323.0, 298928.0, 0.019), (324.0, 1488870669.0, 0.005), (325.0, 332634484.0, 0.003), (326.0, 9656265.0, 0.011), (327.0, 2347809210.0, 0.013), (331.0, 138818749.0, 0.007), (332.0, 5756215.0, 0.014), (333.0, 2441740.0, 0.007), (334.0, 264753.0, 0.003), (335.0, 1815183.0, 0.007), (336.0, 15747364.0, 0.003), (337.0, 883908.0, 0.008), (339.0, 434962.0, 0.009), (423.0, 26560430.0, 0.023), (424.0, 138593836.0, 0.013), (454.0, 35653332.0, 0.005), (493.0, 83685705.0, 0.005), (511.0, 543866.0, 0.006), (551.0, 2.11E+50, 0.018)], dtype=[('NAICS', '<i4'), ('alpha', '<f8'), ('beta', '<f8')])


UsedTables = []
i = 0
for m in Metrics:
    for n in Models:
        m = m.split(";")
        m = m[0].replace("'", "")
        n = n.replace("'", "")
        if m+n in ModMetDictionary:
                    TableName = ModMetDictionary[m+n]
                    UsedTables.append(TableName)

        elif m in FTGDictionary:
            if FTGDictionary[m] not in UsedTables:
                    TableName = FTGDictionary[m]
                    UsedTables.append(TableName)
        elif m in FADictionary:
            if FADictionary[m] not in UsedTables:
                    TableName = FADictionary[m]
                    UsedTables.append(TableName)
for c in CFS:
    c = c.split(";")
    c = c[0].replace("'", "")
    c = c.replace("'", "")
    if c in FPDictionary:
        TableName = FPDictionary[c]
        UsedTables.append(TableName)
arcpy.AddMessage("Done With Task II")
arcpy.AddMessage("----------------")

arcpy.AddMessage("Task III: Processing Input Tables")
DeleteTable = []
for TableName in UsedTables:
    arcpy.AddMessage("-------------")
    arcpy.AddMessage("Task III: Input Table processed: " + TableName)

    # Create Empty Array to store New Generated trips
    arrayOut = np.zeros(array['OBJECTID'].size, dtype=[('OBJECTID', '<i4'), (TableName, '<f8')])

    TableDictionary = {'Table_9_Both': Table_9_Both, 'Table_9_Both_ALL': Table_9_Both_ALL, 'Table_9_NYC': Table_9_NYC, 'Table_9_NYC_ALL': Table_9_NYC_ALL, 'Table_9_CR': Table_9_CR, 'Table_9_CR_ALL': Table_9_CR_ALL,
                       'Table_10_Both': Table_10_Both, 'Table_10_Both_ALL': Table_10_Both_ALL, 'Table_10_NYC': Table_10_NYC, 'Table_10_NYC_ALL': Table_10_NYC_ALL, 'Table_10_CR': Table_10_CR, 'Table_10_CR_ALL': Table_10_CR_ALL,
                       'Table_11_Both': Table_11_Both, 'Table_11_Both_ALL': Table_11_Both_ALL, 'Table_11_NYC': Table_11_NYC, 'Table_11_NYC_ALL': Table_11_NYC_ALL, 'Table_11_CR': Table_11_CR, 'Table_11_CR_ALL': Table_11_CR_ALL,
                       'Table_12_Both': Table_12_Both, 'Table_12_Both_ALL': Table_12_Both_ALL, 'Table_12_NYC': Table_12_NYC, 'Table_12_NYC_ALL': Table_12_NYC_ALL, 'Table_12_CR': Table_12_CR, 'Table_12_CR_ALL': Table_12_CR_ALL,
                       'Table_13': Table_13, 'Table_13_ALL': Table_13,
                       'Table_14_Both': Table_14_Both, 'Table_14_Both_ALL': Table_14_Both_ALL, 'Table_14_NYC': Table_14_NYC, 'Table_14_NYC_ALL': Table_14_NYC_ALL, 'Table_14_CR': Table_14_CR, 'Table_14_CR_ALL': Table_14_CR_ALL,
                       'Table_15_Both': Table_15_Both, 'Table_15_Both_ALL': Table_15_Both_ALL, 'Table_15_NYC': Table_15_NYC, 'Table_15_NYC_ALL': Table_15_NYC_ALL, 'Table_15_CR': Table_15_CR, 'Table_15_CR_ALL': Table_15_CR_ALL,
                       'Table_16_Both': Table_16_Both, 'Table_16_NYC': Table_16_NYC, 'Table_16_CR': Table_16_CR,
                       'Table_17_Both': Table_17_Both, 'Table_17_Both_ALL': Table_17_Both_ALL, 'Table_17_NYC': Table_17_NYC, 'Table_17_NYC_ALL': Table_17_NYC_ALL, 'Table_17_CR': Table_17_CR, 'Table_17_CR_ALL': Table_17_CR_ALL,
                       'Table_18_Both': Table_18_Both, 'Table_18_NYC': Table_18_NYC, 'Table_18_CR': Table_18_CR,
                       'Table_19_Both': Table_19_Both, 'Table_19_Both_ALL': Table_19_Both_ALL, 'Table_19_NYC': Table_19_NYC, 'Table_19_NYC_ALL': Table_19_NYC_ALL, 'Table_19_CR': Table_19_CR, 'Table_19_CR_ALL': Table_19_CR_ALL,
                       'Table_20_Both': Table_20_Both, 'Table_21_Both': Table_21_Both, 'Table_21_Both_ALL': Table_21_Both_ALL, 'Table_22_Both': Table_22_Both,
                       'Table_23_Both': Table_23_Both, 'Table_23_Both_ALL': Table_23_Both_ALL,
                       'Table_24_CFS': Table_24_CFS, 'Table_25_CFS': Table_25_CFS, 'Table_26_CFS': Table_26_CFS, 'Table_27_CFS': Table_27_CFS, 'Table_28_CFS': Table_28_CFS, 'Table_29_CFS': Table_29_CFS, 'Table_30_CFS': Table_30_CFS,
                       'Table_31_CFS': Table_31_CFS,'Table_32_CFS': Table_32_CFS,'Table_33_CFS': Table_33_CFS, 'Table_34_CFS': Table_34_CFS, 'Table_35_CFS': Table_35_CFS, 'Table_36_CFS': Table_36_CFS, 'Table_37_CFS': Table_37_CFS,
                       'Table_38_CFS': Table_38_CFS, 'Table_39_CFS': Table_39_CFS, 'Table_40_CFS': Table_40_CFS, 'Table_41_CFS': Table_41_CFS,'Table_42_CFS': Table_42_CFS,'Table_43_CFS': Table_43_CFS,'Table_44_CFS': Table_44_CFS,
                       'Table_45_CFS': Table_45_CFS, 'Table_46_CFS': Table_46_CFS, 'Table_47_CFS': Table_47_CFS, 'Table_48_CFS': Table_48_CFS, 'Table_49_CFS': Table_49_CFS, 'Table_50_CFS': Table_50_CFS, 'Table_51_CFS': Table_51_CFS,
                       'Table_52_CFS': Table_52_CFS, 'Table_53_CFS': Table_53_CFS, 'Table_54_CFS': Table_54_CFS, 'Table_55_CFS': Table_55_CFS, 'Table_56_CFS': Table_56_CFS, 'Table_57_CFS': Table_57_CFS, 'Table_58_CFS': Table_58_CFS,
                       'Table_59_CFS': Table_59_CFS, 'Table_60_CFS': Table_60_CFS, 'Table_61_CFS': Table_61_CFS, 'Table_62_CFS': Table_62_CFS, 'Table_63_CFS': Table_63_CFS, 'Table_64_CFS': Table_64_CFS, 'Table_65_CFS': Table_65_CFS,
                       'Table_66_CFS': Table_66_CFS, 'Table_67_CFS': Table_67_CFS,'Table_68_CFS': Table_68_CFS, 'Table_69_CFS': Table_69_CFS, 'Table_70_CFS': Table_70_CFS, 'Table_71_CFS': Table_71_CFS, 'Table_72_CFS': Table_72_CFS,
                       'Table_73_CFS': Table_73_CFS, 'Table_74_CFS': Table_74_CFS, 'Table_75_CFS': Table_75_CFS, 'Table_76_CFS': Table_76_CFS, 'Table_77_CFS': Table_77_CFS, 'Table_78_CFS': Table_78_CFS, 'Table_79_CFS': Table_79_CFS,
                       'Table_80_CFS': Table_80_CFS, 'Table_81_CFS': Table_81_CFS, 'Table_82_CFS': Table_82_CFS, 'Table_83_CFS': Table_83_CFS, 'Table_84_CFS': Table_84_CFS, 'Table_85_CFS': Table_85_CFS, 'Table_86_CFS': Table_86_CFS,
                       'Table_87_CFS': Table_87_CFS, 'Table_88_CFS': Table_88_CFS, 'Table_89_CFS': Table_89_CFS, 'Table_90_CFS': Table_90_CFS, 'Table_91_CFS': Table_91_CFS, 'Table_92_CFS': Table_92_CFS, 'Table_93_CFS': Table_93_CFS,
                       'Table_94_CFS': Table_94_CFS, 'Table_95_CFS': Table_95_CFS, 'Table_96_CFS': Table_96_CFS, 'Table_97_CFS': Table_97_CFS, 'Table_98_CFS': Table_98_CFS, 'Table_99_CFS': Table_99_CFS, 'Table_100_CFS': Table_100_CFS,
                       'Table_101_CFS': Table_101_CFS, 'Table_102_CFS': Table_102_CFS, 'Table_103_CFS': Table_103_CFS, 'Table_104_CFS': Table_104_CFS, 'Table_105_CFS': Table_105_CFS, 'Table_106_CFS': Table_106_CFS, 'Table_107_CFS': Table_107_CFS,
                       'Table_108_CFS': Table_108_CFS, 'Table_109_CFS': Table_109_CFS, 'Table_110_CFS': Table_110_CFS, 'Table_111_CFS': Table_111_CFS, 'Table_112_CFS': Table_112_CFS, 'Table_113_CFS': Table_113_CFS, 'Table_114_CFS': Table_114_CFS,
                       'Table_115_CFS': Table_115_CFS, 'Table_116_CFS': Table_116_CFS, 'Table_117_CFS': Table_117_CFS, 'Table_118_CFS': Table_118_CFS, 'Table_119_CFS': Table_119_CFS}

    # GET ALL INDECES FOR NAICS THAT ARE GOING TO BE USED FOR ALL FREIGHT FIELD
    if TableName in ModMetDictionary.values():
        DifNaics = np.setdiff1d(uniqueNAICS, TableDictionary[TableName]['NAICS'])

    if TableName in FTGDictionary.values():
        if SICField:
            DifSIC = np.setdiff1d(uniqueSIC, TableDictionary[TableName]['SIC2D'])

    # GET NUMBER FROM TABLE NAME (TableName)
    Number = [s for s in TableName if s.isdigit()]
    Nbr = ''.join(Number)

    # NUMBER OF USED EQUATIONS FOR TABLES
    equation1 = ["9", "11", "14"]
    equation2 = ["10", "12", "15", "17", "19", '29', '35', "45", "48", "51", "61", "67", "77", "83", "93", "99", "109", "115"]
    equation3 = ["16", "18", "24", "26", '40', "42", "56", "58", "72", "74", "88", "90" "104", "106"]
    equation4 = ["13"]
    equation5 = ["25", "27", "41", "43", "57", "59", "73", "75", "89", "91", "105", "107"]
    equation6 = ["28", '34', "44", "50", "60", "66", "76", "82", "92", "98", "108", "114"]
    equation7 = ['30', '36', "46", "52", "62", "68", "78", "84", "94", "100", "110", "116"]
    equation8 = ['31', '37', "47", "53", "63", "69", "79", "85", "95", "101", "111", "117"]
    equation9 = ['32', '38', "54", "64", "70", "80", "86", "96", "102", "112", "118"]
    equation10 = ['33', '39', "49", "55", "65", "71", "81", "87", "97", "103", "103", "119"]
    equation11 = ["20"]
    equation12 = ["21"]
    equation13 = ["22"]
    equation14 = ["23"]

    # EQUATION 1
    if Nbr in equation1:
        for n, a, b in zip(TableDictionary[TableName]["NAICS"], TableDictionary[TableName]["alpha"], TableDictionary[TableName]["beta"]):
            SectorID = np.where(array['NAICS2D'] == n)  # Get Establishment indices in array for each NAICS code
            Emp = array['Employment'][SectorID]  # Get Employment in array for each NAICS code
            STA = a + b * Emp
            arrayOut[TableName][SectorID] = STA  # Store Calculated Trips for each Establishment

        if ALLFreight:
            if TableName in ModMetDictionary.values():
                if DifNaics.any():
                    for a in DifNaics:
                        SectorIDII = np.where(array['NAICS2D'] == a)
                        EmpII = array['Employment'][SectorIDII]
                        STAII = TableDictionary[TableName + "_ALL"]['alpha'] + TableDictionary[TableName + "_ALL"]['beta'] * EmpII
                        arrayOut[TableName][SectorIDII] = STAII  # Store Calculated Trips for each Establishment

        OutTable = OutFolder + "/OutTable" + str(i)
        i = i + 1
        arcpy.da.NumPyArrayToTable(arrayOut, OutTable)
        arcpy.JoinField_management(OutFeatureClass, 'OBJECTID', OutTable, 'OBJECTID', TableName)
        DeleteTable.append(OutTable)

    # EQUATION 2
    elif Nbr in equation2:
        for n, a, b in zip(TableDictionary[TableName]["NAICS"], TableDictionary[TableName]["alpha"], TableDictionary[TableName]["beta"]):
            SectorID = np.where(array['NAICS2D'] == n)  # Get Establishment indices in array for each NAICS code
            Emp = array['Employment'][SectorID]  # Get Employment in array for each NAICS code
            STA = a * (Emp ** b)
            arrayOut[TableName][SectorID] = STA  # Store Calculated Trips for each Establishment

        if ALLFreight:
            if TableName in ModMetDictionary.values():
                if DifNaics.any():
                    for a in DifNaics:
                        SectorIDII = np.where(array['NAICS2D'] == a)
                        EmpII = array['Employment'][SectorIDII]
                        STAII = TableDictionary[TableName + "_ALL"]['alpha'] + (EmpII ** TableDictionary[TableName + "_ALL"]['beta'])
                        arrayOut[TableName][SectorIDII] = STAII  # Store Calculated Trips for each Establishment

        OutTable = OutFolder + "/OutTable" + str(i)
        i = i + 1
        arcpy.da.NumPyArrayToTable(arrayOut, OutTable)
        arcpy.JoinField_management(OutFeatureClass, 'OBJECTID', OutTable, 'OBJECTID', TableName)
        DeleteTable.append(OutTable)

    # EQUATION 3
    elif Nbr in equation3:
        for n, b in zip(TableDictionary[TableName]["NAICS"], TableDictionary[TableName]["beta"]):
            SectorID = np.where(array['NAICS2D'] == n)  # Get Establishment indices in array for each NAICS code
            Emp = array['Employment'][SectorID]  # Get Employment in array for each NAICS code
            STA = Emp * b
            arrayOut[TableName][SectorID] = STA  # Store Calculated Trips for each Establishment
        OutTable = OutFolder + "/OutTable" + str(i)
        i = i + 1
        arcpy.da.NumPyArrayToTable(arrayOut, OutTable)
        arcpy.JoinField_management(OutFeatureClass, 'OBJECTID', OutTable, 'OBJECTID', TableName)
        DeleteTable.append(OutTable)

    # EQUATION 4
    elif Nbr in equation4:
        for s, f10, f40, f149, f999, f1000 in zip(TableDictionary[TableName]['SIC2D'], TableDictionary[TableName]['F10'], TableDictionary[TableName]['F40'], TableDictionary[TableName]['F149'], TableDictionary[TableName]['F999'], TableDictionary[TableName]['F1000']):
            with np.errstate(invalid='ignore'):
                SectorID = np.where((array['SIC2D'] == s) & (array['Employment'] <= 10))
                Emp = array['Employment'][SectorID]
                STA = Emp * f10
                arrayOut[TableName][SectorID] = STA

                SectorID = np.where((array['SIC2D'] == s) & (array['Employment'] <= 40) & (array['Employment'] > 10))
                Emp = array['Employment'][SectorID]
                STA = Emp * f40
                arrayOut[TableName][SectorID] = STA

                SectorID = np.where((array['SIC2D'] == s) & (array['Employment'] <= 149) & (array['Employment'] > 40))
                Emp = array['Employment'][SectorID]
                STA = Emp * f149
                arrayOut[TableName][SectorID] = STA

                SectorID = np.where((array['SIC2D'] == s) & (array['Employment'] <= 999) & (array['Employment'] > 149))
                Emp = array['Employment'][SectorID]
                STA = Emp * f999
                arrayOut[TableName][SectorID] = STA

                SectorID = np.where((array['SIC2D'] == s) & (array['Employment'] >= 1000))
                Emp = array['Employment'][SectorID]
                STA = Emp * f1000
                arrayOut[TableName][SectorID] = STA

        if ALLFreight:
            for a in DifSIC:
                SectorIDII = np.where((array['SIC2D'] == a) & (array['Employment'] <= 10))
                EmpII = array['Employment'][SectorIDII]
                STAII = Table_13_ALL['F10'] * EmpII
                arrayOut[TableName][SectorIDII] = STAII

                SectorIDII = np.where((array['SIC2D'] == a) & (array['Employment'] <= 40) & (array['Employment'] > 10))
                EmpII = array['Employment'][SectorIDII]
                STAII = Table_13_ALL['F40'] * EmpII
                arrayOut[TableName][SectorIDII] = STAII

                SectorIDII = np.where((array['SIC2D'] == a) & (array['Employment'] <= 149) & (array['Employment'] > 40))
                EmpII = array['Employment'][SectorIDII]
                STAII = Table_13_ALL['F149'] * EmpII
                arrayOut[TableName][SectorIDII] = STAII

                SectorIDII = np.where((array['SIC2D'] == s) & (array['Employment'] <= 999) & (array['Employment'] > 149))
                EmpII = array['Employment'][SectorIDII]
                STAII = Table_13_ALL['F999'] * EmpII
                arrayOut[TableName][SectorIDII] = STAII

                SectorIDII = np.where((array['SIC2D'] == s) & (array['Employment'] >= 1000))
                EmpII = array['Employment'][SectorIDII]
                STAII = Table_13_ALL['F1000'] * EmpII
                arrayOut[TableName][SectorIDII] = STAII

        OutTable = OutFolder + "/OutTable" + str(i)
        i = i + 1
        arcpy.da.NumPyArrayToTable(arrayOut, OutTable)
        arcpy.JoinField_management(OutFeatureClass, 'OBJECTID', OutTable, 'OBJECTID', TableName)
        DeleteTable.append(OutTable)

    # EQUATION 5
    elif Nbr in equation5:
        for n, b in zip(TableDictionary[TableName]["NAICS"], TableDictionary[TableName]["beta"]):
            SectorID = np.where(array['NAICS3D'] == n)  # Get Establishment indices in array for each NAICS code
            Emp = array['Employment'][SectorID]  # Get Employment in array for each NAICS code
            STA = Emp * b
            arrayOut[TableName][SectorID] = STA  # Store Calculated Trips for each Establishment
        OutTable = OutFolder + "/OutTable" + str(i)
        i = i + 1
        arcpy.da.NumPyArrayToTable(arrayOut, OutTable)
        arcpy.JoinField_management(OutFeatureClass, 'OBJECTID', OutTable, 'OBJECTID', TableName)
        DeleteTable.append(OutTable)

    # EQUATION 6
    elif Nbr in equation6:
        for n, b in zip(TableDictionary[TableName]["NAICS"], TableDictionary[TableName]["beta"]):
            SectorID = np.where(array['NAICS2D'] == n)  # Get Establishment indices in array for each NAICS code
            Emp = array['Employment'][SectorID]  # Get Employment in array for each NAICS code
            STA = np.log10(np.abs(Emp)) * b
            arrayOut[TableName][SectorID] = STA  # Store Calculated Trips for each Establishment
        OutTable = OutFolder + "/OutTable" + str(i)
        i = i + 1
        arcpy.da.NumPyArrayToTable(arrayOut, OutTable)
        arcpy.JoinField_management(OutFeatureClass, 'OBJECTID', OutTable, 'OBJECTID', TableName)
        DeleteTable.append(OutTable)

    # EQUATION 7
    elif Nbr in equation7:
        for n, a, b in zip(TableDictionary[TableName]["NAICS"], TableDictionary[TableName]["alpha"], TableDictionary[TableName]["beta"]):
            SectorID = np.where(array['NAICS2D'] == n)  # Get Establishment indices in array for each NAICS code
            Emp = array['Employment'][SectorID]  # Get Employment in array for each NAICS code
            STA = a * np.exp(b * Emp)
            arrayOut[TableName][SectorID] = STA  # Store Calculated Trips for each Establishment

        OutTable = OutFolder + "/OutTable" + str(i)
        i = i + 1
        arcpy.da.NumPyArrayToTable(arrayOut, OutTable)
        arcpy.JoinField_management(OutFeatureClass, 'OBJECTID', OutTable, 'OBJECTID', TableName)
        DeleteTable.append(OutTable)

    # EQUATION 7
    elif Nbr in equation8:
        for n, b in zip(TableDictionary[TableName]["NAICS"], TableDictionary[TableName]["beta"]):
            SectorID = np.where(array['NAICS3D'] == n)  # Get Establishment indices in array for each NAICS code
            Emp = array['Employment'][SectorID]  # Get Employment in array for each NAICS code
            STA = np.log10(np.abs(Emp)) * b
            arrayOut[TableName][SectorID] = STA  # Store Calculated Trips for each Establishment
        OutTable = OutFolder + "/OutTable" + str(i)
        i = i + 1
        arcpy.da.NumPyArrayToTable(arrayOut, OutTable)
        arcpy.JoinField_management(OutFeatureClass, 'OBJECTID', OutTable, 'OBJECTID', TableName)
        DeleteTable.append(OutTable)

    # EQUATION 8
    elif Nbr in equation9:
        for n, a, b in zip(TableDictionary[TableName]["NAICS"], TableDictionary[TableName]["alpha"], TableDictionary[TableName]["beta"]):
            SectorID = np.where(array['NAICS3D'] == n)  # Get Establishment indices in array for each NAICS code
            Emp = array['Employment'][SectorID]  # Get Employment in array for each NAICS code
            STA = a * (Emp ** b)
            arrayOut[TableName][SectorID] = STA  # Store Calculated Trips for each Establishment

        OutTable = OutFolder + "/OutTable" + str(i)
        i = i + 1
        arcpy.da.NumPyArrayToTable(arrayOut, OutTable)
        arcpy.JoinField_management(OutFeatureClass, 'OBJECTID', OutTable, 'OBJECTID', TableName)
        DeleteTable.append(OutTable)

    # EQUATION 10
    elif Nbr in equation10:
        for n, a, b in zip(TableDictionary[TableName]["NAICS"], TableDictionary[TableName]["alpha"], TableDictionary[TableName]["beta"]):
            SectorID = np.where(array['NAICS3D'] == n)  # Get Establishment indices in array for each NAICS code
            Emp = array['Employment'][SectorID]  # Get Employment in array for each NAICS code
            STA = a * np.exp(b * Emp)
            arrayOut[TableName][SectorID] = STA  # Store Calculated Trips for each Establishment

        OutTable = OutFolder + "/OutTable" + str(i)
        i = i + 1
        arcpy.da.NumPyArrayToTable(arrayOut, OutTable)
        arcpy.JoinField_management(OutFeatureClass, 'OBJECTID', OutTable, 'OBJECTID', TableName)
        DeleteTable.append(OutTable)

    # EQUATION 11
    elif Nbr in equation11:

        TableName1 = "Table_16_Both"

        for n, b, l in zip(TableDictionary[TableName1]["NAICS"], TableDictionary[TableName1]["beta"], TableDictionary[TableName]["lamb"]):
            SectorID = np.where(array['NAICS2D'] == n)  # Get Establishment indices in array for each NAICS code
            Emp = array['Employment'][SectorID]  # Get Employment in array for each NAICS code
            STA = Emp * b * l
            arrayOut[TableName][SectorID] = STA  # Store Calculated Trips for each Establishment

        OutTable = OutFolder + "/OutTable" + str(i)
        i = i + 1
        arcpy.da.NumPyArrayToTable(arrayOut, OutTable)
        arcpy.JoinField_management(OutFeatureClass, 'OBJECTID', OutTable, 'OBJECTID', TableName)
        DeleteTable.append(OutTable)

    # EQUATION 12
    elif Nbr in equation12:
        TableName1 = "Table_17_Both"
        for n, a, b, c, l in zip(TableDictionary[TableName1]["NAICS"], TableDictionary[TableName1]["alpha"], TableDictionary[TableName1]["beta"], TableDictionary[TableName]["alpha"], TableDictionary[TableName]["lamb"]):
            SectorID = np.where(array['NAICS2D'] == n)  # Get Establishment indices in array for each NAICS code
            Emp = array['Employment'][SectorID]  # Get Employment in array for each NAICS code
            temp = a * (Emp ** b)
            STA = c * (temp ** l)
            arrayOut[TableName][SectorID] = STA  # Store Calculated Trips for each Establishment

        if ALLFreight:
            TableName2 = "Table_21_Both"
            DifNaics = np.setdiff1d(uniqueNAICS, TableDictionary[TableName2]['NAICS'])
            for a in DifNaics:
                    SectorIDII = np.where(array['NAICS2D'] == a)
                    EmpII = array['Employment'][SectorIDII]
                    temp = TableDictionary[TableName1 + "_ALL"]['alpha'] * (EmpII ** TableDictionary[TableName1 + "_ALL"]['beta'])
                    STAIII = (temp ** TableDictionary[TableName2 + "_ALL"]['lamb']) * TableDictionary[TableName2 + "_ALL"]['alpha']
                    arrayOut[TableName][SectorIDII] = STAIII  # Store Calculated Trips for each Establishment

        OutTable = OutFolder + "/OutTable" + str(i)
        i = i + 1
        arcpy.da.NumPyArrayToTable(arrayOut, OutTable)
        arcpy.JoinField_management(OutFeatureClass, 'OBJECTID', OutTable, 'OBJECTID', TableName)

    # EQUATION 13
    elif Nbr in equation13:

            TableName1 = "Table_18_Both"

            for n, b, l in zip(TableDictionary[TableName1]["NAICS"], TableDictionary[TableName1]["beta"], TableDictionary[TableName]["lamb"]):
                SectorID = np.where(array['NAICS2D'] == n)  # Get Establishment indices in array for each NAICS code
                Emp = array['Employment'][SectorID]  # Get Employment in array for each NAICS code
                STA = Emp * b * l
                arrayOut[TableName][SectorID] = STA  # Store Calculated Trips for each Establishment

            OutTable = OutFolder + "/OutTable" + str(i)
            i = i + 1
            arcpy.da.NumPyArrayToTable(arrayOut, OutTable)
            arcpy.JoinField_management(OutFeatureClass, 'OBJECTID', OutTable, 'OBJECTID', TableName)
            DeleteTable.append(OutTable)

    # EQUATION 14
    elif Nbr in equation14:
        TableName1 = "Table_19_Both"
        for n, a, b, c, l in zip(TableDictionary[TableName1]["NAICS"], TableDictionary[TableName1]["alpha"], TableDictionary[TableName1]["beta"], TableDictionary[TableName]["alpha"], TableDictionary[TableName]["lamb"]):
            SectorID = np.where(array['NAICS2D'] == n)  # Get Establishment indices in array for each NAICS code
            Emp = array['Employment'][SectorID]  # Get Employment in array for each NAICS code
            temp = a * (Emp ** b)
            STA = c * (temp ** l)
            arrayOut[TableName][SectorID] = STA  # Store Calculated Trips for each Establishment
        if ALLFreight:
            TableName2 = "Table_23_Both"
            DifNaics = np.setdiff1d(uniqueNAICS, TableDictionary[TableName2]['NAICS'])
            for a in DifNaics:
                    SectorIDII = np.where(array['NAICS2D'] == a)
                    EmpII = array['Employment'][SectorIDII]
                    temp = TableDictionary[TableName1 + "_ALL"]['alpha'] * (EmpII ** TableDictionary[TableName1 + "_ALL"]['beta'])
                    STAII = TableDictionary[TableName2 + "_ALL"]['alpha'] * (temp ** TableDictionary[TableName2 + "_ALL"]['lamb'])
                    arrayOut[TableName][SectorIDII] = STAII  # Store Calculated Trips for each Establishment

        OutTable = OutFolder + "/OutTable" + str(i)
        i = i + 1
        arcpy.da.NumPyArrayToTable(arrayOut, OutTable)
        arcpy.JoinField_management(OutFeatureClass, 'OBJECTID', OutTable, 'OBJECTID', TableName)
        DeleteTable.append(OutTable)

arcpy.AddMessage("Done with Task III")
arcpy.AddMessage("-------------------")

# Delete newly added attribute columns
arcpy.AddMessage("Task IV: Remove Temporary Files")
arcpy.DeleteField_management(Establishments, ['NAICS3D', 'NAICS2D', 'Employment', 'SIC2D'])
arcpy.DeleteField_management(OutFeatureClass, ['Employment'])

arcpy.AddMessage("Done With Task IV")
arcpy.AddMessage("-----------------")

print DeleteTable
for d in DeleteTable:
    arcpy.Delete_management(d)

arcpy.AddMessage("Task V: Importing Freight Generation Trip Output to ArcMAp")

mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]
newLayer = arcpy.mapping.Layer(OutFeatureClass)
arcpy.mapping.AddLayer(df, newLayer, "BOTTOM")
arcpy.RefreshActiveView()
arcpy.RefreshTOC()
del mxd, df, newLayer

arcpy.AddMessage("Done with Task V")
arcpy.AddMessage("Finished")






