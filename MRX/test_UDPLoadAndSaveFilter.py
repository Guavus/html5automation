from Utils.SetUp import *
from classes.Pages.MRXScreens.UDScreenClass import *
from MRXUtils.MRXConstants import *
from classes.Pages.ExplorePageClass import *
from MRXUtils import UDHelper
from MRXUtils import SegmentHelper

try:
    import MRX.DeleteSegment
    newFilterDetails=ConfigManager().getNodeElements("savenewfilter","filter")

    setup = SetUp()
    login(setup, Constants.USERNAME, Constants.PASSWORD)
    udScreenInstance = UDScreenClass(setup.d)
    exploreHandle = getHandle(setup, MRXConstants.ExploreScreen)
    udScreenInstance.explore.exploreList.launchModule(exploreHandle, "WORKFLOWS")
    udScreenInstance.wfstart.launchScreen("Distribution", getHandle(setup, MRXConstants.WFSCREEN))
    time.sleep(5)

    for k, filterDetail in newFilterDetails.iteritems():
        timeRangeFromPopup=''
        measureFromPopup=''
        overWriteFlag=True
        UDHelper.clearFilter(setup,MRXConstants.UDSCREEN)

        ########################################## Apply Filter ########################################################

        timeRangeFromPopup, measureFromPopup = UDHelper.setQuickLink_Measure(setup, udScreenInstance, k)
        SegmentHelper.clickOnfilterIcon(setup,MRXConstants.UDSCREEN,'nofilterIcon')

        expected_filter = {}
        expected_filter = UDHelper.setUDPFilters(udScreenInstance, setup, k)
        udScreenInstance.clickButton("Apply", getHandle(setup, MRXConstants.UDPPOPUP, MuralConstants.ALLBUTTONS))
        isError(setup)
        screenTooltipData = UDHelper.getUDPFiltersToolTipData(MRXConstants.UDSCREEN, setup)
        udpFilterFromScreen_1 = UDHelper.getUDPFiltersFromScreen(MRXConstants.UDSCREEN,setup)
        checkEqualDict(expected_filter, screenTooltipData, message="Verify Filters Selections",doSortingBeforeCheck=True)

        ############################################ Save Filter########################################################

        h=getHandle(setup,MRXConstants.UDSCREEN,'filterArea')
        h['filterArea']['toggleicon'][0].click()
        udScreenInstance.multiDropdown.domultipleSelectionWithNameWithoutActiveDropDown(getHandle(setup,MRXConstants.UDSCREEN,'filterArea'),'Save New Filter',0,parent="filterArea", child="multiSelectDropDown")
        filterDetailFromUI,msg=UDHelper.saveNewFilter(setup,MRXConstants.SNFPOPUP,udScreenInstance,filterDetail)
        if filterDetail['button']=='Save':
            expected_detail = [filterDetail['filtername'], filterDetail['default']]
            checkEqualAssert(expected_detail,filterDetailFromUI,message='Verify Entered detail for Save New filter')

        ############################################ Verify new added Filter############################################

        h = getHandle(setup, MRXConstants.UDSCREEN, 'filterArea')
        h['filterArea']['toggleicon'][0].click()
        udScreenInstance.multiDropdown.domultipleSelectionWithNameWithoutActiveDropDown(getHandle(setup, MRXConstants.UDSCREEN, 'filterArea'), 'Load Filter', 0, parent="filterArea",child="multiSelectDropDown")
        UDHelper.verifySaveFilterFromLoadFilter(setup, udScreenInstance, MRXConstants.LFPOPUP,filterDetail)

        ######################################### Load Filter ##########################################################

        UDHelper.clearFilter(setup,MRXConstants.UDSCREEN)
        filterFromScreen= UDHelper.getUDPFiltersFromScreen(MRXConstants.UDSCREEN, setup)
        checkEqualAssert(MRXConstants.NO_FILTER,filterFromScreen,message='Verify that an applied filter can be removed by pressing the "x" present in the filter bar just below Edit Filter option',testcase_id='MKR-1806')

        if filterDetail['button']=='Save':
            h = getHandle(setup, MRXConstants.UDSCREEN, 'filterArea')
            h['filterArea']['toggleicon'][0].click()
            udScreenInstance.multiDropdown.domultipleSelectionWithNameWithoutActiveDropDown(getHandle(setup, MRXConstants.UDSCREEN, 'filterArea'), 'Load Filter', 0, parent="filterArea",child="multiSelectDropDown")
            UDHelper.loadFilterFormSaveFilter(setup,MRXConstants.LFPOPUP, filterDetail)

            # screenHandle=getHandle(setup, MRXConstants.UDSCREEN, 'time_measure')
            # timeRangeFromScreen = str(screenHandle['time_measure']['span'][0].text).strip()
            # measureFromScreen = udScreenInstance.dropdown.getSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.UDSCREEN, "allselects"))

            # checkEqualAssert(timeRangeFromPopup, timeRangeFromScreen,message='After load filter verify timerange value on screen '+msg+' (Part of mention TC)',testcase_id='MKR-1801')
            # checkEqualAssert(measureFromPopup, measureFromScreen,message='After load filter verify measure value on screen '+msg+' (Part of mention TC)',testcase_id='MKR-1801')
            udpFilterFromScreen_2 = UDHelper.getUDPFiltersFromScreen(MRXConstants.UDSCREEN, setup)
            checkEqualDict(udpFilterFromScreen_1, udpFilterFromScreen_2, message="Verify that a user can re-apply any saved filter "+msg,doSortingBeforeCheck=True,testcase_id='MKR-1801')

            ############################################### Check Default Filter #######################################

            UDHelper.clearFilter(setup, MRXConstants.UDSCREEN)
            UDHelper.checkDefaultFilter(setup,udScreenInstance,MRXConstants.ExploreScreen,filterDetail,udpFilterFromScreen_1)
    setup.d.close()

    for k, filterDetail in newFilterDetails.iteritems():
        if filterDetail['default']=='1'and filterDetail['button']=='Save':
            setup = SetUp()
            login(setup, Constants.USERNAME, Constants.PASSWORD)
            udScreenInstance = UDScreenClass(setup.d)
            exploreHandle = getHandle(setup, MRXConstants.ExploreScreen)
            udScreenInstance.explore.exploreList.launchModule(exploreHandle, "WORKFLOWS")
            udScreenInstance.wfstart.launchScreen("Distribution", getHandle(setup, MRXConstants.WFSCREEN))
            time.sleep(5)
            UDHelper.removeAndVerifyDefaultFilter(setup, udScreenInstance, MRXConstants.UDSCREEN, MRXConstants.ExploreScreen,filterDetail)
            setup.d.close()
            break

    import MRX.UDPDeleteSaveFilter

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    resultlogger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()
