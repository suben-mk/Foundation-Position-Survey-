# MainPro_Setting-outFoundation_Rev02
# By Suben Mukem
# Revision 06.08.2022

import numpy as np
import pandas as pd
from GeneralSurveyFunction import*

# ----------------------------------- Calculation of  Setting-out Foundation ----------------------------------- #

# 1. Import data
# Pier schedule data (PIER NO., CH, N, E, AZ, SKEW, TYPE)
df_PSD = pd.read_excel("Pier Schedule & Foundation Type.xlsx", "Pier Schedule")

# Foundation type data (TYPE, P0, Y0, X0 -->,Pi, Yi, Xi)
df_FTD = pd.read_excel("Pier Schedule & Foundation Type.xlsx", "Foundation Type")


# 2. Calculation of  setting-out foundation
# Fill "N/A" if data is nan
df_PSD.fillna("N/A", inplace=True)
df_FTD.fillna("N/A", inplace=True)

# Convert dataframe to numpy array
PSD = df_PSD.to_numpy()
FTD = df_FTD.to_numpy()

count_PSD = len(df_PSD) # Count pier schedule data (row)
RESULT = [] # Record results

for i in range(count_PSD):
    PIER = PSD[i][0] # Pier No.
    CH = PSD[i][1] # Chainage
    NCL = PSD[i][2] # Northing at Pier center
    ECL = PSD[i][3] # Easting at Pier center
    PIER_AZ = PSD[i][4] # Pier Azimuth
    F_SKEW = PSD[i][5] # Footing Skew
    F_TYPE1 = PSD[i][6] # Foundation Type

    # Convert degrees to dd°mm'ss.ss"
    # Pier Azimuth
    d1, m1, s1, sign1 = DegtoDMS(PIER_AZ)
    PIER_AzDMS = DMSStr(d1, m1, s1, sign1)
    
    # Footing Skew
    d2, m2, s2, sign2 = DegtoDMS(F_SKEW)
    F_SkewDMS = DMSStr(d2, m2, s2, sign2)   

    if F_TYPE1 == "N/A":
        RESULT.append([PIER, CH, np.nan, NCL, ECL, PIER_AzDMS, F_SkewDMS, np.nan]) # if Foundation Type is n/a
    else:
        count_FTD = len(df_FTD) # Count foundation type data (row)

        for j in range(count_FTD):
            F_TYPE2 = FTD[j][0] # Foundation Type

            if F_TYPE1 != F_TYPE2:
                continue # Skip data if  F_TYPE1 is not match to F_TYPE2
            else:
                RESULT.append([PIER, CH, np.nan, NCL, ECL, PIER_AzDMS, F_SkewDMS, F_TYPE1])

                for k in range(1, len(df_FTD.columns), 3): # range(Start, End, Step)
                    Index_PN = k # Index Point No.
                    Index_Y = Index_PN + 1 # Index Y 
                    Index_X = Index_Y + 1 # Index X 
                    FINAL_AZ = PIER_AZ + F_SKEW # Final azimuth

                    if FTD[j][Index_Y] and FTD[j][Index_X] == "N/A":
                        continue # Skip calculation if Y and X are n/a
                    else:
                        P = PIER + "/" + str(FTD[j][Index_PN]) # Point No.
                        Y = FTD[j][Index_Y] # Y axis is along with alignment
                        X = FTD[j][Index_X] # X axis is offset with alignment 
                        SOF = CoorXYtoEN(ECL, NCL, FINAL_AZ, Y, X) # Setting-Out Foundation

                        RESULT.append([np.nan, np.nan, P, SOF[1], SOF[0]])

# 3. Export Setting-Out Foundation Result
Names = ["PIER NO.", "CHAINAGE", "POINT NO.", "NORTHING", "EASTING", "PIER AZIMUTH", "FOOTING SKEW", "FOUNDATION TYPE"]
df_Result = pd.DataFrame(RESULT , columns= Names)
df_Result.to_excel("Setting-Out Foundation Result.xlsx", sheet_name="Result", index = False)