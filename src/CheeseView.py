from CheeseDAO import CheeseDAO
from CheeseDataLoader import CheeseDataLoader
from CheeseModel import CheeseModel
import datetime
import math
from os import system, name
import re

class CheeseFormatter:
  def getCheeseSummaryInfo(self, cheese):
    return (str(cheese.CheeseId) + ": " + 
      ("Unknown" if cheese.CheeseNameEN == None else cheese.CheeseNameEN) 
      + " made by " + 
      ("Unknown" if cheese.ManufacturerNameEN == None else cheese.ManufacturerNameEN)
      + ", Province: " +
      ("Unknown" if cheese.ManufacturerProvCode == None else cheese.ManufacturerProvCode)
      + ", Type: " +
      ("Unknown" if cheese.ManufacturingTypeEN == None else cheese.ManufacturingTypeEN))
  
  def getLongformCheeseLines(self, cheese):
    lines = []
    lines.append(self.getCheeseSummaryInfo(cheese))
    lines.append("WebSite: " + ("Unknown" if cheese.WebSiteEN == None else cheese.WebSiteEN))
    lines.append("FatContentPercent: " + ("Unknown" if cheese.FatContentPercent == None else str(cheese.FatContentPercent)))
    lines.append("MoisturePercent: " + ("Unknown" if cheese.MoisturePercent == None else str(cheese.MoisturePercent)))
    lines.append("Particularities: " + ("Unknown" if cheese.ParticularitiesEN == None else cheese.ParticularitiesEN))
    lines.append("Flavour: " + ("Unknown" if cheese.FlavourEN == None else cheese.FlavourEN))
    lines.append("Characteristics: " + ("Unknown" if cheese.CharacteristicsEN == None else cheese.CharacteristicsEN))
    lines.append("Ripening: " + ("Unknown" if cheese.RipeningEN == None else cheese.RipeningEN))
    lines.append("Organic: " + ("Yes" if cheese.Organic == "1" else "No"))
    lines.append("CategoryType: " + ("Unknown" if cheese.CategoryTypeEN == None else cheese.CategoryTypeEN))
    lines.append("MilkType: " + ("Unknown" if cheese.MilkTypeEN == None else cheese.MilkTypeEN))
    lines.append("MilkTreatmentType: " + ("Unknown" if cheese.MilkTreatmentTypeEN == None else cheese.MilkTreatmentTypeEN))
    lines.append("RindType: " + ("Unknown" if cheese.RindTypeEN == None else cheese.RindTypeEN))
    lines.append("LastUpdateDate: " + ("Unknown" if cheese.LastUpdateDate == None else str(cheese.LastUpdateDate)))
    return lines

class Page:
  def __init__(self, headerLines = [], mainLines = [], footerLines = [], acceptLine = [], waitAfterDraw = False, numberMainLines = False):
    self.headerLines = headerLines
    self.mainLines = mainLines
    self.footerLines = footerLines
    self.informLine = ""
    self.acceptLine = acceptLine
    self.acceptValue = None
    self.waitAfterDraw = waitAfterDraw
    self.numberMainLines = numberMainLines
  
  def displayLine(self, message):
    print(message)

  def accept(self, message):
    self.acceptValue = input(message)
    return self.acceptValue
  
  def enterToContinue(self):
    self.accept("Press enter to continue")
  
  def displayName(self):
    self.displayLine("Nicholas Bright")
  
  def clear(self):
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
    # for mac and linux(here, os.name is 'posix') 
    elif name == 'posix': 
        _ = system('clear')

  def draw(self):
    self.clear()
    for line in self.headerLines:
      self.displayLine(line)
    lineCount = 0
    for line in self.mainLines:
      lineCount += 1
      self.displayLine(line if not self.numberMainLines else "(" + str(lineCount) + ") " + line)
    for line in self.footerLines:
      self.displayLine(line)
    self.displayLine(self.informLine)
    self.informLine = ""
    if self.acceptLine != None:
      self.accept(self.acceptLine)
      self.processInput()
    elif self.waitAfterDraw:
      self.enterToContinue()
  
  def processInput(self):
    pass

