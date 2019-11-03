from os import system, name
from CheeseDAO import CheeseDAO
import math
import re

class CheeseView:
  "A menu for reading cheese data"

  cheeseDAO = CheeseDAO()

  def __init__(self):
    self.quitFlag = 0
    self.options = []

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
    while ((pageCount-1) * displayedPerPage) < len(cheeseList):
      self.clear()
      self.displayName()
      displayCount = 0
      while(displayCount < displayedPerPage) & ((pageCount -1)*displayedPerPage + displayCount < len(cheeseList)):
        self.displayCheeseSummaryInfo(cheeseList[(pageCount -1)*displayedPerPage + displayCount])
        displayCount += 1
      self.display("Page (" + str(pageCount) + "/" + str(int(math.ceil(len(cheeseList)/displayedPerPage))) + ")")
      self.display(userMessage)
      userInput = self.accept("Input: (Q)uit, (N)ext, (P)rev, or enter ID for details:(N) ")
      if userInput == "q":
        break
      elif re.match("\\d+",userInput) is not None:
        cheese = self.cheeseDAO.find(int(userInput))
        if cheese != None:
          self.clear()
          self.displayName()
          self.displayLongformCheese(cheese)
          self.enterToContinue()
        userMessage = "ID not found"
      elif (userInput == "n") | (userInput == ""):
        pageCount += 1
        if pageCount > len(cheeseList):
          break
      elif userInput == "p":
        pageCount -= 1
        if pageCount < 1:
          pageCount = 1

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
    userInput = input("CheeseNameEN(" + cheese.CheeseNameEN + ")")
    if userInput != "":
      cheese.CheeseNameEN = userInput
    userInput = input("CheeseNameFR(" + cheese.CheeseNameFR + ")")
    if userInput != "":
      cheese.CheeseNameFR = userInput
    userInput = input("ManufacturerNameEN(" + cheese.ManufacturerNameEN + ")")
    if userInput != "":
      cheese.ManufacturerNameEN = userInput
    userInput = input("ManufacturerNameFR(" + cheese.ManufacturerNameFR + ")")
    if userInput != "":
      cheese.ManufacturerNameFR = userInput
    userInput = input("ManufacturerProvCode(" + cheese.ManufacturerProvCode + ")")
    if userInput != "":
      cheese.ManufacturerProvCode = userInput
    userInput = input("ManufacturingTypeEN(" + cheese.ManufacturingTypeEN + ")")
    if userInput != "":
      cheese.ManufacturingTypeEN = userInput
    userInput = input("ManufacturingTypeFR(" + cheese.ManufacturingTypeFR + ")")
    if userInput != "":
      cheese.ManufacturingTypeFR = userInput
    userInput = input("WebSiteEN(" + cheese.WebSiteEN + ")")
    if userInput != "":
      cheese.WebSiteEN = userInput
    userInput = input("WebSiteFR(" + cheese.WebSiteFR + ")")
    if userInput != "":
      cheese.WebSiteFR = userInput
    userInput = input("FatContentPercent(" + cheese.FatContentPercent + ")")
    if userInput != "":
      cheese.FatContentPercent = userInput
    userInput = input("MoisturePercent(" + cheese.MoisturePercent + ")")
    if userInput != "":
      cheese.MoisturePercent = userInput
    userInput = input("ParticularitiesEN(" + cheese.ParticularitiesEN + ")")
    if userInput != "":
      cheese.ParticularitiesEN = userInput
    userInput = input("ParticularitiesFR(" + cheese.ParticularitiesFR + ")")
    if userInput != "":
      cheese.ParticularitiesFR = userInput
    userInput = input("FlavourEN(" + cheese.FlavourEN + ")")
    if userInput != "":
      cheese.FlavourEN = userInput
    userInput = input("FlavourFR(" + cheese.FlavourFR + ")")
    if userInput != "":
      cheese.FlavourFR = userInput
    userInput = input("CharacteristicsEN(" + cheese.CharacteristicsEN + ")")
    if userInput != "":
      cheese.CharacteristicsEN = userInput
    userInput = input("CharacteristicsFR(" + cheese.CharacteristicsFR + ")")
    if userInput != "":
      cheese.CharacteristicsFR = userInput
    userInput = input("RipeningEN(" + cheese.RipeningEN + ")")
    if userInput != "":
      cheese.RipeningEN = userInput
    userInput = input("RipeningFR(" + cheese.RipeningFR + ")")
    if userInput != "":
      cheese.RipeningFR = userInput
    userInput = input("Organic(" + cheese.Organic + ")")
    if userInput != "":
      cheese.Organic = userInput
    userInput = input("CategoryTypeEN(" + cheese.CategoryTypeEN + ")")
    if userInput != "":
      cheese.CategoryTypeEN = userInput
    userInput = input("CategoryTypeFR(" + cheese.CategoryTypeFR + ")")
    if userInput != "":
      cheese.CategoryTypeFR = userInput
    userInput = input("MilkTypeEN(" + cheese.MilkTypeEN + ")")
    if userInput != "":
      cheese.MilkTypeEN = userInput
    userInput = input("MilkTypeFR(" + cheese.MilkTypeFR + ")")
    if userInput != "":
      cheese.MilkTypeFR = userInput
    userInput = input("MilkTreatmentTypeEN(" + cheese.MilkTreatmentTypeEN + ")")
    if userInput != "":
      cheese.MilkTreatmentTypeEN = userInput
    userInput = input("MilkTreatmentTypeFR(" + cheese.MilkTreatmentTypeFR + ")")
    if userInput != "":
      cheese.MilkTreatmentTypeFR = userInput
    userInput = input("RindTypeEN(" + cheese.RindTypeEN + ")")
    if userInput != "":
      cheese.RindTypeEN = userInput
    userInput = input("RindTypeFR(" + cheese.RindTypeFR + ")")
    if userInput != "":
      cheese.RindTypeFR = userInput
    userInput = input("LastUpdateDate(" + cheese.LastUpdateDate + ")")
    if userInput != "":
      cheese.LastUpdateDate = userInput
  
  def enterToContinue(self):
    input("Press enter to continue")

  def displayCheeseSummaryInfo(self, cheese):
    self.display(str(cheese.CheeseId) + ": " + 
      ("Unknown" if cheese.CheeseNameEN == "" else cheese.CheeseNameEN) 
      + " made by " + 
      ("Unknown" if cheese.ManufacturerNameEN == "" else cheese.ManufacturerNameEN)
      + ", Province: " +
      ("Unknown" if cheese.ManufacturerProvCode == "" else cheese.ManufacturerProvCode)
      + ", Type: " +
      ("Unknown" if cheese.ManufacturingTypeEN == "" else cheese.ManufacturingTypeEN))

  def displayLongformCheese(self, cheese):
    self.displayCheeseSummaryInfo(cheese)
    self.display("WebSite: " + ("Unknown" if cheese.WebSiteEN == "" else cheese.WebSiteEN))
    self.display("FatContentPercent: " + ("Unknown" if cheese.FatContentPercent == "" else cheese.FatContentPercent))
    self.display("MoisturePercent: " + ("Unknown" if cheese.MoisturePercent == "" else cheese.MoisturePercent))
    self.display("Particularities: " + ("Unknown" if cheese.ParticularitiesEN == "" else cheese.ParticularitiesEN))
    self.display("Flavour: " + ("Unknown" if cheese.FlavourEN == "" else cheese.FlavourEN))
    self.display("Characteristics: " + ("Unknown" if cheese.CharacteristicsEN == "" else cheese.CharacteristicsEN))
    self.display("Ripening: " + ("Unknown" if cheese.RipeningEN == "" else cheese.RipeningEN))
    self.display("Organic: " + ("Yes" if cheese.Organic == "1" else "No"))
    self.display("CategoryType: " + ("Unknown" if cheese.CategoryTypeEN == "" else cheese.CategoryTypeEN))
    self.display("MilkType: " + ("Unknown" if cheese.MilkTypeEN == "" else cheese.MilkTypeEN))
    self.display("MilkTreatmentType: " + ("Unknown" if cheese.MilkTreatmentTypeEN == "" else cheese.MilkTreatmentTypeEN))
    self.display("RindType: " + ("Unknown" if cheese.RindTypeEN == "" else cheese.RindTypeEN))
    self.display("LastUpdateDate: " + ("Unknown" if cheese.LastUpdateDate == "" else cheese.LastUpdateDate))
  
  def displayName(self):
    self.display("Nicholas Bright")