from os import system, name
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
def clear():
  # for windows 
  if name == 'nt': 
      _ = system('cls') 
  # for mac and linux(here, os.name is 'posix') 
  elif name == 'posix': 
      _ = system('clear')

def saveCheeseFile():
  clear()
  dataLoader.saveCheeseData(input("File name:"))
  exit

def displayCheeses():
  clear()
  for cheese in cheeseDAO.getCheeses():
    print(cheese)
  menu.enterToContinue()

def createNewCheese():
  clear()
  menu.display("Nicholas Bright")
  newCheese = CheeseModel()
  newCheese.CheeseNameEN = menu.accept("CheeseNameEN:")
  newCheese.CheeseNameFR = input("CheeseNameFR:")
  newCheese.ManufacturerNameEN = input("ManufacturerNameEN:")
  newCheese.ManufacturerNameFR = input("ManufacturerNameFR:")
  newCheese.ManufacturerProvCode = input("ManufacturerProvCode:")
  newCheese.ManufacturingTypeEN = input("ManufacturingTypeEN:")
  newCheese.ManufacturingTypeFR = input("ManufacturingTypeFR:")
  newCheese.WebSiteEN = input("WebSiteEN:")
  newCheese.WebSiteFR = input("WebSiteFR:")
  newCheese.FatContentPercent = input("FatContentPercent:")
  newCheese.MoisturePercent = input("MoisturePercent:")
  newCheese.ParticularitiesEN = input("ParticularitiesEN:")
  newCheese.ParticularitiesFR = input("ParticularitiesFR:")
  newCheese.FlavourEN = input("FlavourEN:")
  newCheese.FlavourFR = input("FlavourFR:")
  newCheese.CharacteristicsEN = input("CharacteristicsEN:")
  newCheese.CharacteristicsFR = input("CharacteristicsFR:")
  newCheese.RipeningEN = input("RipeningEN:")
  newCheese.RipeningFR = input("RipeningFR:")
  newCheese.Organic = input("Organic:")
  newCheese.CategoryTypeEN = input("CategoryTypeEN:")
  newCheese.CategoryTypeFR = input("CategoryTypeFR:")
  newCheese.MilkTypeEN = input("MilkTypeEN:")
  newCheese.MilkTypeFR = input("MilkTypeFR:")
  newCheese.MilkTreatmentTypeEN = input("MilkTreatmentTypeEN:")
  newCheese.MilkTreatmentTypeFR = input("MilkTreatmentTypeFR:")
  newCheese.RindTypeEN = input("RindTypeEN:")
  newCheese.RindTypeFR = input("RindTypeFR:")
  newCheese.LastUpdateDate = input("LastUpdateDate:")
  cheeseDAO.putCheese(newCheese)

def viewCheese():
  clear()
  cheeseId = input("ID of the cheese to view:")
  cheese = cheeseDAO.find(int(cheeseId))

  if cheese == None:
    print("Cheese with that ID not found.")
    menu.enterToContinue()
  else:
    userMessage = ""
    recieved = ""
    while (recieved != "y") & (recieved != "n"):
      clear()
      menu.display(cheese)
      menu.display(userMessage)
      recieved = menu.accept("Modify this entry?:(y/n):")
      userMessage = "Invalid input"
    if recieved == "y":
      menu.modifyCheeseMenu(cheese)

def removeCheese():
  clear()
  cheeseId = input("ID of the cheese to remove:")
  if cheeseDAO.remove(int(cheeseId)):
    print("Cheese removed")
  else:
    print("Cheese wtih that ID not found")
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
  clear()
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