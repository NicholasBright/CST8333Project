from CheeseModel import CheeseModel

def readCheeseData ( cheeseData ):
  "Converts a line from the data csv file into a CheeseModel.Cheese"
  fields = cheeseData.split(",")
  newCheese = CheeseModel()
  newCheese.CheeseId = fields[headers.index("CheeseId")]
  newCheese.CheeseName = fields[headers.index("CheeseNameEn")]
  newCheese.ManufacturerName = fields[headers.index("ManufacturerNameEn")]
  newCheese.ManufacturerProvCode = fields[headers.index("ManufacturerProvCode")]
  newCheese.ManufacturingType = fields[headers.index("ManufacturingTypeEn")]
  newCheese.WebSite = fields[headers.index("WebSiteEn")]
  newCheese.FatContentPercent = fields[headers.index("FatContentPercent")]
  newCheese.MoisturePercent = fields[headers.index("MoisturePercent")]
  newCheese.Particularities = fields[headers.index("ParticularitiesEn")]
  newCheese.Flavour = fields[headers.index("FlavourEn")]
  newCheese.Characteristics = fields[headers.index("CharacteristicsEn")]
  newCheese.Ripening = fields[headers.index("RipeningEn")]
  newCheese.Organic = fields[headers.index("Organic")]
  newCheese.CategoryType = fields[headers.index("CategoryTypeEn")]
  newCheese.MilkType = fields[headers.index("MilkTypeEn")]
  newCheese.MilkTreatmentType = fields[headers.index("MilkTreatmentTypeEn")]
  newCheese.RindType = fields[headers.index("RindTypeEn")]
  newCheese.LastUpdateDate = fields[headers.index("LastUpdateDate")]
  return newCheese

filename = "canadianCheeseDirectory.csv"
headers = []
data = []

#Open the file
cheeseFile = open(filename, encoding="utf8")
#I save this now because it might be useful in the future
#For now, I just use it to find the index of the data I am looking
# from the line once it has been split. MilkTypeEn has the same index
# in the headers and the data, so I can use headers.index("MilkTypeEn")
# to get the index and pull from the split line at that index for the data
headers = cheeseFile.readline().replace("\ufeff","").replace("\n","").split(",")

#Reading in the first 5 lines and making them objects
for x in range(0, 5):
  data.append(readCheeseData(cheeseFile.readline()))

#Outputting each of the cheses
for field in data :
  print(field, "\n")

print("Nicholas Bright")
