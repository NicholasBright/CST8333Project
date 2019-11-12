from CheeseModel import CheeseModel
import mysql.connector
import time

class CheeseDAO:
  "An object for managing data access to cheese"

  instance = None

  # The data used when a connection to the DB is established
  _connectionData = {
    'host':"localhost",
    'user':"cst8333",
    'passwd':"piedas",
    'database':"cst8333"
  }

  # The statements are written in a separate file for easier editing
  # and to keep my files just a bit smaller
  _insertStatement = open("resources/insertStatement.txt").read()
  _selectStatement = open("resources/selectStatement.txt").read()
  _deleteStatement = open("resources/deleteStatement.txt").read()
  _updateStatement = open("resources/updateStatement.txt").read()

  def __init__(self):
    # When the CheeseDAO is created it connects to the DB
    # and checks to see if the table exists, and creates it if it doesn't
    DB = mysql.connector.connect(**CheeseDAO._connectionData) 
    tableExistsCursor = DB.cursor()
    tableExistsCursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'cheese'")
    if tableExistsCursor.fetchone()[0] == 0:
      self.recreateTable()
    tableExistsCursor.close()
    DB.close()

  def recreateTable(self):
    DB = mysql.connector.connect(**CheeseDAO._connectionData)
    createTableCursor = DB.cursor()
    createTableSQL = open("resources/cheeseDirectoryDDL.sql").read()
    createTableCursor.execute(createTableSQL)
    createTableCursor.close()
    DB.close()

  def insertCheese(self, cheese):
    DB = mysql.connector.connect(**CheeseDAO._connectionData)
    insertCursor = DB.cursor()
    insertCursor.execute(CheeseDAO._insertStatement, tuple(self._getListOfFields(cheese)))
    DB.commit()
    insertCursor.close()
    DB.close()

  def getCheese(self, id):
    DB = mysql.connector.connect(**CheeseDAO._connectionData)
    getCursor = DB.cursor()
    selectStatement = CheeseDAO._selectStatement#"SELECT * FROM cheese WHERE cheese_id = " + str(id)
    getCursor.execute(selectStatement, (id,))
    row = getCursor.fetchone()
    getCursor.close()
    DB.close()
    return self._rowIntoCheese(row) if row != None else None

  def getAllCheeses(self):
    cheeseList = []
    DB = mysql.connector.connect(**CheeseDAO._connectionData)
    getAllCursor = DB.cursor()
    selectStatement = "SELECT * FROM cheese"
    getAllCursor.execute(selectStatement)
    for row in getAllCursor:
      cheeseList.append(self._rowIntoCheese(row))
    getAllCursor.close()
    DB.close()
    return cheeseList

  def updateCheese(self, cheese):
    DB = mysql.connector.connect(**CheeseDAO._connectionData)
    updateCursor = DB.cursor()
    fieldList = self._getListOfFields(cheese)
    fieldList.remove(cheese.CheeseId)
    fieldList.append(cheese.CheeseId)
    updateCursor.execute(CheeseDAO._updateStatement, tuple(fieldList))
    DB.commit()
    updateCursor.close()
    DB.close()
  
  def deleteCheese(self, id):
    DB = mysql.connector.connect(**CheeseDAO._connectionData)
    deleteCursor = DB.cursor()
    deleteCursor.execute(CheeseDAO._deleteStatement, (id,))
    DB.commit()
    toRet = deleteCursor.rowcount > 0
    deleteCursor.close()
    DB.close()
    return toRet

  def truncateCheese(self):
    truncateStatement = "TRUNCATE TABLE cheese"
    DB = mysql.connector.connect(**CheeseDAO._connectionData)
    deleteCursor = DB.cursor()
    deleteCursor.execute(truncateStatement)
    DB.commit()
    toRet = deleteCursor.rowcount > 0
    deleteCursor.close()
    DB.close()
    return toRet

  def _rowIntoCheese(self, row):
    cheese = CheeseModel(row[0])
    cheese.CheeseNameEN = row[1]
    cheese.CheeseNameFR = row[2]
    cheese.ManufacturerNameEN = row[3]
    cheese.ManufacturerNameFR = row[4]
    cheese.ManufacturerProvCode = row[5]
    cheese.ManufacturingTypeEN = row[6]
    cheese.ManufacturingTypeFR = row[7]
    cheese.WebSiteEN = row[8]
    cheese.WebSiteFR = row[9]
    cheese.FatContentPercent = float(row[10]) if row[10] != None else None
    cheese.MoisturePercent = float(row[11]) if row[11] != None else None
    cheese.ParticularitiesEN = row[12]
    cheese.ParticularitiesFR = row[13]
    cheese.FlavourEN = row[14]
    cheese.FlavourFR = row[15]
    cheese.CharacteristicsEN = row[16]
    cheese.CharacteristicsFR = row[17]
    cheese.RipeningEN = row[18]
    cheese.RipeningFR = row[19]
    cheese.Organic = row[20]
    cheese.CategoryTypeEN = row[21]
    cheese.CategoryTypeFR = row[22]
    cheese.MilkTypeEN = row[23]
    cheese.MilkTypeFR = row[24]
    cheese.MilkTreatmentTypeEN = row[25]
    cheese.MilkTreatmentTypeFR = row[26]
    cheese.RindTypeEN = row[27]
    cheese.RindTypeFR = row[28]
    cheese.LastUpdateDate = row[29]
    return cheese

  def _getListOfFields(self, cheese):
    return [
      cheese.CheeseId,
      cheese.CheeseNameEN,
      cheese.CheeseNameFR,
      cheese.ManufacturerNameEN,
      cheese.ManufacturerNameFR,
      cheese.ManufacturerProvCode,
      cheese.ManufacturingTypeEN,
      cheese.ManufacturingTypeFR,
      cheese.WebSiteEN,
      cheese.WebSiteFR,
      cheese.FatContentPercent,
      cheese.MoisturePercent,
      cheese.ParticularitiesEN,
      cheese.ParticularitiesFR,
      cheese.FlavourEN,
      cheese.FlavourFR,
      cheese.CharacteristicsEN,
      cheese.CharacteristicsFR,
      cheese.RipeningEN,
      cheese.RipeningFR,
      cheese.Organic,
      cheese.CategoryTypeEN,
      cheese.CategoryTypeFR,
      cheese.MilkTypeEN,
      cheese.MilkTypeFR,
      cheese.MilkTreatmentTypeEN,
      cheese.MilkTreatmentTypeFR,
      cheese.RindTypeEN,
      cheese.RindTypeFR,
      cheese.LastUpdateDate,
    ]

CheeseDAO.instance = CheeseDAO()