from os import system, name
from CheeseDAO import CheeseDAO
from CheeseModel import CheeseModel
import math
import re
class CheeseView:
  "A menu for reading cheese data"

  def __init__(self):
    self.quitFlag = 0
    self.options = []
    self.cheeseDAO = CheeseDAO.instance

  #The following method was taken from this source:
  #
  #https://www.geeksforgeeks.org/clear-screen-python/
  #Accessed On: 10/20/2019
  #Author: mohit_negi
  #Link to profile: https://auth.geeksforgeeks.org/user/mohit_negi/articles
  #
  #I used it since it doesn't provide any required functionality
  #The method clears the screen is an OS dependant way
  # which I use because I think it makes the program
  # look cleaner. I made poxis explicit in case you're on
  # a different OS. The program still works just looks worse.
  # define our clear function 
  def clear(self):
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
    # for mac and linux(here, os.name is 'posix') 
    elif name == 'posix': 
        _ = system('clear')

  def showCheeseList(self, cheeseList):
    userMessage = ""
    pageCount = 1
    displayedPerPage = 10
    self.clear()
    self.displayName()
    if len(cheeseList) == 0:
      self.display("There are no cheeses to show")
      self.enterToContinue()
    while ((pageCount-1) * displayedPerPage) < len(cheeseList):
      displayCount = 0
      while(displayCount < displayedPerPage) & ((pageCount -1)*displayedPerPage + displayCount < len(cheeseList)):
        self.displayCheeseSummaryInfo(cheeseList[(pageCount -1)*displayedPerPage + displayCount])
        displayCount += 1
      self.display("Page (" + str(pageCount) + "/" + str(int(math.ceil(len(cheeseList)/displayedPerPage))) + ")")
      self.display(userMessage)
      userInput = self.accept("Input: (Q)uit, (N)ext, (P)rev, (S)ort, or enter ID for details:(N) ")
      if userInput == "q":
        break
      elif re.match("\\d+",userInput) is not None:
        cheese = self.cheeseDAO.getCheese(int(userInput))
        if cheese != None:
          self.clear()
          self.displayName()
          self.displayLongformCheese(cheese)
          self.enterToContinue()
        else:
          userMessage = "ID not found"
      elif (userInput == "n") | (userInput == ""):
        pageCount += 1
        if pageCount > len(cheeseList):
          break
      elif userInput == "p":
        pageCount -= 1
        if pageCount < 1:
          pageCount = 1
      elif userInput == "s":
        self.clear()
        self.displayName()
        attr = self.accept("What attribute do you want to sort on? ")
        if hasattr(CheeseModel(),attr):
          reverse = (self.accept("Reserve order? (No by default, anything else for yes)") == "")
          cheeseList.sort(key=lambda x: getattr(x, attr), reverse=reverse)
        else:
          self.display("Cheeses don't have that attribute")
          self.enterToContinue()

  def showMenu(self):
    self.displayName()
    self.displayMenuOptions()

  def displayMenuOptions (self):
    for option in self.options:
      self.display("(" + str(self.options.index(option) + 1) + ") - " + option)
  
  def getOptions(self):
    return self.options

  def setOptions(self, options = []):
    self.options = options

  def display(self, message):
    print(message)
  
  def accept(self, message):
    return input(message)

  def modifyCheeseMenu(self, cheese):
    self.displayName()
    userInput = input("CheeseNameEN(" + str(cheese.CheeseNameEN) + ")")
    if userInput != "":
      cheese.CheeseNameEN = userInput
    userInput = input("CheeseNameFR(" + str(cheese.CheeseNameFR) + ")")
    if userInput != "":
      cheese.CheeseNameFR = userInput
    userInput = input("ManufacturerNameEN(" + str(cheese.ManufacturerNameEN) + ")")
    if userInput != "":
      cheese.ManufacturerNameEN = userInput
    userInput = input("ManufacturerNameFR(" + str(cheese.ManufacturerNameFR) + ")")
    if userInput != "":
      cheese.ManufacturerNameFR = userInput
    userInput = input("ManufacturerProvCode(" + str(cheese.ManufacturerProvCode) + ")")
    if userInput != "":
      cheese.ManufacturerProvCode = userInput
    userInput = input("ManufacturingTypeEN(" + str(cheese.ManufacturingTypeEN) + ")")
    if userInput != "":
      cheese.ManufacturingTypeEN = userInput
    userInput = input("ManufacturingTypeFR(" + str(cheese.ManufacturingTypeFR) + ")")
    if userInput != "":
      cheese.ManufacturingTypeFR = userInput
    userInput = input("WebSiteEN(" + str(cheese.WebSiteEN) + ")")
    if userInput != "":
      cheese.WebSiteEN = userInput
    userInput = input("WebSiteFR(" + str(cheese.WebSiteFR) + ")")
    if userInput != "":
      cheese.WebSiteFR = userInput
    userInput = input("FatContentPercent(" + str(cheese.FatContentPercent) + ")")
    if userInput != "":
      cheese.FatContentPercent = userInput
    userInput = input("MoisturePercent(" + str(cheese.MoisturePercent) + ")")
    if userInput != "":
      cheese.MoisturePercent = userInput
    userInput = input("ParticularitiesEN(" + str(cheese.ParticularitiesEN) + ")")
    if userInput != "":
      cheese.ParticularitiesEN = userInput
    userInput = input("ParticularitiesFR(" + str(cheese.ParticularitiesFR) + ")")
    if userInput != "":
      cheese.ParticularitiesFR = userInput
    userInput = input("FlavourEN(" + str(cheese.FlavourEN) + ")")
    if userInput != "":
      cheese.FlavourEN = userInput
    userInput = input("FlavourFR(" + str(cheese.FlavourFR) + ")")
    if userInput != "":
      cheese.FlavourFR = userInput
    userInput = input("CharacteristicsEN(" + str(cheese.CharacteristicsEN) + ")")
    if userInput != "":
      cheese.CharacteristicsEN = userInput
    userInput = input("CharacteristicsFR(" + str(cheese.CharacteristicsFR)+ ")")
    if userInput != "":
      cheese.CharacteristicsFR = userInput
    userInput = input("RipeningEN(" + str(cheese.RipeningEN) + ")")
    if userInput != "":
      cheese.RipeningEN = userInput
    userInput = input("RipeningFR(" + str(cheese.RipeningFR) + ")")
    if userInput != "":
      cheese.RipeningFR = userInput
    userInput = input("Organic(" + str(cheese.Organic) + ")")
    if userInput != "":
      cheese.Organic = userInput
    userInput = input("CategoryTypeEN(" + str(cheese.CategoryTypeEN) + ")")
    if userInput != "":
      cheese.CategoryTypeEN = userInput
    userInput = input("CategoryTypeFR(" + str(cheese.CategoryTypeFR) + ")")
    if userInput != "":
      cheese.CategoryTypeFR = userInput
    userInput = input("MilkTypeEN(" + str(cheese.MilkTypeEN) + ")")
    if userInput != "":
      cheese.MilkTypeEN = userInput
    userInput = input("MilkTypeFR(" + str(cheese.MilkTypeFR) + ")")
    if userInput != "":
      cheese.MilkTypeFR = userInput
    userInput = input("MilkTreatmentTypeEN(" + str(cheese.MilkTreatmentTypeEN) + ")")
    if userInput != "":
      cheese.MilkTreatmentTypeEN = userInput
    userInput = input("MilkTreatmentTypeFR(" + str(cheese.MilkTreatmentTypeFR) + ")")
    if userInput != "":
      cheese.MilkTreatmentTypeFR = userInput
    userInput = input("RindTypeEN(" + str(cheese.RindTypeEN) + ")")
    if userInput != "":
      cheese.RindTypeEN = userInput
    userInput = input("RindTypeFR(" + str(cheese.RindTypeFR) + ")")
    if userInput != "":
      cheese.RindTypeFR = userInput
    userInput = input("LastUpdateDate(" + str(cheese.LastUpdateDate) + ")")
    if userInput != "":
      cheese.LastUpdateDate = userInput
  
  def enterToContinue(self):
    input("Press enter to continue")

  def displayCheeseSummaryInfo(self, cheese):
    self.display(str(cheese.CheeseId) + ": " + 
      ("Unknown" if cheese.CheeseNameEN == None else cheese.CheeseNameEN) 
      + " made by " + 
      ("Unknown" if cheese.ManufacturerNameEN == None else cheese.ManufacturerNameEN)
      + ", Province: " +
      ("Unknown" if cheese.ManufacturerProvCode == None else cheese.ManufacturerProvCode)
      + ", Type: " +
      ("Unknown" if cheese.ManufacturingTypeEN == None else cheese.ManufacturingTypeEN))

  def displayLongformCheese(self, cheese):
    self.displayCheeseSummaryInfo(cheese)
    self.display("WebSite: " + ("Unknown" if cheese.WebSiteEN == None else cheese.WebSiteEN))
    self.display("FatContentPercent: " + ("Unknown" if cheese.FatContentPercent == None else str(cheese.FatContentPercent)))
    self.display("MoisturePercent: " + ("Unknown" if cheese.MoisturePercent == None else str(cheese.MoisturePercent)))
    self.display("Particularities: " + ("Unknown" if cheese.ParticularitiesEN == None else cheese.ParticularitiesEN))
    self.display("Flavour: " + ("Unknown" if cheese.FlavourEN == None else cheese.FlavourEN))
    self.display("Characteristics: " + ("Unknown" if cheese.CharacteristicsEN == None else cheese.CharacteristicsEN))
    self.display("Ripening: " + ("Unknown" if cheese.RipeningEN == None else cheese.RipeningEN))
    self.display("Organic: " + ("Yes" if cheese.Organic == "1" else "No"))
    self.display("CategoryType: " + ("Unknown" if cheese.CategoryTypeEN == None else cheese.CategoryTypeEN))
    self.display("MilkType: " + ("Unknown" if cheese.MilkTypeEN == None else cheese.MilkTypeEN))
    self.display("MilkTreatmentType: " + ("Unknown" if cheese.MilkTreatmentTypeEN == None else cheese.MilkTreatmentTypeEN))
    self.display("RindType: " + ("Unknown" if cheese.RindTypeEN == None else cheese.RindTypeEN))
    self.display("LastUpdateDate: " + ("Unknown" if cheese.LastUpdateDate == None else str(cheese.LastUpdateDate)))
  
  def displayName(self):
    self.display("Nicholas Bright")