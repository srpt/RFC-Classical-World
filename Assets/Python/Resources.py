# Dynamic resources - based on Rhye's and Fall of Civilizations
# rewritten by edead

from CvPythonExtensions import *
import CvUtil
import Consts as con
from StoredData import sd
from RFCUtils import utils

# globals
gc = CyGlobalContext()
localText = CyTranslator()


class Resources:


	def createResource(self, iX, iY, iBonus, textKey="TXT_KEY_MISC_DISCOVERED_NEW_RESOURCE"):
		"""Creates a bonus resource and alerts the plot owner"""
		
		if gc.getMap().plot(iX,iY).getBonusType(-1) == -1 or iBonus == -1: # only proceed if the bonus isn't already there or if we're removing the bonus
			if iBonus == -1:
				iBonus = gc.getMap().plot(iX,iY).getBonusType(-1) # for alert
				gc.getMap().plot(iX,iY).setBonusType(-1)
			else:
				gc.getMap().plot(iX,iY).setBonusType(iBonus)
				
			iOwner = gc.getMap().plot(iX,iY).getOwner()
			if iOwner >= 0 and textKey != -1: # only show alert to the tile owner
				city = gc.getMap().findCity(iX, iY, iOwner, TeamTypes.NO_TEAM, True, False, TeamTypes.NO_TEAM, DirectionTypes.NO_DIRECTION, CyCity())
				if not city.isNone():
					szText = localText.getText(textKey, (gc.getBonusInfo(iBonus).getTextKey(), city.getName(), gc.getPlayer(iOwner).getCivilizationAdjective(0)))
					CyInterface().addMessage(iOwner, False, con.iDuration, szText, "AS2D_DISCOVERBONUS", InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, gc.getBonusInfo(iBonus).getButton(), ColorTypes(con.iWhite), iX, iY, True, True)


	def removeResource(self, iX, iY, textKey="TXT_KEY_MISC_EVENT_RESOURCE_EXHAUSTED"):
		"""Removes a bonus resource and alerts the plot owner"""
		
		self.createResource(iX, iY, -1, textKey)


	def checkTurn(self, iGameTurn):
		
		return


	def onTechAcquired(self, iTech):
		pass


	def onSetPlayerAlive(self, argsList):
		'Set Player Alive Event'
		iPlayer, bNewValue = argsList
		
		iHuman = utils.getHumanID()
		if iPlayer == iHuman: 
			return
			
		return

#setImprovementType(ImprovementType eNewValue)
#setPlotType(PlotType eNewValue, BOOL bRecalculate, BOOL bRebuildGraphics)
#setTerrainType(TerrainType eNewValue, BOOL bRecalculate, BOOL bRebuildGraphics)