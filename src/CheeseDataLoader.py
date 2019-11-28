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

  def openCheeseFile(self, filename):
    "Opens a file that contains cheese data"
    self.cheeseFile = open(CheeseDataLoader._resourceFolder + filename, encoding="utf8")
  
  def readCheeseFile(self, filename, linesToRead = -1):
    "Read Cheese data from a file. It will read the number of lines specified, the default value reads all lines."
    with open(CheeseDataLoader._dataFolder + filename, mode="r", encoding="utf-8-sig") as cheeseFile:
      headers = None
      dataReader = csv.reader(cheeseFile, delimiter=',', quotechar='"')
      recordsRead = 0
      for row in dataReader:
        if (recordsRead >= linesToRead) and (linesToRead != -1):
          break
        elif dataReader.line_num == 1:
          headers = row
        else:
          self.cheeseDAO.insertLater(self.convertRowToCheese(row))
          recordsRead += 1
      self.cheeseDAO.insertAll()
    return
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
      #cheese = self.readCheeseDataLine(cheeseDataLine.replace("\n",""))
      #self.cheeseDAO.insertCheese(cheese)
      recordsRead += 1
    self.cheeseFile.close()

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