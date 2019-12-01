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

  # Create table statement
  _createTableStatement = "\
DROP TABLE IF EXISTS cheese;\
CREATE TABLE cheese (\
  cheese_id INT PRIMARY KEY AUTO_INCREMENT,\
  cheese_name_en VARCHAR ( 100 ),\
  cheese_name_fr VARCHAR ( 100 ),\
  manufacturer_name_en VARCHAR ( 50 ),\
  manufacturer_name_fr VARCHAR ( 50 ),\
  manufacturer_prov_code CHAR ( 2 ),\
  manufacturing_type_en VARCHAR ( 50 ),\
  manufacturing_type_fr VARCHAR ( 50 ),\
  website_en VARCHAR ( 100 ),\
  website_fr VARCHAR ( 100 ),\
  fat_content_percent INT,\
  moisture_percent INT,\
  particularities_en VARCHAR ( 200 ),\
  particularities_fr VARCHAR ( 200 ),\
  flavour_en VARCHAR ( 200 ),\
  flavour_fr VARCHAR ( 200 ),\
  characteristics_en VARCHAR ( 200 ),\
  characteristics_fr VARCHAR ( 200 ),\
  ripening_en VARCHAR ( 50 ),\
  ripening_fr VARCHAR ( 50 ),\
  organic BOOLEAN,\
  category_type_en VARCHAR ( 50 ),\
  category_type_fr VARCHAR ( 50 ),\
  milk_type_en VARCHAR ( 50 ),\
  milk_type_fr VARCHAR ( 50 ),\
  milk_treatmentType_en VARCHAR ( 20 ),\
  milk_treatmentType_fr VARCHAR ( 20 ),\
  rind_type_en VARCHAR ( 20 ),\
  rind_type_fr VARCHAR ( 20 ),\
  last_update_date DATE\
);"

  # These are the statments used for CRUD operations
  _insertStatement = "\
INSERT INTO cheese\
(cheese_id,cheese_name_en,cheese_name_fr,manufacturer_name_en,manufacturer_name_fr,\
manufacturer_prov_code,manufacturing_type_en,manufacturing_type_fr,website_en,website_fr,\
fat_content_percent,moisture_percent,particularities_en,particularities_fr,flavour_en,\
flavour_fr,characteristics_en,characteristics_fr,ripening_en,ripening_fr,\
organic,category_type_en,category_type_fr,milk_type_en,milk_type_fr,\
milk_treatmentType_en,milk_treatmentType_fr,rind_type_en,rind_type_fr,last_update_date)\
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

  _selectStatement =\
"SELECT * FROM cheese WHERE cheese_id = %s"

  _deleteStatement = \
"DELETE FROM cheese WHERE cheese_id = %s"

  _updateStatement ="\
UPDATE cheese SET \
cheese_name_en = %s, cheese_name_fr = %s, \
manufacturer_name_en = %s, manufacturer_name_fr = %s, manufacturer_prov_code = %s, \
manufacturing_type_en = %s, manufacturing_type_fr = %s, website_en = %s,\
website_fr = %s, fat_content_percent = %s, moisture_percent = %s,\
particularities_en = %s, particularities_fr = %s, flavour_en = %s,\
flavour_fr = %s, characteristics_en = %s, characteristics_fr = %s, \
ripening_en = %s, ripening_fr = %s, organic = %s, \
category_type_en = %s, category_type_fr = %s, milk_type_en = %s, \
milk_type_fr = %s, milk_treatmentType_en = %s, milk_treatmentType_fr = %s, \
rind_type_en = %s, rind_type_fr = %s, last_update_date = %s \
WHERE cheese_id = %s"

  _truncateStatement = "TRUNCATE TABLE cheese"

  def __init__(self):
    "Connects to the DB and ensures that the table exists"
    self.toInsert = []
    self.DB = mysql.connector.connect(**CheeseDAO._connectionData)
  
  def rebuildTable(self):
    # When the CheeseDAO is created it connects to the DB
    # and checks to see if the table exists, and creates it if it doesn't
    DB = mysql.connector.connect(**CheeseDAO._connectionData) 
    cursor = DB.cursor()
    cursor.execute(CheeseDAO._createTableStatement)
    cursor.close()
    DB.close()

  def insert(self, cheese):
    "Inserts a cheese into the DB"
    #DB = mysql.connector.connect(**CheeseDAO._connectionData)
    insertCursor = self.DB.cursor()
    insertCursor.execute(CheeseDAO._insertStatement, tuple(self._getListOfFields(cheese)))
    self.DB.commit()
    insertCursor.close()
    #DB.close()
  
  def insertLater(self, cheese):
    "Puts a cheese into a list of cheeses to be added en mass later"
    self.toInsert.append(tuple(self._getListOfFields(cheese)))
  
  def insertAll(self):
    "Inserts all cheeses added via insertLater into the DB"
    #DB = mysql.connector.connect(**CheeseDAO._connectionData)
    cursor = self.DB.cursor()
    cursor.executemany(CheeseDAO._insertStatement, self.toInsert)
    self.DB.commit()
    cursor.close()
    #DB.close()

  def get(self, id):
    "Fetches a cheese from the DB and returns it"
    #DB = mysql.connector.connect(**CheeseDAO._connectionData)
    getCursor = self.DB.cursor()
    selectStatement = CheeseDAO._selectStatement
    getCursor.execute(selectStatement, (id,))
    row = getCursor.fetchone()
    getCursor.close()
    #DB.close()
    return self._rowIntoCheese(row) if row != None else None

  def getAll(self):
    "Fetch all cheeses in the DB and returns a list of them"
    cheeseList = []
    #DB = mysql.connector.connect(**CheeseDAO._connectionData)
    getAllCursor = self.DB.cursor()
    selectStatement = "SELECT * FROM cheese"
    getAllCursor.execute(selectStatement)
    for row in getAllCursor:
      cheeseList.append(self._rowIntoCheese(row))
    getAllCursor.close()
    #DB.close()
    return cheeseList

  def update(self, cheese):
    "Updates a cheese in the DB"
    #DB = mysql.connector.connect(**CheeseDAO._connectionData)
    updateCursor = self.DB.cursor()
    fieldList = self._getListOfFields(cheese)[1:]
    fieldList.append(cheese.CheeseId)
    updateCursor.execute(CheeseDAO._updateStatement, tuple(fieldList))
    self.DB.commit()
    updateCursor.close()
    #DB.close()
  
  def delete(self, id):
    "Deletes a cheese from the DB"
    #DB = mysql.connector.connect(**CheeseDAO._connectionData)
    deleteCursor = self.DB.cursor()
    deleteCursor.execute(CheeseDAO._deleteStatement, (id,))
    self.DB.commit()
    toRet = deleteCursor.rowcount > 0
    deleteCursor.close()
    #DB.close()
    return toRet

  def truncate(self):
    "Empties the DB of all cheeses"
    #DB = mysql.connector.connect(**CheeseDAO._connectionData)
    deleteCursor = self.DB.cursor()
    deleteCursor.execute(CheeseDAO._truncateStatement)
    self.DB.commit()
    toRet = deleteCursor.rowcount > 0
    deleteCursor.close()
    #DB.close()
    return toRet

  def _rowIntoCheese(self, row):
    "Turns a row from the DB into a cheese"
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
    cheese.Organic = row[20] == "1"
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
    "Turns a cheese into a list of it's values"
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