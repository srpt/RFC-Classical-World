# Religions

from CvPythonExtensions import *
import CvUtil
import Consts as con
from CvMainInterface import CvMainInterface
from PyHelpers import PyPlayer
from StoredData import sd
from RFCUtils import utils

# globals
gc = CyGlobalContext()
localText = CyTranslator()


class Religions:


#######################################
### Main methods (Event-Triggered) ###
#####################################


	def setup(self):
		
		# Piety
		for iPlayer in range(con.iNumPlayers):
			if con.tBirth[iPlayer] <= con.iStartYear and gc.getPlayer(iPlayer).getStateReligion() > 0:
				iBasePiety = self.calcBasePiety(iPlayer)
				if iBasePiety < 40: iBasePiety = 40
				sd.setBasePiety(iPlayer, iBasePiety)
				sd.setPiety(iPlayer, iBasePiety)


	def eventApply7624(self, popupReturn):
		"""Holy war popup event."""
		iPlayer = utils.getCaliphController()
		targetList = utils.getHolyWarTargets(iPlayer)
		if popupReturn.getButtonClicked() < len(targetList):
			tTarget = targetList[popupReturn.getButtonClicked()]
			CyInterface().addMessage(iPlayer, False, con.iDuration, localText.getText("TXT_KEY_HOLY_WAR_CALLED", (gc.getPlayer(iPlayer).getName(), gc.getPlayer(tTarget[0]).getCivilizationDescription(0))), "AS2D_DECLAREWAR", InterfaceMessageTypes.MESSAGE_TYPE_MAJOR_EVENT, "", ColorTypes(con.iRed), -1, -1, False, False)
			sd.setVal('iLastHolyWarTurn', gc.getGame().getGameTurn())
			sd.setVal('iHolyWarTarget', tTarget[0])


	def eventApply7625(self, popupReturn):
		"""Holy war call."""
		iHuman = utils.getHumanID()
		if popupReturn.getButtonClicked() == 0: # YES
			gc.getTeam(gc.getPlayer(iHuman).getTeam()).declareWar(sd.getVal('iHolyWarTarget'), False, -1)
			sd.changePiety(iHuman, max(5, (100 - sd.getPiety(iHuman)) / 5))
		else:
			sd.changePiety(iHuman, min(-10, -(sd.getPiety(iHuman) * 2 / 5)))
		CvMainInterface().updateGameDataStrings()


	def eventApply7626(self, popupReturn):
		"""Persecution popup event."""
		iUnitX, iUnitY, iUnitID = sd.getPersecutionData()
		religionList = sd.getPersecutionReligions()
		utils.doPersecution(iUnitX, iUnitY, iUnitID, religionList[popupReturn.getButtonClicked()])


	def changePiety(self, iPlayer, iChange):
		
		if iPlayer < con.iNumPlayers:
			iPiety = sd.getPiety(iPlayer)
			if iPiety >= 0:
				iPreviousPiety = iPiety
				iPiety += iChange
				sd.setPiety(iPlayer, iPiety)


	def checkTurn(self, iGameTurn):
		
		iHuman = utils.getHumanID()
		
		# Piety rise/decay
		if iGameTurn % utils.getTurns(5) == 1:
			for iPlayer in range(con.iNumPlayers):
				if gc.getPlayer(iPlayer).isAlive():
					iBasePiety = self.calcBasePiety(iPlayer)
					sd.setBasePiety(iPlayer, iBasePiety)
					iPiety = sd.getPiety(iPlayer)
					if iPiety < 0:
						sd.setPiety(iPlayer, iBasePiety)
					elif iPiety > iBasePiety:
						self.changePiety(iPlayer, -1)
					elif iPiety < iBasePiety:
						self.changePiety(iPlayer, min(5, (iBasePiety + 1) / (iPiety + 1)))
			# Piety effects
			#for iPlayer in range(con.iNumPlayers):
				#if gc.getPlayer(iPlayer).isAlive():
					#self.doPietyEffects(iPlayer)
					
		return


	def spreadReligion(self, city, iReligion, textKey=False):
		
		if city is None or city.isNone():
			return -1
		
		# do not spread the religion if the city already has it, or the owner is using Persecution civic
		if city.isHasReligion(iReligion):
			return -1
			
		city.setHasReligion(iReligion, True, True, True)
		
		return True


	def removeReligion(self, city, iReligion):
		
		if city is None: return -1
		elif city.isNone(): return -1
		elif not city.isHasReligion(iReligion): return -1
		
		city.setHasReligion(iReligion, False, True, True)
		return True


	def onPlayerChangeStateReligion(self, argsList):
		'Player changes his state religion'
		iPlayer, iNewReligion, iOldReligion = argsList
		
		if iPlayer >= con.iNumPlayers: return
		
		pPlayer = gc.getPlayer(iPlayer)
		iBasePiety = self.calcBasePiety(iPlayer)
		sd.setBasePiety(iPlayer, iBasePiety)
		sd.setPiety(iPlayer, iBasePiety)
		
		
		# reset diplomatic penalty from persecution
		for iLoopPlayer in range(con.iNumPlayers):
			if gc.getPlayer(iLoopPlayer).isAlive() and iLoopPlayer != iPlayer:
				pPlayer.AI_setAttitudeExtra(iLoopPlayer, 0)


	def calcBasePiety(self, iPlayer):
		"""Calculates base piety level for a given player."""
		
		iPiety = 0
		
		return min(100, iPiety)


	def onBuildingBuilt(self, iPlayer, iBuilding):
		
		return


	def onTechAcquired(self, iTech, iPlayer):
		
		if iPlayer >= con.iNumPlayers: return
		
		return


	def makePilgrim(self):
		"""Generate a pilgrim at a random city."""
		
		# make a list of eligible players, count each player several times depending on piety
		playerList = []
		for iPlayer in range(con.iNumPlayers):
			pPlayer = gc.getPlayer(iPlayer)
			iPiety = sd.getPiety(iPlayer)
			if pPlayer.isAlive() and iPiety > 20:
				for i in range(iPiety/10 - 1):
					playerList.append(iPlayer)
		
		if len(playerList) > 1:
		
			# determine the recipient
			iRandNum = gc.getGame().getSorenRandNum(len(playerList), 'Random Player')
			iPlayer = playerList[iRandNum]
			pPlayer = gc.getPlayer(iPlayer)
			
			pCity = utils.getRandomCity(iPlayer)
			tCoords = utils.getPilgrimageSite(iPlayer)
			
			# make the pilgrim
			if pCity != -1:
				if pCity.getX() != tCoords[0] and pCity.getY() != tCoords[1]:
					pPlayer.initUnit(con.iPilgrim, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
					szText = localText.getText("TXT_KEY_MINOR_EVENT_PILGRIM_ARRIVED", (pCity.getName(), gc.getMap().plot(tCoords[0],tCoords[1]).getPlotCity().getName()))
					CyInterface().addMessage(iPlayer, False, con.iDuration, szText, "AS2D_RELIGION_CONVERT", InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, gc.getUnitInfo(con.iPilgrim).getButton(), ColorTypes(con.iGreen), pCity.getX(), pCity.getY(), True, True)


	def onChangeWar(self, argsList):
		bIsWar, iTeam, iRivalTeam = argsList
		
		if iTeam >= con.iNumPlayers or iRivalTeam >= con.iNumPlayers: return
		
		bSameReligion = False
		if gc.getPlayer(iTeam).getStateReligion() == gc.getPlayer(iRivalTeam).getStateReligion():
			bSameReligion = True
		
		return


	def onCityRazed(self, argsList):
		city, iPlayer = argsList
		
		if iPlayer >= con.iNumPlayers: return
		
		iStateReligion = gc.getPlayer(iPlayer).getStateReligion()
		
		# apply diplomatic penalty
		for iReligion in range(con.iNumReligions):
			if city.isHasReligion(iReligion):
				for iLoopPlayer in range(con.iNumPlayers):
					pLoopPlayer = gc.getPlayer(iLoopPlayer)
					if iLoopPlayer != iPlayer and pLoopPlayer.isAlive() and pLoopPlayer.getStateReligion() == iReligion:
						pLoopPlayer.AI_changeAttitudeExtra(iPlayer, -1)


	def onCityAcquired(self, argsList):
		iPreviousOwner, iNewOwner, city, bConquest, bTrade = argsList
		
		pNewOwner = gc.getPlayer(iNewOwner)
		iStateReligion = pNewOwner.getStateReligion()
		
		# Make sure stupid AI civs don't switch religions if they capture their first city
		if bConquest and pNewOwner.getNumCities() <= 1 and not pNewOwner.isHuman() and iStateReligion > 0:
			if not city.isHasReligion(iStateReligion):
				city.setHasReligion(iStateReligion, True, True, True)


	def onCityAcquiredAndKept(self, argsList):
		'City Acquired and Kept'
		iOwner, city, bMassacre = argsList
		
		pOwner = gc.getPlayer(iOwner)
		iStateReligion = pOwner.getStateReligion()
		
		return


	def onUnitSpreadReligionAttempt(self, argsList):
		'Unit tries to spread religion to a city'
		pUnit, iReligion, bSuccess = argsList
		
		return


	def onUnitBuilt(self, argsList):
		'Unit Completed'
		pCity, pUnit = argsList
		
		iPlayer = pCity.getOwner()
		if iPlayer >= con.iNumPlayers: return