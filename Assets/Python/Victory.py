# Rhye's and Fall of Civilization - Historical Victory Goals
# The Sword of Islam - Religious Victory Goals


from CvPythonExtensions import *
import CvUtil
import PyHelpers
import Popup
import Consts as con
from StoredData import sd
from RFCUtils import utils

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
localText = CyTranslator()

iReligiousVictory = 7
iHistoricalVictory = 8


class Victory:


	def checkPlayerTurn(self, iGameTurn, iPlayer):
		
		iHuman = utils.getHumanID()
		pPlayer = gc.getPlayer(iPlayer)
		
		# HISTORICAL VICTORY
		if gc.getGame().isVictoryValid(iHistoricalVictory):
		
			
			
			#generic checks
			if pPlayer.isAlive() and iPlayer < con.iNumPlayers:
				if sd.get2OutOf3(iPlayer) == False:
					if utils.countAchievedGoals(iPlayer) == 2:
						#intermediate bonus
						sd.set2OutOf3(iPlayer, True)
						if pPlayer.getNumCities() > 0: #this check is needed, otherwise game crashes
							pPlayer.changeGoldenAgeTurns(pPlayer.getGoldenAgeLength()) # edead
							iWarCounter = 0
							iRndnum = gc.getGame().getSorenRandNum(con.iNumPlayers, 'civs')
							iHandicap = gc.getGame().getHandicapType()
							for i in range(iRndnum, con.iNumPlayers + iRndnum):
								iCiv = i % con.iNumPlayers
								pCiv = gc.getPlayer(iCiv)
								if pCiv.isAlive() and pCiv.canContact(iPlayer):                                                                
									if pCiv.AI_getAttitude(iPlayer) <= 0:
										teamCiv = gc.getTeam(pCiv.getTeam())
										if not teamCiv.isAtWar(iPlayer) and not teamCiv.isDefensivePact(iPlayer) and not utils.isAVassal(iCiv):
											teamCiv.AI_setWarPlan(iPlayer, WarPlanTypes.WARPLAN_PREPARING_TOTAL) # edead: prepare for total war
											iWarCounter += 1
											if iWarCounter == 1 + max(1, iHandicap):
												break
			if gc.getGame().getWinner() == -1:
				if sd.getGoal(iPlayer, 0) == 1 and sd.getGoal(iPlayer, 1) == 1 and sd.getGoal(iPlayer, 2) == 1:
					gc.getGame().setWinner(iPlayer, iHistoricalVictory)
				
		# RELIGIOUS VICTORY
		if gc.getGame().isVictoryValid(iReligiousVictory) and iPlayer == iHuman:
			if iGameTurn >= getTurnForYear(con.tBirth[iPlayer]) and gc.getPlayer(iPlayer).getStateReligion() != -1:
				for i in range(3):
					if sd.getReligiousGoal(iPlayer, i) == -1:
						if self.getURV(iPlayer, i):
							sd.setReligiousGoal(iPlayer, i, 1)
				if gc.getGame().getWinner() == -1:
					if sd.getReligiousGoal(iPlayer, 0) == 1 and sd.getReligiousGoal(iPlayer, 1) == 1 and sd.getReligiousGoal(iPlayer, 2) == 1:
						gc.getGame().setWinner(iPlayer, iReligiousVictory)
			

	def onCityAcquired(self, argsList):
		iPreviousOwner, iNewOwner, city, bConquest, bTrade = argsList
		
		if not gc.getGame().isVictoryValid(iHistoricalVictory):
			return
		
		iYear = utils.getYear()
		
		return


	def onCityAcquiredAndKept(self, argsList):
		iOwner,pCity,bMassacre = argsList
		
		if not gc.getGame().isVictoryValid(iHistoricalVictory):
			return
		
		return


	def onCityRazed(self, iPlayer):
		
		if not gc.getGame().isVictoryValid(iHistoricalVictory):
			return
		
		return


	def onTechAcquired(self, iTech, iPlayer):
		
		if not gc.getGame().isVictoryValid(iHistoricalVictory):
			return
		
		return

	def onBuildingBuilt(self, iPlayer, iBuilding, city):
		
		if not gc.getGame().isVictoryValid(iHistoricalVictory):
			return
		
		iGameTurn = gc.getGame().getGameTurn()
		pPlayer = gc.getPlayer(iPlayer)
		
		return
		

	def onCombatResult(self, argsList):
		
		if not gc.getGame().isVictoryValid(iHistoricalVictory):
			return
		# srpt Slavery
		pWinningUnit,pLosingUnit,pAttackingUnit = argsList
		#pWinner,pLoser,pAttacker = argsList
		# end
		pWinningPlayer = gc.getPlayer(pWinningUnit.getOwner())
		pLosingPlayer = gc.getPlayer(pLosingUnit.getOwner())
		cLosingUnit = PyHelpers.PyInfo.UnitInfo(pLosingUnit.getUnitType())
		
		return


	def onUnitSpreadReligionAttempt(self, argsList):
		'Unit tries to spread religion to a city'
		pUnit, iReligion, bSuccess = argsList
		
		if not gc.getGame().isVictoryValid(iHistoricalVictory):
			return
		
		return


	def onGreatPersonBorn(self, argsList):
		pUnit, iPlayer, pCity = argsList
		
		iGameTurn = gc.getGame().getGameTurn()
		
		return


	def onPlayerChangeStateReligion(self, argsList):
		iPlayer, iNewReligion, iOldReligion = argsList
		
		for i in range(3):
			sd.setReligiousGoal(iPlayer, i, -1)
	
	
	def calculateTopCityCulture(self, x, y):
		"""Returns the CyCity object with the highest culture,
		but if no city is located at (x,y), returns -1."""
		iBestCityValue = 0
		pCurrent = gc.getMap().plot( x, y )
		if pCurrent.isCity():
			bestCity = pCurrent.getPlotCity()
			for iPlayerLoop in range(gc.getMAX_PLAYERS()):
				apCityList = PyPlayer(iPlayerLoop).getCityList()
				for pCity in apCityList:
					iTotalCityValue = pCity.GetCy().getCultureTimes100(pCity.getOwner())
					if iTotalCityValue > iBestCityValue:
						bestCity = pCity
						iBestCityValue = iTotalCityValue
			return bestCity
		return -1


	def calculateTopCityPopulation(self, x, y):
		"""Returns the CyCity object with the highest population,
		but if no city is located at (x,y), returns -1."""		
		iBestCityValue = 0
		pCurrent = gc.getMap().plot( x, y )
		if (pCurrent.isCity()):
			bestCity = pCurrent.getPlotCity()
			for iPlayerLoop in range(gc.getMAX_PLAYERS()):
				apCityList = PyPlayer(iPlayerLoop).getCityList()
				for pCity in apCityList:
					iTotalCityValue = pCity.getPopulation()
					if (iTotalCityValue > iBestCityValue and not pCity.isBarbarian()):
						bestCity = pCity
						iBestCityValue = iTotalCityValue
			return bestCity
		return -1


	def getNumOpenBorders(self, iPlayer):
		"""Returns the number of Open Borders agreements that iPlayer has."""
		pTeam = gc.getTeam(gc.getPlayer(iPlayer).getTeam())
		iCount = 0
		for iLoopCiv in range(con.iNumPlayers):
			if iLoopCiv != iPlayer:
				if pTeam.isOpenBorders(iLoopCiv):
					iCount += 1
		return iCount


	def getNumBuildings(self, iPlayer, iBuilding):
		"""Returns the number of iBuilding that iPlayer has in his cities."""
		iCount = 0
		apCityList = PyPlayer(iPlayer).getCityList()
		for pCity in apCityList:
			if pCity.getNumBuilding(iBuilding): iCount += 1
		return iCount


	def getNumProvinces(self, iPlayer):
		"""Returns the number of regions (provinces) that iPlayer controls."""
		iNumProvinces = 0
		regionList = []
		apCityList = PyPlayer(iPlayer).getCityList()
		for pCity in apCityList:
			regionID = gc.getMap().plot(pCity.getX(), pCity.getY()).getRegionID()
			if regionID not in regionList and utils.checkRegionControl(iPlayer, regionID):
				regionList.append(regionID)
				iNumProvinces += 1
		return iNumProvinces


	def isHighestGold(self, iPlayer):
		"""Checks whether iPlayer has the highest amount of Gold."""
		bHighest = True
		iGold = gc.getPlayer(iPlayer).getGold()
		for iLoopCiv in range(con.iNumPlayers):
			if iLoopCiv != iPlayer and gc.getPlayer(iLoopCiv).isAlive():
				if gc.getPlayer(iLoopCiv).getGold() > iGold:
					bHighest = False
					break
		return bHighest


	def isTopCityCulture(self, iPlayer, tCoords):
		"""Checks whether the city at tCoords(x,y) is the city with the highest culture."""
		bestCity = self.calculateTopCityCulture(tCoords[0], tCoords[1])
		if bestCity != -1:
			if bestCity.getOwner() == iPlayer and bestCity.getX() == tCoords[0] and bestCity.getY() == tCoords[1]:
				return True
		return False


	def isTopCityPopulation(self, iPlayer, tCoords):
		"""Checks whether the city at tCoords(x,y) is the city with the highest population."""
		bestCity = self.calculateTopCityPopulation(tCoords[0], tCoords[1])
		if bestCity != -1:
			if bestCity.getOwner() == iPlayer and bestCity.getX() == tCoords[0] and bestCity.getY() == tCoords[1]:
				return True
		return False


	def getNumShrines(self, iPlayer):
		"""Returns the number of Shrines belonging to iPlayer."""
		iNumShrines = 0
		apCityList = PyPlayer(iPlayer).getCityList()
		for pCity in apCityList:
			if pCity.getNumBuilding(con.iCatholicShrine): iNumShrines += 1
			if pCity.getNumBuilding(con.iOrthodoxShrine): iNumShrines += 1
			if pCity.getNumBuilding(con.iHinduShrine): iNumShrines += 1
			if pCity.getNumBuilding(con.iSunniShrine): iNumShrines += 1
			if pCity.getNumBuilding(con.iShiaShrine): iNumShrines += 1
		return iNumShrines
	
	
	def isPlayerHasBuilding(self, iPlayer, iBuilding):
		"""Checks whether iPlayers has at least one iBuilding in his cities."""
		apCityList = PyPlayer(iPlayer).getCityList()
		for pCity in apCityList:
			if pCity.GetCy().getNumRealBuilding(iBuilding): 
				return True
		return False
	
	
	def isCityHasBuilding(self, tCoords, iBuilding):
		"""Checks whether the city at tCoords(x,y) has iBuilding."""
		plot = gc.getMap().plot(tCoords[0], tCoords[1])
		if plot.isCity():
			if plot.getPlotCity().getNumRealBuilding(iBuilding): 
				return True
		return False
	
	
	def isRegionHasBuilding(self, regionID, iBuilding):
		"""Checks whether any city in the region (province) has iBuilding."""
		plotList = utils.getRegionPlotList([regionID])
		for tCoords in plotList:
			if self.isCityHasBuilding(tCoords, iBuilding):
				return True
		return False


	def isTopTech(self, iPlayer):
		"""Checks whether iPlayer has accumulated the higest amount of Science."""
		iNumTotalTechs = gc.getNumTechInfos()
		bTopTech = True
		iNumTechs = 0
		for iTechLoop in range(iNumTotalTechs):
			if gc.getTeam(gc.getPlayer(iPlayer).getTeam()).isHasTech(iTechLoop):
				iNumTechs += 1
		for iPlayerLoop in range(con.iNumPlayers):
			if gc.getPlayer(iPlayerLoop).isAlive() and iPlayerLoop != iPlayer:
				iPlayerNumTechs = 0
				for iTechLoop in range(iNumTotalTechs):
					if gc.getTeam(gc.getPlayer(iPlayerLoop).getTeam()).isHasTech(iTechLoop):
						iPlayerNumTechs = iPlayerNumTechs + 1
				if iPlayerNumTechs >= iNumTechs:
					bTopTech = False
					break
		return bTopTech


	def isTopCulture(self, iPlayer):
		"""Checks whether iPlayer has accumulated the higest number of Culture."""
		bTopCulture = True
		iCulture = gc.getPlayer(iPlayer).countTotalCulture()
		for iPlayerLoop in range(con.iNumPlayers):
			if gc.getPlayer(iPlayerLoop).isAlive() and iPlayerLoop != iPlayer:
				if gc.getPlayer(iPlayerLoop).countTotalCulture() > iCulture:
					bTopCulture = False
					break
		return bTopCulture


	def isHighestPopulation(self, iPlayer):
		"""Checks whether iPlayer has the highest total population."""
		iPop = gc.getPlayer(iPlayer).getRealPopulation()
		bHighest = True
		for iLoopCiv in range(con.iNumPlayers):
			if iPop < gc.getPlayer(iLoopCiv).getRealPopulation():
				bHighest = False
				break
		return bHighest


	def isMostProductive(self, iPlayer):
		"""Checks whether iPlayer has the highest amount of total Production in this cities."""
		iTopValue = 0
		iTopCiv = -1
		for iLoopPlayer in range(con.iNumPlayers):
			pLoopPlayer = gc.getPlayer(iLoopPlayer)
			if pLoopPlayer.getNumCities() > 0:
				iValue = pLoopPlayer.calculateTotalYield(YieldTypes.YIELD_PRODUCTION)
				if iValue > iTopValue:
					iTopValue = iValue
					iTopCiv = iLoopPlayer
		return (iTopCiv == iPlayer)


	def getNumVassals(self, iPlayer):
		"""Returns the number of vassals belonging to iPlayer."""
		iCounter = 0
		for iCiv in range(con.iNumPlayers):
			if iCiv != iPlayer:
				if gc.getPlayer(iCiv).isAlive():
					if gc.getTeam(gc.getPlayer(iCiv).getTeam()).isVassal(iPlayer):
						iCounter += 1
		return iCounter


	def getNumLuxuries(self, iPlayer):
		"""Returns the number of happiness-giving resources available to iPlayer."""
		nLuxuries = 0
		pPlayer = gc.getPlayer(iPlayer)
		for iBonus in range(con.iNumResources):
			if gc.getBonusInfo(iBonus).getHappiness() > 0:
				if pPlayer.getNumAvailableBonuses(iBonus) > 0:
					nLuxuries += 1
		return nLuxuries


	def getRegionsOwnedCity(self, iPlayer, regionList, bCoastal=False):
		"""Checks whether the player has any city in the provided list of regions (provinces)."""
		bFound = False
		for regionID in regionList:
			if utils.checkRegionOwnedCity(iPlayer, regionID, bCoastal):
				bFound = True
				break
		return bFound


	def isFreeOfIslam(self, regionList):
		"""Checks whether there is Sunni or Shia Islam present in the list of regions (provinces)."""
		bSuccess = True
		for regionID in regionList:
			plotList = utils.getRegionPlotList([regionID])
			for tPlot in plotList:
				pCurrent = gc.getMap().plot(tPlot[0], tPlot[1])
				if pCurrent.isCity():
					if pCurrent.getPlotCity().isHasReligion(con.iSunni) or pCurrent.getPlotCity().isHasReligion(con.iShia):
						bSuccess = False
						break
		return bSuccess


	def isHasLegendaryCity(self, iPlayer):
		"""Checks whether iPlayer has a city with Legendary culture."""
		apCityList = PyPlayer(iPlayer).getCityList()
		for pCity in apCityList:
			if pCity.GetCy().countTotalCultureTimes100() >= utils.getTurns(2500000):
				return True
		return False


	def isTopReligion(self, iReligion, bAllowDraw=False):
		"""Checks whether iReligion is the most popular religion. If bAllowDraw is set to True,
		the function will return True even in case of a draw with another religion."""
		religionPercent = gc.getGame().calculateReligionPercent(iReligion)
		bFirst = True
		for iLoop in range(con.iNumReligions):
			if iLoop != iReligion:
				if gc.getGame().calculateReligionPercent(iLoop) >= religionPercent:
					if bAllowDraw and gc.getGame().calculateReligionPercent(iLoop) == religionPercent:
						continue
					bFirst = False
					break
		return bFirst


	def checkRegions(self, iPlayer, regionList, bVassal=False):
		"""Checks whether iPlayer and his vassals (if bVassal is True) control
		all regions (provinces) in regionList."""
		for regionID in regionList:
			if not utils.checkRegionControl(iPlayer, regionID, bVassal):
				return False
		return True
	
	
	def countUniqueGreatPeople(self, tCoords):
		"""Returns the number of Great People settled at tCoords(x,y)."""
		iCount = 0
		plot = gc.getMap().plot(tCoords[0], tCoords[1])
		if plot.isCity():
			city = plot.getPlotCity()
			iGreatPriest = gc.getInfoTypeForString("SPECIALIST_GREAT_PRIEST")
			for i in range(iGreatPriest, iGreatPriest+7, 1):
				iCount += min(1, city.getFreeSpecialistCount(i))
		return iCount
	
	
	def countRelics(self, iPlayer):
		"""Returns the number of relic units and reliquaries belonging to iPlayer."""
		iCount = 0
		iReligion = gc.getPlayer(iPlayer).getStateReligion()
		playerHelper = PyPlayer(iPlayer)
		apCityList = playerHelper.getCityList()
		for iRelic in con.relics.keys():
			if gc.getBuildingInfo(iRelic).getStateReligion() != iReligion and gc.getBuildingInfo(iRelic).getOrStateReligion() != iReligion:
				continue
			if playerHelper.hasUnitType(con.relics[iRelic][0]):
				iCount += 1
			for pCity in apCityList:
				iCount += pCity.getNumBuilding(iRelic)
		return iCount
	
	
	def countVassalReligions(self, iPlayer):
		"""Returns the number of unique state religions found among vassals of iPlayer."""
		religionList = []
		iTeam = gc.getPlayer(iPlayer).getTeam()
		for iLoopPlayer in range(con.iNumPlayers):
			if iLoopPlayer != iPlayer:
				pLoopPlayer = gc.getPlayer(iLoopPlayer)
				if gc.getTeam(pLoopPlayer.getTeam()).isVassal(iPlayer) and pLoopPlayer.getStateReligion() != -1:
					religionList.append(pLoopPlayer.getStateReligion())
		return len(utils.uniq(religionList))
	
	
	def countPlayersByMinAttitude(self, iPlayer, iMinAttitude=4):
		"""Returns the number of players with attitude towards iPlayer being 
		greater or equal to iMinAttitude; The default of 4 is ATTITUDE_FRIENDLY."""
		iCount = 0
		for iLoopPlayer in range(con.iNumPlayers):
			if iLoopPlayer != iPlayer and gc.getPlayer(iLoopPlayer).isAlive():
				if gc.getPlayer(iLoopPlayer).AI_getAttitude(iPlayer) >= iMinAttitude:
					iCount += 1
		return iCount
	
	
	def getTopPopulationRegion(self):
		"""Returns the ID of the most populous region (province)."""
		data = {}
		for iProvince in range(con.iNumRegions):
			data[iProvince] = 0
		for iLoopPlayer in range(con.iBarbarian + 1):
			apCityList = PyPlayer(iLoopPlayer).getCityList()
			for pCity in apCityList:
				data[pCity.GetCy().plot().getRegionID()] += pCity.getPopulation()
		key = -1
		for key, value in sorted(data.iteritems(), key=lambda (k,v): (v,k)):
			pass
		return key
	
	
	def getIcon(self, bVal):
		"""Returns a green check mark if bVal is True, or a red cross if bVal is False."""
		if bVal:
			return u"%c" %(CyGame().getSymbolID(FontSymbols.POWER_CHAR) + 14)
		else:
			return u"%c" %(CyGame().getSymbolID(FontSymbols.POWER_CHAR) + 15)


	def getUHVHelp(self, iPlayer, iGoal):
		"""Returns an array of help strings used by the Victory Screen table."""
		
		aHelp = []
		pPlayer = gc.getPlayer(iPlayer)
		
		# the info is outdated or irrelevant once the goal has been accomplished or failed
		if sd.getGoal(iPlayer, iGoal) == 1:
			aHelp.append(self.getIcon(True) + localText.getText("TXT_KEY_VICTORY_GOAL_ACCOMPLISHED", ()))
			return aHelp
		elif sd.getGoal(iPlayer, iGoal) == 0:
			aHelp.append(self.getIcon(False) + localText.getText("TXT_KEY_VICTORY_GOAL_FAILED", ()))
			return aHelp
		
		return aHelp
	