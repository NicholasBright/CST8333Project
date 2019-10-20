from CheeseMenu import CheeseMenu
from CheeseModel import CheeseModel
from CheeseDataLoader import CheeseDataLoader
from CheeseDAO import CheeseDAO

filename = "canadianCheeseDirectory.csv"
userInput = None
menu = CheeseMenu()
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
  menu.clear()
  dataLoader.saveCheeseData(menu.accept("File name:"))
  exit

def displayCheeses():
  menu.showCheeseList(cheeseDAO.getCheeses())

def createNewCheese():
  menu.clear()
  menu.display("Nicholas Bright")
  newCheese = CheeseModel()
  newCheese.CheeseNameEN = menu.accept("CheeseNameEN:")
  newCheese.CheeseNameFR = menu.accept("CheeseNameFR:")
  newCheese.ManufacturerNameEN = menu.accept("ManufacturerNameEN:")
  newCheese.ManufacturerNameFR = menu.accept("ManufacturerNameFR:")
  newCheese.ManufacturerProvCode = menu.accept("ManufacturerProvCode:")
  newCheese.ManufacturingTypeEN = menu.accept("ManufacturingTypeEN:")
  newCheese.ManufacturingTypeFR = menu.accept("ManufacturingTypeFR:")
  newCheese.WebSiteEN = menu.accept("WebSiteEN:")
  newCheese.WebSiteFR = menu.accept("WebSiteFR:")
  newCheese.FatContentPercent = menu.accept("FatContentPercent:")
  newCheese.MoisturePercent = menu.accept("MoisturePercent:")
  newCheese.ParticularitiesEN = menu.accept("ParticularitiesEN:")
  newCheese.ParticularitiesFR = menu.accept("ParticularitiesFR:")
  newCheese.FlavourEN = menu.accept("FlavourEN:")
  newCheese.FlavourFR = menu.accept("FlavourFR:")
  newCheese.CharacteristicsEN = menu.accept("CharacteristicsEN:")
  newCheese.CharacteristicsFR = menu.accept("CharacteristicsFR:")
  newCheese.RipeningEN = menu.accept("RipeningEN:")
  newCheese.RipeningFR = menu.accept("RipeningFR:")
  newCheese.Organic = menu.accept("Organic:")
  newCheese.CategoryTypeEN = menu.accept("CategoryTypeEN:")
  newCheese.CategoryTypeFR = menu.accept("CategoryTypeFR:")
  newCheese.MilkTypeEN = menu.accept("MilkTypeEN:")
  newCheese.MilkTypeFR = menu.accept("MilkTypeFR:")
  newCheese.MilkTreatmentTypeEN = menu.accept("MilkTreatmentTypeEN:")
  newCheese.MilkTreatmentTypeFR = menu.accept("MilkTreatmentTypeFR:")
  newCheese.RindTypeEN = menu.accept("RindTypeEN:")
  newCheese.RindTypeFR = menu.accept("RindTypeFR:")
  newCheese.LastUpdateDate = menu.accept("LastUpdateDate:")
  cheeseDAO.putCheese(newCheese)

def viewCheese():
  menu.clear()
  cheeseId = menu.accept("ID of the cheese to view:")
  cheese = cheeseDAO.find(int(cheeseId))

  if cheese == None:
    menu.display("Cheese with that ID not found.")
    menu.enterToContinue()
  else:
    userMessage = ""
    recieved = ""
    while (recieved != "y") & (recieved != "n"):
      menu.clear()
      menu.display(cheese)
      menu.display(userMessage)
      recieved = menu.accept("Modify this entry?:(y/n):")
      userMessage = "Invalid input"
    if recieved == "y":
      menu.modifyCheeseMenu(cheese)

def removeCheese():
  menu.clear()
  cheeseId = menu.accept("ID of the cheese to remove:")
  if cheeseDAO.remove(int(cheeseId)):
    menu.display("Cheese removed")
  else:
    menu.display("Cheese wtih that ID not found")
  menu.enterToContinue()

menuOptions = [
  "Reload the dataset",
  "Save data to file",
  "Display records",
  "Create new cheese",
  "Select, Display, or Edit Cheese",
  "Remove a cheese",
  "Quit"
  ]

menu.setOptions( menuOptions )

quitFlag = 0
userMessage = None
while quitFlag == 0:
  menu.clear()
  userInput = menu.showMenu(userMessage)
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