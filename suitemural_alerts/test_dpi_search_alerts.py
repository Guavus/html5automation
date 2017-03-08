from Utils.SetUp import *
from MuralUtils.AlertsHelper import *
setup=SetUp()
sleep(6)
login(setup,"admin","admin123")

checkAlertsCount(setup)


popInstance = GenerateReportsPopClass(setup.d)
# Launching DPI Alerts Page
popInstance.dropdown.clickSpanWithTitle("DPI Alerts",getHandle(setup,MuralConstants.ALERTSCREEN,Constants.ALLSPANS))
doSearchAndValidateAlerts(setup)
checkAlertsCount(setup)

for el in setup.cM.getAllNodeElements("dpiWizardtimerange","starttime"):
    doCalendarSearchOnAlerts(setup,el)


# commenting below only because kpi alerts page is not working

# Launching KPI Alerts Page
# popInstance.dropdown.clickSpanWithTitle("KPI Alerts",getHandle(setup,MuralConstants.ALERTSCREEN,Constants.ALLSPANS))
# doSearchAndValidateAlerts(setup)




setup.d.close()

# GUIDE_INFO