import mysql.connector
import time

class CheeseDAO:
  "An object for managing data access to cheese"

  #This class level array is at class level.
  # Normally my DAO would interace with the DB
  # but since I don't have a DB this array acts as
  # a raw table that is shared by all instances
  _cheeseData = []
  _cheeseDB = None

  def __init__(self):
    if CheeseDAO._cheeseDB == None:
      CheeseDAO._cheeseDB = mysql.connector.connect(
        host="localhost",
        user="cst8333",
        passwd="piedas",
        database="cst8333"
      )

      aCursor = CheeseDAO._cheeseDB.cursor()
      aCursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'cheese'")
      if aCursor.fetchone()[0] == 0 | True:
        aCursor.execute(open("resources/cheeseDirectoryDDL.sql").read())
        aCursor.close()

  def executeStatement(self, sql):
    DB = mysql.connector.connect(
      host="localhost",
      user="cst8333",
      passwd="piedas",
      database="cst8333"
    )

    cursor = DB.cursor()#CheeseDAO._cheeseDB.cursor()
    cursor.execute(sql)
    DB.commit()

  def insertCheese(self, cheese):
    insertStatement = \
    "INSERT INTO cheese VALUES ("\
      + str(cheese.CheeseId) + ", "\
      + "'" + cheese.CheeseNameEN.replace("'","''") + "', '" + cheese.CheeseNameFR.replace("'","''") + "'," \
      + "'" + cheese.ManufacturerNameEN.replace("'","''") + "', '" + cheese.ManufacturerNameFR.replace("'","''") + "', " \
      + "'" + cheese.ManufacturerProvCode + "', " \
      + "'" + cheese.ManufacturingTypeEN.replace("'","''") + "', '" + cheese.ManufacturingTypeFR.replace("'","''") + "', " \
      + "'" + cheese.WebSiteEN.replace("'","''") + "', '" + cheese.WebSiteFR.replace("'","''") + "', " \
      + ("NULL" if cheese.FatContentPercent == None else cheese.FatContentPercent) + "," \
      + ("NULL" if cheese.MoisturePercent == None else cheese.MoisturePercent) + "," \
      + "'" + cheese.ParticularitiesEN.replace("'","''") + "', '" + cheese.ParticularitiesFR.replace("'","''") + "', " \
      + "'" + cheese.FlavourEN.replace("'","''") + "', '" + cheese.FlavourFR.replace("'","''") + "', " \
      + "'" + cheese.CharacteristicsEN.replace("'","''") + "', '" + cheese.CharacteristicsFR.replace("'","''") + "', " \
      + "'" + cheese.RipeningEN.replace("'","''") + "', '" + cheese.RipeningFR.replace("'","''") + "', " \
      + "'" + cheese.Organic.replace("'","''") + "', " \
      + "'" + cheese.CategoryTypeEN.replace("'","''") + "', '" + cheese.CategoryTypeFR.replace("'","''") + "', " \
      + "'" + cheese.MilkTypeEN.replace("'","''") + "', '" + cheese.MilkTypeFR.replace("'","''") + "', " \
      + "'" + cheese.MilkTreatmentTypeEN.replace("'","''") + "', '" + cheese.MilkTreatmentTypeFR.replace("'","''") + "', " \
      + "'" + cheese.RindTypeEN.replace("'","''") + "', '" + cheese.RindTypeFR.replace("'","''") + "', " \
      + "'" + cheese.LastUpdateDate + "');"
    self.executeStatement(insertStatement)

  def putCheese(self, newCheese):
    if newCheese.CheeseId == -1:
      newCheese.CheeseId = self.__getNextID()
    
    if len(CheeseDAO._cheeseData) == 0:
      CheeseDAO._cheeseData.append(newCheese)
      return
    
    for cheese in CheeseDAO._cheeseData:
      if cheese.CheeseId == newCheese.CheeseId:
        CheeseDAO._cheeseData[CheeseDAO._cheeseData.index(cheese)] = newCheese
        return
      if cheese.CheeseId > newCheese.CheeseId:
        CheeseDAO._cheeseData.insert(CheeseDAO._cheeseData.index(cheese), newCheese)
        return
    CheeseDAO._cheeseData.append(newCheese)

  def getCheeses(self):
    return CheeseDAO._cheeseData.copy()
  
  def find(self, cheeseId):
    for cheese in CheeseDAO._cheeseData:
      if cheese.CheeseId == cheeseId:
        return cheese
    return None
  
  def remove(self, cheeseId):
    if(cheeseId == "ALL"):
      CheeseDAO._cheeseData = []
      return True
    try:
      CheeseDAO._cheeseData.remove(self.find(cheeseId))
      return True
    except (ValueError):
      return False
  
  def __getNextID(self) -> int:
    return CheeseDAO._cheeseData[len(CheeseDAO._cheeseData)-1].CheeseId + 1
