class CheeseMenu:
  "A menu for reading cheese data"

  def __init__(self):
    self.quitFlag = 0
    self.options = []

  def showMenu(self, userMessage = None ):
    print("Nicholas Bright")
    self.printMenuOptions()
    if userMessage == None:
      userMessage = ""
    return input(userMessage.__add__("\n") + "Selection: ")

  def printMenuOptions (self):
    for option in self.options:
      print("(", self.options.index(option) + 1, ") - ", option, sep="")
    exit
  
  def getOptions(self):
    return self.options

  def setOptions(self, options = []):
    self.options = options

  def display(self, message):
    print(message)
  
  def accept(self, message):
    return input(message)

  def modifyCheeseMenu(self, cheese):
    print("Nicholas Bright")
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