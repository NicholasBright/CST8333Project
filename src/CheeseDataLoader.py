from CheeseModel import CheeseModel
from CheeseDAO import CheeseDAO
import datetime
import logging
import sys

class CheeseDataLoader:
  "Object that loads cheese data from a file and sends them to the DB"
  
  resourceFolder = "resources/"
  savedListFolder = "lists/"

  def __init__(self, filename = None, linesToRead = 0):
    "Creates a new CheeseDataLoader and if a filename is supplied begins reading that file into the DB"
    self.headers = []
    self.cheeseFile = None
    self.cheeseDAO = CheeseDAO.instance
    if(filename != None):
      self.openCheeseFile(filename)
      self.readCheeseData(linesToRead)
  
  def openCheeseFile(self, filename):
    "Opens a file that contains cheese data"
    self.cheeseFile = open(CheeseDataLoader.resourceFolder + filename, encoding="utf8")
  
  def readCheeseData (self, linesToRead = -1):
    "Read Cheese data from a file. It will read the number of lines specified, the default value reads all lines."
    # I just use this to find the index of the data I am looking
    # from the line once it has been split. MilkTypeEn has the same index
    # in the headers and the data, so I can use headers.index("MilkTypeEn")
    # to get the index and pull from the split line at that index for the data
    self.headers = self.cheeseFile.readline().replace("\ufeff","").replace("\n","").split(",")

    recordsRead = 0
    #Reading in the number of lines specified by 
    # linesToRead and creating an object for each
    for cheeseDataLine in self.cheeseFile:
      if recordsRead >= linesToRead & linesToRead != -1:
        break
      cheese = self.readCheeseDataLine(cheeseDataLine.replace("\n",""))
      self.cheeseDAO.insertCheese(cheese)
      recordsRead += 1
    self.cheeseFile.close()

  def readCheeseDataLine (self, cheeseData):
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
    newCheese.CheeseNameEN = fields[self.headers.index("CheeseNameEn")] if fields[self.headers.index("CheeseNameEn")] != "" else None
    newCheese.CheeseNameFR = fields[self.headers.index("CheeseNameFr")] if fields[self.headers.index("CheeseNameFr")] != "" else None
    newCheese.ManufacturerNameEN = fields[self.headers.index("ManufacturerNameEn")] if fields[self.headers.index("ManufacturerNameEn")] != "" else None
    newCheese.ManufacturerNameFR = fields[self.headers.index("ManufacturerNameFr")] if fields[self.headers.index("ManufacturerNameFr")] != "" else None
    newCheese.ManufacturerProvCode = fields[self.headers.index("ManufacturerProvCode")] if fields[self.headers.index("ManufacturerProvCode")] != "" else None
    newCheese.ManufacturingTypeEN = fields[self.headers.index("ManufacturingTypeEn")] if fields[self.headers.index("ManufacturingTypeEn")] != "" else None
    newCheese.ManufacturingTypeFR = fields[self.headers.index("ManufacturingTypeFr")] if fields[self.headers.index("ManufacturingTypeFr")] != "" else None
    newCheese.WebSiteEN = fields[self.headers.index("WebSiteEn")] if fields[self.headers.index("WebSiteEn")] != "" else None
    newCheese.WebSiteFR = fields[self.headers.index("WebSiteFr")] if fields[self.headers.index("WebSiteFr")] != "" else None
    newCheese.FatContentPercent = float(fields[self.headers.index("FatContentPercent")]) if fields[self.headers.index("FatContentPercent")].isnumeric() else None
    newCheese.MoisturePercent = float(fields[self.headers.index("MoisturePercent")]) if fields[self.headers.index("MoisturePercent")].isnumeric() else None
    newCheese.ParticularitiesEN = fields[self.headers.index("ParticularitiesEn")] if fields[self.headers.index("ParticularitiesEn")] != "" else None
    newCheese.ParticularitiesFR = fields[self.headers.index("ParticularitiesFr")] if fields[self.headers.index("ParticularitiesFr")] != "" else None
    newCheese.FlavourEN = fields[self.headers.index("FlavourEn")] if fields[self.headers.index("FlavourEn")] != "" else None
    newCheese.FlavourFR = fields[self.headers.index("FlavourFr")] if fields[self.headers.index("FlavourFr")] != "" else None
    newCheese.CharacteristicsEN = fields[self.headers.index("CharacteristicsEn")] if fields[self.headers.index("CharacteristicsEn")] != "" else None
    newCheese.CharacteristicsFR = fields[self.headers.index("CharacteristicsFr")] if fields[self.headers.index("CharacteristicsFr")] != "" else None
    newCheese.RipeningEN = fields[self.headers.index("RipeningEn")] if fields[self.headers.index("RipeningEn")] != "" else None
    newCheese.RipeningFR = fields[self.headers.index("RipeningFr")] if fields[self.headers.index("RipeningFr")] != "" else None
    newCheese.Organic = fields[self.headers.index("Organic")] if fields[self.headers.index("Organic")] != "" else None
    newCheese.CategoryTypeEN = fields[self.headers.index("CategoryTypeEn")] if fields[self.headers.index("CategoryTypeEn")] != "" else None
    newCheese.CategoryTypeFR = fields[self.headers.index("CategoryTypeFr")] if fields[self.headers.index("CategoryTypeFr")] != "" else None
    newCheese.MilkTypeEN = fields[self.headers.index("MilkTypeEn")] if fields[self.headers.index("MilkTypeEn")] != "" else None
    newCheese.MilkTypeFR = fields[self.headers.index("MilkTypeFr")] if fields[self.headers.index("MilkTypeFr")] != "" else None
    newCheese.MilkTreatmentTypeEN = fields[self.headers.index("MilkTreatmentTypeEn")] if fields[self.headers.index("MilkTreatmentTypeEn")] != "" else None
    newCheese.MilkTreatmentTypeFR = fields[self.headers.index("MilkTreatmentTypeFr")] if fields[self.headers.index("MilkTreatmentTypeFr")] != "" else None
    newCheese.RindTypeEN = fields[self.headers.index("RindTypeEn")] if fields[self.headers.index("RindTypeEn")] != "" else None
    newCheese.RindTypeFR = fields[self.headers.index("RindTypeFr")] if fields[self.headers.index("RindTypeFr")] != "" else None
    try:
      newCheese.LastUpdateDate = datetime.datetime.strptime(fields[self.headers.index("LastUpdateDate")],"%Y-%m-%d").date()
    except (ValueError, TypeError):
      newCheese.LastUpdateDate = None
    return newCheese

  def saveCheeseData(self, filename):
    "Saves the cheeses in the DB to a file with the name passed to the method"
    saveToFile = open( CheeseDataLoader.savedListFolder + filename + ".csv", "w", encoding = "utf8")
    if len(self.headers) == 0:
      try:
        self.openCheeseFile("canadianCheeseDirectory.csv")
        self.readCheeseData(0)
      except FileNotFoundError:
        print("WARNING - canadianCheeseDirecorty.csv wasn't found in the resources folder")
        input("The file will be saved but will be missing the header data")
    for header in self.headers:
      saveToFile.write(header)
      if(self.headers.index(header)+1 != len(self.headers)):
        saveToFile.write(',')
    saveToFile.write("\n")
    for cheese in self.cheeseDAO.getAllCheeses():
      saveToFile.write(self.__generateCheeseCSVLine__(cheese) + "\n")
    saveToFile.close()

  def __generateCheeseCSVLine__(self, cheese ) -> "":
    "Turns a cheese into a csv value string"
    cheeseStr = ""
    separator = ","
    cheeseStr += "" if cheese.CheeseId == None else str(cheese.CheeseId)
    cheeseStr += separator
    cheeseStr += "" if cheese.CheeseNameEN == None else str(cheese.CheeseNameEN)
    cheeseStr += separator
    cheeseStr += "" if cheese.CheeseNameFR == None else str(cheese.CheeseNameFR)
    cheeseStr += separator
    cheeseStr += "" if cheese.ManufacturerNameEN == None else str(cheese.ManufacturerNameEN)
    cheeseStr += separator
    cheeseStr += "" if cheese.ManufacturerNameFR == None else str(cheese.ManufacturerNameFR)
    cheeseStr += separator
    cheeseStr += "" if cheese.ManufacturerProvCode == None else str(cheese.ManufacturerProvCode)
    cheeseStr += separator
    cheeseStr += "" if cheese.ManufacturingTypeEN == None else str(cheese.ManufacturingTypeEN)
    cheeseStr += separator
    cheeseStr += "" if cheese.ManufacturingTypeFR == None else str(cheese.ManufacturingTypeFR)
    cheeseStr += separator
    cheeseStr += "" if cheese.WebSiteEN == None else str(cheese.WebSiteEN)
    cheeseStr += separator
    cheeseStr += "" if cheese.WebSiteFR == None else str(cheese.WebSiteFR)
    cheeseStr += separator
    cheeseStr += "" if cheese.FatContentPercent == None else str(cheese.FatContentPercent)
    cheeseStr += separator
    cheeseStr += "" if cheese.MoisturePercent == None else str(cheese.MoisturePercent)
    cheeseStr += separator
    cheeseStr += "" if cheese.ParticularitiesEN == None else str(cheese.ParticularitiesEN)
    cheeseStr += separator
    cheeseStr += "" if cheese.ParticularitiesFR == None else str(cheese.ParticularitiesFR)
    cheeseStr += separator
    cheeseStr += "" if cheese.FlavourEN == None else str(cheese.FlavourEN)
    cheeseStr += separator
    cheeseStr += "" if cheese.FlavourFR == None else str(cheese.FlavourFR)
    cheeseStr += separator
    cheeseStr += "" if cheese.CharacteristicsEN == None else str(cheese.CharacteristicsEN)
    cheeseStr += separator
    cheeseStr += "" if cheese.CharacteristicsFR == None else str(cheese.CharacteristicsFR)
    cheeseStr += separator
    cheeseStr += "" if cheese.RipeningEN == None else str(cheese.RipeningEN)
    cheeseStr += separator
    cheeseStr += "" if cheese.RipeningFR == None else str(cheese.RipeningFR)
    cheeseStr += separator
    cheeseStr += "" if cheese.Organic == None else str(cheese.Organic)
    cheeseStr += separator
    cheeseStr += "" if cheese.CategoryTypeEN == None else str(cheese.CategoryTypeEN)
    cheeseStr += separator
    cheeseStr += "" if cheese.CategoryTypeFR == None else str(cheese.CategoryTypeFR)
    cheeseStr += separator
    cheeseStr += "" if cheese.MilkTypeEN == None else str(cheese.MilkTypeEN)
    cheeseStr += separator
    cheeseStr += "" if cheese.MilkTypeFR == None else str(cheese.MilkTypeFR)
    cheeseStr += separator
    cheeseStr += "" if cheese.MilkTreatmentTypeEN == None else str(cheese.MilkTreatmentTypeEN)
    cheeseStr += separator
    cheeseStr += "" if cheese.MilkTreatmentTypeFR == None else str(cheese.MilkTreatmentTypeFR)
    cheeseStr += separator
    cheeseStr += "" if cheese.RindTypeEN == None else str(cheese.RindTypeEN)
    cheeseStr += separator
    cheeseStr += "" if cheese.RindTypeFR == None else str(cheese.RindTypeFR)
    cheeseStr += separator
    cheeseStr += "" if cheese.LastUpdateDate == None else str(cheese.LastUpdateDate)
    return cheeseStr.replace("\n","")