# The Sword of Islam - Honorific Titles

from CvPythonExtensions import *
import CvUtil
import PyHelpers
import Consts as con
from StoredData import sd
from RFCUtils import utils

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

class Titles:


	def setup(self):
		
		return


	def checkPlayerTitle(self, iTitle, iPlayer):
		"""Checks if the player is eligible for the given title."""
		
		return


	def onCityAcquired(self, argsList):
		iPreviousOwner, iNewOwner, city, bConquest, bTrade = argsList
		
		return


	def onCityBuilt(self, city):
		
		return


	def onPlayerChangeStateReligion(self, argsList):
		iPlayer, iNewReligion, iOldReligion = argsList
		
		pPlayer = gc.getPlayer(iPlayer)
		pTeam = gc.getTeam(pPlayer.getTeam())
		iStateReligion = pPlayer.getStateReligion()
		
		return


	def onSetPlayerAlive(self, argsList):
		iPlayer, bNewValue = argsList
		
		# remove titles
		if bNewValue == False:
			for iTitle in range(con.iNumTitles):
				pTeam = gc.getTeam(gc.getPlayer(iPlayer).getTeam())
				if pTeam.getProjectCount(iTitle):
					pTeam.changeProjectCount(iTitle, -1)
					for iLoopPlayer in range(con.iNumPlayers):
						if iLoopPlayer != iPlayer:
							self.checkPlayerTitle(iTitle, iLoopPlayer)