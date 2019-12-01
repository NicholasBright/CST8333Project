from CheeseDAO import CheeseDAO
from CheeseDataLoader import CheeseDataLoader
from CheeseModel import CheeseModel
import datetime
import math
from os import system, name
import re
from ViewBasics import Menu, Page, LoopingPage, ListPage, YesNoPage, EditorPage, SearchListPage

cheeseHeader = [
  "Nicholas Bright"
]

DAO = CheeseDAO.instance
dataLoader = CheeseDataLoader()

def getCheeseSummaryInfo(cheese):
  "Creates a string summarizing the info the the passed cheese"
  return (str(cheese.CheeseId) + ": " + 
    ("Unknown" if cheese.CheeseNameEN == None else cheese.CheeseNameEN) 
    + " made by " + 
    ("Unknown" if cheese.ManufacturerNameEN == None else cheese.ManufacturerNameEN)
    + ", Province: " +
    ("Unknown" if cheese.ManufacturerProvCode == None else cheese.ManufacturerProvCode)
    + ", Type: " +
    ("Unknown" if cheese.ManufacturingTypeEN == None else cheese.ManufacturingTypeEN))
  
def getLongformCheeseLines(cheese):
  "Creates an array of strings based on the passed cheese containing all cheese info"
  lines = []
  lines.append(getCheeseSummaryInfo(cheese))
  lines.append("WebSite: " + ("Unknown" if cheese.WebSiteEN == None else cheese.WebSiteEN))
  lines.append("FatContentPercent: " + ("Unknown" if cheese.FatContentPercent == None else str(cheese.FatContentPercent)))
  lines.append("MoisturePercent: " + ("Unknown" if cheese.MoisturePercent == None else str(cheese.MoisturePercent)))
  lines.append("Particularities: " + ("Unknown" if cheese.ParticularitiesEN == None else cheese.ParticularitiesEN))
  lines.append("Flavour: " + ("Unknown" if cheese.FlavourEN == None else cheese.FlavourEN))
  lines.append("Characteristics: " + ("Unknown" if cheese.CharacteristicsEN == None else cheese.CharacteristicsEN))
  lines.append("Ripening: " + ("Unknown" if cheese.RipeningEN == None else cheese.RipeningEN))
  lines.append("Organic: " + ("Yes" if cheese.Organic else "No"))
  lines.append("CategoryType: " + ("Unknown" if cheese.CategoryTypeEN == None else cheese.CategoryTypeEN))
  lines.append("MilkType: " + ("Unknown" if cheese.MilkTypeEN == None else cheese.MilkTypeEN))
  lines.append("MilkTreatmentType: " + ("Unknown" if cheese.MilkTreatmentTypeEN == None else cheese.MilkTreatmentTypeEN))
  lines.append("RindType: " + ("Unknown" if cheese.RindTypeEN == None else cheese.RindTypeEN))
  lines.append("LastUpdateDate: " + ("Unknown" if cheese.LastUpdateDate == None else str(cheese.LastUpdateDate)))
  return lines

class MainMenu (Menu):
  "A main menu of the cheese program"
  def __init__(self):
    "Initiates the main menu with options for the program"
    optionDict = {
      "Data Options":self.DataOptions,
      "Display records":self.displayRecords,
      "Create new cheese":self.createNewCheese,
      "View Cheese Info":self.cheeseInfo,
      "Remove a cheese":self.removeCheese
    }
    Menu.__init__(self, headerLines=cheeseHeader, optionDict=optionDict, numberMainLines=True)
  
  def DataOptions(self):
    "Navigate to the data options menu"
    DataOptionsMenu().draw()

  def displayRecords(self):
    "Draws the DisplayCheeseListPage"
    DisplayCheeseListPage().draw()

  def createNewCheese(self):
    "Creates a cheese info page on a new cheese"
    EditCheesePage(CheeseModel()).draw()


  def cheeseInfo(self):
    "Draws the CheeseInfoPage"
    FindCheesePage().draw()

  def removeCheese(self):
    "Drwas the RemoveCheesePage"
    RemoveCheesePage().draw()

class DataOptionsMenu(Menu):
  def __init__(self):
    optionDict = {
      "Reload Dataset":self.reloadDataset,
      "Truncate the table":self.truncateTable,
      "Save data to file":self.saveDataToFile
    }
    super().__init__(headerLines=cheeseHeader, optionDict=optionDict)
  
  def reloadDataset(self):
    ReloadDatasetPage().draw()
  
  def truncateTable(self):
    DAO.truncate()
    self.informLine = "Table truncated"

  def saveDataToFile(self):
    "Draws the SaveDataToFilePage"
    SaveDataToFilePage().draw()

