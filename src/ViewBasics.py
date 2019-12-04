'''
Author: Nicholas Bright
Created Date: 2019-11-15
Last Updated: 2019-12-03
Version: 1.0.0
Purpose:
Defines a number of classes to make drawing "pages" of console
output easier. These pages have differnt uses, the simplest being 
the "Page" class which is basically just something that outputs
string lists and then takes an input.

On the more complex end these classes fufill my needs for more complex
pages but were designed to be general so that this file can be reused by myself
for any future projects I feel would benefit from it
'''
from Input import getStringInput, isCharacter
from math import ceil
from os import system, name

class Page:
  """A basic page that only draws lists of strings.
  The page also calls methods, like processInput, that are meant to be overriden by subclasses.
  This class functions as is, but is better suited being used as a base class."""

  def __init__(self, headerLines = [], mainLines = [], footerLines = [], acceptLine = "", waitAfterDraw = False):
    """Initializes a new Page Object. Paramters are:
    headerLines - A list of strings to draw before the main content.
    mainLines - A list of strings to form the main content of the page.
    footerLines - A list of strings to be drawn below the main content.
    acceptLine - A string the program will prompt for when getting input.
    waitAfterDraw - A boolean value. If true, the program will wait for any key after drawing the page."""
    self.headerLines = headerLines
    self.mainLines = mainLines
    self.footerLines = footerLines
    self.informLine = ""
    self.acceptLine = acceptLine
    self.acceptValue = None
    self.waitAfterDraw = waitAfterDraw
  
  def displayLine(self, message):
    """Displays a single line. Can be overriden to redirect output (such as to a file)
    message - The line to draw"""
    print(message)

  def accept(self, message):
    """Prompts the user for a value, and returns the key they pressed
    message - What the prompt will prompt for"""
    self.acceptValue = getStringInput(message)
    return self.acceptValue
  
  def enterToContinue(self):
    """A shell for the accept method that prompts the user to press a key to continue"""
    self.accept("Press any key to continue")
  
  #The following "clear" method was taken from this source:
  #
  #https://www.geeksforgeeks.org/clear-screen-python/
  #Accessed On: 10/20/2019
  #Author: mohit_negi
  #Link to profile: https://auth.geeksforgeeks.org/user/mohit_negi/articles
  def clear(self):
    """Clears the console using console commands. Functionality will differ by OS and shell"""
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
    # for mac and linux(here, os.name is 'posix') 
    elif name == 'posix': 
        _ = system('clear')

  def draw(self):
    """Draws the page. This will draw the page exactly once. In order:
    The page clears the screen.
    The page displays the headerLines.
    The page displays the mainLines.
    The page displays the footerLines.
    The page displays the informLine.
    The page resets the informLine.
    If an acceptLine is specified, accepts a value then called processInput().
    If no acceptLine is specified and waitAfterDraw is true, the page prompts for any key"""
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
    """This method has no functionality, and is meant to be overriden.
    It doesnt throw a NotImplementedError because this isn't a required function,
    but it is good for the page to call so subclasses don't need to add anything to draw"""
    pass

class LoopingPage (Page):
  """A variation of the page class that loops it's draw method when called, until LoopingPage.quit() is called"""
  def __init__(self, headerLines = [], mainLines = [], footerLines = [], acceptLine = ""):
    """Initializes a new LoopingPage. Parameters are:
    headerLines - A list of strings to draw before the main content.
    mainLines - A list of strings to form the main content of the page.
    footerLines - A list of strings to be drawn below the main content.
    acceptLine - A string the program will prompt for when getting input."""
    self.quitFlag = False
    super().__init__(headerLines, mainLines, footerLines, acceptLine, False)
  
  def draw(self):
    """Creates a loop, and calls Page's draw method until the quitFlag is false"""
    while not self.quitFlag:
      self.populateLines()
      Page.draw(self)
  
  def quit(self):
    """Sets quit flag to false to exit the draw loop"""
    self.quitFlag = True

  def populateLines(self):
    """Similar to processInput inside of the Page class, this method does nothing and exists
    only so that subclasses don't have to override the draw method and instead can override
    this one, keeping implementations more consistent"""
    pass

class InputPage(LoopingPage):
  """An implementation of looping page designed for taking in 1 piece of input"""
  def __init__(self, inputName = "Input", formatInput = lambda a : a, checkValid = lambda a : True, enterAction = None, headerLines = [], mainLines = [], footerLines = [], acceptLine = ""):
    """Initializes a new InputPage"""
    self.inputLine = ""
    self.inputName = inputName
    self.checkValid = checkValid
    self.enterAction = enterAction
    self.formatInput = formatInput
    super().__init__(headerLines=headerLines,mainLines=mainLines,footerLines=footerLines,acceptLine=acceptLine)
  
  def populateLines(self):
    """Populates the mainLines with the name of the input being entered and it's value"""
    self.mainLines = [self.inputName + ": " + self.inputLine]
  
  def processInput(self):
    """If the use typed a character add it to the input, if they typed a backspace delete from the input, if they typed enter verify their input and if valid perform selectAction, or if they typed escape then quit"""
    if isCharacter(self.acceptValue):
      self.inputLine += self.acceptValue
    elif (self.acceptValue == "BACKSPACE") and (self.inputLine.__len__() > 0):
      self.inputLine = self.inputLine[:-1]
    elif self.acceptValue == "ENTER":
      if self.checkValid(self.inputLine):
        self.quit()
        self.enterAction(self.formatInput(self.inputLine))
      else:
        self.informLine = "Invalid input"
    elif self.acceptValue == "ESCAPE":
      self.quit()
        

