from Input import getStringInput, isCharacter
from math import ceil
from os import system, name

class Page:
  def __init__(self, headerLines = [], mainLines = [], footerLines = [], acceptLine = "", waitAfterDraw = False):
    self.headerLines = headerLines
    self.mainLines = mainLines
    self.footerLines = footerLines
    self.informLine = ""
    self.acceptLine = acceptLine
    self.acceptValue = None
    self.waitAfterDraw = waitAfterDraw
  
  def displayLine(self, message):
    print(message)

  def accept(self, message):
    self.acceptValue = getStringInput(message)
    return self.acceptValue
  
  def enterToContinue(self):
    self.accept("Press enter to continue")
  
  def displayName(self):
    self.displayLine("Nicholas Bright")
  
  #The following "clear" method was taken from this source:
  #
  #https://www.geeksforgeeks.org/clear-screen-python/
  #Accessed On: 10/20/2019
  #Author: mohit_negi
  #Link to profile: https://auth.geeksforgeeks.org/user/mohit_negi/articles
  def clear(self):
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
    # for mac and linux(here, os.name is 'posix') 
    elif name == 'posix': 
        _ = system('clear')

  def draw(self):
    self.clear()
    for line in self.headerLines:
      self.displayLine(line)
    for line in self.mainLines:
      self.displayLine(line)
    for line in self.footerLines:
      self.displayLine(line)
    self.displayLine(self.informLine)
    self.informLine = ""
    if self.acceptLine != None:
      self.accept(self.acceptLine)
      self.processInput()
    elif self.waitAfterDraw:
      self.enterToContinue()
  
  def processInput(self):
    pass

class LoopingPage (Page):
  def __init__(self, headerLines = [], mainLines = [], footerLines = [], acceptLine = ""):
    self.quitFlag = False
    Page.__init__(self, headerLines, mainLines, footerLines, acceptLine, False)
  
  def draw(self):
    while not self.quitFlag:
      self.populateLines()
      Page.draw(self)
  
  def quit(self):
    self.quitFlag = True

  def populateLines(self):
    pass

class Menu (LoopingPage):
  def __init__(self, headerLines = [], optionDict = {}, footerLines = [], acceptLine = "Selection: ", numberMainLines = True, addQuitOption = True):
    LoopingPage.__init__(self, headerLines, None, footerLines, acceptLine)
    self.numberMainLines = numberMainLines
    self.addQuitOption = addQuitOption
    self.setOptions(optionDict)

  def setOptions(self, optionDict):
    self.optionDict = optionDict
    if self.addQuitOption:
      self.optionDict["Quit"] = self.quit
    if self.numberMainLines:
      lineCount = 0
      self.mainLines = []
      for line in list(optionDict.keys()):
        lineCount += 1
        self.mainLines.append( "(" + str(lineCount) + ") " + line)
    else:
      self.mainLines = list(optionDict.keys())

  def triggerOption(self, val):
    self.optionDict[val]()
  
  def triggerOptionByNumber(self, num):
    self.triggerOption(list(self.optionDict.keys())[num])

  def processInput(self):
    if self.acceptValue.isdigit():
      try:
        self.acceptValue = int(self.acceptValue)
        if self.acceptValue < 1:
          raise IndexError("Index value below 0 no accepted")
        self.triggerOptionByNumber(self.acceptValue-1)
      except IndexError:
        self.informLine = "Not an option"
    else:
      self.informLine = "Invalid input "