class ReloadDatasetPage(ListPage):
  "A page to get input from the user about which file to load and fill the DB with"
  def __init__(self):
    "Initializes the ReloadDatasetPage"
    super().__init__(displayList=dataLoader.getListOfDataFiles(), headerLines=cheeseHeader, selectAction=self.loadDataset)
  
  def loadDataset(self, item):
    truncate = YesNoPage(["Do you wish to truncate the db before loading?"])
    truncate.draw()
    if truncate.acceptValue:
      DAO.truncate()
    dataLoader.readCheeseFile(item)
    self.quit()

class TryAgainPage(LoopingPage):
  "A page to prompt the user if they want to try again"
  def __init__(self, ErrorMessages = []):
    "Initializes the TryAgainPage"
    LoopingPage.__init__(self, headerLines = cheeseHeader, mainLines = ErrorMessages, acceptLine = "Try again? (Y/N) ")

  def processInput(self):
    "If the user enters valid input the page will quit, and the acepted value can be read to see the user's response"
    if self.acceptValue.lower() in {"y", "n"}:
      self.acceptValue = self.acceptValue.lower() == "y"
      self.quit()
    else:
      self.informLine = "Enter Y or N"

class DisplayCheeseListPage (SearchListPage):
  "Displays the list of all cheeses from the DB"
  def __init__(self):
    "Initializes the DisplayCheeseListPage"
    super().__init__(searchList=DAO.getAll(), headerLines = cheeseHeader, formatter=getCheeseSummaryInfo, selectAction=self.displaySummaryOfCheese)

  def displaySummaryOfCheese(self, cheese):
    CheeseInfoPage(cheese).draw()
  
  def processInput(self):
    super().processInput()
    if self.acceptValue == "DELETE":
      selectedCheese = self.displayList[super().getSelectedIndex()]
      confirmDelete = YesNoPage(headerLines=cheeseHeader,messages=["You are about to delete", getCheeseSummaryInfo(selectedCheese)])
      confirmDelete.draw()
      if confirmDelete.acceptValue:
        self.displayList.remove(selectedCheese)
        DAO.delete(selectedCheese.CheeseId)

class CheeseInfoPage (YesNoPage):
  "A page to select a cheese then display it's data"
  def __init__(self, cheese):
    "Initializes the SelectDsplayCheesePage"
    self.cheese = cheese
    self.cheeseDAO = CheeseDAO.instance
    super().__init__(headerLines = cheeseHeader, messages=getLongformCheeseLines(cheese), acceptLine="Modify this cheese? (Y\\N)")

  def processInput(self):
    super().processInput()
    if self.acceptValue == True:
      EditCheesePage(self.cheese).draw()

