# UnitArtStyler by edead
# Works only with the related DLL changes (CvUnit::setArtDefineTag and CvUnitInfo::getArtDefineTag)
# Use to convert unit art of independent units based on the city art style, or province, or w/e

from CvPythonExtensions import *
import Consts as con

gc = CyGlobalContext()

# Unit Art Styles for a particular city/plot Art Style
g_CityArtStyles = (

)

# Unit Art Styles for a particular region (province)
g_RegionArtStyles = {
	#Celtic
	con.rCaledonia 			: "UNIT_ARTSTYLE_CELTIC",
	con.rHibernia 			: "UNIT_ARTSTYLE_CELTIC",
	con.rBritannia 			: "UNIT_ARTSTYLE_CELTIC",
	con.rAquitania 			: "UNIT_ARTSTYLE_CELTIC",
	con.rGaul 				: "UNIT_ARTSTYLE_CELTIC",
	con.rSeptimania 		: "UNIT_ARTSTYLE_CELTIC",
	con.rIberia 			: "UNIT_ARTSTYLE_CELTIC",
	con.rNItaly 			: "UNIT_ARTSTYLE_CELTIC",
	#Greek
	con.rGreece 			: "UNIT_ARTSTYLE_GREEK",
	con.rSicily 			: "UNIT_ARTSTYLE_GREEK",
	con.rSItaly 			: "UNIT_ARTSTYLE_GREEK",
	con.rRhodes 			: "UNIT_ARTSTYLE_GREEK",
	con.rCrete 				: "UNIT_ARTSTYLE_GREEK",
	con.rMacedonia 			: "UNIT_ARTSTYLE_GREEK",
	con.rCyprus 			: "UNIT_ARTSTYLE_GREEK",
	#Persian
	con.rPersia 			: "UNIT_ARTSTYLE_PERSIA",
	con.rArmenia 			: "UNIT_ARTSTYLE_PERSIA",
	con.rMedia 				: "UNIT_ARTSTYLE_PERSIA",
	con.rParthia 			: "UNIT_ARTSTYLE_PERSIA",
	con.rArachosia 			: "UNIT_ARTSTYLE_PERSIA",
	con.rSogdiana 			: "UNIT_ARTSTYLE_PERSIA",
	con.rFerghana 			: "UNIT_ARTSTYLE_PERSIA",
	con.rBactria 			: "UNIT_ARTSTYLE_PERSIA",
	con.rMargiana 			: "UNIT_ARTSTYLE_PERSIA",
	con.rGedrosia 			: "UNIT_ARTSTYLE_PERSIA",
	#India
	con.rSindh 				: "UNIT_ARTSTYLE_INDIA",
	con.rGandhara 			: "UNIT_ARTSTYLE_INDIA",
	con.rPunjab 			: "UNIT_ARTSTYLE_INDIA",
	con.rMagadha 			: "UNIT_ARTSTYLE_INDIA",
	con.rBangala 			: "UNIT_ARTSTYLE_INDIA",
	con.rKalinka 			: "UNIT_ARTSTYLE_INDIA",
	con.rKerala 			: "UNIT_ARTSTYLE_INDIA",
	con.rTamilNadu 			: "UNIT_ARTSTYLE_INDIA",
	con.rAvanti 			: "UNIT_ARTSTYLE_INDIA",
	con.rDeccan 			: "UNIT_ARTSTYLE_INDIA",
	con.rLanka 				: "UNIT_ARTSTYLE_INDIA",
	con.rSaurashtra 		: "UNIT_ARTSTYLE_INDIA",
	con.rAndhra 			: "UNIT_ARTSTYLE_INDIA",
	con.rBharat 			: "UNIT_ARTSTYLE_INDIA",
	#China
	con.rQin 				: "UNIT_ARTSTYLE_CHINA",
	con.rChu 				: "UNIT_ARTSTYLE_CHINA",
	con.rQi 				: "UNIT_ARTSTYLE_CHINA",
	con.rYan 				: "UNIT_ARTSTYLE_CHINA",
	con.rZhao 				: "UNIT_ARTSTYLE_CHINA",
	con.rWei 				: "UNIT_ARTSTYLE_CHINA",
	con.rHan 				: "UNIT_ARTSTYLE_CHINA",
	con.rJin 				: "UNIT_ARTSTYLE_CHINA",
	con.rShu 				: "UNIT_ARTSTYLE_CHINA",
	con.rGansu 				: "UNIT_ARTSTYLE_CHINA",
	con.rWu 				: "UNIT_ARTSTYLE_CHINA",

}

