class CheeseModel:
  "A class to hold the cheese data"
  def __init__(self, CheeseId=-1):
    "Create a new Cheese object"
    self.CheeseId = CheeseId
    self.CheeseNameEN = ""
    self.CheeseNameFR = ""
    self.ManufacturerNameEN = ""
    self.ManufacturerNameFR = ""
    self.ManufacturerProvCode = ""
    self.ManufacturingTypeEN = ""
    self.ManufacturingTypeFR = ""
    self.WebSiteEN = ""
    self.WebSiteFR = ""
    self.FatContentPercent = ""
    self.MoisturePercent = ""
    self.ParticularitiesEN = ""
    self.ParticularitiesFR = ""
    self.FlavourEN = ""
    self.FlavourFR = ""
    self.CharacteristicsEN = ""
    self.CharacteristicsFR = ""
    self.RipeningEN = ""
    self.RipeningFR = ""
    self.Organic = ""
    self.CategoryTypeEN = ""
    self.CategoryTypeFR = ""
    self.MilkTypeEN = ""
    self.MilkTypeFR = ""
    self.MilkTreatmentTypeEN = ""
    self.MilkTreatmentTypeFR = ""
    self.RindTypeEN = ""
    self.RindTypeFR = ""
    self.LastUpdateDate = ""
  def __str__(self):
    "Convert a Cheese object to a string"
    cheeseStr = cheeseStr = ""
    cheeseStr = cheeseStr.__add__(str(self.CheeseId))
    cheeseStr = cheeseStr.__add__(", ")
    cheeseStr = cheeseStr.__add__(self.CheeseNameEN)
    cheeseStr = cheeseStr.__add__(", ")
    cheeseStr = cheeseStr.__add__(self.ManufacturerNameEN)
    cheeseStr = cheeseStr.__add__(", ")
    cheeseStr = cheeseStr.__add__(self.ManufacturerProvCode)
    cheeseStr = cheeseStr.__add__(", ")
    cheeseStr = cheeseStr.__add__(self.ManufacturingTypeEN)
    cheeseStr = cheeseStr.__add__(", ")
    cheeseStr = cheeseStr.__add__(self.WebSiteEN)
    cheeseStr = cheeseStr.__add__(", ")
    cheeseStr = cheeseStr.__add__(self.FatContentPercent)
    cheeseStr = cheeseStr.__add__(", ")
    cheeseStr = cheeseStr.__add__(self.MoisturePercent)
    cheeseStr = cheeseStr.__add__(", ")
    cheeseStr = cheeseStr.__add__(self.ParticularitiesEN)
    cheeseStr = cheeseStr.__add__(", ")
    cheeseStr = cheeseStr.__add__(self.FlavourEN)
    cheeseStr = cheeseStr.__add__(", ")
    cheeseStr = cheeseStr.__add__(self.CharacteristicsEN)
    cheeseStr = cheeseStr.__add__(", ")
    cheeseStr = cheeseStr.__add__(self.RipeningEN)
    cheeseStr = cheeseStr.__add__(", ")
    cheeseStr = cheeseStr.__add__(self.Organic)
    cheeseStr = cheeseStr.__add__(", ")
    cheeseStr = cheeseStr.__add__(self.CategoryTypeEN)
    cheeseStr = cheeseStr.__add__(", ")
    cheeseStr = cheeseStr.__add__(self.MilkTypeEN)
    cheeseStr = cheeseStr.__add__(", ")
    cheeseStr = cheeseStr.__add__(self.MilkTreatmentTypeEN)
    cheeseStr = cheeseStr.__add__(", ")
    cheeseStr = cheeseStr.__add__(self.RindTypeEN)
    cheeseStr = cheeseStr.__add__(", ")
    cheeseStr = cheeseStr.__add__(self.LastUpdateDate)
    return cheeseStr
  
  def __eq__(self, other):
    if (other != None) & (isinstance(other, CheeseModel)):
      return self.CheeseId == other.CheeseId
    return False