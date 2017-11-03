from BasePageClass import BasePageClass
from classes.Components.BTVComponentClass import BTVComponentClass
from classes.Components.ContextMenuComponentClass import *
from classes.Components.SwitcherComponentClass import *
from classes.Components.TableComponentClass import *
from classes.Components.MeasureComponentClass import *
from classes.Components.PieLegendComponentClass import *
from classes.Components.QuicklinkTimeRangeComponentClass import *
from classes.Components.PieComponentClass import *
from classes.Components.SummaryBarComponentClass import *
from classes.Components.SearchComponentClass import *
from classes.Components.MenuComponentClass import *
from classes.Components.CollapseChartsComponentClass import *
from classes.Components.QuickTrendsComponentClass import *
from classes.Components.DropdownComponentClass import *
from classes.Components.TimeRangeComponentClass import *
from classes.Components.TreeComponentClass import *
from classes.Components.WorkflowStartComponent import *


class TrendingMonitoringPageClass(BasePageClass):
    def __init__(self, driver):
        '''
        Constructor
        '''
        self.driver = driver

        self.switcher = SwitcherComponentClass()
        self.table = TableComponentClass()
        self.quiklinkTimeRange = QuicklinkTimeRangeComponentClass()
        self.menu = MenuComponentClass()
        self.collapseCharts = CollapseChartsComponentClass()
        self.quicktrends = QuickTrendsComponentClass()
        self.dropdown = DropdownComponentClass()
        self.timeBar = TimeRangeComponentClass()

        self.multiDropdown = MulitpleDropdownComponentClass()
        self.calendar = CalendarComponentClass()
        self.tree = TreeComponentClass(driver)
        self.wfstart=WorkflowStartComponentClass()


        # Common Components
        BasePageClass.__init__(self, driver)