# Conditional Unit Art Styles for a particular region : (iDate, tReligions, eArtStyle)
g_ConditionalArtStyles = {
	#Hellenism
	con.rSeptimania			: (con.iStartYear, [con.iHellenism], "UNIT_ARTSTYLE_GREEK"),
	con.rIberia				: (con.iStartYear, [con.iHellenism], "UNIT_ARTSTYLE_GREEK"),
	con.rNItaly				: (con.iStartYear, [con.iHellenism], "UNIT_ARTSTYLE_GREEK"),
	con.rIllyricum			: (con.iStartYear, [con.iHellenism], "UNIT_ARTSTYLE_GREEK"),
	con.rThrace				: (con.iStartYear, [con.iHellenism], "UNIT_ARTSTYLE_GREEK"),
	con.rAsia				: (con.iStartYear, [con.iHellenism], "UNIT_ARTSTYLE_GREEK"),
	con.rLibya				: (con.iStartYear, [con.iHellenism], "UNIT_ARTSTYLE_GREEK"),
	con.rAfrica				: (con.iStartYear, [con.iHellenism], "UNIT_ARTSTYLE_GREEK"),
	con.rMauretania			: (con.iStartYear, [con.iHellenism], "UNIT_ARTSTYLE_GREEK"),
	con.rMedia				: (con.iStartYear, [con.iHellenism], "UNIT_ARTSTYLE_GREEK"),
	con.rPersia				: (con.iStartYear, [con.iHellenism], "UNIT_ARTSTYLE_GREEK"),
	con.rParthia			: (con.iStartYear, [con.iHellenism], "UNIT_ARTSTYLE_GREEK"),
	con.rArachosia			: (con.iStartYear, [con.iHellenism], "UNIT_ARTSTYLE_GREEK"),
	con.rSogdiana			: (con.iStartYear, [con.iHellenism], "UNIT_ARTSTYLE_GREEK"),
	con.rSindh				: (con.iStartYear, [con.iHellenism], "UNIT_ARTSTYLE_GREEK"),
	con.rGandhara			: (con.iStartYear, [con.iHellenism], "UNIT_ARTSTYLE_GREEK"),
	con.rPunjab				: (con.iStartYear, [con.iHellenism], "UNIT_ARTSTYLE_GREEK"),
	con.rFerghana			: (con.iStartYear, [con.iHellenism], "UNIT_ARTSTYLE_GREEK"),
	con.rBactria			: (con.iStartYear, [con.iHellenism], "UNIT_ARTSTYLE_GREEK"),
	con.rMargiana			: (con.iStartYear, [con.iHellenism], "UNIT_ARTSTYLE_GREEK"),
	con.rCrimea				: (con.iStartYear, [con.iHellenism], "UNIT_ARTSTYLE_GREEK"),
	con.rBaetica			: (con.iStartYear, [con.iHellenism], "UNIT_ARTSTYLE_GREEK"),
	con.rLusitania			: (con.iStartYear, [con.iHellenism], "UNIT_ARTSTYLE_GREEK"),
	con.rGedrosia			: (con.iStartYear, [con.iHellenism], "UNIT_ARTSTYLE_GREEK"),
	con.rMoesia				: (con.iStartYear, [con.iHellenism], "UNIT_ARTSTYLE_GREEK"),
	con.rColchis			: (con.iStartYear, [con.iHellenism], "UNIT_ARTSTYLE_GREEK"),
	#Phoenicians
	con.rAfrica				: (con.iStartYear, [con.iPhoenicianPolytheism], "UNIT_ARTSTYLE_CARTHAGE"),
	con.rIberia				: (con.iStartYear, [con.iPhoenicianPolytheism], "UNIT_ARTSTYLE_CARTHAGE"),
	con.rMauretania			: (con.iStartYear, [con.iPhoenicianPolytheism], "UNIT_ARTSTYLE_CARTHAGE"),
	con.rNumidia			: (con.iStartYear, [con.iPhoenicianPolytheism], "UNIT_ARTSTYLE_CARTHAGE"),
	con.rLibya				: (con.iStartYear, [con.iPhoenicianPolytheism], "UNIT_ARTSTYLE_CARTHAGE"),
	con.rBaetica			: (con.iStartYear, [con.iPhoenicianPolytheism], "UNIT_ARTSTYLE_CARTHAGE"),
	con.rLibya				: (con.iStartYear, [con.iPhoenicianPolytheism], "UNIT_ARTSTYLE_CARTHAGE"),
	con.rLusitania			: (con.iStartYear, [con.iPhoenicianPolytheism], "UNIT_ARTSTYLE_CARTHAGE"),
	#Chinese religions
	con.rTibet				: (con.iStartYear, [con.iConfucianism,con.iTaoism], "UNIT_ARTSTYLE_CHINA"),
	con.rTarim				: (con.iStartYear, [con.iConfucianism,con.iTaoism], "UNIT_ARTSTYLE_CHINA"),
	con.rFerghana			: (con.iStartYear, [con.iConfucianism,con.iTaoism], "UNIT_ARTSTYLE_CHINA"),
	con.rBirma				: (con.iStartYear, [con.iConfucianism,con.iTaoism], "UNIT_ARTSTYLE_CHINA"),
	con.rFunan				: (con.iStartYear, [con.iConfucianism,con.iTaoism], "UNIT_ARTSTYLE_CHINA"),
	con.rAnnam				: (con.iStartYear, [con.iConfucianism,con.iTaoism], "UNIT_ARTSTYLE_CHINA"),
	con.rMalaya				: (con.iStartYear, [con.iConfucianism,con.iTaoism], "UNIT_ARTSTYLE_CHINA"),
	con.rSumatra			: (con.iStartYear, [con.iConfucianism,con.iTaoism], "UNIT_ARTSTYLE_CHINA"),
	con.rJava				: (con.iStartYear, [con.iConfucianism,con.iTaoism], "UNIT_ARTSTYLE_CHINA"),
	con.rBorneo				: (con.iStartYear, [con.iConfucianism,con.iTaoism], "UNIT_ARTSTYLE_CHINA"),
	con.rPhilipines			: (con.iStartYear, [con.iConfucianism,con.iTaoism], "UNIT_ARTSTYLE_CHINA"),
	con.rGoguryeo			: (con.iStartYear, [con.iConfucianism,con.iTaoism], "UNIT_ARTSTYLE_CHINA"),
	con.rMongolianSteppe	: (con.iStartYear, [con.iConfucianism,con.iTaoism], "UNIT_ARTSTYLE_CHINA"),
	con.rBa					: (con.iStartYear, [con.iConfucianism,con.iTaoism], "UNIT_ARTSTYLE_CHINA"),
	con.rMinYue				: (con.iStartYear, [con.iConfucianism,con.iTaoism], "UNIT_ARTSTYLE_CHINA"),
	con.rChampa				: (con.iStartYear, [con.iConfucianism,con.iTaoism], "UNIT_ARTSTYLE_CHINA"),
	con.rNanzhao			: (con.iStartYear, [con.iConfucianism,con.iTaoism], "UNIT_ARTSTYLE_CHINA"),
	con.rAssam				: (con.iStartYear, [con.iConfucianism,con.iTaoism], "UNIT_ARTSTYLE_CHINA"),
	con.rQinghai			: (con.iStartYear, [con.iConfucianism,con.iTaoism], "UNIT_ARTSTYLE_CHINA"),

}


