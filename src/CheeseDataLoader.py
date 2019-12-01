from CheeseModel import CheeseModel
from CheeseDAO import CheeseDAO
import csv
import datetime
import logging
import os
import sys

class CheeseDataLoader:
  "Object that loads cheese data from a file and sends them to the DB"
  
  _resourceFolder = "resources/"
  _dataFolder = _resourceFolder + "dataFiles/"

  def __init__(self, filename = None, linesToRead = -1):
    "Creates a new CheeseDataLoader and if a filename is supplied begins reading that file into the DB"
    self.cheeseDAO = CheeseDAO.instance
    if(filename != None):
      self.readCheeseFile(filename, linesToRead)
  
  def getListOfDataFiles(self):
    return os.listdir(CheeseDataLoader._dataFolder)
  
  def readCheeseFile(self, filename, linesToRead = -1):
    "Read Cheese data from a file. It will read the number of lines specified, the default value reads all lines."
    with open(CheeseDataLoader._dataFolder + filename, mode="r", encoding="utf-8-sig") as cheeseFile:
      dataReader = csv.reader(cheeseFile, delimiter=',', quotechar='"')
      recordsRead = 0
      for row in dataReader:
        if (recordsRead >= linesToRead) and (linesToRead != -1):
          break
        elif dataReader.line_num == 1:
          pass
        else:
          recordsRead += 1
          self.cheeseDAO.insertLater(self.convertRowToCheese(row))
      self.cheeseDAO.insertAll()

  def convertRowToCheese (self, row):
    newCheese = CheeseModel(row[0])
    newCheese.CheeseNameEN = row[1] if row[1] != "" else None
    newCheese.CheeseNameFR = row[2] if row[2] != "" else None
    newCheese.ManufacturerNameEN = row[3] if row[3] != "" else None
    newCheese.ManufacturerNameFR = row[4] if row[4] != "" else None
    newCheese.ManufacturerProvCode = row[5] if row[5] != "" else None
    newCheese.ManufacturingTypeEN = row[6] if row[6] != "" else None
    newCheese.ManufacturingTypeFR = row[7] if row[7] != "" else None
    newCheese.WebSiteEN = row[8] if row[8] != "" else None
    newCheese.WebSiteFR = row[9] if row[9] != "" else None
    newCheese.FatContentPercent = float(row[10]) if row[10] != "" else None
    newCheese.MoisturePercent = float(row[11]) if row[11] != "" else None
    newCheese.ParticularitiesEN = row[12] if row[12] != "" else None
    newCheese.ParticularitiesFR = row[13] if row[13] != "" else None
    newCheese.FlavourEN = row[14] if row[14] != "" else None
    newCheese.FlavourFR = row[15] if row[15] != "" else None
    newCheese.CharacteristicsEN = row[16] if row[16] != "" else None
    newCheese.CharacteristicsFR = row[17] if row[17] != "" else None
    newCheese.RipeningEN = row[18] if row[18] != "" else None
    newCheese.RipeningFR = row[19] if row[19] != "" else None
    newCheese.Organic = (row[20]=="1") if row[20] != "" else None
    newCheese.CategoryTypeEN = row[21] if row[21] != "" else None
    newCheese.CategoryTypeFR = row[22] if row[22] != "" else None
    newCheese.MilkTypeEN = row[23] if row[23] != "" else None
    newCheese.MilkTypeFR = row[24] if row[24] != "" else None
    newCheese.MilkTreatmentTypeEN = row[25] if row[25] != "" else None
    newCheese.MilkTreatmentTypeFR = row[26] if row[26] != "" else None
    newCheese.RindTypeEN = row[27] if row[27] != "" else None
    newCheese.RindTypeFR = row[28] if row[28] != "" else None
    if row[29] == "":
      newCheese.LastUpdateDate = None
    else:
      newCheese.LastUpdateDate = datetime.datetime.strptime(row[29],"%Y-%m-%d").date()
    return newCheese

  def saveCheeseData(self, filename):
    "Saves the cheeses in the DB to a file with the name passed to the method"
    saveToFile = open( CheeseDataLoader._dataFolder + filename + ".csv", "w", encoding = "utf8")
    keyList = list(CheeseModel().__dict__.keys())
    for header in keyList:
      saveToFile.write(header + ("," if keyList[-1:][0] != header else ""))
    saveToFile.write("\n")
    for cheese in self.cheeseDAO.getAll():
      saveToFile.write(self.__generateCheeseCSVLine__(cheese) + "\n")
    saveToFile.close()

  def __generateCheeseCSVLine__(self, cheese ) -> "":
    "Turns a cheese into a csv value string"
    cheeseStr = ""
    separator = ","
    cheeseStr += "" if cheese.CheeseId == None else "\"{0}\"".format(str(cheese.CheeseId).replace("\"","\"\""))
    cheeseStr += separator
    cheeseStr += "" if cheese.CheeseNameEN == None else "\"{0}\"".format(str(cheese.CheeseNameEN).replace("\"","\"\""))
    cheeseStr += separator
    cheeseStr += "" if cheese.CheeseNameFR == None else "\"{0}\"".format(str(cheese.CheeseNameFR).replace("\"","\"\""))
    cheeseStr += separator
    cheeseStr += "" if cheese.ManufacturerNameEN == None else "\"{0}\"".format(str(cheese.ManufacturerNameEN).replace("\"","\"\""))
    cheeseStr += separator
    cheeseStr += "" if cheese.ManufacturerNameFR == None else "\"{0}\"".format(str(cheese.ManufacturerNameFR).replace("\"","\"\""))
    cheeseStr += separator
    cheeseStr += "" if cheese.ManufacturerProvCode == None else "\"{0}\"".format(str(cheese.ManufacturerProvCode).replace("\"","\"\""))
    cheeseStr += separator
    cheeseStr += "" if cheese.ManufacturingTypeEN == None else "\"{0}\"".format(str(cheese.ManufacturingTypeEN).replace("\"","\"\""))
    cheeseStr += separator
    cheeseStr += "" if cheese.ManufacturingTypeFR == None else "\"{0}\"".format(str(cheese.ManufacturingTypeFR).replace("\"","\"\""))
    cheeseStr += separator
    cheeseStr += "" if cheese.WebSiteEN == None else "\"{0}\"".format(str(cheese.WebSiteEN).replace("\"","\"\""))
    cheeseStr += separator
    cheeseStr += "" if cheese.WebSiteFR == None else "\"{0}\"".format(str(cheese.WebSiteFR).replace("\"","\"\""))
    cheeseStr += separator
    cheeseStr += "" if cheese.FatContentPercent == None else "\"{0}\"".format(str(cheese.FatContentPercent).replace("\"","\"\""))
    cheeseStr += separator
    cheeseStr += "" if cheese.MoisturePercent == None else "\"{0}\"".format(str(cheese.MoisturePercent).replace("\"","\"\""))
    cheeseStr += separator
    cheeseStr += "" if cheese.ParticularitiesEN == None else "\"{0}\"".format(str(cheese.ParticularitiesEN).replace("\"","\"\""))
    cheeseStr += separator
    cheeseStr += "" if cheese.ParticularitiesFR == None else "\"{0}\"".format(str(cheese.ParticularitiesFR).replace("\"","\"\""))
    cheeseStr += separator
    cheeseStr += "" if cheese.FlavourEN == None else "\"{0}\"".format(str(cheese.FlavourEN).replace("\"","\"\""))
    cheeseStr += separator
    cheeseStr += "" if cheese.FlavourFR == None else "\"{0}\"".format(str(cheese.FlavourFR).replace("\"","\"\""))
    cheeseStr += separator
    cheeseStr += "" if cheese.CharacteristicsEN == None else "\"{0}\"".format(str(cheese.CharacteristicsEN).replace("\"","\"\""))
    cheeseStr += separator
    cheeseStr += "" if cheese.CharacteristicsFR == None else "\"{0}\"".format(str(cheese.CharacteristicsFR).replace("\"","\"\""))
    cheeseStr += separator
    cheeseStr += "" if cheese.RipeningEN == None else "\"{0}\"".format(str(cheese.RipeningEN).replace("\"","\"\""))
    cheeseStr += separator
    cheeseStr += "" if cheese.RipeningFR == None else "\"{0}\"".format(str(cheese.RipeningFR).replace("\"","\"\""))
    cheeseStr += separator
    cheeseStr += "" if cheese.Organic == None else "\"{0}\"".format(str(cheese.Organic).replace("\"","\"\""))
    cheeseStr += separator
    cheeseStr += "" if cheese.CategoryTypeEN == None else "\"{0}\"".format(str(cheese.CategoryTypeEN).replace("\"","\"\""))
    cheeseStr += separator
    cheeseStr += "" if cheese.CategoryTypeFR == None else "\"{0}\"".format(str(cheese.CategoryTypeFR).replace("\"","\"\""))
    cheeseStr += separator
    cheeseStr += "" if cheese.MilkTypeEN == None else "\"{0}\"".format(str(cheese.MilkTypeEN).replace("\"","\"\""))
    cheeseStr += separator
    cheeseStr += "" if cheese.MilkTypeFR == None else "\"{0}\"".format(str(cheese.MilkTypeFR).replace("\"","\"\""))
    cheeseStr += separator
    cheeseStr += "" if cheese.MilkTreatmentTypeEN == None else "\"{0}\"".format(str(cheese.MilkTreatmentTypeEN).replace("\"","\"\""))
    cheeseStr += separator
    cheeseStr += "" if cheese.MilkTreatmentTypeFR == None else "\"{0}\"".format(str(cheese.MilkTreatmentTypeFR).replace("\"","\"\""))
    cheeseStr += separator
    cheeseStr += "" if cheese.RindTypeEN == None else "\"{0}\"".format(str(cheese.RindTypeEN).replace("\"","\"\""))
    cheeseStr += separator
    cheeseStr += "" if cheese.RindTypeFR == None else "\"{0}\"".format(str(cheese.RindTypeFR).replace("\"","\"\""))
    cheeseStr += separator
    cheeseStr += "" if cheese.LastUpdateDate == None else "\"{0}\"".format(str(cheese.LastUpdateDate).replace("\"","\"\""))
    return cheeseStr.replace("\n","")