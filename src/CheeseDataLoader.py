from CheeseModel import CheeseModel
from CheeseDAO import CheeseDAO
import datetime
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
      cheeseDAO.insertCheese(cheese)
      recordsRead += 1
      if recordsRead >= linesToRead:
        break
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
    filename = filename.__str__()
    saveToFile = open(filename+".csv", "w", encoding="utf8")
    for header in self.headers:
      saveToFile.write(header)
      if(self.headers.index(header)+1 != len(self.headers)):
        saveToFile.write(',')
    saveToFile.write("\n")
    for cheese in CheeseDAO().getAllCheeses():
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