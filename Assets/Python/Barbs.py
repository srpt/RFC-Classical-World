# Rhye's and Fall of Civilization - Barbarian units and cities

from CvPythonExtensions import *
import CvUtil
import UnitArtStyler
import Consts as con
from RFCUtils import utils

# globals
gc = CyGlobalContext()
localText = CyTranslator()

### Constants ###

iIndependent1 = con.iIndependent1
iIndependent2 = con.iIndependent2
iIndependent3 = con.iIndependent3
iIndependent4 = con.iIndependent4
iBarbarian = con.iBarbarian

# iCiv, Name, Year, X, Y, iReligion, Skip
tMinorCities = (
	(iIndependent1,  "Kasi",			 -480,  97, 46, [], [], [], 0), 
	
	
)

# These cities will receive extra defense if controlled by indeps/barbs: Start, End, X, Y
tMinorStates = (
	
)




class Barbs:


	def checkTurn(self, iGameTurn):
			
		iHuman = utils.getHumanID()
		iHandicap = gc.getGame().getHandicapType() - 1
		
		# Randomness
		iRand1 = gc.getGame().getSorenRandNum(2, 'Random spawn size for this turn')
		iRand2 = gc.getGame().getSorenRandNum(2, 'Another one')
		iRand3 = gc.getGame().getSorenRandNum(2, 'One more')
		
		# Independent cities
		for i in range(len(tMinorCities)):
			if tMinorCities[i][8] == 0:
				iTurn = getTurnForYear(tMinorCities[i][2])
				if iGameTurn == iTurn or iGameTurn == iTurn + 5 or iGameTurn == iTurn + 10:
					if self.foundCity(tMinorCities[i][0], tMinorCities[i][1], tMinorCities[i][3], tMinorCities[i][4], tMinorCities[i][5], tMinorCities[i][6], tMinorCities[i][7]):
						tMinorCities[i][8] == 1
						
		## BARB SPAWNS ##
		#Numidians
		if iGameTurn >= getTurnForYear(-460) and iGameTurn <= getTurnForYear(200):
			self.spawnUnits(iBarbarian, (10,34),(23,28), con.iSkirmisher, 1, iGameTurn, 10, 0, utils.outerInvasion, UnitAITypes.UNITAI_PILLAGE, "Numidian", "ART_DEF_UNIT_SKIRMISHER_CARTHAGE")
			self.spawnUnits(iBarbarian, (10,34),(23,28), con.iSkirmisher, 1+iRand1, iGameTurn, 15, 0, utils.outerInvasion, UnitAITypes.UNITAI_PILLAGE, "Numidian", "ART_DEF_UNIT_SKIRMISHER_CARTHAGE")
		#Libyans
		if iGameTurn >= getTurnForYear(-460) and iGameTurn <= getTurnForYear(200):
			self.spawnUnits(iBarbarian, (34,28),(47,18), con.iBarbWarrior, 1, iGameTurn, 10, 1, utils.outerInvasion, UnitAITypes.UNITAI_PILLAGE, "Libyan", "ART_DEF_UNIT_WARRIOR_LIBYAN")
			self.spawnUnits(iBarbarian, (34,28),(47,18), con.iBarbWarrior, 1+iRand1, iGameTurn, 15, 1, utils.outerInvasion, UnitAITypes.UNITAI_PILLAGE, "Libyan", "ART_DEF_UNIT_WARRIOR_LIBYAN")
		#Iberians
		if iGameTurn >= getTurnForYear(-460) and iGameTurn <= getTurnForYear(200):
			self.spawnUnits(iBarbarian, (1,44),(12,33), con.iLevySpearman, 1, iGameTurn, 10, 2, utils.outerInvasion, UnitAITypes.UNITAI_PILLAGE, "Libyan", "ART_DEF_UNIT_LEVY_SPEARMAN_CELTIC")
			self.spawnUnits(iBarbarian, (1,44),(12,33), con.iLevySpearman, 1+iRand1, iGameTurn, 15, 2, utils.outerInvasion, UnitAITypes.UNITAI_PILLAGE, "Libyan", "ART_DEF_UNIT_LEVY_SPEARMAN_CELTIC")
		#Celts in Gaul
		if iGameTurn >= getTurnForYear(-460) and iGameTurn <= getTurnForYear(200):
			self.spawnUnits(iBarbarian, (5,58),(20,46), con.iLevySpearman, 1, iGameTurn, 10, 3, utils.outerInvasion, UnitAITypes.UNITAI_PILLAGE, "Gallic", "ART_DEF_UNIT_LEVY_SPEARMAN_CELTIC")
			self.spawnUnits(iBarbarian, (5,58),(20,46), con.iLevySpearman, 1+iRand1, iGameTurn, 15, 3, utils.outerInvasion, UnitAITypes.UNITAI_PILLAGE, "Gallic", "ART_DEF_UNIT_LEVY_SPEARMAN_CELTIC")
		#Celts in N Italy
		if iGameTurn >= getTurnForYear(-460) and iGameTurn <= getTurnForYear(200):
			self.spawnUnits(iBarbarian, (21,50),(29,46), con.iLevySpearman, 1, iGameTurn, 10, 4, utils.outerInvasion, UnitAITypes.UNITAI_PILLAGE, "Gallic", "ART_DEF_UNIT_LEVY_SPEARMAN_CELTIC")
			self.spawnUnits(iBarbarian, (21,50),(29,46), con.iLevySpearman, 1+iRand1, iGameTurn, 15, 4, utils.outerInvasion, UnitAITypes.UNITAI_PILLAGE, "Gallic", "ART_DEF_UNIT_LEVY_SPEARMAN_CELTIC")
		#Illyrians
		if iGameTurn >= getTurnForYear(-460) and iGameTurn <= getTurnForYear(200):
			self.spawnUnits(iBarbarian, (30,51),(38,43), con.iLevySpearman, 1, iGameTurn, 10, 5, utils.outerInvasion, UnitAITypes.UNITAI_PILLAGE, "Illyrian", "ART_DEF_UNIT_LEVY_SPEARMAN_CELTIC")
			self.spawnUnits(iBarbarian, (30,51),(38,43), con.iLevySpearman, 1+iRand1, iGameTurn, 15, 5, utils.outerInvasion, UnitAITypes.UNITAI_PILLAGE, "Illyrian", "ART_DEF_UNIT_LEVY_SPEARMAN_CELTIC")
		#return
		#Scythians
		if iGameTurn >= getTurnForYear(-460) and iGameTurn <= getTurnForYear(200):
			self.spawnUnits(iBarbarian, (46,53),(59,50), con.iHorseman, 1, iGameTurn, 10, 6, utils.outerInvasion, UnitAITypes.UNITAI_PILLAGE, "Scythian", "ART_DEF_UNIT_HORSEMAN_SCYTHIAN")
			self.spawnUnits(iBarbarian, (46,53),(59,50), con.iHorseman, 1+iRand1, iGameTurn, 15, 6, utils.outerInvasion, UnitAITypes.UNITAI_PILLAGE, "Scythian", "ART_DEF_UNIT_HORSEMAN_SCYTHIAN")
		#Scythians in the Caucasus
		if iGameTurn >= getTurnForYear(-460) and iGameTurn <= getTurnForYear(200):
			self.spawnUnits(iBarbarian, (60,45),(69,41), con.iHorseman, 1, iGameTurn, 10, 7, utils.outerInvasion, UnitAITypes.UNITAI_PILLAGE, "Scythian", "ART_DEF_UNIT_HORSEMAN_SCYTHIAN")
			self.spawnUnits(iBarbarian, (60,45),(69,41), con.iHorseman, 1+iRand1, iGameTurn, 15, 7, utils.outerInvasion, UnitAITypes.UNITAI_PILLAGE, "Scythian", "ART_DEF_UNIT_HORSEMAN_SCYTHIAN")
		#Scythians in Bulgaria
		if iGameTurn >= getTurnForYear(-460) and iGameTurn <= getTurnForYear(200):
			self.spawnUnits(iBarbarian, (40,50),(45,45), con.iHorseman, 1, iGameTurn, 10, 7, utils.outerInvasion, UnitAITypes.UNITAI_PILLAGE, "Scythian", "ART_DEF_UNIT_HORSEMAN_SCYTHIAN")
			self.spawnUnits(iBarbarian, (40,50),(45,45), con.iHorseman, 1+iRand1, iGameTurn, 15, 7, utils.outerInvasion, UnitAITypes.UNITAI_PILLAGE, "Scythian", "ART_DEF_UNIT_HORSEMAN_SCYTHIAN")
		#Sarmatians
		if iGameTurn >= getTurnForYear(-460) and iGameTurn <= getTurnForYear(200):
			self.spawnUnits(iBarbarian, (72,48),(85,43), con.iHorseman, 1, iGameTurn, 10, 0, utils.outerInvasion, UnitAITypes.UNITAI_PILLAGE, "Sarmatian", "ART_DEF_UNIT_HORSEMAN_SCYTHIAN")
			self.spawnUnits(iBarbarian, (72,48),(85,43), con.iHorseman, 1+iRand1, iGameTurn, 15, 0, utils.outerInvasion, UnitAITypes.UNITAI_PILLAGE, "Sarmatian", "ART_DEF_UNIT_HORSEMAN_SCYTHIAN")
		
		#return
		#Yuezhi
		if iGameTurn >= getTurnForYear(-460) and iGameTurn <= getTurnForYear(200):
			self.spawnUnits(iBarbarian, (116,49),(130,43), con.iHorseman, 1, iGameTurn, 10, 1, utils.outerInvasion, UnitAITypes.UNITAI_PILLAGE, "Yuezhi", "ART_DEF_UNIT_HORSEMAN_SCYTHIAN")
			self.spawnUnits(iBarbarian, (116,49),(130,43), con.iHorseman, 1+iRand1, iGameTurn, 15, 1, utils.outerInvasion, UnitAITypes.UNITAI_PILLAGE, "Yuezhi", "ART_DEF_UNIT_HORSEMAN_SCYTHIAN")
		#return
		#Bai
		if iGameTurn >= getTurnForYear(-460) and iGameTurn <= getTurnForYear(200):
			self.spawnUnits(iBarbarian, (125,35),(130,30), con.iBarbWarrior, 1, iGameTurn, 10, 1, utils.outerInvasion, UnitAITypes.UNITAI_PILLAGE, "Bai", "ART_DEF_UNIT_WARRIOR_BAI")
			self.spawnUnits(iBarbarian, (125,35),(130,30), con.iBarbWarrior, 1+iRand1, iGameTurn, 15, 1, utils.outerInvasion, UnitAITypes.UNITAI_PILLAGE, "Bai", "ART_DEF_UNIT_WARRIOR_BAI")
		return
		#Quanrong
		if iGameTurn >= getTurnForYear(-460) and iGameTurn <= getTurnForYear(200):
			self.spawnUnits(iBarbarian, (118,44),(126,38), con.iBarbWarrior, 1, iGameTurn, 10, 1, utils.outerInvasion, UnitAITypes.UNITAI_PILLAGE, "Quanrong", "ART_DEF_UNIT_WARRIOR_QUANRONG")
			self.spawnUnits(iBarbarian, (118,44),(126,38), con.iBarbWarrior, 1+iRand1, iGameTurn, 15, 1, utils.outerInvasion, UnitAITypes.UNITAI_PILLAGE, "Quanrong", "ART_DEF_UNIT_WARRIOR_QUANRONG")
		
		


	def invasionAlert(self, textKey, playerList = []):
		
		iHuman = utils.getHumanID()
		if utils.isActive(iHuman):
			if not playerList or iHuman in playerList:
				szBuffer = localText.getText(textKey, ())
				CyInterface().addMessage(iHuman, False, con.iDuration, szBuffer, "AS2D_CIVIC_ADOPT", InterfaceMessageTypes.MESSAGE_TYPE_MAJOR_EVENT, None, gc.getInfoTypeForString("COLOR_WHITE"), -1, -1, False, False)


	def foundCity(self, iCiv, sName, iX, iY, lReligions=[], lCorporations =[], lBuildings=[]):
	
		#print ("CITY:", sName, "lReligions=", lReligions, "lCorporations=", lCorporations, "lBuildings=", lBuildings)
	
		if not self.checkRegion(iX, iY):
			return None
		
		pCiv = gc.getPlayer(iCiv)
		pCiv.initCity(iX, iY)
		city = gc.getMap().plot(iX, iY).getPlotCity()
		
		if not city or city.isNone():
			return None
		
		city.setName(sName, False)
		
		if utils.getYear() < -100:
			pCiv.initUnit(con.iMilitiaSpearman, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		elif utils.getYear() < 100:
			pCiv.initUnit(con.iSpearman, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		else:
			pCiv.initUnit(con.iHeavySpearman, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		
		if utils.getYear() < 0:
			pCiv.initUnit(con.iArcher, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		elif utils.getYear() < 200:
			pCiv.initUnit(con.iBowman, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		else:
			pCiv.initUnit(con.iHeavyBowman, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		
		for iReligion in lReligions:
			city.setHasReligion(iReligion, True, False, False)
		
		for iCorporation in lCorporations:
			city.setHasCorporation(iCorporation, True, False, False)
			
		for iBuilding in lBuildings:
			city.setNumRealBuilding(iBuilding, 1)
			
		UnitArtStyler.updateUnitArtAtPlot(city.plot())
		
		return city	


	# from Rhye's, simplified
	def checkRegion(self, plotX, plotY):
		
		cityPlot = gc.getMap().plot(plotX, plotY)
		iNumUnitsInAPlot = cityPlot.getNumUnits()
		
		#checks if the plot already belongs to someone
		if cityPlot.isOwned():
			if cityPlot.getOwner() != iBarbarian:
				return False
		
		#checks if there's a unit on the plot
		if iNumUnitsInAPlot:
			for i in range(iNumUnitsInAPlot):
				unit = cityPlot.getUnit(i)
				iOwner = unit.getOwner()
				if iOwner == iBarbarian:
					return False
		
		#checks the surroundings and allows only AI units
		for x in range(plotX-1, plotX+2):
			for y in range(plotY-1, plotY+2):
				currentPlot = gc.getMap().plot(x,y)
				if currentPlot.isCity():
					return False
				iNumUnitsInAPlot = currentPlot.getNumUnits()
				if iNumUnitsInAPlot:
					for i in range(iNumUnitsInAPlot):
						unit = currentPlot.getUnit(i)
						iOwner = unit.getOwner()
						pOwner = gc.getPlayer(iOwner)
						if pOwner.isHuman():
							return False
		
		return True


	def spawnUnits(self, iCiv, tTopLeft, tBottomRight, iUnitType, iNumUnits, iTurn, iPeriod, iRest, function, eUnitAIType = UnitAITypes.UNITAI_ATTACK, prefix = 0, art = "", promotionList = [], argsList = []):
		
		print "spawnUnits called"
		if iNumUnits <= 0: # edead
			return None
		pUnit = None # edead
		if (iTurn % utils.getTurns(iPeriod) == iRest):
			dummy, plotList = utils.squareSearch( tTopLeft, tBottomRight, function, argsList )
			if (len(plotList)):
				rndNum = gc.getGame().getSorenRandNum(len(plotList), 'Spawn units')
				result = plotList[rndNum]
				if (result):
					pUnit = utils.makeUnit(iUnitType, iCiv, result, iNumUnits, eUnitAIType, promotionList, prefix, art) # edead: pass the object
					
		return pUnit # edead: pass the object


	def getRandomUnit(self, unitList):
		
		return unitList[gc.getGame().getSorenRandNum(len(unitList), 'Random unit')]

		
	def isChristianRegion(self, regionID):
		
		bFound = False
		plotList = utils.getRegionPlotList([regionID])
		for tPlot in plotList:
				pCurrent = gc.getMap().plot(tPlot[0], tPlot[1])
				if pCurrent.isCity():
					iOwner = pCurrent.getPlotCity().getOwner()
					if iOwner not in []:
						return False
					else:
						bFound = True
		return bFound

		
	#rfctemp
	"""def makeLeader(self, pUnit, szName, iLeaderType=con.iGreatGeneral):
		
		if pUnit:
			pUnit.setHasPromotion(con.iLeader, True)
			pUnit.setExperience(20, -1)
			pUnit.setLeaderUnitType(iLeaderType)
			pUnit.setName(szName)"""
	
	
	def getInvasionForce(self, iBaseNumUnits, iCiv):
		
		iNumUnits = iBaseNumUnits + gc.getGame().getHandicapType() - 1 + gc.getGame().getSorenRandNum(2, 'Random invasion force')
		iNumCities = gc.getPlayer(iCiv).getNumCities()
		if iNumCities >= 14:
			iNumUnits += 3
		elif iNumCities >= 11:
			iNumUnits += 2
		elif iNumCities >= 8:
			iNumUnits += 1
		return iNumUnits

