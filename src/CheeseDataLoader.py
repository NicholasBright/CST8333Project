from CheeseModel import CheeseModel
from CheeseDAO import CheeseDAO
import logging
import sys

class CheeseDataLoader:
  "Object that loads cheese data from a file"
  
  def __init__(self, filename = None, linesToRead = 0):
    self.headers = []
    if(filename != None):
      self.readCheeseData(filename, linesToRead)
  
  def readCheeseData ( self, filename, linesToRead ) -> CheeseDAO:
    if(filename == None):
      exit
    #Open the file
    try:
      cheeseFile = open(filename, encoding="utf8")
      #I save this now because it might be useful in the future
      #For now, I just use it to find the index of the data I am looking
      # from the line once it has been split. MilkTypeEn has the same index
      # in the headers and the data, so I can use headers.index("MilkTypeEn")
      # to get the index and pull from the split line at that index for the data
      self.headers = cheeseFile.readline().replace("\ufeff","").replace("\n","").split(",")
    except (FileNotFoundError):
      print("\"", filename, "\" not found. Please place \"", filename, "\" in the same directory as the program.", sep="")
      exit

    cheeseDAO = CheeseDAO()
    recordsRead = 0
    #Reading in the number of lines specified by 
    # linesToRead and creating an object for each
    for cheeseDataLine in cheeseFile:
      cheese = self.readCheeseDataLine(cheeseDataLine.replace("\n",""))
      cheeseDAO.putCheese(cheese)
      cheeseDAO.insertCheese(cheese)
      recordsRead += 1
      if recordsRead >= linesToRead:
        break
    input(cheeseDAO.getCheeses().__len__())
    return cheeseDAO

  def readCheeseDataLine ( self, cheeseData ):
    "Converts a line from the data csv file into a CheeseModel.Cheese"
    fields = cheeseData.split(",")
    fieldIndex = 0
    while fieldIndex < len(fields):
      if fields[fieldIndex].startswith("\""):
        newField = fields[fieldIndex]
        while(newField.count("\"") % 2 == 1):
          newField += ","
          newField = newField.__add__(fields[fieldIndex + 1])
          fields.remove(fields[fieldIndex + 1])
        fields[fieldIndex] = newField
      fieldIndex += 1

    newCheese = CheeseModel(int(fields[self.headers.index("CheeseId")]))
    newCheese.CheeseNameEN = fields[self.headers.index("CheeseNameEn")]
    newCheese.CheeseNameFR = fields[self.headers.index("CheeseNameFr")]
    newCheese.ManufacturerNameEN = fields[self.headers.index("ManufacturerNameEn")]
    newCheese.ManufacturerNameFR = fields[self.headers.index("ManufacturerNameFr")]
    newCheese.ManufacturerProvCode = fields[self.headers.index("ManufacturerProvCode")]
    newCheese.ManufacturingTypeEN = fields[self.headers.index("ManufacturingTypeEn")]
    newCheese.ManufacturingTypeFR = fields[self.headers.index("ManufacturingTypeFr")]
    newCheese.WebSiteEN = fields[self.headers.index("WebSiteEn")]
    newCheese.WebSiteFR = fields[self.headers.index("WebSiteFr")]
    newCheese.FatContentPercent = fields[self.headers.index("FatContentPercent")]
    if newCheese.FatContentPercent == "":  newCheese.FatContentPercent = None
    newCheese.MoisturePercent = fields[self.headers.index("MoisturePercent")]
    if newCheese.MoisturePercent == "":  newCheese.MoisturePercent = None
    newCheese.ParticularitiesEN = fields[self.headers.index("ParticularitiesEn")]
    newCheese.ParticularitiesFR = fields[self.headers.index("ParticularitiesFr")]
    newCheese.FlavourEN = fields[self.headers.index("FlavourEn")]
    newCheese.FlavourFR = fields[self.headers.index("FlavourFr")]
    newCheese.CharacteristicsEN = fields[self.headers.index("CharacteristicsEn")]
    newCheese.CharacteristicsFR = fields[self.headers.index("CharacteristicsFr")]
    newCheese.RipeningEN = fields[self.headers.index("RipeningEn")]
    newCheese.RipeningFR = fields[self.headers.index("RipeningFr")]
    newCheese.Organic = fields[self.headers.index("Organic")]
    newCheese.CategoryTypeEN = fields[self.headers.index("CategoryTypeEn")]
    newCheese.CategoryTypeFR = fields[self.headers.index("CategoryTypeFr")]
    newCheese.MilkTypeEN = fields[self.headers.index("MilkTypeEn")]
    newCheese.MilkTypeFR = fields[self.headers.index("MilkTypeFr")]
    newCheese.MilkTreatmentTypeEN = fields[self.headers.index("MilkTreatmentTypeEn")]
    newCheese.MilkTreatmentTypeFR = fields[self.headers.index("MilkTreatmentTypeFr")]
    newCheese.RindTypeEN = fields[self.headers.index("RindTypeEn")]
    newCheese.RindTypeFR = fields[self.headers.index("RindTypeFr")]
    newCheese.LastUpdateDate = fields[self.headers.index("LastUpdateDate")]
    return newCheese

  def saveCheeseData(self, filename):
    filename = filename.__str__()
    saveToFile = open(filename+".csv", "w", encoding="utf8")
    for header in self.headers:
      saveToFile.write(header)
      if(self.headers.index(header)+1 != len(self.headers)):
        saveToFile.write(',')
    saveToFile.write("\n")
    for cheese in CheeseDAO().getCheeses():
      saveToFile.write(self.__generateCheeseCSVLine__(cheese) + "\n")
    input("Completed successfully. Press enter to contue")

  def __generateCheeseCSVLine__(self, cheese ) -> "":
    cheeseStr = ""
    separator = ","
    cheeseStr = cheeseStr.__add__(str(cheese.CheeseId))
    cheeseStr = cheeseStr.__add__(separator)
    cheeseStr = cheeseStr.__add__(cheese.CheeseNameEN)
    cheeseStr = cheeseStr.__add__(separator)
    cheeseStr = cheeseStr.__add__(cheese.CheeseNameFR)
    cheeseStr = cheeseStr.__add__(separator)
    cheeseStr = cheeseStr.__add__(cheese.ManufacturerNameEN)
    cheeseStr = cheeseStr.__add__(separator)
    cheeseStr = cheeseStr.__add__(cheese.ManufacturerNameFR)
    cheeseStr = cheeseStr.__add__(separator)
    cheeseStr = cheeseStr.__add__(cheese.ManufacturerProvCode)
    cheeseStr = cheeseStr.__add__(separator)
    cheeseStr = cheeseStr.__add__(cheese.ManufacturingTypeEN)
    cheeseStr = cheeseStr.__add__(separator)
    cheeseStr = cheeseStr.__add__(cheese.ManufacturingTypeFR)
    cheeseStr = cheeseStr.__add__(separator)
    cheeseStr = cheeseStr.__add__(cheese.WebSiteEN)
    cheeseStr = cheeseStr.__add__(separator)
    cheeseStr = cheeseStr.__add__(cheese.WebSiteFR)
    cheeseStr = cheeseStr.__add__(separator)
    cheeseStr = cheeseStr.__add__(cheese.FatContentPercent)
    cheeseStr = cheeseStr.__add__(separator)
    cheeseStr = cheeseStr.__add__(cheese.MoisturePercent)
    cheeseStr = cheeseStr.__add__(separator)
    cheeseStr = cheeseStr.__add__(cheese.ParticularitiesEN)
    cheeseStr = cheeseStr.__add__(separator)
    cheeseStr = cheeseStr.__add__(cheese.ParticularitiesFR)
    cheeseStr = cheeseStr.__add__(separator)
    cheeseStr = cheeseStr.__add__(cheese.FlavourEN)
    cheeseStr = cheeseStr.__add__(separator)
    cheeseStr = cheeseStr.__add__(cheese.FlavourFR)
    cheeseStr = cheeseStr.__add__(separator)
    cheeseStr = cheeseStr.__add__(cheese.CharacteristicsEN)
    cheeseStr = cheeseStr.__add__(separator)
    cheeseStr = cheeseStr.__add__(cheese.CharacteristicsFR)
    cheeseStr = cheeseStr.__add__(separator)
    cheeseStr = cheeseStr.__add__(cheese.RipeningEN)
    cheeseStr = cheeseStr.__add__(separator)
    cheeseStr = cheeseStr.__add__(cheese.RipeningFR)
    cheeseStr = cheeseStr.__add__(separator)
    cheeseStr = cheeseStr.__add__(cheese.Organic)
    cheeseStr = cheeseStr.__add__(separator)
    cheeseStr = cheeseStr.__add__(cheese.CategoryTypeEN)
    cheeseStr = cheeseStr.__add__(separator)
    cheeseStr = cheeseStr.__add__(cheese.CategoryTypeFR)
    cheeseStr = cheeseStr.__add__(separator)
    cheeseStr = cheeseStr.__add__(cheese.MilkTypeEN)
    cheeseStr = cheeseStr.__add__(separator)
    cheeseStr = cheeseStr.__add__(cheese.MilkTypeFR)
    cheeseStr = cheeseStr.__add__(separator)
    cheeseStr = cheeseStr.__add__(cheese.MilkTreatmentTypeEN)
    cheeseStr = cheeseStr.__add__(separator)
    cheeseStr = cheeseStr.__add__(cheese.MilkTreatmentTypeFR)
    cheeseStr = cheeseStr.__add__(separator)
    cheeseStr = cheeseStr.__add__(cheese.RindTypeEN)
    cheeseStr = cheeseStr.__add__(separator)
    cheeseStr = cheeseStr.__add__(cheese.RindTypeFR)
    cheeseStr = cheeseStr.__add__(separator)
    cheeseStr = cheeseStr.__add__(cheese.LastUpdateDate)
    return cheeseStr.replace("\n","")