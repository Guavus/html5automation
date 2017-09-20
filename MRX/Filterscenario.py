from Utils.SetUp import *
from classes.Components.TimeRangeComponentClass import *
from classes.Pages.MRXScreens.SegmentScreenClass import *
from MRXUtils.MRXConstants import *
from MRXUtils import SegmentHelper
from MRXUtils import UDHelper
from Utils.AvailableMethod import *
import json



def measureAndDimensionAfterMapping(tableMap):
    query={}
    query['data']=[]
    query['table_header']=[]
    count=0
    dimensions = ConfigManager().getNodeElements("segment_Table_Mapping", "dimension")

    for i in range(len(tableMap['header'])):
        if dimensions.has_key(str(tableMap['header'][i])):
            query['table_header'].append(dimensions[str(tableMap['header'][i])]['backEnd_ID'])

    # for k, row_value in tableMap['rows'].iteritems():
    #     if len(row_value)==9:
    #         row_value.pop()
    #         row_value.pop()
    #         query['data'].append(row_value)
    #         count=count+1

    for row_value in tableMap['rows']:
        if len(row_value)==9:
            row_value.pop()
            row_value.pop()
            query['data'].append(row_value)
            count=count+1

    query['count']=count
    return query


def fireBV(dataFromUI,method,table_name,sort_property,testcase=''):
    sleep(1)
    dataFromUI_For_Dump=deepcopy(dataFromUI)
    dataFromUI_For_Dump['measure']=[]
    dataFromUI_For_Dump['dimension'] = []
    dataFromUI_For_Dump['method']=method
    dataFromUI_For_Dump['table_name']=table_name
    dataFromUI_For_Dump['testcase']=testcase
    dataFromUI_For_Dump['sort_property']=sort_property

    import time
    dataFromUI_For_Dump['id'] = str(time.time()).split('.')[0]

    logger.info("Going to dump info from UI for Backend Data validation ::" + str(dataFromUI_For_Dump))
    with open("DumpFileForSegment.txt",mode='a') as fs:
        fs.write(json.dumps(dataFromUI_For_Dump))
        fs.write(" __DONE__" + "\n")