class LoopingPage (Page):
  def __init__(self, headerLines = [], mainLines = [], footerLines = [], acceptLine = [], waitAfterDraw = False, numberMainLines = False):
    self.quitFlag = False
    Page.__init__(self, headerLines, mainLines, footerLines, acceptLine, waitAfterDraw, numberMainLines)
  
  def draw(self):
    while not self.quitFlag:
      Page.draw(self)

class Menu (Page):
  def __init__(self, headerLines = [], optionDict = {}, footerLines = [], acceptLine = [], waitAfterDraw = False, numberMainLines = False):
    self.optionDict = optionDict
    Page.__init__(self, headerLines, list(optionDict.keys()), footerLines, acceptLine, waitAfterDraw, numberMainLines)

  def triggerOption(self, val):
    self.optionDict[val]()
  
  def triggerOptionByNumber(self, num):
    self.triggerOption(list(self.optionDict.keys())[num])

class MainMenu (Menu):
  def __init__(self):
    self._quitFlag = False
    headerLines = [
      "Nicholas Bright"
    ]
    optionDict = {
      "Reload the dataset":self.reloadTheDataset,
      "Save data to file":self.saveDataToFile,
      "Display records":self.displayRecords,
      "Create new cheese":self.createNewCheese,
      "Select, Display, or Edit Cheese":self.selectDisplayCheese,
      "Remove a cheese":self.removeCheese,
      "Quit":self.quit
    }
    footerLines = []
    acceptLine = "Selection: "
    Menu.__init__(self, headerLines, optionDict, footerLines, acceptLine, False, True)
  
  def draw(self):
    while not self._quitFlag:
      Page.draw(self)
  
  def processInput(self):
    if self.acceptValue.isdigit():
      intVal = int(self.acceptValue) - 1
      self.triggerOptionByNumber(intVal)
    else:
      self.informLine = "Please enter a number"
  
  def reloadTheDataset(self):
    ReloadDatasetPage().draw()

  def saveDataToFile(self):
    SaveDataToFilePage().draw()

  def displayRecords(self):
    DisplayCheeseListPage().draw()

  def createNewCheese(self):
    CreateNewCheesePage().draw()

  def selectDisplayCheese(self):
    SelectDisplayCheesePage(None).draw()

  def removeCheese(self):
    RemoveCheesePage().draw()

  def quit(self):
    self._quitFlag = True

class ReloadDatasetPage(LoopingPage):
  def __init__(self):
    self.cheeseDAO = CheeseDAO.instance
    self.dataLoader = CheeseDataLoader()
    LoopingPage.__init__(self, headerLines=["Nicholas Bright"], mainLines=["What file to should be read?"], acceptLine="Filename: ")
  
  def draw(self):
    while not self.quitFlag:
      Page.draw(self)
  
  def processInput(self):
    try:
      self.dataLoader.openCheeseFile(self.acceptValue)
      self.cheeseDAO.truncateCheese()
      self.dataLoader.readCheeseData(200)
      self.quitFlag = True
    except (FileNotFoundError, PermissionError):
      tryAgainPage = TryAgainPage(["File not found"])
      tryAgainPage.draw()
      self.quitFlag = not tryAgainPage.acceptValue

class SaveDataToFilePage(Page):
  def __init__(self):
    self.dataLoader = CheeseDataLoader()
    Page.__init__(self, headerLines = ["Nicholas Bright"], acceptLine = "Filename to save to: ")
  
  def processInput(self):
    self.dataLoader.saveCheeseData(self.acceptValue)

class TryAgainPage(LoopingPage):
  def __init__(self, ErrorMessages = []):
    LoopingPage.__init__(self, headerLines = ["Nicholas Bright"], mainLines = ErrorMessages, acceptLine = "Try again? (Y/N) ")
  
  def draw(self):
    while not self.quitFlag:
      Page.draw(self)

  def processInput(self):
    if self.acceptValue.lower() in {"y", "n"}:
      self.acceptValue = self.acceptValue.lower() == "y"
      self.quitFlag = True
    else:
      self.informLine = "Enter Y or N"

