'''
Author: Nicholas Bright
Created Date: 2019-10-06
Last Updated: 2019-12-03
Version: 1.0.0
Purpose:
A model class used to store cheese data for transport between lists, databases, and files.
'''

class CheeseModel:
  """A class to hold cheese data"""
  def __init__(self,
    CheeseId = None,
    CheeseNameEN = None,
    CheeseNameFR = None,
    ManufacturerNameEN = None,
    ManufacturerNameFR = None,
    ManufacturerProvCode = None,
    ManufacturingTypeEN = None,
    ManufacturingTypeFR = None,
    WebSiteEN = None,
    WebSiteFR = None,
    FatContentPercent = None,
    MoisturePercent = None,
    ParticularitiesEN = None,
    ParticularitiesFR = None,
    FlavourEN = None,
    FlavourFR = None,
    CharacteristicsEN = None,
    CharacteristicsFR = None,
    RipeningEN = None,
    RipeningFR = None,
    Organic = False,
    CategoryTypeEN = None,
    CategoryTypeFR = None,
    MilkTypeEN = None,
    MilkTypeFR = None,
    MilkTreatmentTypeEN = None,
    MilkTreatmentTypeFR = None,
    RindTypeEN = None,
    RindTypeFR = None,
    LastUpdateDate = None):
    """Initializes a new CheeseModel"""
    self.CheeseId = CheeseId
    self.CheeseNameEN = CheeseNameEN
    self.CheeseNameFR = CheeseNameFR
    self.ManufacturerNameEN = ManufacturerNameEN
    self.ManufacturerNameFR = ManufacturerNameFR
    self.ManufacturerProvCode = ManufacturerProvCode
    self.ManufacturingTypeEN = ManufacturingTypeEN
    self.ManufacturingTypeFR = ManufacturingTypeFR
    self.WebSiteEN = WebSiteEN
    self.WebSiteFR = WebSiteFR
    self.FatContentPercent = FatContentPercent
    self.MoisturePercent = MoisturePercent
    self.ParticularitiesEN = ParticularitiesEN
    self.ParticularitiesFR = ParticularitiesFR
    self.FlavourEN = FlavourEN
    self.FlavourFR = FlavourFR
    self.CharacteristicsEN = CharacteristicsEN
    self.CharacteristicsFR = CharacteristicsFR
    self.RipeningEN = RipeningEN
    self.RipeningFR = RipeningFR
    self.Organic = Organic
    self.CategoryTypeEN = CategoryTypeEN
    self.CategoryTypeFR = CategoryTypeFR
    self.MilkTypeEN = MilkTypeEN
    self.MilkTypeFR = MilkTypeFR
    self.MilkTreatmentTypeEN = MilkTreatmentTypeEN
    self.MilkTreatmentTypeFR = MilkTreatmentTypeFR
    self.RindTypeEN = RindTypeEN
    self.RindTypeFR = RindTypeFR
    self.LastUpdateDate = LastUpdateDate
  
  def __str__(self):
    """Convert a Cheese object to a string"""
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
    """Checks equality of two cheeses"""
    if (other != None) & (isinstance(other, CheeseModel)):
      return self.CheeseId == other.CheeseId
    return False