try:

    setup = SetUp()
    login(setup,Constants.USERNAME,Constants.PASSWORD)
    segmentScreenInstance = SegmentScreenClass(setup.d)
    exploreHandle = getHandle(setup, MRXConstants.ExploreScreen)
    segmentScreenInstance.explore.exploreList.launchModule(exploreHandle, "USER DISTRIBUTION")
    UDHelper.clearFilter(setup, MRXConstants.UDSCREEN)
    udpFilterFromUDRScreenWithoutAnyFilter = UDHelper.getUDPFiltersFromScreen(MRXConstants.UDSCREEN, setup)

    exploreHandle = getHandle(setup, MRXConstants.ExploreScreen)
    segmentScreenInstance.explore.exploreList.launchModule(exploreHandle,"SEGMENTS")
    segmentScreenHandle = getHandle(setup, MRXConstants.SEGMENTSCREEN)
    global_filter = setup.cM.getNodeElements("segmentFilter", "filter")
    filtericonlocation_y = getHandle(setup, MRXConstants.SEGMENTSCREEN, 'filterArea')['filterArea']['nofilterIcon'][0].location['y']

    exportIconLocation_y= setup.d.execute_script("return document.getElementsByClassName('exportImg dropdown-toggle')")[0].location['y']
    exportIconLocation_x =setup.d.execute_script("return document.getElementsByClassName('exportImg dropdown-toggle')")[0].location['x']
    handle = getHandle(setup, MRXConstants.SEGMENTSCREEN, 'table')
    tablelocation_y = handle['table']['HEADERROW'][0].location['y']
    tablelocation_x = handle['table']['HEADERROW'][8].location['x']
    checkEqualAssert(True, tablelocation_y > filtericonlocation_y,message='Verify that there is a "Filter" button just above the Segment table...... table(y) ='+str(tablelocation_y)+'filterIcon(y) '+str(filtericonlocation_y),testcase_id='MKR-1675')
    checkEqualAssert(True,tablelocation_y > exportIconLocation_y and (exportIconLocation_x - tablelocation_x)<200,message='Verify that there is "Export Table Data" option just above the segments tables.....table(y) ='+str(tablelocation_y)+' ExportIcon(y)= '+str(exportIconLocation_y)+ ' table(x) ='+str(tablelocation_x)+' ExportIcon(x)= '+str(exportIconLocation_x ),testcase_id='MKR-1710')
    ########################################################################################################################

    tableHandle = getHandle(setup, MRXConstants.SEGMENTSCREEN, 'table')
    tableData = segmentScreenInstance.table.getTableData1(tableHandle,length=20)
    dataFromUI=measureAndDimensionAfterMapping(tableData)

    fireBV(dataFromUI,AvailableMethod.Top_Row,MRXConstants.SEGMENT_TABLE_AT_BACKEND,sort_property="created")

    #segmentScreenInstance.cm.clickButton('Refresh', getHandle(setup, MRXConstants.SEGMENTSCREEN, 'allbuttons'))
    tableMap1 = segmentScreenInstance.table.getTableDataMap(tableHandle, driver=setup)
    click_status=SegmentHelper.clickOnfilterIcon(setup,MRXConstants.SEGMENTSCREEN,'nofilterIcon')
    expected = SegmentHelper.setSegmentFilter(setup,segmentScreenInstance,k=1)
    segmentScreenInstance.cm.clickButton("Apply Filters", getHandle(setup, MRXConstants.FILTERSCREEN, 'allbuttons'))
    isError(setup)

    handle=getHandle(setup,MRXConstants.SEGMENTSCREEN,'table')
    columnValueFromTable=segmentScreenInstance.table.getColumnValueFromTable(0,handle)
    SegmentHelper.clickOnfilterIcon(setup, MRXConstants.SEGMENTSCREEN, 'filterClearIcon')
    filterFromScreenAfterClear = SegmentHelper.getGlobalFiltersFromScreen(MRXConstants.SEGMENTSCREEN,segmentScreenInstance, setup, flag=False)

    tableHandle = getHandle(setup, MRXConstants.SEGMENTSCREEN, 'table')
    tableMap2 = segmentScreenInstance.table.getTableDataMap(tableHandle, driver=setup)

    checkEqualAssert(str(udpFilterFromUDRScreenWithoutAnyFilter).strip(), str(filterFromScreenAfterClear).strip(),message='Verify No filter text on Segment Screen',testcase_id='MKR-3450')

    checkEqualAssert(len(tableMap1['rows']),len(tableMap2['rows']),message='Verify Cross (X) functionality on Segment Screen :: Before any filter total segment ='+str(len(tableMap1['rows']))+' After Clear Applied Filter total Segment ='+str(len(tableMap2['rows'])),testcase_id='MKR-1690')
    #h=getHandle(setup,MRXConstants.SEGMENTSCREEN,'filterArea')
    #checkEqualAssert(0,len(h['filterArea']['filterClearIcon']),message='Verify Cross (X) functionality on Segment Screen',testcase_id='MKR-1690')


########################################################################################################################
    click_status = SegmentHelper.clickOnfilterIcon(setup, MRXConstants.SEGMENTSCREEN, 'nofilterIcon')
    SegmentHelper.setSegmentFilter(setup, segmentScreenInstance, k=2)
    segmentScreenInstance.cm.clickButton("Apply Filters", getHandle(setup, MRXConstants.FILTERSCREEN, 'allbuttons'))
    isError(setup)

    handle = getHandle(setup, MRXConstants.SEGMENTSCREEN, 'table')
    columnValueFromTable1 = segmentScreenInstance.table.getColumnValueFromTable(0, handle)
    checkEqualAssert(True,len(columnValueFromTable)>=len(columnValueFromTable1),message='Segmment Filter apply sucessfully')
    checkEqualAssert(True,set(columnValueFromTable1)<set(columnValueFromTable),message='Verify Table Data after apply Segment Filter ='+str(global_filter[str(2)]['segmentname'])+'  Before Filter = '+str(columnValueFromTable)+' After Filter = '+str(columnValueFromTable1),testcase_id='MKR-1682')
    SegmentHelper.clickOnfilterIcon(setup, MRXConstants.SEGMENTSCREEN, 'filterClearIcon')


