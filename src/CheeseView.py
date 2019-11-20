from CheeseDAO import CheeseDAO
from CheeseDataLoader import CheeseDataLoader
from CheeseModel import CheeseModel
import datetime
import math
from os import system, name
import re

class CheeseFormatter:
  "Formaters cheese objects for use with the pages"
  def getCheeseSummaryInfo(self, cheese):
    "Creates a string summarizing the info the the passed cheese"
    return (str(cheese.CheeseId) + ": " + 
      ("Unknown" if cheese.CheeseNameEN == None else cheese.CheeseNameEN) 
      + " made by " + 
      ("Unknown" if cheese.ManufacturerNameEN == None else cheese.ManufacturerNameEN)
      + ", Province: " +
      ("Unknown" if cheese.ManufacturerProvCode == None else cheese.ManufacturerProvCode)
      + ", Type: " +
      ("Unknown" if cheese.ManufacturingTypeEN == None else cheese.ManufacturingTypeEN))
  
  def getLongformCheeseLines(self, cheese):
    "Creates an array of strings based on the passed cheese containing all cheese info"
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
  "Defines a basic set of functions for a single page in the program"
  def __init__(self, headerLines = [], mainLines = [], footerLines = [], acceptLine = "", waitAfterDraw = False, numberMainLines = False):
    "Initializes all values that the page will print"
    self.headerLines = headerLines
    self.mainLines = mainLines
    self.footerLines = footerLines
    self.informLine = ""
    self.acceptLine = acceptLine
    self.acceptValue = None
    self.waitAfterDraw = waitAfterDraw
    self.numberMainLines = numberMainLines
  
  def displayLine(self, message):
    "Prints a line to the output stream"
    print(message)

  def accept(self, message):
    "Takes input from the input stream"
    self.acceptValue = input(message)
    return self.acceptValue
  
  def enterToContinue(self):
    "This \"accepts\" a value so make the user press enter to continue"
    self.accept("Press enter to continue")
  
  #The following "clear" method was taken from this source:
  #
  #https://www.geeksforgeeks.org/clear-screen-python/
  #Accessed On: 10/20/2019
  #Author: mohit_negi
  #Link to profile: https://auth.geeksforgeeks.org/user/mohit_negi/articles
  def clear(self):
    "Clear the console"
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
    # for mac and linux(here, os.name is 'posix') 
    elif name == 'posix': 
        _ = system('clear')

  def draw(self):
    "Calling this method makes the page print itself to the screen"
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
    "This method does nothing in page, it's up to subclasses to define it, but the draw method call it so it exists here"
    pass

class LoopingPage (Page):
  "A page that continues to draw until the quit method is called"
  def __init__(self, headerLines = [], mainLines = [], footerLines = [], acceptLine = "", numberMainLines = False):
    "Creates a new looping page"
    self.quitFlag = False
    Page.__init__(self, headerLines, mainLines, footerLines, acceptLine, False, numberMainLines)
  
  def draw(self):
    "Starts the drawing loop"
    while not self.quitFlag:
      Page.draw(self)
  
  def quit(self):
    "Set the quit flag to true to exit the draw loop"
    self.quitFlag = True

class Menu (LoopingPage):
  "A looping page that takes a dict and automatically fill it's main content with options based on the keys of this dict and calls the methods which are values in the dict"
  def __init__(self, headerLines = [], optionDict = {}, footerLines = [], acceptLine = "Selection: ", numberMainLines = False):
    "Initiate a new menu"
    self.optionDict = optionDict
    LoopingPage.__init__(self, headerLines, list(optionDict.keys()), footerLines, acceptLine, numberMainLines)

  def triggerOption(self, val):
    "Triggers an option at a key in the dict"
    self.optionDict[val]()
  
  def triggerOptionByNumber(self, num):
    "Triggers an option by a number in the list of key"
    self.triggerOption(list(self.optionDict.keys())[num])
  
  def processInput(self):
    "Checks which option was input and triggers the proper method"
    if self.acceptValue.isdigit():
      intVal = int(self.acceptValue) - 1
      self.triggerOptionByNumber(intVal)
    else:
      self.informLine = "Please enter a number"

