'''
Author: Nicholas Bright
Created Date: 2019-10-20
Last Updated: 2019-12-03
Version: 1.0.0
Purpose:
Defines a class used to access a cheese table in a mysql database
'''
from CheeseModel import CheeseModel
import mysql.connector
import time

class CheeseDAO:
  """A DataAccessObject for accessing and executing on the cheese DB"""

  instance = None

  # The data used when a connection to the DB is established
  _connectionData = {
    'host':"localhost",
    'user':"cst8333",
    'passwd':"piedas",
    'database':"cst8333",
    'auth_plugin':'mysql_native_password'
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

  _selectAllStatement =\
"SELECT * FROM cheese"

  _deleteStatement = \
"DELETE FROM cheese WHERE cheese_id = %s"

  _deleteAllStatement = \
"DELETE FROM cheese"

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

  def __init__(self):
    """Establishs a connection to the DB"""
    self.toInsert = []
    self.DB = mysql.connector.connect(**CheeseDAO._connectionData)

  def insert(self, cheese):
    """Inserts a cheese into the DB
    cheese - The cheese to insert to the DB"""
    cursor = self.DB.cursor()
    cursor.execute(CheeseDAO._insertStatement, tuple(self._getListOfFields(cheese)))
    self.DB.commit()
    cursor.close()
  
  def insertLater(self, cheese):
    """Puts a cheese into a list of cheeses to be added en mass later.
    cheese - The cheese to add to the list of cheeses to insert later"""
    self.toInsert.append(tuple(self._getListOfFields(cheese)))
  
  def insertAll(self):
    """Inserts all cheeses added via insertLater into the DB"""
    cursor = self.DB.cursor()
    cursor.executemany(CheeseDAO._insertStatement, self.toInsert)
    self.toInsert.clear()
    self.DB.commit()
    cursor.close()

  def get(self, id):
    """Fetches a cheese from the DB and returns it
    id - The ID of the cheese to get"""
    cursor = self.DB.cursor()
    cursor.execute(CheeseDAO._selectStatement, (id,))
    row = cursor.fetchone()
    cursor.close()
    return self._rowIntoCheese(row) if row != None else None

  def getAll(self):
    """Fetches all cheeses in the DB and returns a list of them"""
    cheeseList = []
    cursor = self.DB.cursor()
    cursor.execute(CheeseDAO._selectAllStatement)
    for row in cursor:
      cheeseList.append(self._rowIntoCheese(row))
    return cheeseList

  def update(self, cheese):
    """Updates a cheese in the DB"""
    #_getListOfFields has CheeseID at the start since it was built for 
    # insert cheese not update.
    #To remedy this I get the sublist of fields from the 2nd item to the end
    # and the CheeseId to the end
    fieldList = self._getListOfFields(cheese)[1:]
    fieldList.append(cheese.CheeseId)
    cursor = self.DB.cursor()
    cursor.execute(CheeseDAO._updateStatement, tuple(fieldList))
    self.DB.commit()
    cursor.close()
  
  def delete(self, id):
    """Deletes a cheese from the DB"""
    cursor = self.DB.cursor()
    cursor.execute(CheeseDAO._deleteStatement, (id,))
    self.DB.commit()
    toRet = cursor.rowcount > 0
    cursor.close()
    return toRet
  
  def deleteAll(self):
    """Deletes all data from the cheese table"""
    cursor = self.DB.cursor()
    cursor.execute(CheeseDAO._deleteAllStatement)
    self.DB.commit()
    cursor.close()

  def _rowIntoCheese(self, row):
    """Turns a row from the DB into a cheese"""
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
    """Turns a cheese into a list of it's values"""
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