########################################################################################################################
    click_status = SegmentHelper.clickOnfilterIcon(setup, MRXConstants.SEGMENTSCREEN, 'nofilterIcon')
    SegmentHelper.setSegmentFilter(setup, segmentScreenInstance, k=3)
    segmentScreenInstance.cm.clickButton("Apply Filters", getHandle(setup, MRXConstants.FILTERSCREEN, 'allbuttons'))
    isError(setup)

    handle =getHandle(setup, MRXConstants.SEGMENTSCREEN, 'table')
    column_1_ValueFromTable = segmentScreenInstance.table.getColumnValueFromTable(1, handle)
    flag_user=True
    min=int(str(global_filter[str(3)]['user']).split('::')[0].strip())
    max=int(str(global_filter[str(3)]['user']).split('::')[1].strip())
    for i in range(len(column_1_ValueFromTable)):
        if int(str(column_1_ValueFromTable[i]).strip())>max or int(str(column_1_ValueFromTable[i]).strip())<min:
            flag_user=False
            break

    checkEqualAssert(True,flag_user,message='Verify Table Data after apply #Users Filter, Value must be Greater than Equal to '+str(min)+ ' Less than Equal to '+str(max)+ 'Value form table = '+str(column_1_ValueFromTable),testcase_id='MKR-1683')
    SegmentHelper.clickOnfilterIcon(setup, MRXConstants.SEGMENTSCREEN, 'filterClearIcon')

########################################################################################################################
    click_status = SegmentHelper.clickOnfilterIcon(setup, MRXConstants.SEGMENTSCREEN, 'nofilterIcon')
    expected_Createdon=SegmentHelper.setSegmentFilter(setup, segmentScreenInstance, k=4)
    segmentScreenInstance.cm.clickButton("Apply Filters", getHandle(setup, MRXConstants.FILTERSCREEN, 'allbuttons'))
    isError(setup)
    handle = getHandle(setup, MRXConstants.SEGMENTSCREEN, 'table')
    column_6_ValueFromTable = segmentScreenInstance.table.getColumnValueFromTable(6, handle)
    Createdon=str(global_filter[str(4)]['createdon']).split('::')[0].strip()
    ChoosedDate=str(global_filter[str(4)]['createdon']).split('::')[1].strip()
    Createdon_flag=True

    epochTime=getepoch(str(ChoosedDate),MRXConstants.TIMEZONEOFFSET, "%Y %B %d %H %M")
    column_6_valueIn_epoch=[]
    for i in range(len(column_6_ValueFromTable)):
        column_6_valueIn_epoch.append(getepoch(str(column_6_ValueFromTable[i]).strip(), MRXConstants.TIMEZONEOFFSET,MRXConstants.TIMEPATTERN))
    if Createdon=='1':
        for j in range(len(column_6_valueIn_epoch)):
            if long(column_6_valueIn_epoch[j])<long(epochTime):
                Createdon_flag=False
                break
    elif Createdon=='2':
        for j in range(len(column_6_valueIn_epoch)):
            if long(column_6_valueIn_epoch[j]) >= long(epochTime):
                Createdon_flag = False
                break

    checkEqualAssert(True,Createdon_flag,message='Verify Table Data after apply Created on Filter, filter applied = '+str(expected_Createdon['Created on'])+' Value form table = '+str(column_6_ValueFromTable),testcase_id='MKR-1688')
    SegmentHelper.clickOnfilterIcon(setup, MRXConstants.SEGMENTSCREEN, 'filterClearIcon')

########################################################################################################################
    click_status = SegmentHelper.clickOnfilterIcon(setup, MRXConstants.SEGMENTSCREEN, 'nofilterIcon')
    expected_Status=SegmentHelper.setSegmentFilter(setup, segmentScreenInstance, k=5)
    segmentScreenInstance.cm.clickButton("Apply Filters", getHandle(setup, MRXConstants.FILTERSCREEN, 'allbuttons'))
    isError(setup)

    handle = getHandle(setup, MRXConstants.SEGMENTSCREEN, 'table')
    column_2_ValueFromTable = segmentScreenInstance.table.getColumnValueFromTable(2, handle)
    flag_status=True

    for i in range(len(column_2_ValueFromTable)):
        if not str(column_2_ValueFromTable[i]).strip() in expected_Status['Status'][0]:
            flag_status=False
            break

    checkEqualAssert(True,flag_status,message='Verify Table Data after apply Status Filter, filter applied = '+str(expected_Status['Status'])+' Value form table = '+str(column_2_ValueFromTable),testcase_id='MKR-1684')
    SegmentHelper.clickOnfilterIcon(setup, MRXConstants.SEGMENTSCREEN, 'filterClearIcon')