class MainMenu (Menu):
  "A main menu of the cheese program"
  def __init__(self):
    "Initiates the main menu with options for the program"
    optionDict = {
      "Reload the dataset":self.reloadTheDataset,
      "Save data to file":self.saveDataToFile,
      "Display records":self.displayRecords,
      "Create new cheese":self.createNewCheese,
      "Select, Display, or Edit Cheese":self.selectDisplayCheese,
      "Remove a cheese":self.removeCheese,
      "Quit":self.quit
    }
    Menu.__init__(self, headerLines=["Nicholas Bright"], optionDict=optionDict, numberMainLines=True)
  
  def reloadTheDataset(self):
    "Draws the ReloadDatasetPage"
    ReloadDatasetPage().draw()

  def saveDataToFile(self):
    "Draws the SaveDataToFilePage"
    SaveDataToFilePage().draw()

  def displayRecords(self):
    "Draws the DisplayCheeseListPage"
    DisplayCheeseListPage().draw()

  def createNewCheese(self):
    "Draws the CreateNewCheesePage"
    CreateNewCheesePage().draw()

  def selectDisplayCheese(self):
    "Draws the SelectDisplayCheesePage"
    SelectDisplayCheesePage(None).draw()

  def removeCheese(self):
    "Drwas the RemoveCheesePage"
    RemoveCheesePage().draw()

class ReloadDatasetPage(LoopingPage):
  "A page to get input from the user about which file to load and fill the DB with"
  def __init__(self):
    "Initializes the ReloadDatasetPage"
    self.cheeseDAO = CheeseDAO.instance
    self.dataLoader = CheeseDataLoader()
    LoopingPage.__init__(self, headerLines=["Nicholas Bright"], mainLines=["What file to should be read?"], acceptLine="Filename: ")
  
  def processInput(self):
    "Processes user input, and either triggers the reload or informs the user of failure"
    try:
      self.dataLoader.openCheeseFile(self.acceptValue)
      self.cheeseDAO.truncateCheese()
      self.dataLoader.readCheeseData(200)
      self.quit()
    except (FileNotFoundError, PermissionError):
      tryAgainPage = TryAgainPage(["File not found"])
      tryAgainPage.draw()
      if not tryAgainPage.acceptValue:
        self.quit()

class SaveDataToFilePage(Page):
  "A page to get input to save the DB to a csv file"
  def __init__(self):
    "Initialize the SaveDataToFilePage"
    self.dataLoader = CheeseDataLoader()
    Page.__init__(self, headerLines = ["Nicholas Bright"], acceptLine = "Filename to save to: ")
  
  def processInput(self):
    "Triggers the save based on the filename specified"
    self.dataLoader.saveCheeseData(self.acceptValue)

class TryAgainPage(LoopingPage):
  "A page to prompt the user if they want to try again"
  def __init__(self, ErrorMessages = []):
    "Initializes the TryAgainPage"
    LoopingPage.__init__(self, headerLines = ["Nicholas Bright"], mainLines = ErrorMessages, acceptLine = "Try again? (Y/N) ")

  def processInput(self):
    "If the user enters valid input the page will quit, and the acepted value can be read to see the user's response"
    if self.acceptValue.lower() in {"y", "n"}:
      self.acceptValue = self.acceptValue.lower() == "y"
      self.quit()
    else:
      self.informLine = "Enter Y or N"

class DisplayCheeseListPage (LoopingPage):
  "Displays the list of all cheeses from the DB"
  def __init__(self):
    "Initializes the DisplayCheeseListPage"
    self.cheeseDAO = CheeseDAO.instance
    self.formatter = CheeseFormatter()
    self.cheeseList = self.cheeseDAO.getAllCheeses()
    self.pageCount = 1
    self.displayedPerPage = 10
    self.maxPage = int(math.ceil(len(self.cheeseList)/self.displayedPerPage))
    LoopingPage.__init__(self, headerLines = ["Nicholas Bright"], acceptLine = "Input: (Q)uit, (N)ext, (P)rev, (S)ort, or enter ID for details:(N) ")
    self.populateLines()

  def processInput(self):
    "The page presents the user a number of options, and this method checks which they have chosen and takes appropriate action"
    if self.acceptValue.isdigit():
      cheese = self.cheeseDAO.getCheese(int(self.acceptValue))
      if cheese == None:
        self.informLine = "No cheese with that ID found"
      else:
        SelectDisplayCheesePage(cheese).draw()
    else:
      self.acceptValue = self.acceptValue.lower()
      if self.acceptValue == "q":
        self.quit()
      elif self.acceptValue in {"n", ""}:
        self.pageCount += 1
        if self.pageCount > self.maxPage:
          self.quit()
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
    "Repopulates the mainlines of this page based on where in the list the page is showing atm"
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
  "A page to sort a list of cheeses"
  def __init__(self, cheeseList):
    "Initializes the SortCheeseListPage"
    self.cheeseList = cheeseList
    self.sortBy = None
    self.reverseVal = None
    LoopingPage.__init__(self, headerLines = ["Nicholas Bright"], acceptLine = "What attribute do you want to sort on? ")
  
  def processInput(self):
    "Sorts the list based on the property the user supplied or informs the user of failure"
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
        self.quit()
      else:
        self.informLine = "Enter Y or N"

