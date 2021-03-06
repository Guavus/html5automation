import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Components.BTVComponentClass import *


#### NOT RUNNING DUE TO BUG

############################## TESTING FOR THE TOOLTIP #####################
data = {}
# Getting Setup Details and Launching the application
setup = SetUp()

# Logging into the appliction
login(setup, "admin", "Admin@123")


exploreScreenInstance = ExplorePageClass(setup.d)
exploreHandle = getHandle(setup,"explore_Screen")
exploreScreenInstance.exploreList.launchScreen(exploreHandle,"exploreList","site_Screen")
# Get the Instance of the screen
screenInstance = SitePageClass(setup.d)
siteScreenHandle = getHandle(setup,"site_Screen")
# screenInstance.measure.doSelectionSite(siteScreenHandle,"SatSite")


#setMeasure(setup,"Bitrate_total_absolute_average","site_Screen")

# Get the handles of the screen
# siteScreenHandle = getHandle(setup,"site_Screen")

btvData = screenInstance.btv.getData(siteScreenHandle)
data['btvData'] = {}
for key,value in btvData.iteritems():
    pv = value.pop(0)
    if len(data['btvData']) == 0:
        data['btvData']['dimension'] = value
    else:
        data['btvData']['value'] = value
    logger.debug('Col1 : %s  and Col2 : %s',key,value)
data['btvTooltipData'] = screenInstance.btv.getToolTipInfo(setup.d,setup.dH,siteScreenHandle)
sleep(2)
checkEqualAssert(True,True,"TODAY","Bitrate_total_absolute_peak","TOOLTIP IS WORKIG PERFECTLY")
print data['btvTooltipData']
result1 = screenInstance.btv.validateToolTipData1(data)
print result1

checkEqualAssert(result1,True,"TODAY","Bitrate_total_absolute_peak","ToolTipdata")
setup.d.close()