def checkUnitArt(unit):
	"""Checks unit and either updates or resets the ArtDefineTag."""
	if unit:
		if gc.getPlayer(unit.getOwner()).isMinorCiv():
			updateUnitArt(unit)
		else:
			resetUnitArt(unit)

			
def setUnitArt(unit, eUnitArtStyle):
	"""Sets the ArtDefineTag of unit based on eArtStyle (not UnitArtStyle!)."""
	if unit and eUnitArtStyle >= 0:
		unit.setArtDefineTag(gc.getUnitInfo(unit.getUnitType()).getArtDefineTag(0, eUnitArtStyle))


def updateUnitArt(unit):
	"""Updates the ArtDefineTag of unit based on the ArtStyle of its plot or region (province)."""
	if unit:
		plot = unit.plot()
		if plot:
			# base art style from plot art
			eUnitArtStyle = -1
			if plot.getArtStyleType() >= 0 and plot.getArtStyleType() < len(g_CityArtStyles):
				eUnitArtStyle = gc.getInfoTypeForString(g_CityArtStyles[plot.getArtStyleType()])
			# art style based on province
			if plot.getRegionID() in g_RegionArtStyles:
				#print "plot in province"
				eUnitArtStyle = gc.getInfoTypeForString(g_RegionArtStyles[plot.getRegionID()])
			# art style change based on date and religions present in city
			if plot.getRegionID() in g_ConditionalArtStyles:
				if gc.getGame().getGameTurnYear() >= g_ConditionalArtStyles[plot.getRegionID()][0]:
					bFound = True
					if plot.isCity():
						city = plot.getPlotCity()
						bFound = False
						for iReligion in g_ConditionalArtStyles[plot.getRegionID()][1]:
							if city.isHasReligion(iReligion):
								bFound = True
								break
					if bFound:
						eUnitArtStyle = gc.getInfoTypeForString(g_ConditionalArtStyles[plot.getRegionID()][2])
			setUnitArt(unit, eUnitArtStyle)


def updateUnitArtAtPlot(plot):
	"""Updates the ArtDefineTag of all units at a given plot."""
	if plot:
		for i in range(plot.getNumUnits()):
			updateUnitArt(plot.getUnit(i))


def resetUnitArt(unit):
	"""Resets the ArtDefineTag, bringing back the default civ-based UnitArtStyle."""
	if unit:
		unit.setArtDefineTag("")
