class CheeseDAO:
  "An object for managing data access to cheese"

  #This class level array is at class level.
  # Normally my DAO would interace with the DB
  # but since I don't have a DB this array acts as
  # a raw table that is shared by all instances
  _cheeseData = []

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
