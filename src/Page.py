from os import system, name

class Page:
  def __init__(self):
    self.resetLines()
  
  def resetLines(self):
    self.headerLines = []
    self.mainLines = []
    self.footerLines = []
    self.acceptLine = None
    self.acceptValue = None
    self.waitAfterDraw = False
  
  def displayLine(self, message):
    print(message)

  def accept(self, message):
    self.acceptValue = input(message)
    return self.acceptValue
  
  def enterToContinue(self):
    self.accept("Press enter to continue")
  
  def displayName(self):
    self.displayLine("Nicholas Bright")
  
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
    if self.acceptLine != None:
      self.accept(self.acceptLine)
    elif self.waitAfterDraw:
      self.enterToContinue()