class SelectDisplayCheesePage (LoopingPage):
  "A page to select a cheese then display it's data"
  def __init__(self, cheese):
    "Initializes the SelectDsplayCheesePage"
    self.cheese = cheese
    self.formatter = CheeseFormatter()
    self.cheeseDAO = CheeseDAO.instance
    LoopingPage.__init__(self, headerLines = ["Nicholas Bright"])
    self.populateLines()

  def processInput(self):
    "Processes the options the user inputs as they input them"
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
          self.quit()
        else:
          self.quitFlag = self.acceptValue == "n"
      else:
        self.informLine = "Enter Y or N"

  def populateLines(self):
    "Repopulates the mainlines of the page based on if there is a cheese to diplay or not"
    if self.cheese == None:
      self.mainLines = []
      self.acceptLine = "Enter the ID of the cheese: "
    else:
      self.mainLines = self.formatter.getLongformCheeseLines(self.cheese)
      self.acceptLine = "Modify this cheese? (Y/N)"

class ModifyCheeseMenu (LoopingPage):
  "A page to let the user modify the attributes of a cheese"
  def __init__(self, cheese):
    "Initializes the ModifyCheeseMenu"
    self.cheese = cheese
    self.cheeseDAO = CheeseDAO.instance
    self.modifying = False
    self.nextToModify = list(cheese.__dict__.keys())
    self.nextToModify.remove("CheeseId")
    LoopingPage.__init__(self, headerLines = ["Nicholas Bright"])
    self.populateLines()
  
  def processInput(self):
    "Assigns the value supplied to the attribute being modified, or asks the user if they want to edit the next attribute"
    if not self.modifying:
      self.acceptValue = self.acceptValue.lower()
      if self.acceptValue in {"y", "n"}:
        self.modifying = self.acceptValue == "y"
        if self.modifying:
          self.acceptLine = "Enter a new value "
        else:
          self.nextToModify.pop(0)
          if len(self.nextToModify) == 0:
            self.quit()
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
      self.quit()
      if self.cheese.CheeseId == None:
        self.cheeseDAO.insertCheese(self.cheese)
      else:
        self.cheeseDAO.updateCheese(self.cheese)
    elif not self.modifying:
      self.populateLines()

  def populateLines(self):
    "Repopulates the main lines with the attribute data"
    attrVal = self.cheese.__getattribute__(self.nextToModify[0])
    self.mainLines = [(self.nextToModify[0] + " = " + ("" if attrVal == None else str(attrVal)))]
    self.acceptLine = "Modify this attribute? (Y/N)"

class CreateNewCheesePage (ModifyCheeseMenu):
  "A page to create a new cheese in the DB. Really it's just the ModifyCheeseMenu with a new cheese passed to it"
  def __init__(self):
    "Initializes the CreateNewCheesePage"
    ModifyCheeseMenu.__init__(self, CheeseModel())
    ModifyCheeseMenu.modifying = True

class RemoveCheesePage (LoopingPage):
  "A page to remove a cheese from the DB"
  def __init__(self):
    "Initializes the RemoveCheesePage"
    self.cheeseDAO = CheeseDAO.instance
    LoopingPage.__init__(self, headerLines = ["Nicholas Bright"], acceptLine = "ID of the cheese to remove ")
  
  def processInput(self):
    "Triggers removal from the DB is a correct ID is supplied to informs the user of failure"
    if self.acceptValue.isdigit():
      self.acceptValue = int(self.acceptValue)
      if not self.cheeseDAO.deleteCheese(self.acceptValue):
        tryAgainPage = TryAgainPage(["Failed to remove cheese with that ID"])
        tryAgainPage.draw()
        self.quitFlag = not tryAgainPage.acceptValue
      else:
        self.quit()
    else:
      self.informLine = "Please enter an integer ID"