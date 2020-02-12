# Dynamic Civs - edead

from CvPythonExtensions import *
import CvUtil
import PyHelpers
import Consts as con
from StoredData import sd
from RFCUtils import utils

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
PyInfo = PyHelpers.PyInfo
localText = CyTranslator()
iNumPlayers = con.iNumPlayers


class DynamicCivs:


	def __init__(self):
		
		self.defaultNames = {
			
		}
		
		self.vassalNames = {
			
		}
		
		self.respawnedNames = {
			
		}
		
		self.empireNames = {
			
		}
		

	def setCivDesc(self, iCiv, sName, sShort="", sAdj=""):
	
		gc.getPlayer(iCiv).setCivName(localText.getText(sName, ()), localText.getText(sShort, ()), localText.getText(sAdj, ()))


	def setup(self):
		
		return

	def checkName(self, iPlayer):
	
		return
	
		if iPlayer >= iNumPlayers: return
	
		bVassal = utils.isAVassal(iPlayer)
		pPlayer = gc.getPlayer(iPlayer)
		bRespawned = sd.getCivStatus(iPlayer)
		iReligion = pPlayer.getStateReligion()
		capital = gc.getPlayer(iPlayer).getCapitalCity()
		
		# respawn > capital > religion > empire > vassal
		
		# by respawns
		if bRespawned and iPlayer in self.respawnedNames:
			
			return
		
		# by vassalage
		if bVassal and iPlayer in self.vassalNames:
			szName = self.vassalNames[iPlayer]
		else:
			szName = self.defaultNames[iPlayer]

		# by status (empires)
		if not bVassal:
			iCivic = pPlayer.getCivics(0)
			if iPlayer in self.empireNames:
				minCities = 8 # 8/6
				if iPlayer in []: minCities = 4 # 4/3
				elif iPlayer in []: minCities = 16 # 16/12
				if pPlayer.getNumCities() >= minCities:
					if pPlayer.getNumCities() >= (minCities * 3 / 4):
						szName = self.empireNames[iPlayer]
		
		self.setCivDesc(iPlayer, szName)


	def onCivRespawn(self, iPlayer):
		
		pPlayer = gc.getPlayer(iPlayer)
		
		# change balance modifiers for respawned civs - use modifiers of a civ that spawns around the same time for convenience
		
		sd.setCivStatus(iPlayer, 1)
		
		
		self.setCivDesc(iPlayer, self.respawnedNames[iPlayer])
			
				
	def onVassalState(self, argsList):
		iMaster, iVassal, bVassal = argsList
		self.checkName(iVassal)
	
	
	def onPlayerChangeStateReligion(self, argsList):
		iPlayer, iNewReligion, iOldReligion = argsList
		self.checkName(iPlayer)


	def onRevolution(self, iPlayer):
		self.checkName(iPlayer)
		

	def onCityAcquired(self, argsList):
		iPreviousOwner, iNewOwner, city, bConquest, bTrade = argsList
		
		self.checkName(iPreviousOwner)
		self.checkName(iNewOwner)