class ListPage (LoopingPage):
  def __init__(self, displayList=[], itemsPerPage=10, formatter=lambda item: item.__str__(), selectAction=None, headerLines = [], acceptLine = "Use the arrows to navigate, Enter to show details"):
    self.displayList = displayList
    self.currentPage = 1
    self.itemsPerPage = itemsPerPage
    self.formatter = formatter
    self.selectAction = selectAction
    self.selectedItem = 1
    self.maxPage = lambda : int(ceil(self.displayList.__len__() / self.itemsPerPage))
    LoopingPage.__init__(self, headerLines=headerLines, acceptLine=acceptLine)
    if selectAction == None:
      self.acceptLine = "Use the arrows to navigate between pages, Escape to quit"
  
  def populateLines(self):
    displayedCount = 0
    self.mainLines = []
    self.footerLines = []
    if self.displayList.__len__() == 0:
      self.mainLines = ["None to show"]
      self.acceptLine = "Press any key to continue"
      return
    while \
      (displayedCount < self.itemsPerPage) and \
      (displayedCount + self.itemsPerPage * (self.currentPage - 1) < self.displayList.__len__()):
      displayedCount += 1
      self.mainLines.append(\
        ("(" if (self.selectedItem == displayedCount) & (self.selectAction != None) else "") +
        self.formatter(
        self.displayList[displayedCount + self.itemsPerPage * (self.currentPage - 1) - 1]) +\
        (")" if (self.selectedItem == displayedCount) & (self.selectAction != None)  else ""))
    self.footerLines.append("Page (" + str(self.currentPage) + "/" + str(self.maxPage()) + ")")

  def processInput(self):
    if self.acceptValue == "ARROW_RIGHT":
      self.selectedItem = 1
      self.currentPage += 1
      if self.currentPage > self.maxPage():
        self.currentPage = 1
    elif self.acceptValue == "ARROW_LEFT":
      self.selectedItem = 1
      self.currentPage -= 1
      if self.currentPage < 1:
       self.currentPage = self.maxPage()
    elif self.acceptValue == "ARROW_UP":
      self.selectedItem -= 1
      if self.selectedItem < 1:
        self.selectedItem = 1
    elif self.acceptValue == "ARROW_DOWN":
      self.selectedItem += 1
      if self.selectedItem > self.mainLines.__len__():
        self.selectedItem = self.mainLines.__len__()
    elif self.acceptValue == "ENTER":
      if self.selectAction == None:
        self.informLine = "No details page was specified"
      else:
        self.selectAction(self.displayList[self.selectedItem - 1 + (self.currentPage-1)*self.itemsPerPage])
    elif self.acceptValue == "ESCAPE":
      self.quit()
  
  def getSelectedIndex(self):
    return self.selectedItem-1+((self.currentPage-1)*self.itemsPerPage)

class EditorPage(ListPage):
  def __init__(self, editingObject, attributeNameDict = None, headerLines=[], testValidDict = None, formatDict = {}):
    self.formatDict = formatDict
    self.testValidDict = testValidDict
    self.editingItem = 0
    self.editingObject = editingObject
    self.editLine = ""
    if attributeNameDict == None:
      self.attributeNameDict = {}
      for attr in list(editingObject.__dict__.keys()):
        self.attributeNameDict[attr] = attr
    else:
      self.attributeNameDict = attributeNameDict
    self.editingFlag = False
    self.listAccept = "Use the arrows to navigate, Escape to quit, enter to edit"
    super().__init__(displayList=self.createAttrList(), headerLines=headerLines, selectAction=self.enterEditing, formatter=self.formatLine, acceptLine=self.listAccept)
  
  def createAttrList(self):
    return list(self.attributeNameDict.keys())
  
  def formatLine(self, key):
    if not self.editingFlag:
      return str(key) + ":" + str(self.editingObject.__getattribute__(key))
    
    if self.displayList[(self.editingItem+((self.currentPage-1)*self.itemsPerPage))] == key:
      return (str(key) + ":" + self.editLine + "_")
    return str(key) + ":" + str(self.editingObject.__getattribute__(key))
  
  def enterEditing(self, attr):
    key = self.displayList[(self.selectedItem-1+((self.currentPage-1)*self.itemsPerPage))]
    value = self.editingObject.__getattribute__(key)
    if type(value) is bool:
      self.editingObject.__setattr__(key, not value)
      return
    self.editLine = str(value) if value != None else ""
    self.editingFlag = True
    self.editingItem = self.selectedItem - 1
    self.selectedItem = -1
    self.listAccept = self.acceptLine
    self.acceptLine = "Modifying Attribute. Enter to save, Escape to cancel"

  def processInput(self):
    if not self.editingFlag:
      super().processInput()
    else:
      if self.acceptValue == "ESCAPE":
        self.editingFlag = False
        self.selectedItem = self.editingItem + 1
        self.acceptLine = self.listAccept
      elif self.acceptValue == "ENTER":
        key = self.displayList[(self.editingItem+((self.currentPage-1)*self.itemsPerPage))]
        if self.editLine == "":
          self.editingObject.__setattr__(key, None)
        elif self.testValidity(key, self.editLine):
          value = self.editLine
          if key in self.formatDict:
            value = self.formatDict[key](value)
          self.editingObject.__setattr__(key, value)
        else:
          self.informLine = "Invalid attribute, value reset"
        self.editingFlag = False
        self.selectedItem = self.editingItem + 1
        self.acceptLine = self.listAccept
      elif self.acceptValue == "BACKSPACE":
        self.editLine = self.editLine[:-1]
      elif isCharacter(self.acceptValue):
        self.editLine += self.acceptValue
  
  def testValidity(self, key, value):
    if self.testValidDict == None:
      return True
    if key in self.testValidDict:
      return self.testValidDict[key](value)
    return True