class DisplayCheeseListPage (LoopingPage):
  def __init__(self):
    self.cheeseDAO = CheeseDAO.instance
    self.formatter = CheeseFormatter()
    self.cheeseList = self.cheeseDAO.getAllCheeses()
    self.pageCount = 1
    self.displayedPerPage = 10
    self.maxPage = int(math.ceil(len(self.cheeseList)/self.displayedPerPage))
    LoopingPage.__init__(self, headerLines = ["Nicholas Bright"], acceptLine = "Input: (Q)uit, (N)ext, (P)rev, (S)ort, or enter ID for details:(N) ")
    self.populateLines()

  def processInput(self):
    if self.acceptValue.isdigit():
      cheese = self.cheeseDAO.getCheese(int(self.acceptValue))
      if cheese == None:
        self.informLine = "No cheese with that ID found"
      else:
        SelectDisplayCheesePage(cheese).draw()
    else:
      self.acceptValue = self.acceptValue.lower()
      if self.acceptValue == "q":
        self.quitFlag = True
      elif self.acceptValue in {"n", ""}:
        self.pageCount += 1
        if self.pageCount > self.maxPage:
          self.quitFlag = True
        else:
          self.populateLines()
      elif self.acceptValue == "p":
        self.pageCount -= 1
        if self.pageCount < 1:
          self.pageCount = 1
        self.populateLines()
      elif self.acceptValue == "s":
        SortCheeseListPage(self.cheeseList).draw()
        self.populateLines()

  def populateLines(self):
    self.mainLines = []
    self.footerLines = []
    if len(self.cheeseList) == 0:
      self.mainLines.append("There are no cheeses to show")
    displayCount = 0
    while(displayCount < self.displayedPerPage) & ((self.pageCount -1)*self.displayedPerPage + displayCount < len(self.cheeseList)):
      self.mainLines.append(self.formatter.getCheeseSummaryInfo(self.cheeseList[(self.pageCount -1)*self.displayedPerPage + displayCount]))
      displayCount += 1
    self.footerLines.append("Page (" + str(self.pageCount) + "/" + str(self.maxPage) + ")")

class SortCheeseListPage (LoopingPage):
  def __init__(self, cheeseList):
    self.cheeseList = cheeseList
    self.sortBy = None
    self.reverseVal = None
    LoopingPage.__init__(self, headerLines = ["Nicholas Bright"], acceptLine = "What attribute do you want to sort on? ")
  
  def processInput(self):
    if self.sortBy == None:
      if hasattr(CheeseModel(),self.acceptValue):
        self.sortBy = self.acceptValue
        self.acceptLine = "Reserve order? (Y/N)"
      else:
        tryAgainPage = TryAgainPage(["Cheeses don't have that attribute"])
        tryAgainPage.draw()
        self.quitFlag = not tryAgainPage.acceptValue
    else:
      self.acceptValue = self.acceptValue.lower()
      if self.acceptValue in {"y", "n"}:
        self.cheeseList.sort(key=lambda x: getattr(x, self.sortBy), reverse = self.acceptValue == "y")
        self.quitFlag = True
      else:
        self.informLine = "Enter Y or N"

class SelectDisplayCheesePage (LoopingPage):
  def __init__(self, cheese):
    self.cheese = cheese
    self.formatter = CheeseFormatter()
    self.cheeseDAO = CheeseDAO.instance
    LoopingPage.__init__(self, headerLines = ["Nicholas Bright"])
    self.populateLines()

  def processInput(self):
    if self.cheese == None:
      if self.acceptValue.isdigit():
        self.cheese = self.cheeseDAO.getCheese(int(self.acceptValue))
        self.populateLines()
        if self.cheese == None:
          tryAgainPage = TryAgainPage(["Cheese with that ID not found"])
          tryAgainPage.draw()
          self.quitFlag = not tryAgainPage.acceptValue
      else:
        self.informLine = "Please enter a valid ID"
    else:
      self.acceptValue = self.acceptValue.lower()
      if self.acceptValue in {"y", "n"}:
        if self.acceptValue == "y":
          ModifyCheeseMenu(self.cheese).draw()
          self.quitFlag = True
        else:
          self.quitFlag = self.acceptValue == "n"
      else:
        self.informLine = "Enter Y or N"

  def populateLines(self):
    if self.cheese == None:
      self.mainLines = []
      self.acceptLine = "Enter the ID of the cheese: "
    else:
      self.mainLines = self.formatter.getLongformCheeseLines(self.cheese)
      self.acceptLine = "Modify this cheese? (Y/N)"

