'''
Author: Nicholas Bright
Created Date: 2019-10-20
Last Updated: 2019-12-03
Version: 1.0.0
Purpose:
Defines a series of classes that implement various pages from ViewBasics.py.
These classes each have their own purposes within the mangement of cheese data
however they all revolve around CRUD for the canadian cheese directory.
'''

from CheeseDAO import CheeseDAO
from CheeseDataLoader import CheeseDataLoader
from CheeseModel import CheeseModel
import datetime
import re
from mysql.connector.errors import IntegrityError
from ViewBasics import Menu, ListPage, EditorPage, YesNoPage, SearchListPage, InputPage

cheeseHeader = [
  "Nicholas Bright"
]

DAO = CheeseDAO.instance
dataLoader = CheeseDataLoader()

def getCheeseSummaryInfo(cheese):
  """Creates a string summarizing the info the the passed cheese
  cheese - The cheese to summarize"""
  return (str(cheese.CheeseId) + ": " + 
    ("Unknown" if cheese.CheeseNameEN == None else cheese.CheeseNameEN) 
    + " made by " + 
    ("Unknown" if cheese.ManufacturerNameEN == None else cheese.ManufacturerNameEN)
    + ", Province: " +
    ("Unknown" if cheese.ManufacturerProvCode == None else cheese.ManufacturerProvCode)
    + ", Type: " +
    ("Unknown" if cheese.ManufacturingTypeEN == None else cheese.ManufacturingTypeEN))
  
def getLongformCheeseLines(cheese):
  """Creates an array of strings based on the passed cheese containing all cheese info
  cheese - The cheese to create the strings about"""
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
  """A main menu of the cheese program"""
  def __init__(self):
    """Initiates a new MainMenu"""
    optionDict = {
      "Data Options":self.DataOptions,
      "Display records":self.displayRecords,
      "Create new cheese":self.createNewCheese,
      "View Cheese Info":self.cheeseInfo,
      "Remove a cheese":self.removeCheese
    }
    super().__init__(headerLines=cheeseHeader, optionDict=optionDict, numberMainLines=True)
  
  def DataOptions(self):
    """Navigate to the data options menu"""
    DataOptionsMenu().draw()

  def displayRecords(self):
    """Draws the DisplayCheeseListPage"""
    DisplayCheeseListPage().draw()

  def createNewCheese(self):
    """Creates a cheese info page on a new cheese"""
    EditCheesePage(CheeseModel()).draw()

  def cheeseInfo(self):
    """Draws the CheeseInfoPage"""
    FindCheesePage().draw()

  def removeCheese(self):
    """Draws the RemoveCheesePage"""
    RemoveCheesePage().draw()

class DataOptionsMenu(Menu):
  """An implementation of Menu that gives a list of options regarding cheese data"""
  def __init__(self):
    """Initializes a new DataOptionsMenu. Gives options to the user for reloading data from a file, clearing the table, and creating a new data file."""
    optionDict = {
      "Reload Dataset":self.reloadDataset,
      "Clear the table of data":self.clearTable,
      "Save data to file":self.saveDataToFile
    }
    super().__init__(headerLines=cheeseHeader, optionDict=optionDict)
  
  def reloadDataset(self):
    """Creates a new ReloadDatasetPage and draws it"""
    ReloadDatasetPage().draw()
  
  def clearTable(self):
    """Clears the database of all cheeses"""
    DAO.deleteAll()
    self.informLine = "Table cleared"

  def saveDataToFile(self):
    """Draws the SaveDataToFilePage"""
    SaveDataToFilePage().draw()

class ReloadDatasetPage(ListPage):
  """A page to get input from the user about which file to load and fill the DB with"""
  def __init__(self):
    """Initializes the ReloadDatasetPage"""
    super().__init__(displayList=dataLoader.getListOfDataFiles(), headerLines=cheeseHeader, selectAction=self.loadDataset)
  
  def loadDataset(self, filename):
    """Asks the user if they want to clear the table first, and then executes the delete (if they said yes) and loads data from the file
    filename - The filename to load from"""
    clearPage = YesNoPage(["Do you wish to delete all cheeses in the db before loading?"])
    clearPage.draw()
    if clearPage.acceptValue:
      DAO.deleteAll()
    try:
      dataLoader.readCheeseFile(filename)
      self.quit()
    except IntegrityError as e:
      self.informLine = e.msg