########################################################################################################################
    click_status = SegmentHelper.clickOnfilterIcon(setup, MRXConstants.SEGMENTSCREEN, 'nofilterIcon')
    expected_Source=SegmentHelper.setSegmentFilter(setup, segmentScreenInstance, k=6)
    segmentScreenInstance.cm.clickButton("Apply Filters", getHandle(setup, MRXConstants.FILTERSCREEN, 'allbuttons'))
    isError(setup)

    handle = getHandle(setup, MRXConstants.SEGMENTSCREEN, 'table')
    column_3_ValueFromTable = segmentScreenInstance.table.getColumnValueFromTable(3, handle)
    flag_source=True

    for i in range(len(column_3_ValueFromTable)):
        if not str(column_3_ValueFromTable[i]).strip() in expected_Source['Source'][0]:
            flag_source=False
            break

    checkEqualAssert(True,flag_source,message='Verify Table Data after apply Source Filter, filter applied = '+str(expected_Source['Source'])+' Value form table = '+str(column_3_ValueFromTable),testcase_id='MKR-1685')
    SegmentHelper.clickOnfilterIcon(setup, MRXConstants.SEGMENTSCREEN, 'filterClearIcon')

#######################################################################################################################
    click_status=SegmentHelper.clickOnfilterIcon(setup,MRXConstants.SEGMENTSCREEN,'nofilterIcon')
    expected_Owner = SegmentHelper.setSegmentFilter(setup,segmentScreenInstance,k=7)
    segmentScreenInstance.cm.clickButton("Apply Filters", getHandle(setup, MRXConstants.FILTERSCREEN, 'allbuttons'))
    isError(setup)

    handle=getHandle(setup,MRXConstants.SEGMENTSCREEN,'table')
    column_4_ValueFromTable=segmentScreenInstance.table.getColumnValueFromTable(4,handle)
    flag_owner = True

    for i in range(len(column_4_ValueFromTable)):
        if not expected_Owner['Owner'] in str(column_4_ValueFromTable[i]).strip():
            flag_owner=False
            break

    checkEqualAssert(True,flag_owner,message='Verify Table Data after apply owner Filter, filter applied = '+str(expected_Owner['Owner'])+' Value form table = '+str(column_4_ValueFromTable),testcase_id='MKR-1686')
    SegmentHelper.clickOnfilterIcon(setup, MRXConstants.SEGMENTSCREEN, 'filterClearIcon')

########################################################################################################################
    click_status = SegmentHelper.clickOnfilterIcon(setup, MRXConstants.SEGMENTSCREEN, 'nofilterIcon')
    expected_Access=SegmentHelper.setSegmentFilter(setup, segmentScreenInstance, k=8)
    segmentScreenInstance.cm.clickButton("Apply Filters", getHandle(setup, MRXConstants.FILTERSCREEN, 'allbuttons'))
    isError(setup)

    handle = getHandle(setup, MRXConstants.SEGMENTSCREEN, 'table')
    column_5_ValueFromTable = segmentScreenInstance.table.getColumnValueFromTable(5, handle)
    flag_access=True

    for i in range(len(column_5_ValueFromTable)):
        if not str(column_5_ValueFromTable[i]).strip() in expected_Access['Access'][0]:
            flag_access=False
            break

    checkEqualAssert(True,flag_access,message='Verify Table Data after apply Access Filter, filter applied = '+str(expected_Access['Access'])+' Value form table = '+str(column_5_ValueFromTable),testcase_id='MKR-1687')
    SegmentHelper.clickOnfilterIcon(setup, MRXConstants.SEGMENTSCREEN, 'filterClearIcon')