class ModifyCheeseMenu (LoopingPage):
  def __init__(self, cheese):
    self.cheese = cheese
    self.cheeseDAO = CheeseDAO.instance
    self.modifying = False
    self.nextToModify = list(cheese.__dict__.keys())
    self.nextToModify.remove("CheeseId")
    LoopingPage.__init__(self, headerLines = ["Nicholas Bright"])
    self.populateLines()
  
  def processInput(self):
    if not self.modifying:
      self.acceptValue = self.acceptValue.lower()
      if self.acceptValue in {"y", "n"}:
        self.modifying = self.acceptValue == "y"
        if self.modifying:
          self.acceptLine = "Enter a new value "
        else:
          self.nextToModify.pop(0)
          if len(self.nextToModify) == 0:
            self.quitFlag = True
            if self.cheese.CheeseId == None:
              self.cheeseDAO.insertCheese(self.cheese)
            else:
              self.cheeseDAO.updateCheese(self.cheese)
      else:
        self.informLine = "Enter Y or N"
    else:
      setAttr = True
      attrToModify = self.nextToModify[0]
      if attrToModify in {"FatContentPercent", "MoisturePercent"}:
        if re.match("^\\d+(\\.\\d+)*$", self.acceptValue) is not None:
          self.acceptValue = float(self.acceptValue)
        else:
          setAttr = False
          self.informLine = "Please enter an integer or a float"
      elif attrToModify == "LastUpdateDate":
        try:
          newDate = datetime.datetime.strptime(self.acceptValue,"%Y-%m-%d").date()
          self.cheese.LastUpdateDate = newDate
        except (ValueError, TypeError):
          setAttr = False
          self.informLine = "Please use the format YYYY-MM-DD"
      if setAttr:
        self.modifying = False
        self.cheese.__setattr__(attrToModify, None if self.acceptValue == "" else self.acceptValue)
        self.nextToModify.pop(0)
    
    if len(self.nextToModify) == 0:
      self.quitFlag = True
      if self.cheese.CheeseId == None:
        self.cheeseDAO.insertCheese(self.cheese)
      else:
        self.cheeseDAO.updateCheese(self.cheese)
    elif not self.modifying:
      self.populateLines()

  def populateLines(self):
    attrVal = self.cheese.__getattribute__(self.nextToModify[0])
    self.mainLines = [(self.nextToModify[0] + " = " + ("" if attrVal == None else str(attrVal)))]
    self.acceptLine = "Modify this attribute? (Y/N)"

class CreateNewCheesePage (ModifyCheeseMenu):
  def __init__(self):
    ModifyCheeseMenu.__init__(self, CheeseModel())
    ModifyCheeseMenu.modifying = True

class RemoveCheesePage (LoopingPage):
  def __init__(self):
    self.cheeseDAO = CheeseDAO.instance
    LoopingPage.__init__(self, headerLines = ["Nicholas Bright"], acceptLine = "ID of the cheese to remove ")
  
  def processInput(self):
    if self.acceptValue.isdigit():
      self.acceptValue = int(self.acceptValue)
      if not self.cheeseDAO.deleteCheese(self.acceptValue):
        tryAgainPage = TryAgainPage(["Failed to remove cheese with that ID"])
        tryAgainPage.draw()
        self.quitFlag = not tryAgainPage.acceptValue
      else:
        self.quitFlag = True
    else:
      self.informLine = "Please enter an integer ID"