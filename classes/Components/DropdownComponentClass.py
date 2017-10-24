from BaseComponentClass import BaseComponentClass
from Utils.ConfigManager import ConfigManager
import time
from Utils.logger import *
from selenium.webdriver.common.keys import *
import random

class DropdownComponentClass(BaseComponentClass):

    def __init__(self):
        BaseComponentClass.__init__(self)
        self.configmanager = ConfigManager()

    def doSelection(self,h,value,parent,child=""):
        try:
            self.set(value, h[parent][child])
            return True
        except Exception as e:
            return e

    def set(self, value, handle):
        try:
            l = len(handle)
            h = handle[len(handle)-1]
        except:
            h = handle


        for ele in h.find_elements_by_xpath(".//*"):
            if str(ele.text).strip().strip('\n').strip() == value:
                try:
                    logger.debug("Setting DropDown to %s",value)
                    ele.click()
                    selected_option = str(self.get(h).strip().strip('\n').strip())
                    logger.debug("DropDown Selected to %s",selected_option)
                    return selected_option
                except Exception as e:
                    logger.error("Exception found while selecting %s on DropDown",value)
                    return "Exception : "+str(e)
        currentValue = str(self.get(h).strip().strip('\n').strip())
        logger.error("Option : %s not present in dropdown and returning the currentValue selected = %s",value,currentValue)
        return currentValue


    def setByIndex(self, indexToBeSelected, handle):
        try:
            l = len(handle)
            h = handle[len(handle)-1]
        except:
            h = handle

        elements = h.find_elements_by_xpath(".//*")
        for i in range(len(elements)):
            if i == indexToBeSelected:
                try:
                    logger.debug("Selecting DropDown with Index = %s and Text = %s",str(i),str(elements[i].text))
                    elements[i].click()
                    logger.debug("DropDown with Index = %s and Text = %s is selected",str(i),str(elements[i].text))
                    return str(self.get(h).strip().strip('\n').strip())
                except Exception as e:
                    logger.error("Exception found while selecting DropDown with Index = %s and Text = %s = %s",str(i),str(elements[i].text),str(e))
                    return e
        currentValue = self.get(h)
        logger.error("Option with index %s not present in dropdown and returning the currentValue selected = %s",str(indexToBeSelected),currentValue)
        return currentValue

    def randomSet(self, handle):
        try:
            l = len(handle)
            h = handle[len(handle)-1]
        except:
            h = handle

        elements = h.find_elements_by_xpath(".//*")
        try:
            indexToBeSelected = random.randint(0,len(elements)-1)
        except ValueError or Exception as e:
            logger.error("Exception found (No options available) for selection in DropDown = %s",str(e))
            return "Exception :"+str(e)

        for i in range(len(elements)):
            if i == indexToBeSelected:
                try:
                    logger.debug("Selecting DropDown with Index = %s and Text = %s",str(i),str(elements[i].text))
                    elements[i].click()
                    logger.debug("DropDown with Index = %s and Text = %s is selected",str(i),str(elements[i].text))
                    return self.get(h)
                except Exception as e:
                    logger.error("Exception found while selecting DropDown with Index = %s and Text = %s = %s",str(i),str(elements[i].text),str(e))
                    return "Exception :"+str(e)
        currentValue = self.get(h)
        logger.error("Option with index %s not present in dropdown and returning the currentValue selected = %s",str(indexToBeSelected),currentValue)
        return currentValue





    def doSelectionOnVisibleDropDown(self,h,value,index=0,parent="allselects",child="select"):
        activedrops  = self.getAllActiveElements(h[parent][child])
        return self.set(value, activedrops[index])

    def doSelectionOnVisibleDropDownByIndex(self,h,indexToBeSelected=1,index=0,parent="allselects",child="select"):
        activedrops  = self.getAllActiveElements(h[parent][child])
        return self.setByIndex(indexToBeSelected, activedrops[index])

    def doRandomSelectionOnVisibleDropDown(self,h,index=0,parent="allselects",child="select"):
        activedrops  = self.getAllActiveElements(h[parent][child])
        return self.randomSet(activedrops[index])


    def get(self, handle):
        try:
            l = len(handle)
            h = handle[len(handle)-1]
        except:
            h = handle

        try:
            logger.info("Getting DropDown Selection using ng-reflect-model property")
            for ele in h.find_elements_by_xpath(".//*"):
                try:
                    if str(ele.get_attribute('selected')).lower() == 'true':
                        selection = ele.text
                        break
                    else:
                        selection = ''
                except Exception as e:
                    logger.error("Exception found while getting DropDown Selection using selected attribute = %s", e)
                    return "Exception : " + str(e)

            if not selection:
                selection = h.get_attribute("ng-reflect-model")
            logger.debug("Got Selection as %s",selection)
            return selection
        except Exception as e:
            logger.error("Exception found while getting DropDown Selection using ng-reflect-model = %s",e)
            return "Exception : "+str(e)

    def getSelectionOnVisibleDropDown(self,h,index=0,parent="allselects",child="select"):
        activedrops  = self.getAllActiveElements(h[parent][child])
        return str(self.get(activedrops[index]).strip().strip('\n').strip())


    def availableDropDownOption(self,handle, index=0, parent='allselects', child='select'):
        logger.info("Method Called : availableDropDownOption")
        availableDropDownOptionList = []
        if len(handle[parent][child]) > index:
            for ele in handle[parent][child][index].find_elements_by_tag_name('option'):
                availableDropDownOptionList.append(str(ele.text).strip())
        else:
            logger.error("Drop Down not found :: Check manually")

        return availableDropDownOptionList