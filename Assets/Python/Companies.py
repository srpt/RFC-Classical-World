# The Sword of Islam - Companies

from CvPythonExtensions import *
import CvUtil
import PyHelpers
import Consts as con
from StoredData import sd
from RFCUtils import utils
from operator import itemgetter

# globals
gc = CyGlobalContext()
localText = CyTranslator()
PyPlayer = PyHelpers.PyPlayer

iNumPlayers = con.iNumPlayers
iNumTotalPlayers = con.iNumTotalPlayers
iNumCompanies = con.iNumCompanies
tCompaniesBirth = con.tCompaniesBirth
tCompaniesDeath = con.tCompaniesDeath
tCompaniesLimit = con.tCompaniesLimit
lCompanyRegions = con.lCompanyRegions

class Companies:


	def checkTurn(self, iGameTurn):
		
		# Check if it's not too early
		iCompany = iGameTurn % iNumCompanies
		if iGameTurn < getTurnForYear(tCompaniesBirth[iCompany]):
			return
		
		# Check if it's not too late
		if iGameTurn > getTurnForYear(tCompaniesDeath[iCompany]):
			iMaxCompanies = 0
			
		else:
			iMaxCompanies = tCompaniesLimit[iCompany]
		
		# loop through all cities, check the company value for each and add the good ones to a list of tuples (city, value)
		cityValueList = []
		for iPlayer in range(iNumPlayers):
			apCityList = PyPlayer(iPlayer).getCityList()
			for pCity in apCityList:
				city = pCity.GetCy()
				iValue = self.getCityValue(city, iCompany)
				if iValue > 0: 
					cityValueList.append((city, iValue * 10 + gc.getGame().getSorenRandNum(10, 'random bonus')))
				elif city.isHasCorporation(iCompany): # quick check to remove companies
					city.setHasCorporation(iCompany, False, True, True)
		
		# sort cities from highest to lowest value
		cityValueList.sort(key=itemgetter(1), reverse=True)
		
		# count the number of companies
		iCompanyCount = 0
		for iLoopPlayer in range(iNumPlayers):
			if utils.isActive(iLoopPlayer):
				iCompanyCount += gc.getPlayer(iLoopPlayer).countCorporations(iCompany)
		
		# debugText = 'ID: %d, ' %(iCompany)
		# spread the company
		for i in range(len(cityValueList)):
			city = cityValueList[i][0]
			if city.isHasCorporation(iCompany):
				# debugText += '%s:%d(skip), ' %(city.getName(), cityValueList[i][1])
				continue
			if iCompanyCount >= iMaxCompanies and i >= iMaxCompanies: # don't spread to weak cities if the limit was reached
				# debugText += 'limit reached'
				break
			city.setHasCorporation(iCompany, True, True, True)
			# debugText += '%s(OK!), ' %(city.getName())
			break
		# utils.echo(debugText)
		
		# if the limit was exceeded, remove company from the worst city
		if iCompanyCount > iMaxCompanies:
			for i in range(len(cityValueList)-1, 0, -1):
				city = cityValueList[i][0]
				if city.isHasCorporation(iCompany):
					city.setHasCorporation(iCompany, False, True, True)
					break


	def onPlayerChangeStateReligion(self, argsList):
		iPlayer, iNewReligion, iOldReligion = argsList
		
		apCityList = PyPlayer(iPlayer).getCityList()
		for pCity in apCityList:
			city = pCity.GetCy()
			for iCompany in range(iNumCompanies):
				if city.isHasCorporation(iCompany):
					if self.getCityValue(city, iCompany) < 0:
						city.setHasCorporation(iCompany, False, True, True)


	def onCityAcquired(self, argsList):
		iPreviousOwner, iNewOwner, city, bConquest, bTrade = argsList
		
		for iCompany in range(iNumCompanies):
			if city.isHasCorporation(iCompany):
				if self.getCityValue(city, iCompany) < 0:
					city.setHasCorporation(iCompany, False, True, True)


	def getCityValue(self, city, iCompany):
		
		if city is None: return -1
		elif city.isNone(): return -1
		
		iValue = 0
		
		owner = gc.getPlayer(city.getOwner())
		ownerTeam = gc.getTeam(owner.getTeam())
		
		
		
		# geographical requirements
		plot = gc.getMap().plot(city.getX(),city.getY())
		if len(lCompanyRegions[iCompany]) > 0 and plot.getRegionID() not in lCompanyRegions[iCompany]:
			return -1
		
		
		
		
		# resources
		
		# competition
		
		# threshold
		if iValue < 3: return -1
		
		# spread it out
		iValue -= owner.countCorporations(iCompany)
		
		return iValue