#######################################################################################################################

    click_status = SegmentHelper.clickOnfilterIcon(setup, MRXConstants.SEGMENTSCREEN, 'nofilterIcon')
    expected_ALL = SegmentHelper.setSegmentFilter(setup, segmentScreenInstance, k=0)
    segmentScreenInstance.cm.clickButton("Apply Filters", getHandle(setup, MRXConstants.FILTERSCREEN, 'allbuttons'))
    isError(setup)

    handle = getHandle(setup, MRXConstants.SEGMENTSCREEN, 'table')

    column_0_ValueFromTableAll = segmentScreenInstance.table.getColumnValueFromTable(0, handle)
    column_1_ValueFromTableAll = segmentScreenInstance.table.getColumnValueFromTable(1, handle)
    column_2_ValueFromTableAll = segmentScreenInstance.table.getColumnValueFromTable(2, handle)
    column_3_ValueFromTableAll = segmentScreenInstance.table.getColumnValueFromTable(3, handle)
    column_4_ValueFromTableAll = segmentScreenInstance.table.getColumnValueFromTable(4, handle)
    column_5_ValueFromTableAll = segmentScreenInstance.table.getColumnValueFromTable(5, handle)
    column_6_ValueFromTableAll = segmentScreenInstance.table.getColumnValueFromTable(6, handle)

    minimum = int(str(global_filter[str(0)]['user']).split('::')[0].strip())
    maximum = int(str(global_filter[str(0)]['user']).split('::')[1].strip())

    CreatedonAll = str(global_filter[str(0)]['createdon']).split('::')[0].strip()
    ChoosedDateAll = str(global_filter[str(0)]['createdon']).split('::')[1].strip()

    epochTimeAll = getepoch(str(ChoosedDateAll), MRXConstants.TIMEZONEOFFSET, "%Y %B %d %H %M")
    column_6_valueIn_epochAll = []
    for i in range(len(column_6_ValueFromTableAll)):
        column_6_valueIn_epochAll.append(getepoch(str(column_6_ValueFromTableAll[i]).strip(), MRXConstants.TIMEZONEOFFSET, MRXConstants.TIMEPATTERN))


    flag_All = True

    for i in range(len(column_0_ValueFromTableAll)):

        if CreatedonAll=='1':
            if (not str(column_5_ValueFromTableAll[i]).strip() in expected_ALL['Access'][0]) and (not str(column_4_ValueFromTableAll[i]).strip() in expected_ALL['Owner'][0]) and (not str(column_3_ValueFromTableAll[i]).strip() in expected_ALL['Source'][0]) and (not str(column_2_ValueFromTableAll[i]).strip() in expected_ALL['Status'][0]) and (not str(column_0_ValueFromTableAll[i]).strip() in expected_ALL['Segment Name'][0]) and (int(str(column_1_ValueFromTableAll[i]).strip()) > maximum or int(str(column_1_ValueFromTableAll[i]).strip()) < minimum )and (long(column_6_valueIn_epochAll[i]) < long(epochTimeAll)):
                flag_All = False
                break
        elif CreatedonAll=='2':
            if (not str(column_5_ValueFromTableAll[i]).strip() in expected_ALL['Access'][0]) and (not str(column_4_ValueFromTableAll[i]).strip() in expected_ALL['Owner'][0]) and (not str(column_3_ValueFromTableAll[i]).strip() in expected_ALL['Source'][0]) and (not str(column_2_ValueFromTableAll[i]).strip() in expected_ALL['Status'][0]) and (not str(column_0_ValueFromTableAll[i]).strip() in expected_ALL['Segment Name'][0]) and (int(str(column_1_ValueFromTableAll[i]).strip()) > maximum or int(str(column_1_ValueFromTableAll[i]).strip()) < minimum ) and (long(column_6_valueIn_epochAll[i]) > long(epochTimeAll)):
                flag_All = False
                break

    checkEqualAssert(True, flag_All, message='Verify Table Data after apply Multiple Filter, Filter applied ='+str(expected_ALL),testcase_id='MKR-1689')
    SegmentHelper.clickOnfilterIcon(setup, MRXConstants.SEGMENTSCREEN, 'filterClearIcon')


    setup.d.close()


except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    resultlogger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved and Exception = %s", r, str(e))
    setup.d.close()
