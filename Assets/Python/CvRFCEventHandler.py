from CvPythonExtensions import *
import CvUtil
import CvEventManager
import PyHelpers

from StoredData import sd
from RFCUtils import utils
import Consts as con
import Resources
import Religions
import CityNameManager
import RiseAndFall
import Barbs
import AIWars
import Victory
import Stability
import Plague
import Communications
import DynamicCivs
import Companies
import Titles
import DataLoader
import UnitArtStyler
import BugTimer

gc = CyGlobalContext()

if gc.getMap().getMapScriptName(): # Baldyr: loads stored data on module reload
	sd.load()

PyPlayer = PyHelpers.PyPlayer
PyGame = PyHelpers.PyGame()
PyInfo = PyHelpers.PyInfo

iNumPlayers = con.iNumPlayers
iHuman = utils.getHumanID()

class CvRFCEventHandler:

	def __init__(self, eventManager):
		
		self.lastRegionID = -1
		self.bStabilityOverlay = False
		self.EventKeyDown = 6
		self.EventKeyUp = 7
		self.eventManager = eventManager
		
		# initialize base class
		eventManager.addEventHandler("GameStart", self.onGameStart)
		eventManager.addEventHandler("OnLoad", self.onLoadGame)
		eventManager.addEventHandler("OnPreSave", self.onPreSave)
		eventManager.addEventHandler("BeginGameTurn", self.onBeginGameTurn)
		eventManager.addEventHandler("EndGameTurn", self.onEndGameTurn)
		eventManager.addEventHandler("BeginPlayerTurn", self.onBeginPlayerTurn)
		eventManager.addEventHandler("EndPlayerTurn", self.onEndPlayerTurn)
		eventManager.addEventHandler("firstContact", self.onFirstContact)
		eventManager.addEventHandler("cityAcquired", self.onCityAcquired)
		eventManager.addEventHandler("cityAcquiredAndKept", self.onCityAcquiredAndKept)
		eventManager.addEventHandler("cityRazed", self.onCityRazed)
		eventManager.addEventHandler("cityBuilt", self.onCityBuilt)
		eventManager.addEventHandler("combatResult", self.onCombatResult)
		eventManager.addEventHandler("buildingBuilt", self.onBuildingBuilt)
		eventManager.addEventHandler("projectBuilt", self.onProjectBuilt)
		eventManager.addEventHandler("techAcquired", self.onTechAcquired)
		eventManager.addEventHandler("religionSpread", self.onReligionSpread)
		eventManager.addEventHandler("unitSpreadReligionAttempt", self.onUnitSpreadReligionAttempt)
		eventManager.addEventHandler("playerChangeStateReligion", self.onPlayerChangeStateReligion)
		eventManager.addEventHandler("vassalState", self.onVassalState)
		eventManager.addEventHandler("changeWar", self.onChangeWar)
		eventManager.addEventHandler("unitBuilt", self.onUnitBuilt)
		eventManager.addEventHandler("revolution", self.onRevolution)
		eventManager.addEventHandler("setPlayerAlive", self.onSetPlayerAlive)
		eventManager.addEventHandler("greatPersonBorn", self.onGreatPersonBorn)
		eventManager.addEventHandler("kbdEvent", self.onKbdEvent)		
		
		self.rnf = RiseAndFall.RiseAndFall()
		self.cnm = CityNameManager.CityNameManager()
		self.res = Resources.Resources()
		self.rel = Religions.Religions()
		self.barb = Barbs.Barbs()
		self.aiw = AIWars.AIWars()
		self.vic = Victory.Victory()
		self.sta = Stability.Stability()
		self.pla = Plague.Plague()
		self.com = Communications.Communications()
		self.dc = DynamicCivs.DynamicCivs()
		self.corp = Companies.Companies()
		self.tit = Titles.Titles()


	def onGameStart(self, argsList):
		'Called at the start of the game'
		
		DataLoader.setup()
		sd.setup()
		self.rnf.setup()
		self.sta.setup()
		self.aiw.setup()
		#self.pla.setup()
		self.dc.setup()
		self.rel.setup()
		#self.tit.setup()
		sd.save()
		
		
		# update unit art styles of independents
		for iLoopPlayer in range(con.iIndependent1, con.iIndependent4 + 1):
			unitList = PyPlayer(iLoopPlayer).getUnitList()
			for pUnit in unitList:
				UnitArtStyler.updateUnitArt(pUnit)

		return 0


	def onPreSave(self, argsList):
		'called before a game is actually saved'
		sd.save() # pickle & save script data


	def onLoadGame(self, argsList):
		sd.load() # load & unpickle script data
		return 0


	def onBeginGameTurn(self, argsList):
		'Called at the beginning of the end of each turn'
		iGameTurn = argsList[0]
		
		# timer = BugTimer.Timer('onBeginGameTurn')
		
		# print ("iGameTurn", iGameTurn)
		# self.printDebug(iGameTurn)
		
		self.rnf.checkTurn(iGameTurn)
		self.res.checkTurn(iGameTurn)
		self.barb.checkTurn(iGameTurn)
		self.rel.checkTurn(iGameTurn)
		self.sta.checkTurn(iGameTurn)
		self.aiw.checkTurn(iGameTurn)
		#self.pla.checkTurn(iGameTurn)
		self.com.checkTurn(iGameTurn)
		self.corp.checkTurn(iGameTurn)
		
		
		
		# Refugees
		"""if sd.getVal('tRazedCityData'):
			map = CyMap()
			tRazedCityData = sd.getVal('tRazedCityData') #(city.getNameKey(), city.getX(), city.getY())
			sd.delVal('tRazedCityData')
			cityList = []
			for x in range(tRazedCityData[0]-12, tRazedCityData[0]+12, 1):
				if x >= 0 and x < map.getGridWidth():
					for y in range(tRazedCityData[1]-12, tRazedCityData[1]+12, 1):
						if y >= 0 and y < map.getGridHeight():
							plot = map.plot(x, y)
							if plot.isCity():
								targetCity = plot.getPlotCity()
								cityList.append(targetCity)
			if cityList:
				targetCity = cityList[gc.getGame().getSorenRandNum(len(cityList), 'Random city')]
				gc.getPlayer(targetCity.getOwner()).initTriggeredData(gc.getInfoTypeForString("EVENTTRIGGER_REFUGEES"), True, targetCity.getID(), targetCity.getX(), targetCity.getY(), -1, -1, -1, -1, -1, -1, tRazedCityData[2])"""
		
		


	def onEndGameTurn(self, argsList):
		'Called at the end of the end of each turn'
		iGameTurn = argsList[0]
		
		self.sta.checkImplosion(iGameTurn)


	def onBeginPlayerTurn(self, argsList):
		'Called at the beginning of a players turn'
		iGameTurn, iPlayer = argsList
		
		# timer = BugTimer.Timer('onBeginPlayerTurn')
		
		pPlayer = gc.getPlayer(iPlayer)
		
		if self.rnf.getDeleteMode(0) != -1:
			self.rnf.deleteMode(iPlayer)
		
		#self.pla.checkPlayerTurn(iGameTurn, iPlayer)
		
		#srpt only check human player victory
		if pPlayer.isAlive() and iPlayer == utils.getHumanID():
		#if pPlayer.isAlive() and iPlayer < iNumPlayers:
			self.vic.checkPlayerTurn(iGameTurn, iPlayer)
			sd.setLastTurnAlive(iPlayer, iGameTurn)
			if pPlayer.getNumCities() > 0:
				self.sta.updateBaseStability(iGameTurn, iPlayer)
		
		# timer.log()


	def onEndPlayerTurn(self, argsList):
		'Called at the end of a players turn'
		iGameTurn, iPlayer = argsList


	def onFirstContact(self, argsList):
		'Contact'
		iTeamX,iHasMetTeamY = argsList


	def onBuildingBuilt(self, argsList):
		'Building Completed'
		city, iBuildingType = argsList
		
		iOwner = city.getOwner()
		if iOwner < iNumPlayers:
			self.sta.onBuildingBuilt(iOwner, iBuildingType, city)
			self.rel.onBuildingBuilt(iOwner, iBuildingType)
			if iOwner == iHuman:
				self.vic.onBuildingBuilt(iOwner, iBuildingType, city)
		if iBuildingType == con.iLegalistSchool:
			for iReligion in range(con.iNumReligions):
				city.setHasReligion(iReligion, True, False)


	def onProjectBuilt(self, argsList):
		'Project Completed'
		pCity, iProjectType = argsList


	def onTechAcquired(self, argsList):
		'Tech Acquired'
		iTechType, iTeam, iPlayer, bAnnounce = argsList
		
		if iPlayer < iNumPlayers:
			if iPlayer == iHuman:
				self.vic.onTechAcquired(iTechType, iPlayer) # Ottomans
			self.res.onTechAcquired(iTechType)
			self.rel.onTechAcquired(iTechType, iPlayer)
			if gc.getPlayer(iPlayer).isAlive() and gc.getGame().getGameTurn() > getTurnForYear(con.tBirth[iPlayer]):
				self.sta.onTechAcquired(iTechType, iPlayer)


	def onReligionSpread(self, argsList):
		'Religion Has Spread to a City'
		iReligion, iOwner, pSpreadCity = argsList


	def onCityBuilt(self, argsList):
		'City Built'
		city = argsList[0]
		
		iOwner = city.getOwner()
		player = gc.getPlayer(iOwner)
		
		self.cnm.assignName(city)
		#self.tit.onCityBuilt(city)
		
		#Rhye - delete culture of barbs and minor civs to prevent weird unhappiness
		pCurrent = gc.getMap().plot(city.getX(), city.getY())
		for i in range(con.iNumTotalPlayers - iNumPlayers):
			iMinorCiv = i + iNumPlayers
			pCurrent.setCulture(iMinorCiv, 0, True)
		pCurrent.setCulture(con.iBarbarian, 0, True)
		
		if iOwner < iNumPlayers:
			utils.spreadMajorCulture(iOwner, city.getX(), city.getY())
			if player.getNumCities() < 2:
				player.AI_updateFoundValues(False); # fix for settler maps not updating after 1st city is founded


	def onCityRazed(self, argsList):
		'City Razed'
		city, iPlayer = argsList
		
		iPreviousOwner = city.getOwner()
		if iPreviousOwner == iPlayer and city.getPreviousOwner() != -1:
			iPreviousOwner = city.getPreviousOwner()
		
		self.sta.onCityRazed(iPreviousOwner)
		#self.pla.onCityRazed(argsList)
		self.rel.onCityRazed(argsList)
		
		# Refugees
		sd.setVal('tRazedCityData', (city.getX(), city.getY(), city.getNameKey()))


	def onCityAcquired(self, argsList):
		'City Acquired'
		iPreviousOwner, iNewOwner, city, bConquest, bTrade = argsList
		pNewOwner = gc.getPlayer(iNewOwner)
		
		# timer = BugTimer.Timer('onCityAcquired')
		
		self.cnm.renameCity(city, iNewOwner)
		self.rnf.checkCapitalsOnCapture(city, iNewOwner) # edead: free capital move for the AI
		
		if iNewOwner < iNumPlayers:
			utils.spreadMajorCulture(iNewOwner, city.getX(), city.getY())
			#self.pla.onCityAcquired(iPreviousOwner, iNewOwner, city)
			self.dc.onCityAcquired(argsList)
		
		self.sta.onCityAcquired(iPreviousOwner, iNewOwner, city, bConquest, bTrade)
		self.rel.onCityAcquired(argsList)
		if iPreviousOwner == iHuman or iNewOwner == iHuman:
			self.vic.onCityAcquired(argsList)
		self.corp.onCityAcquired(argsList)
		#self.tit.onCityAcquired(argsList)
		
		# Move the palace to historical backup capital
		if iPreviousOwner < iNumPlayers:
			if (city.getX(), city.getY()) == con.tCapitals[iPreviousOwner]:
				self.rnf.moveCapital(con.tBackupCapitals[iPreviousOwner], iPreviousOwner, True)


	def onCityAcquiredAndKept(self, argsList):
		'City Acquired and Kept'
		iOwner,city,bMassacre = argsList
		
		iVictims = self.rel.onCityAcquiredAndKept(argsList) # massacre
		if iOwner == iHuman:
			self.vic.onCityAcquiredAndKept(argsList)


	def onCombatResult(self, argsList):
		iHuman = utils.getHumanID()
		pWinningUnit, pLosingUnit, pAttackingUnit = argsList
		if pWinningUnit.getOwner() == iHuman:
			self.vic.onCombatResult(argsList) # Mamluks
		self.sta.onCombatResult(argsList)
		self.rnf.immuneMode(argsList)
		# srpt Slavery
		iWinningPlayer = pWinningUnit.getOwner()
		iLosingPlayer = pLosingUnit.getOwner()
		iAttackingPlayer = pAttackingUnit.getOwner()
		pWinningPlayer = gc.getPlayer(pWinningUnit.getOwner())
		pLosingPlayer = gc.getPlayer(pLosingUnit.getOwner())
		pAttackingPlayer = gc.getPlayer(pAttackingUnit.getOwner())
		
		#land only
		if not (gc.getMap().plot(pWinningUnit.getX(),pWinningUnit.getY()).isWater()):
			
			if (pWinningPlayer.getCivics(2) != con.iSlavery):
				return
			
			cLosingUnit = PyHelpers.PyInfo.UnitInfo(pLosingUnit.getUnitType())
			
			if (con.iRam < pLosingUnit.getUnitType() < con.iLevySpearman):
				return
			
			# Only enslave land units!!
			if (cLosingUnit.getDomainType() == gc.getInfoTypeForString("DOMAIN_LAND")):
				iThreshold = 20
				iRandom = gc.getGame().getSorenRandNum(100, 'capture chance')
				if pLosingUnit.getOwner() == con.iBarbarian:
					iThreshold += 10
				if iWinningPlayer == iAttackingPlayer:
					iThreshold += 10
					#print ("pWinningPlayer.getCapitalCity().productionLeft()", pWinningPlayer.getCapitalCity().productionLeft())
					if (iRandom < iThreshold):
						#if iWinningPlayer != iHuman and pWinningPlayer.getCapitalCity().isProductionBuilding() and pWinningPlayer.getCapitalCity().productionLeft() > 45:
							#self.aiSlaveFunction(iWinningPlayer, (pLosingUnit.getX(), pLosingUnit.getY()))
						#else:
						if gc.getMap().plot(pLosingUnit.getX(), pLosingUnit.getY()).getNumDefenders(iLosingPlayer) <= 1:
							pPlot = gc.getMap().plot(pLosingUnit.getX(), pLosingUnit.getY())
							if pPlot.getTerrainType() != con.iWasteland and pPlot.getFeatureType() != con.iJungle:
								#pNewUnit = pWinningPlayer.initUnit(con.iSlave, pLosingUnit.getX(), pLosingUnit.getY(), UnitAITypes.UNITAI_SLAVE, DirectionTypes.DIRECTION_SOUTH)
								pNewUnit = utils.makeUnit(con.iSlave, iWinningPlayer, (pLosingUnit.getX(), pLosingUnit.getY()),1)
								CyInterface().addMessage(pWinningPlayer.getID(),True,15,CyTranslator().getText("You have enslaved an enemy unit", ()),'SND_REVOLTEND',1,'Art/Units/Slave/button_slave.dds',ColorTypes(8),pLosingUnit.getX(),pLosingUnit.getY(),True,True)
								CyInterface().addMessage(pLosingPlayer.getID(),True,15,CyTranslator().getText("Your unit has been enslaved", ()),'SND_REVOLTEND',1,'Art/Units/Slave/button_slave.dds',ColorTypes(7),pLosingUnit.getX(),pLosingUnit.getY(),True,True)
								pNewUnit.finishMoves()
						else:
							pPlot = gc.getMap().plot(pWinningUnit.getX(), pWinningUnit.getY())
							if pPlot.getTerrainType() != con.iWasteland and pPlot.getFeatureType() != con.iJungle:
								#pNewUnit = pWinningPlayer.initUnit(con.iSlave, pWinningUnit.getX(), pWinningUnit.getY(), UnitAITypes.UNITAI_SLAVE, DirectionTypes.DIRECTION_SOUTH)
								pNewUnit = utils.makeUnit(con.iSlave, iWinningPlayer, (pWinningUnit.getX(), pWinningUnit.getY()),1)
								CyInterface().addMessage(pWinningPlayer.getID(),True,15,CyTranslator().getText("You have enslaved an enemy unit", ()),'SND_REVOLTEND',1,'Art/Units/Slave/button_slave.dds',ColorTypes(8),pWinningUnit.getX(),pWinningUnit.getY(),True,True)
								CyInterface().addMessage(pLosingPlayer.getID(),True,15,CyTranslator().getText("Your unit has been enslaved", ()),'SND_REVOLTEND',1,'Art/Units/Slave/button_slave.dds',ColorTypes(7),pWinningUnit.getX(),pWinningUnit.getY(),True,True)
								pNewUnit.finishMoves()
						
					
				elif iAttackingPlayer == iLosingPlayer:
					if (iRandom < iThreshold):
						#if iWinningPlayer != iHuman and pWinningPlayer.getCapitalCity().isProductionBuilding():
							#self.aiSlaveFunction(iWinningPlayer, (pWinningUnit.getX(), pWinningUnit.getY()))
						#else:
						pPlot = gc.getMap().plot(pWinningUnit.getX(), pWinningUnit.getY())
						if pPlot.getTerrainType() != con.iWasteland and pPlot.getFeatureType() != con.iJungle:
							#pNewUnit = pWinningPlayer.initUnit(con.iSlave, pWinningUnit.getX(), pWinningUnit.getY(), UnitAITypes.UNITAI_SLAVE, DirectionTypes.DIRECTION_SOUTH)
							pNewUnit = utils.makeUnit(con.iSlave, iWinningPlayer, (pWinningUnit.getX(), pWinningUnit.getY()),1)
							pNewUnit.finishMoves()
							CyInterface().addMessage(pWinningPlayer.getID(),True,15,CyTranslator().getText("TXT_KEY_UP_ENSLAVE_WIN", ()),'SND_REVOLTEND',1,'Art/Units/Slave/button_slave.dds',ColorTypes(8),pWinningUnit.getX(),pWinningUnit.getY(),True,True)
							CyInterface().addMessage(pLosingPlayer.getID(),True,15,CyTranslator().getText("TXT_KEY_UP_ENSLAVE_LOSE", ()),'SND_REVOLTEND',1,'Art/Units/Slave/button_slave.dds',ColorTypes(7),pWinningUnit.getX(),pWinningUnit.getY(),True,True)
							pNewUnit.finishMoves()


	def onPlayerChangeStateReligion(self, argsList):
		'Player changes his state religion'
		iPlayer, iNewReligion, iOldReligion = argsList
		
		if iPlayer < iNumPlayers:
			self.rel.onPlayerChangeStateReligion(argsList)
			self.dc.onPlayerChangeStateReligion(argsList)
			self.corp.onPlayerChangeStateReligion(argsList)
			#self.tit.onPlayerChangeStateReligion(argsList)
			if iPlayer == iHuman:
				self.vic.onPlayerChangeStateReligion(argsList)


	def onVassalState(self, argsList):
		'Vassal State'
		iMaster, iVassal, bVassal = argsList
		
		self.dc.onVassalState(argsList)


	def onChangeWar(self, argsList):
		'War Status Changes'
		bIsWar, iTeam, iRivalTeam = argsList
		
		if bIsWar and iTeam < iNumPlayers and iRivalTeam < iNumPlayers:
			self.rel.onChangeWar(argsList)


	def onUnitSpreadReligionAttempt(self, argsList):
		'Unit tries to spread religion to a city'
		pUnit, iReligion, bSuccess = argsList
		
		self.rel.onUnitSpreadReligionAttempt(argsList)
		if pUnit.getOwner() == iHuman:
			self.vic.onUnitSpreadReligionAttempt(argsList) # Oman


	def onUnitBuilt(self, argsList):
		'Unit Completed'
		pCity, pUnit = argsList
		
		iPlayer = pUnit.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		iUnitType = pUnit.getUnitType()
		
		self.rel.onUnitBuilt(argsList)
		
		# Qin UP
		bNoReligion = True
		for iReligion in range(con.iNumReligions):
			if pCity.isHasReligion(iReligion):
				bNoReligion = False
				break
		if bNoReligion == True:
			pUnit.setExperience(pUnit.getExperience() + 3, -1)
		
		# Update UnitArtStyle for independents
		if iPlayer >= con.iNumPlayers and iPlayer != con.iBarbarian:
			UnitArtStyler.updateUnitArt(pUnit)
		

	def onRevolution(self, argsList):
		'Called at the start of a revolution'
		iPlayer = argsList[0]
		
		if iPlayer < iNumPlayers:
			self.dc.onRevolution(iPlayer)


	def onSetPlayerAlive(self, argsList):
		'Set Player Alive Event'
		iPlayer, bNewValue = argsList
		
		if iPlayer < iNumPlayers:
			#self.tit.onSetPlayerAlive(argsList)
			self.res.onSetPlayerAlive(argsList)


	def onGreatPersonBorn(self, argsList):
		'Unit Promoted'
		pUnit, iPlayer, pCity = argsList
		if pUnit.getOwner() == iHuman:
			self.vic.onGreatPersonBorn(argsList) # Chauhan


	def onKbdEvent(self, argsList):
		'keypress handler - return 1 if the event was consumed'
		
		eventType, key, mx, my, px, py = argsList
		
		# Rhye: RFC debug
		iHuman = utils.getHumanID()
		
		if eventType == self.EventKeyDown and key == InputTypes.KB_N and self.eventManager.bAlt:
			print("ALT-N")
			self.printStabilityDebug()
		
		if eventType == self.EventKeyDown and key == InputTypes.KB_C and self.eventManager.bAlt and self.eventManager.bShift:
			print("SHIFT-ALT-C") #picks a dead civ so that autoplay can be started with game.AIplay xx
			iDebugDeadCiv = iMauryans
			#gc.getTeam(gc.getPlayer(iDebugDeadCiv).getTeam()).setHasTech(con.iCalendar, True, iDebugDeadCiv, False, False)
			utils.makeUnit(con.iSpearman, iDebugDeadCiv, (0,0), 1)
			gc.getGame().setActivePlayer(iDebugDeadCiv, False)
			gc.getPlayer(iDebugDeadCiv).setPlayable(True)
		
		if eventType == self.EventKeyDown and key == InputTypes.KB_Q and self.eventManager.bAlt and self.eventManager.bShift:
			print("SHIFT-ALT-Q") #enables squatting
			self.rnf.setCheatMode(True);
			CyInterface().addMessage(iHuman, True, con.iDuration, "EXPLOITER!!! ;)", "", 0, "", ColorTypes(con.iRed), -1, -1, True, True)
		
		# Baldyr: Stability Cheat
		if self.rnf.getCheatMode() and key == InputTypes.KB_S and self.eventManager.bAlt and self.eventManager.bShift:
			print("SHIFT-ALT-S") #boosts stability by +10 for the human player
			sd.setStability(iHuman, sd.getStability(iHuman)+10)
		
		# edead: SoI Debug
		if eventType == self.EventKeyDown and key == InputTypes.KB_N and self.eventManager.bCtrl and gc.getGame().isDebugMode():
			print("CTRL-N")
			utils.launchDebugScreen()
		
		# edead: province highlight
		if eventType == self.EventKeyDown and px >= 0 and py >= 0 and int(key) == 45 and self.eventManager.bCtrl and not self.eventManager.bAlt:
			
			plot = gc.getMap().plot(px,py)
			iActivePlayer = gc.getGame().getActivePlayer()
			iActiveTeam = gc.getPlayer(iActivePlayer).getTeam()
			iRegionID = plot.getRegionID()
			
			# do not show provinces of unrevealed tiles
			if not plot.isRevealed(iActiveTeam, False) and not gc.getGame().isDebugMode():
				return
			
			# do not redraw if already drawn
			if self.lastRegionID == iRegionID:
				return
			
			map = CyMap()
			engine = CyEngine()
			
			# clear the highlight
			engine.clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_HIGHLIGHT_PLOT)
			#engine.clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS)
			
			# cache the plot's coords
			self.lastRegionID = plot.getRegionID()
			
			# select an appriopriate color
			if plot.isWater():
				return
			else:
				iLevel = utils.getRegionStabilityLevel(iHuman, iRegionID)
				if iLevel == 4:
					color = gc.getColorInfo(gc.getInfoTypeForString("COLOR_HIGHLIGHT_CORE")).getColor()
				elif iLevel == 3:
					color = gc.getColorInfo(gc.getInfoTypeForString("COLOR_HIGHLIGHT_BORDER")).getColor()
				elif iLevel == 2:
					color = gc.getColorInfo(gc.getInfoTypeForString("COLOR_HIGHLIGHT_CONTESTED")).getColor()
				elif iLevel == 1:
					color = gc.getColorInfo(gc.getInfoTypeForString("COLOR_HIGHLIGHT_OUTSIDE")).getColor()
				else:
					color = gc.getColorInfo(gc.getInfoTypeForString("COLOR_HIGHLIGHT_FOREIGN")).getColor()
			
			# apply the highlight
			for i in range(map.numPlots()):
				plot = map.plotByIndex(i)
				if plot.getRegionID() == iRegionID and (gc.getGame().isDebugMode() or plot.isRevealed(iActiveTeam, False)):
					engine.fillAreaBorderPlot(plot.getX(), plot.getY(), color, AreaBorderLayers.AREA_BORDER_LAYER_HIGHLIGHT_PLOT)
			
			return
		
		# clear all hightlights
		if (eventType == self.EventKeyUp and self.eventManager.bCtrl) or (eventType == self.EventKeyDown):
			CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_HIGHLIGHT_PLOT)
			self.lastRegionID = -1


	def printDebug(self, iGameTurn):
		
		# if (iGameTurn % 50 == 1):
			# self.printEmbassyDebug()
		# if (iGameTurn % 20 == 0):
			# self.printPlotsDebug()
		if (iGameTurn % 10 == 0): 
			self.printStabilityDebug()


	def printStabilityDebug(self):
		print ("Stability")
		for iCiv in range(iNumPlayers):
			if (gc.getPlayer(iCiv).isAlive()):
				print ("Base:", sd.getBaseStabilityLastTurn(iCiv), "Modifier:", sd.getStability(iCiv)-sd.getBaseStabilityLastTurn(iCiv), "Total:", sd.getStability(iCiv), "civic", gc.getPlayer(iCiv).getCivics(5), gc.getPlayer(iCiv).getCivilizationDescription(0))
			else:
				print ("dead", iCiv)
		for i in range(con.iNumStabilityParameters):
			print("Parameter", i, utils.getStabilityParameters(i))
		for i in range(iNumPlayers):
			print (gc.getPlayer(i).getCivilizationShortDescription(0), "PLOT OWNERSHIP ABROAD:", self.sta.getOwnedPlotsLastTurn(i), "CITY OWNERSHIP LOST:", self.sta.getOwnedCitiesLastTurn(i) )
