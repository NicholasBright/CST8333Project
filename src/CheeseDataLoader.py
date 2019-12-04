'''
Author: Nicholas Bright
Created Date: 2019-10-20
Last Updated: 2019-12-03
Version: 1.0.0
Purpose:
Defines a class used to load cheese data from CSV files, and save cheese data to CSV files
'''
from CheeseModel import CheeseModel
from CheeseDAO import CheeseDAO
import csv
import datetime
import logging
import os
import sys

class CheeseDataLoader:
  """Object that loads cheese data from a file and sends them to the DB"""
  
  _resourceFolder = "resources/"
  _dataFolder = _resourceFolder + "dataFiles/"

  def __init__(self):
    """Initializes a new CheeseDataLoader"""
    self.cheeseDAO = CheeseDAO.instance
  
  def getListOfDataFiles(self):
    """Returns a list of the names of all files in the folder for csv files"""
    return os.listdir(CheeseDataLoader._dataFolder)
  
  def readCheeseFile(self, filename, linesToRead = -1):
    """Read Cheese data from a file and push it to the DB.
    filename - The name of the file to read from
    linesToRead - The number of lines to read. -1 means all of them"""
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
    """Converts a row from the CSV files into a cheese model
    row - A row if data read from a cheese csv file"""
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
    """Saves the cheeses in the DB to a file with the name passed to the method
    filename - The name of the file to save to"""
    saveToFile = open( CheeseDataLoader._dataFolder + filename + ".csv", "w", encoding = "utf8")
    #Using a new CheeseModel, we write the headers by getting the names 
    # of all cheese properties from the __dict__
    keyList = list(CheeseModel().__dict__.keys())
    for header in keyList:
      saveToFile.write(header + ("," if keyList[-1:][0] != header else ""))
    saveToFile.write("\n")
    for cheese in self.cheeseDAO.getAll():
      saveToFile.write(self.__generateCheeseCSVLine__(cheese) + "\n")
    saveToFile.close()

  def __generateCheeseCSVLine__(self, cheese ):
    """Turns a cheese into a csv string.
    cheese - The cheese to turn into a csv string"""
    cheeseStr = ""
    separator = ","
    cheeseStr += "" if cheese.CheeseId == None else self.formatCSVValue(cheese.CheeseId)
    cheeseStr += separator
    cheeseStr += "" if cheese.CheeseNameEN == None else self.formatCSVValue(cheese.CheeseNameEN)
    cheeseStr += separator
    cheeseStr += "" if cheese.CheeseNameFR == None else self.formatCSVValue(cheese.CheeseNameFR)
    cheeseStr += separator
    cheeseStr += "" if cheese.ManufacturerNameEN == None else self.formatCSVValue(cheese.ManufacturerNameEN)
    cheeseStr += separator
    cheeseStr += "" if cheese.ManufacturerNameFR == None else self.formatCSVValue(cheese.ManufacturerNameFR)
    cheeseStr += separator
    cheeseStr += "" if cheese.ManufacturerProvCode == None else self.formatCSVValue(cheese.ManufacturerProvCode)
    cheeseStr += separator
    cheeseStr += "" if cheese.ManufacturingTypeEN == None else self.formatCSVValue(cheese.ManufacturingTypeEN)
    cheeseStr += separator
    cheeseStr += "" if cheese.ManufacturingTypeFR == None else self.formatCSVValue(cheese.ManufacturingTypeFR)
    cheeseStr += separator
    cheeseStr += "" if cheese.WebSiteEN == None else self.formatCSVValue(cheese.WebSiteEN)
    cheeseStr += separator
    cheeseStr += "" if cheese.WebSiteFR == None else self.formatCSVValue(cheese.WebSiteFR)
    cheeseStr += separator
    cheeseStr += "" if cheese.FatContentPercent == None else self.formatCSVValue(cheese.FatContentPercent)
    cheeseStr += separator
    cheeseStr += "" if cheese.MoisturePercent == None else self.formatCSVValue(cheese.MoisturePercent)
    cheeseStr += separator
    cheeseStr += "" if cheese.ParticularitiesEN == None else self.formatCSVValue(cheese.ParticularitiesEN)
    cheeseStr += separator
    cheeseStr += "" if cheese.ParticularitiesFR == None else self.formatCSVValue(cheese.ParticularitiesFR)
    cheeseStr += separator
    cheeseStr += "" if cheese.FlavourEN == None else self.formatCSVValue(cheese.FlavourEN)
    cheeseStr += separator
    cheeseStr += "" if cheese.FlavourFR == None else self.formatCSVValue(cheese.FlavourFR)
    cheeseStr += separator
    cheeseStr += "" if cheese.CharacteristicsEN == None else self.formatCSVValue(cheese.CharacteristicsEN)
    cheeseStr += separator
    cheeseStr += "" if cheese.CharacteristicsFR == None else self.formatCSVValue(cheese.CharacteristicsFR)
    cheeseStr += separator
    cheeseStr += "" if cheese.RipeningEN == None else self.formatCSVValue(cheese.RipeningEN)
    cheeseStr += separator
    cheeseStr += "" if cheese.RipeningFR == None else self.formatCSVValue(cheese.RipeningFR)
    cheeseStr += separator
    cheeseStr += "" if cheese.Organic == None else self.formatCSVValue(cheese.Organic)
    cheeseStr += separator
    cheeseStr += "" if cheese.CategoryTypeEN == None else self.formatCSVValue(cheese.CategoryTypeEN)
    cheeseStr += separator
    cheeseStr += "" if cheese.CategoryTypeFR == None else self.formatCSVValue(cheese.CategoryTypeFR)
    cheeseStr += separator
    cheeseStr += "" if cheese.MilkTypeEN == None else self.formatCSVValue(cheese.MilkTypeEN)
    cheeseStr += separator
    cheeseStr += "" if cheese.MilkTypeFR == None else self.formatCSVValue(cheese.MilkTypeFR)
    cheeseStr += separator
    cheeseStr += "" if cheese.MilkTreatmentTypeEN == None else self.formatCSVValue(cheese.MilkTreatmentTypeEN)
    cheeseStr += separator
    cheeseStr += "" if cheese.MilkTreatmentTypeFR == None else self.formatCSVValue(cheese.MilkTreatmentTypeFR)
    cheeseStr += separator
    cheeseStr += "" if cheese.RindTypeEN == None else self.formatCSVValue(cheese.RindTypeEN)
    cheeseStr += separator
    cheeseStr += "" if cheese.RindTypeFR == None else self.formatCSVValue(cheese.RindTypeFR)
    cheeseStr += separator
    cheeseStr += "" if cheese.LastUpdateDate == None else self.formatCSVValue(cheese.LastUpdateDate)
    return cheeseStr.replace("\n","")

  def formatCSVValue(self, value):
    """Turns double quotes into double double quotes and value contains a comma, it surrounds value with double quotes
    value - The line that will be formatted for saving to a csv"""
    value = str(value)
    value = value.replace("\"","\"\"")
    if value.__contains__(","):
      value = "\"{0}\"".format(value)
    return value