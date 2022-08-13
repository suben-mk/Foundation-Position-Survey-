# General Survey Function
# 09/08/2022
# By Suben Mukem 

import math

PI = math.pi
DegtoRad = PI / 180.0
RadtoDeg = 180.0 / PI

# Convert degree to degree, minute, second
def DegtoDMS(a):
	if a >= 0:
		m_sign = 1
	else:
		m_sign = -1

	d = abs(a)
	mm, ss = divmod(d * 3600, 60)
	dd, mm = divmod(mm, 60)
	return (dd, mm, ss, m_sign)

# Convert degree, minute, second to string (dd°mm'ss.ss")
def DMSStr(dd, mm, ss, m_sign):
	dd_sign = u'\N{DEGREE SIGN}'
	return '{:.0f}{}{:.0f}'"'{:.2f}"'"'.format(m_sign*dd, dd_sign, mm, ss)

# Convert string (dd°mm'ss.ss") to degree
def DMSStrtoDeg(dms):
	dd_sign = u'\N{DEGREE SIGN}'
	dd_symbol = dms.replace(dd_sign, "-")
	mm_symbol = dd_symbol.replace("'", "-")
	ss_symbol = mm_symbol.replace('"',"")

	d_split = ss_symbol.split("-")
	d = float(d_split[0])
	m = float(d_split[1])
	s = float(d_split[2])

	return d + m/60.0 + s/3600.0

# Calculate distance and azimuth
def Direction(Estart, Nstart, Eend, Nend):
	dE = Eend - Estart
	dN = Nend - Nstart

	Dist = math.sqrt(dE**2 + dN**2)
	A = math.atan(dE / dN) * RadtoDeg

	if   dN < 0:
		 Azi = 180 + A
	elif dE < 0:
		 Azi = 360 + A
	else:
		 Azi = A		
	return Dist, Azi

# Calculate local coordinate (X, Y) to grid coordinate (E, N)
def CoorXYtoEN(ECL, NCL, AZCL, Y, X):
	Ei = ECL + Y * math.sin(AZCL * DegtoRad) + X * math.sin((90 + AZCL) * DegtoRad)
	Ni = NCL + Y * math.cos(AZCL * DegtoRad) + X * math.cos((90 + AZCL) * DegtoRad)
	return Ei, Ni

# Calculate grid coordinate (E, N) to local coordinate (X, Y)
def CoorENtoXY(ECL, NCL, AZCL, Ei, Ni):
	l = math.sqrt((Ei - ECL)**2 + (Ni - NCL)**2)
	Di, Azi = Direction(ECL, NCL, Ei, Ni)
	AZd = (Azi - AZCL)

	Y = l * math.cos(AZd * DegtoRad)
	X = l * math.sin(AZd * DegtoRad)
	return X, Y

# Calculate grid coordinate (E, N) by azimuth and distance
def NextCoorENbyAziDist(Estn, Nstn, Az, Dist):
	Ei = Estn + Dist * math.sin(Az * DegtoRad) 
	Ni = Nstn + Dist * math.cos(Az * DegtoRad)
	return Ei, Ni

# Calculate grid coordinate (E, N) by hor. angle and distance
def NextCoorENbyHAngleDist(Estn, Nstn, Ebs, Nbs, HAngle, Dist):
	DistBStoStn, AzBStoStn = Direction(Ebs, Nbs, Estn, Nstn)

	if   AzBStoStn + HAngle < 180:
		 AzStntoFS = (AzBStoStn + HAngle) + 180
	elif AzBStoStn + HAngle < 180 * 3:
		 AzStntoFS = (AzBStoStn + HAngle) - (180 * 3)
	else:
		 AzStntoFS = (AzBStoStn + HAngle) - 180	

	Ei = Estn + Dist * math.sin(AzStntoFS * DegtoRad) 
	Ni = Nstn + Dist * math.cos(AzStntoFS * DegtoRad)
	return Ei, Ni, AzStntoFS

# Calculate elevation by Total Station
def ElevbyTS(BM, HI, HP, ZA, SD):
	ElevHI = BM + HI
	V = SD * math.sin((90 - ZA) * DegtoRad)
	ELi = ElevHI + V - HP
	return ELi

# Calculate Cross Fall elevation
def CrossFallElev(ElevCL, Offset, CrossFall):
	ELi = ElevCL + abs(Offset) * (CrossFall / 100)
	return ELi

# Calculate circle center from 3 points
def CenterCircle3P(E1, N1, E2, N2, E3, N3):
  EQa = E2 - E1
  EQb = N2 - N1
  EQc = E3 - E1
  EQd = N3 - N1
  EQe = EQa * (E1 + E2) + EQb * (N1 + N2)
  EQf = EQc * (E1 + E3) + EQd * (N1 + N3)
  EQg = 2.0  * (EQa * (N3 - N2) - EQb * (E3 - E2))

  if EQg == 0:
    False
  else:
    Ec = (EQd * EQe - EQb * EQf) / EQg
    Nc = (EQa * EQf - EQc * EQe) / EQg
    radius = math.sqrt((E1 - Ec)**2 + (N1 - Nc)**2)
  return Ec, Nc, radius