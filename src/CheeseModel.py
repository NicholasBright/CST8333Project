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
  def __init__(self, CheeseId=None):
    """Create a new Cheese object"""
    self.CheeseId = CheeseId
    self.CheeseNameEN = None
    self.CheeseNameFR = None
    self.ManufacturerNameEN = None
    self.ManufacturerNameFR = None
    self.ManufacturerProvCode = None
    self.ManufacturingTypeEN = None
    self.ManufacturingTypeFR = None
    self.WebSiteEN = None
    self.WebSiteFR = None
    self.FatContentPercent = None
    self.MoisturePercent = None
    self.ParticularitiesEN = None
    self.ParticularitiesFR = None
    self.FlavourEN = None
    self.FlavourFR = None
    self.CharacteristicsEN = None
    self.CharacteristicsFR = None
    self.RipeningEN = None
    self.RipeningFR = None
    self.Organic = False
    self.CategoryTypeEN = None
    self.CategoryTypeFR = None
    self.MilkTypeEN = None
    self.MilkTypeFR = None
    self.MilkTreatmentTypeEN = None
    self.MilkTreatmentTypeFR = None
    self.RindTypeEN = None
    self.RindTypeFR = None
    self.LastUpdateDate = None
  
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