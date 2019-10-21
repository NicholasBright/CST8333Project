from CheeseView import CheeseView
from CheeseModel import CheeseModel
from CheeseDataLoader import CheeseDataLoader
from CheeseDAO import CheeseDAO

filename = "canadianCheeseDirectory.csv"
userInput = None
view = CheeseView()
dataLoader = CheeseDataLoader(filename, 200)
cheeseDAO = CheeseDAO()

#The following method was taken from this source:
#
#https://www.geeksforgeeks.org/clear-screen-python/
#Accessed On: 10/20/2019
#Author: mohit_negi, link: https://auth.geeksforgeeks.org/user/mohit_negi/articles
#
#I used it since it doesn't provide any required functionality
#The method clears the screen is an OS dependant way
# which I use because I think it makes the program
# look cleaner. I made poxis explicit in case you're on
# a different OS. The program still works just looks worse.
# define our clear function 

def saveCheeseFile():
  userInput = ""
  userMessage = ""
  while (userInput == "") | (userInput == "q"):
    view.clear()
    view.displayName()
    view.display(userMessage)
    userInput = view.accept("(Q)uit, or enter file name: ")
    if (userInput != "") & (userInput != "q"):
      userMessage = "Invalid input"

  if userInput != "q":
    dataLoader.saveCheeseData(userInput)

def displayCheeses():
  view.showCheeseList(cheeseDAO.getCheeses())

def createNewCheese():
  view.clear()
  view.display("Nicholas Bright")
  newCheese = CheeseModel()
  newCheese.CheeseNameEN = view.accept("CheeseNameEN:")
  newCheese.CheeseNameFR = view.accept("CheeseNameFR:")
  newCheese.ManufacturerNameEN = view.accept("ManufacturerNameEN:")
  newCheese.ManufacturerNameFR = view.accept("ManufacturerNameFR:")
  newCheese.ManufacturerProvCode = view.accept("ManufacturerProvCode:")
  newCheese.ManufacturingTypeEN = view.accept("ManufacturingTypeEN:")
  newCheese.ManufacturingTypeFR = view.accept("ManufacturingTypeFR:")
  newCheese.WebSiteEN = view.accept("WebSiteEN:")
  newCheese.WebSiteFR = view.accept("WebSiteFR:")
  newCheese.FatContentPercent = view.accept("FatContentPercent:")
  newCheese.MoisturePercent = view.accept("MoisturePercent:")
  newCheese.ParticularitiesEN = view.accept("ParticularitiesEN:")
  newCheese.ParticularitiesFR = view.accept("ParticularitiesFR:")
  newCheese.FlavourEN = view.accept("FlavourEN:")
  newCheese.FlavourFR = view.accept("FlavourFR:")
  newCheese.CharacteristicsEN = view.accept("CharacteristicsEN:")
  newCheese.CharacteristicsFR = view.accept("CharacteristicsFR:")
  newCheese.RipeningEN = view.accept("RipeningEN:")
  newCheese.RipeningFR = view.accept("RipeningFR:")
  newCheese.Organic = view.accept("Organic:")
  newCheese.CategoryTypeEN = view.accept("CategoryTypeEN:")
  newCheese.CategoryTypeFR = view.accept("CategoryTypeFR:")
  newCheese.MilkTypeEN = view.accept("MilkTypeEN:")
  newCheese.MilkTypeFR = view.accept("MilkTypeFR:")
  newCheese.MilkTreatmentTypeEN = view.accept("MilkTreatmentTypeEN:")
  newCheese.MilkTreatmentTypeFR = view.accept("MilkTreatmentTypeFR:")
  newCheese.RindTypeEN = view.accept("RindTypeEN:")
  newCheese.RindTypeFR = view.accept("RindTypeFR:")
  newCheese.LastUpdateDate = view.accept("LastUpdateDate:")
  cheeseDAO.putCheese(newCheese)

def viewCheese():
  view.clear()
  cheeseId = view.accept("ID of the cheese to view:")
  cheese = cheeseDAO.find(int(cheeseId))

  if cheese == None:
    view.display("Cheese with that ID not found.")
    view.enterToContinue()
  else:
    userMessage = ""
    recieved = ""
    while (recieved != "y") & (recieved != "n"):
      view.clear()
      view.displayLongformCheese(cheese)
      view.display(userMessage)
      recieved = view.accept("Modify this entry?:(y/n):")
      userMessage = "Invalid input"
    if recieved == "y":
      view.modifyCheeseMenu(cheese)

def removeCheese():
  view.clear()
  cheeseId = view.accept("ID of the cheese to remove:")
  if cheeseDAO.remove(int(cheeseId)):
    view.display("Cheese removed")
  else:
    view.display("Cheese wtih that ID not found")
  view.enterToContinue()

menuOptions = [
  "Reload the dataset",
  "Save data to file",
  "Display records",
  "Create new cheese",
  "Select, Display, or Edit Cheese",
  "Remove a cheese",
  "Quit"
  ]

view.setOptions( menuOptions )

quitFlag = 0
userMessage = None
while quitFlag == 0:
  view.clear()
  userInput = view.showMenu(userMessage)
  userMessage = None
  if(userInput == str(menuOptions.index("Reload the dataset")+1)):
    cheeseDAO.remove("ALL")
    dataLoader.readCheeseData(filename, 200)
    userMessage = "Dataset reloaded from disk"
  elif(userInput == str(menuOptions.index("Save data to file")+1)):
    saveCheeseFile()
  elif(userInput == str(menuOptions.index("Display records")+1)):
    displayCheeses()
  elif(userInput == str(menuOptions.index("Create new cheese")+1)):
    createNewCheese()
  elif(userInput == str(menuOptions.index("Select, Display, or Edit Cheese")+1)):
    viewCheese()
  elif(userInput == str(menuOptions.index("Remove a cheese")+1)):
    removeCheese()
  elif userInput == str(menuOptions.index("Quit")+1):
    quitFlag = 1
  else:
    userMessage = "Invalid input"