class EditCheesePage(EditorPage):
  def __init__(self, cheese):
    self.cheese = cheese
    verifyValuesDict = {
      "CheeseId": lambda a: False,
      "CheeseNameEN": lambda a: a.__len__() <= 100,
      "CheeseNameFR": lambda a: a.__len__() <= 100,
      "ManufacturerNameEN": lambda a: a.__len__() <= 50,
      "ManufacturerNameFR": lambda a: a.__len__() <= 50,
      "ManufacturerProvCode": lambda a: a.__len__() <= 2,
      "ManufacturingTypeEN": lambda a: a.__len__() <= 50,
      "ManufacturingTypeFR": lambda a: a.__len__() <= 50,
      "WebSiteEN": lambda a: a.__len__() <= 100,
      "WebSiteFR": lambda a: a.__len__() <= 100,
      "FatContentPercent": lambda a: re.match("^\\d+(\\.\\d+)*$", a) != None,
      "MoisturePercent": lambda a: re.match("^\\d+(\\.\\d+)*$", a) != None,
      "ParticularitiesEN": lambda a: a.__len__() <= 200,
      "ParticularitiesFR": lambda a: a.__len__() <= 200,
      "FlavourEN": lambda a: a.__len__() <= 200,
      "FlavourFR": lambda a: a.__len__() <= 200,
      "CharacteristicsEN": lambda a: a.__len__() <= 200,
      "CharacteristicsFR": lambda a: a.__len__() <= 200,
      "RipeningEN": lambda a: a.__len__() <= 50,
      "RipeningFR": lambda a: a.__len__() <= 50,
      "CategoryTypeEN": lambda a: a.__len__() <= 50,
      "CategoryTypeFR": lambda a: a.__len__() <= 50,
      "MilkTypeEN": lambda a: a.__len__() <= 50,
      "MilkTypeFR": lambda a: a.__len__() <= 50,
      "MilkTreatmentTypeEN": lambda a: a.__len__() <= 20,
      "MilkTreatmentTypeFR": lambda a: a.__len__() <= 20,
      "RindTypeEN": lambda a: a.__len__() <= 20,
      "RindTypeFR": lambda a: a.__len__() <= 20,
      "LastUpdateDate": lambda a: re.match("^\\d{4}-\\d{2}-\\d{2}$", a) != None
    }
    formatDict = {
      "LastUpdateDate": lambda a: datetime.datetime.strptime(a,"%Y-%m-%d").date()
    }
    super().__init__(editingObject=cheese,headerLines=cheeseHeader, testValidDict=verifyValuesDict, formatDict=formatDict)

  def quit(self):
    super().quit()
    saveCheesePage = YesNoPage(headerLines=cheeseHeader, acceptLine="Would you like to save your changes? (Y/N)")
    saveCheesePage.draw()
    if saveCheesePage.acceptValue:
      if self.cheese.CheeseId == None:
        DAO.insert(self.cheese)
      else:
        DAO.update(self.cheese)


class FindCheesePage(EditorPage):
  def __init__(self):
    self.inputLine = ""
    LoopingPage.__init__(self, headerLines = cheeseHeader, acceptLine = "Enter the ID of the Cheese to be viewed and hit enter, or press escape to exit")
  
  def populateLines(self):
    super().populateLines
    self.mainLines = ["ID:" + self.inputLine]

  def processInput(self):
    if self.acceptValue.isdigit():
      self.inputLine += self.acceptValue
    elif (self.acceptValue == "ENTER") and (self.inputLine != ""):
      cheese = DAO.get(int(self.inputLine))
      if cheese != None:
        CheeseInfoPage(cheese).draw()
        self.quit()
      else:
        self.informLine = "Failed to find cheese with that ID"
    elif self.acceptValue == "ESCAPE":
      self.quit()
    elif self.acceptValue == "BACKSPACE":
      if self.inputLine != "":
        self.inputLine = self.inputLine[:-1]
    else:
      self.informLine = "Please enter an integer ID"


class RemoveCheesePage(LoopingPage):
  "A page to remove a cheese from the DB"
  def __init__(self):
    "Initializes the RemoveCheesePage"
    self.inputLine = ""
    LoopingPage.__init__(self, headerLines = cheeseHeader, acceptLine = "Enter the ID of the Cheese to remove and hit enter, or press escape to exit")
  
  def populateLines(self):
    super().populateLines
    self.mainLines = ["ID:" + self.inputLine]

  def processInput(self):
    "Triggers removal from the DB is a correct ID is supplied to informs the user of failure"
    if self.acceptValue.isdigit():
      self.inputLine += self.acceptValue
    elif (self.acceptValue == "ENTER") and (self.inputLine != ""):
      if DAO.delete(int(self.inputLine)):
        self.quit()
      else:
        self.informLine = "Failed to remove cheese with that ID"
    elif self.acceptValue == "ESCAPE":
      self.quit()
    elif self.acceptValue == "BACKSPACE":
      if self.inputLine != "":
        self.inputLine = self.inputLine[:-1]
    else:
      self.informLine = "Please enter an integer ID"

class SaveDataToFilePage(LoopingPage):
  def __init__(self):
    self.inputLine = ""
    LoopingPage.__init__(self, headerLines = cheeseHeader, acceptLine = "Enter the name for the file and hit enter, or press escape to exit")
  
  def populateLines(self):
    super().populateLines
    self.mainLines = ["Filename:" + self.inputLine]

  def processInput(self):
    if (self.acceptValue == "ENTER") and (self.inputLine != ""):
      dataLoader.saveCheeseData(self.inputLine)
      self.quit()
    elif self.acceptValue == "ESCAPE":
      self.quit()
    elif self.acceptValue == "BACKSPACE":
      if self.inputLine != "":
        self.inputLine = self.inputLine[:-1]
    else:
      self.inputLine += self.acceptValue