class DisplayCheeseListPage (SearchListPage):
  """Displays the list of all cheeses from the DB"""
  def __init__(self):
    "Initializes the DisplayCheeseListPage"
    super().__init__(searchList=DAO.getAll(), headerLines = cheeseHeader, formatter=getCheeseSummaryInfo, selectAction=self.displaySummaryOfCheese)

  def displaySummaryOfCheese(self, cheese):
    """Draws a cheese info page for a given cheese
    cheese - The cheese to show info of"""
    CheeseInfoPage(cheese).draw()
  
  def processInput(self):
    """If the user typed DELETE the selected cheese is deleted, if typed anything else it calls super().processInput()"""
    if self.acceptValue == "DELETE":
      selectedCheese = self.displayList[super().getSelectedIndex()]
      confirmDelete = YesNoPage(headerLines=cheeseHeader,messages=["You are about to delete", getCheeseSummaryInfo(selectedCheese)])
      confirmDelete.draw()
      if confirmDelete.acceptValue:
        self.displayList.remove(selectedCheese)
        DAO.delete(selectedCheese.CheeseId)
    else:
      super().processInput()

class CheeseInfoPage (YesNoPage):
  """Displays a cheese's data and prompts if the user wants to modify it"""
  def __init__(self, cheese):
    """Initializes the SelectDsplayCheesePage. Paramters are:
    cheese - The cheese to show the info of"""
    self.cheese = cheese
    self.cheeseDAO = CheeseDAO.instance
    super().__init__(headerLines = cheeseHeader, messages=getLongformCheeseLines(cheese), acceptLine="Modify this cheese? (Y\\N)")

  def processInput(self):
    """Performs super().processInput(), then if the user said yes draws the EditCheesePage for the cheese supplied in the constructor"""
    super().processInput()
    if self.acceptValue == True:
      EditCheesePage(self.cheese).draw()

class EditCheesePage(EditorPage):
  """A page for editing the content of a cheese"""
  def __init__(self, cheese):
    """Initializes a new EditCheesePage.
    cheese - The cheese to edit"""
    self.cheese = cheese
    #This dict has an entry for every attribute of the cheese
    #The float fields verify that the input string is a float
    #The date field verifies that the input string matchs YYYY-MM-DD
    #The remaining string fields only check length, to make sure the fields fit in the DB
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
    #This dict formats the strings into whatever should be stored in the fields
    #Only contains 3 entries since these 3 fields are the only 3 non string fields
    # aside from CheeseId, which the previous dict marks as all edits invalid, since ID is assigned
    # by either the DB or when it is read from a file, NOT by the user
    formatDict = {
      "FatContentPercent": lambda a: float(a),
      "MoisturePercent": lambda a: float(a),
      "LastUpdateDate": lambda a: datetime.datetime.strptime(a,"%Y-%m-%d").date()
    }
    super().__init__(editingObject=cheese,headerLines=cheeseHeader, testValidDict=verifyValuesDict, formatDict=formatDict)

  def quit(self):
    """Overiding LoopingPage.quit(). We want to prompt the user if they want to save their changes, meaning push them to the DB"""
    super().quit()
    saveCheesePage = YesNoPage(headerLines=cheeseHeader, acceptLine="Would you like to save your changes? (Y/N)")
    saveCheesePage.draw()
    if saveCheesePage.acceptValue:
      #A CheeseId of None means the data wasn't read from DB, and must be inserted
      if self.cheese.CheeseId == None:
        DAO.insert(self.cheese)
      else:
        DAO.update(self.cheese)


class FindCheesePage(InputPage):
  """An inplementation of InputPage that finds a Cheese by it's ID and displays it's info"""
  def __init__(self):
    """Initializes a new FindCheesePage"""
    super().__init__(inputName="CheeseId", enterAction=self.findCheese, headerLines = cheeseHeader, acceptLine = "Enter the ID of the Cheese to be viewed and hit enter, or press escape to exit")
  
  def findCheese(self, id):
    """Finds a cheese by it's ID and draws a CheeseInfoPage for it. If the ID was bad the cheese, the user is informed
    id - The id of the cheese to find"""
    cheese = DAO.get(id)
    if cheese is not None:
      CheeseInfoPage(cheese).draw()
    else:
      self.informLine = "Invalid ID"
      self.quitFlag = False

class RemoveCheesePage(InputPage):
  """An inplementation of InputPage that finds a Cheese by it's ID and remove it from the DB"""
  def __init__(self):
    """Initializes the RemoveCheesePage"""
    super().__init__(inputName="CheeseId", enterAction=self.deleteCheese, headerLines = cheeseHeader, acceptLine = "Enter the ID of the Cheese to remove and hit enter, or press escape to exit")

  def deleteCheese(self, id):
    """Finds a cheese by it's ID and removes it. If the ID was bad, the user is informed
    id - The id of the cheese to be removed"""
    if not DAO.delete(id):
      self.informLine = "Invalid ID"
      self.quitFlag = False

class SaveDataToFilePage(InputPage):
  """An inplementation of InputPage that accepts a filename and creates a csv file called the filename containing all cheeses in the DB"""
  def __init__(self):
    """Initializes a new SaveDataToFilePage"""
    super().__init__(inputName="Filename", enterAction=lambda a: dataLoader.saveCheeseData(a), headerLines = cheeseHeader, acceptLine = "Enter the name for the file and hit enter, or press escape to exit")