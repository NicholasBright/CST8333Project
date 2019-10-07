class CheeseModel:
  "A class to hold the cheese data"
  def __init__(self):
    "Create a new Cheese object"
    self.CheeseId = ""
    self.CheeseName = ""
    self.ManufacturerName = ""
    self.ManufacturerProvCode = ""
    self.ManufacturingType = ""
    self.WebSite = ""
    self.FatContentPercent = ""
    self.MoisturePercent = ""
    self.Particularities = ""
    self.Flavour = ""
    self.Characteristics = ""
    self.Ripening = ""
    self.Organic = ""
    self.CategoryType = ""
    self.MilkType = ""
    self.MilkTreatmentType = ""
    self.RindType = ""
    self.LastUpdateDate = ""
  def __str__(self):
    "Convert a Cheese object to a string"
    cheeseStr = cheeseStr = ""
    cheeseStr = cheeseStr.__add__(self.CheeseId)
    cheeseStr = cheeseStr.__add__(", ")
    cheeseStr = cheeseStr.__add__(self.CheeseName)
    cheeseStr = cheeseStr.__add__(", ")
    cheeseStr = cheeseStr.__add__(self.ManufacturerName)
    cheeseStr = cheeseStr.__add__(", ")
    cheeseStr = cheeseStr.__add__(self.ManufacturerProvCode)
    cheeseStr = cheeseStr.__add__(", ")
    cheeseStr = cheeseStr.__add__(self.ManufacturingType)
    cheeseStr = cheeseStr.__add__(", ")
    cheeseStr = cheeseStr.__add__(self.WebSite)
    cheeseStr = cheeseStr.__add__(", ")
    cheeseStr = cheeseStr.__add__(self.FatContentPercent)
    cheeseStr = cheeseStr.__add__(", ")
    cheeseStr = cheeseStr.__add__(self.MoisturePercent)
    cheeseStr = cheeseStr.__add__(", ")
    cheeseStr = cheeseStr.__add__(self.Particularities)
    cheeseStr = cheeseStr.__add__(", ")
    cheeseStr = cheeseStr.__add__(self.Flavour)
    cheeseStr = cheeseStr.__add__(", ")
    cheeseStr = cheeseStr.__add__(self.Characteristics)
    cheeseStr = cheeseStr.__add__(", ")
    cheeseStr = cheeseStr.__add__(self.Ripening)
    cheeseStr = cheeseStr.__add__(", ")
    cheeseStr = cheeseStr.__add__(self.Organic)
    cheeseStr = cheeseStr.__add__(", ")
    cheeseStr = cheeseStr.__add__(self.CategoryType)
    cheeseStr = cheeseStr.__add__(", ")
    cheeseStr = cheeseStr.__add__(self.MilkType)
    cheeseStr = cheeseStr.__add__(", ")
    cheeseStr = cheeseStr.__add__(self.MilkTreatmentType)
    cheeseStr = cheeseStr.__add__(", ")
    cheeseStr = cheeseStr.__add__(self.RindType)
    cheeseStr = cheeseStr.__add__(", ")
    cheeseStr = cheeseStr.__add__(self.LastUpdateDate)
    return cheeseStr