class SearchListPage(ListPage):
  def __init__(self, searchList=[], filterOnInput = False, itemsPerPage=10, formatter=lambda item: item.__str__(), selectAction=None, headerLines = [], acceptLine = "Type in search terms, Press enter to select list items, press Escape to quit"):
    self.searching = True
    self.filterOnInput = filterOnInput
    super().__init__(displayList=searchList, itemsPerPage=itemsPerPage,formatter=formatter, selectAction=selectAction, headerLines=headerLines, acceptLine=acceptLine)
    self.searchList = searchList.copy()
    self.selectedItem = -1
    self.searchLine = ""
  
  def populateLines(self):
    super().populateLines()
    self.footerLines.append("")
    self.footerLines.append("Search format: [AttributeName]:[Value]")
    self.footerLines.append("Multiple terms can be specified, separate then by spaces")
    self.footerLines.append("Use double quotes if [Value] contains spaces")
    self.footerLines.append("Search: " + self.searchLine)

  def processInput(self):
    if (self.acceptValue == "ESCAPE") and (not self.searching):
      self.searching = True
      self.selectedItem = -1
    elif self.searching:
      if self.acceptValue == "ENTER":
        self.filterList()
        self.searching = False
        self.selectedItem = 1
        self.currentPage = 1
      elif self.acceptValue == "ESCAPE":
        self.quit()
      elif self.acceptValue == "BACKSPACE":
        if self.searchLine != "":
          self.searchLine = self.searchLine[:-1]
          if self.filterOnInput:
            self.filterList()
      elif isCharacter(self.acceptValue):
        self.searchLine += self.acceptValue
        if self.filterOnInput:
          self.filterList()
    else:
      super().processInput()
  
  def filterList(self):
    if self.searchList.__len__() == 0:
      return
    example = self.searchList[0]
    attrValueList = []
    for term in self.parseSearchList():
      if term.__contains__(":"):
        termParts = term.split(":")
        key = termParts[0]
        value = termParts[1]
        if key in example.__dict__:
          attrValueList.append((key,value))
        else:
          self.informLine += "Search term \""+key+"\" is not valid. "
      else:
        self.informLine += "Invalid Search Format"
    foundList = []
    for item in self.searchList:
      valid = True
      for term in attrValueList:
        if not str(item.__getattribute__(term[0])).__contains__(term[1]):
          valid = False
          break
      if valid:
        foundList.append(item)
    self.displayList = foundList
  
  def parseSearchList(self):
    "CheeseId:219 CheeseNameEN:\"Goat Cheese\""
    refinedList = []
    splitList = self.searchLine.split(" ")
    finalLine = ""
    inAQuote = False
    for item in splitList:
      if item.__contains__("\""):
        if inAQuote:
          inAQuote = False
          finalLine += item
          refinedList.append(finalLine.replace("\"",""))
        else:
          if item.count("\"") == 1:
            inAQuote = True
            finalLine = item + " "
          else:
            refinedList.append(item.replace("\"",""))
      elif not inAQuote:
        refinedList.append(item)
      else:
        finalLine += item + " "
    if inAQuote:
      self.informLine += "Unclosed quote. "
    return refinedList

class YesNoPage(LoopingPage):
  def __init__(self, headerLines = [], messages = [], acceptLine = "Confirm? (Y/N)"):
    LoopingPage.__init__(self, headerLines = headerLines, mainLines = messages, acceptLine = acceptLine)

  def processInput(self):
    if (self.acceptValue.lower() in {"y", "n"}) and (isCharacter(self.acceptValue)):
      self.acceptValue = (self.acceptValue.lower() == "y")
      self.quit()
    else:
      self.informLine = "Enter Y or N"