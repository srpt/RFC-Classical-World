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
			if tMinorCities[i][6] == 0:
				iTurn = getTurnForYear(tMinorCities[i][2])
				if iGameTurn == iTurn or iGameTurn == iTurn + 5 or iGameTurn == iTurn + 10:
					if self.foundCity(tMinorCities[i][0], tMinorCities[i][1], tMinorCities[i][3], tMinorCities[i][4], tMinorCities[i][5]):
						tMinorCities[i][6] == 1
		
		
		
		# Independent states - extra defense for minor cities
		if iGameTurn % 20 == 10 and iGameTurn >= getTurnForYear(1270):
			for tMinorCity in tMinorStates:
				if iGameTurn > getTurnForYear(tMinorCity[0]) and iGameTurn < getTurnForYear(tMinorCity[1]):
					plot = gc.getMap().plot(tMinorCity[2], tMinorCity[3])
					iOwner = plot.getOwner()
					if plot.isCity() and plot.getNumUnits() < 4 and iOwner >= con.iNumPlayers:
						utils.makeUnit(self.getRandomUnit(lateSupport), iOwner, (tMinorCity[2], tMinorCity[3]), 1)
		
		


	def invasionAlert(self, textKey, playerList = []):
		
		iHuman = utils.getHumanID()
		if utils.isActive(iHuman):
			if not playerList or iHuman in playerList:
				szBuffer = localText.getText(textKey, ())
				CyInterface().addMessage(iHuman, False, con.iDuration, szBuffer, "AS2D_CIVIC_ADOPT", InterfaceMessageTypes.MESSAGE_TYPE_MAJOR_EVENT, None, gc.getInfoTypeForString("COLOR_WHITE"), -1, -1, False, False)


	def foundCity(self, iCiv, sName, iX, iY, lReligions=[]):
		
		if not self.checkRegion(iX, iY):
			return None
		
		pCiv = gc.getPlayer(iCiv)
		pCiv.initCity(iX, iY)
		city = gc.getMap().plot(iX, iY).getPlotCity()
		
		if not city or city.isNone():
			return None
		
		city.setName(sName, False)
		
		if utils.getYear() < 1050:
			pCiv.initUnit(con.iSpearman, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		else:
			pCiv.initUnit(con.iHeavySpearman, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		
		if utils.getYear() < 1000:
			pCiv.initUnit(con.iArcher, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		elif utils.getYear() < 1250:
			pCiv.initUnit(con.iMarksman, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			city.setNumRealBuilding(con.iWalls, 1)
		else:
			pCiv.initUnit(con.iMarksman, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			city.setNumRealBuilding(con.iWalls, 1)
			city.setNumRealBuilding(con.iCastle, 1)
		
		UnitArtStyler.updateUnitArtAtPlot(city.plot())
		
		for iReligion in lReligions:
			city.setHasReligion(iReligion, True, False, False)
		
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


	def spawnUnits(self, iCiv, tTopLeft, tBottomRight, iUnitType, iNumUnits, iTurn, iPeriod, iRest, function, eUnitAIType = UnitAITypes.UNITAI_ATTACK, prefix = 0, promotionList = [], argsList = []):
		
		if iNumUnits <= 0: # edead
			return None
		pUnit = None # edead
		if (iTurn % utils.getTurns(iPeriod) == iRest):
			dummy, plotList = utils.squareSearch( tTopLeft, tBottomRight, function, argsList )
			if (len(plotList)):
				rndNum = gc.getGame().getSorenRandNum(len(plotList), 'Spawn units')
				result = plotList[rndNum]
				if (result):
					pUnit = utils.makeUnit(iUnitType, iCiv, result, iNumUnits, eUnitAIType, promotionList, prefix) # edead: pass the object
					# if eUnitAIType == UnitAITypes.UNITAI_PILLAGE: # edead
						# pUnit.getGroup().setActivityType(ActivityTypes.ACTIVITY_SLEEP) # edead: fortify rebels
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