class Menu (LoopingPage):
  """An implementation of the LoopingPage class that creates a menu where users select an item by number"""
  def __init__(self, headerLines = [], optionDict = {}, footerLines = [], acceptLine = "Selection: ", numberMainLines = True, addQuitOption = True):
    """Creates a new menu object. Parameters are:
    headerLines - A list of strings to draw before the main content.
    optionDict - The keys of the dict will be used as the options, and the values should be methods for the menu to call when the user selects the key from the options
    footerLines - A list of strings to be drawn below the main content.
    acceptLine - A string the program will prompt for when getting input.
    numberMainLines - If true, the menu will add numbers next to each option
    addQuitOption - If true, the menu will automatically add a quit option to the end that called LoopingPage.quit()"""
    super().__init__(headerLines=headerLines, footerLines=footerLines, acceptLine=acceptLine)
    self.numberMainLines = numberMainLines
    self.addQuitOption = addQuitOption
    self.setOptions(optionDict)

  def setOptions(self, optionDict):
    """Takes an option dict and populates the mainlines according to the settings given to the initializer
    optionDict - Must be a dictionary of string keys and function values. The keys become the options and the methods are called based on user input"""
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
    """Triggers an option in optionDict based on the key passed."""
    self.optionDict[val]()
  
  def triggerOptionByNumber(self, num):
    """Triggers an option in optionDict based on a position.
    The keys are turned into a list and this number is used to access optionDict at the value found at that pos."""
    self.triggerOption(list(self.optionDict.keys())[num])

  def processInput(self):
    """Checks if the input value is an integer, and if it is, triggers an option with that number."""
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
  """An implementation of LoopingPage that takes a list and displays the list as pages of strings"""
  def __init__(self, displayList=[], itemsPerPage=10, formatter=lambda item: item.__str__(), selectAction=None, headerLines = [], acceptLine = "Use the arrows to navigate, Enter to show details"):
    """Initializes a new ListPage. Paramters are:
    displayList - The list of items to be displayed. Can be anything, if the formatter is set.
    itemsPerPage - The number of items to show per page
    formatter - A lambda called to turn each item in displayList into a string. 
    selectAction - A lambda called when a list item is selected. Must take an item from displayList.
    headerLines - A list of strings to draw before the main content.
    acceptLine - A string the program will prompt for when getting input."""
    self.displayList = displayList
    self.currentPage = 1
    self.itemsPerPage = itemsPerPage
    self.formatter = formatter
    self.selectAction = selectAction
    self.selectedItem = 1
    self.maxPage = lambda : int(ceil(self.displayList.__len__() / self.itemsPerPage))
    super().__init__(headerLines=headerLines, acceptLine=acceptLine)
    if selectAction == None:
      self.acceptLine = "Use the arrows to navigate between pages, Escape to quit"
  
  def populateLines(self):
    """Fills the mainLines fo the ListPage with content based on the current page, and selected item"""
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
    """Processes input from the user.
    Left and right arrow key inputs move the pages left and right.
    Up and down arrow key inputs move selected item up and down.
    Enter executes selectAction on the selected item, if selectAction is defined.
    Escape quits."""
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
    """Returns the list index of the currrently selected item"""
    return self.selectedItem-1+((self.currentPage-1)*self.itemsPerPage)

class EditorPage(ListPage):
  """An implementation of ListPage that lets the user edit the values of an object passed at contruction"""
  def __init__(self, editingObject, attributeNameDict = None, testValidDict = None, formatDict = {}, headerLines=[], ):
    """Initializes a new EditorPage. Paramters are:
    editingObject - The object to be modified
    attributeNameDict - An optional string to string map. The first string should be a property name, the second is the name you want the page to display.
    testValidDict - A dict of string property names to lambdas. The lambda should take a string value, verify the string is valid and return a boolean.
    formatDict - A dict of string property names to lambdas. The lmabdas should take a string value, and return a formatted version of the property. Useful for numeric or object property formattting.
    headerLines - A list of strings to draw before the main content."""
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
    """Turns the keys of the name dict into a list"""
    return list(self.attributeNameDict.keys())
  
  def formatLine(self, key):
    """Formats each line. This is used so that when editing the property being edited is marked with an underscore
    key - The name of the field being edited"""
    if not self.editingFlag:
      return str(key) + ":" + str(self.editingObject.__getattribute__(key))
    if self.displayList[(self.editingItem+((self.currentPage-1)*self.itemsPerPage))] == key:
      return (str(key) + ":" + self.editLine + "_")
    return str(key) + ":" + str(self.editingObject.__getattribute__(key))
  
  def enterEditing(self, attr):
    """Sets the page to being editing the attribute specified.
    attr - The string name of the attribute to begin editing"""
    key = self.displayList[(self.selectedItem-1+((self.currentPage-1)*self.itemsPerPage))]
    value = self.editingObject.__getattribute__(key)
    #Instead of editing a bool, we can just invert it.
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
    """If not currently editing, call ListPage.processInput().
    If currently editing, escape will quit, enter begins editiing, backspace delets a character, and characters are added to the edit line"""
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
    """Makes sure that the format is valid by executing the lamda found in testValidDict[key].
    key - The key of the attribute
    value - The value to be tested"""
    if self.testValidDict == None:
      return True
    if key in self.testValidDict:
      return self.testValidDict[key](value)
    return True

class SearchListPage(ListPage):
  """A list page that takes character input and filters the list based ons earch terms"""
  def __init__(self, searchList=[], filterOnInput = False, itemsPerPage=10, formatter=lambda item: item.__str__(), selectAction=None, headerLines = [], acceptLine = "Type in search terms, Press enter to select list items, press Escape to quit"):
    """Initializes a new SearchListPage. Parameters are:
    searchList - The list of objects to search through
    filterOnInput - If true, will filter the list after every key input
    itemsPerPage - The number of items to show per page
    formatter - A lambda called to turn each item in displayList into a string. 
    selectAction - A lambda called when a list item is selected. Must take an item from displayList.
    headerLines - A list of strings to draw before the main content.
    acceptLine - A string the program will prompt for when getting input."""
    self.searching = True
    self.filterOnInput = filterOnInput
    super().__init__(displayList=searchList, itemsPerPage=itemsPerPage,formatter=formatter, selectAction=selectAction, headerLines=headerLines)
    self.searchList = searchList.copy()
    self.selectedItem = -1
    self.searchLine = ""
    #We save the accept lines of the ListPage and SearchListPage so we can switch between them
    self.listAcceptLine = self.acceptLine
    self.searchAcceptLine = acceptLine
    self.acceptLine = acceptLine
  
  def populateLines(self):
    """Calls ListPage.populateLines() then adds info to the footerLines"""
    super().populateLines()
    self.footerLines.append("")
    self.footerLines.append("Search format: [AttributeName]:[Value]")
    self.footerLines.append("Multiple terms can be specified, separate then by spaces")
    self.footerLines.append("Use double quotes if [Value] contains spaces")
    self.footerLines.append("Search: " + self.searchLine + "_")

  def processInput(self):
    """If we are entering search terms, processess input. Otherwise called ListPage.processInput()
    Character input is added to the search terms.
    Backspace delets from the search terms.
    Enter filters the list and enters results navigation.
    Escape quits when you are entering search terms
    Escape returns to editing the search terms when nagivating the results"""
    if (self.acceptValue == "ESCAPE") and (not self.searching):
      self.searching = True
      self.selectedItem = -1
      self.acceptLine = self.searchAcceptLine
    elif self.searching:
      if self.acceptValue == "ENTER":
        self.filterList()
        self.searching = False
        self.selectedItem = 1
        self.currentPage = 1
        self.acceptLine = self.listAcceptLine
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
    """Filters the searchList based on the search terms to populate displayList"""
    if (self.searchList.__len__() == 0) or (self.searchLine == ""):
      return
    example = self.searchList[0]
    attrValueList = []
    #Parses the search list, and takes each term and breaks it up into key,value tuples
    # that the objects in searchList will be compared to.
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
    self.displayList = []
    for item in self.searchList:
      valid = True
      for term in attrValueList:
        if not str(item.__getattribute__(term[0])).__contains__(term[1]):
          valid = False
          break
      if valid:
        self.displayList.append(item)
  
  def parseSearchList(self):
    """Parses the search terms into a list of strings with format [attrKey]:[attrValue]"""
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
  """An implementation of LoopingPage that prompts the user for Y/N input and sets its acceptValue to True if they said yes"""
  def __init__(self, headerLines = [], messages = [], acceptLine = "Confirm? (Y/N)"):
    """Initializes a new YesNoPage"""
    super().__init__(headerLines = headerLines, mainLines = messages, acceptLine = acceptLine)

  def processInput(self):
    """Sets acceptValue to a boolean if the input is valid, informs the user if they couldn't even manage a y or n input"""
    if (self.acceptValue.lower() in {"y", "n"}) and (isCharacter(self.acceptValue)):
      self.acceptValue = (self.acceptValue.lower() == "y")
      self.quit()
    else:
      self.informLine = "Enter Y or N"