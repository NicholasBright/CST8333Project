'''
Author: Nicholas Bright
Created Date: 2019-11-15
Last Updated: 2019-12-03
Version: 1.0.0
Purpose:
Defines methods for taking single character input directly from the keyboard.

Currently only works on windows computers, since it relies on getch.

Could for sure be expanded to work with Linux and Mac,
 but that's outside of my current needs so it has to wait
'''
from msvcrt import getch

#A dict mapping byte values of getch inputs to strings of the key name
byteStringDict = {
  b'\x00':"SPECIAL",
  b'\xe0':"SPECIAL",
  b'\x00;':"F1",
  b'\x00<':"F2",
  b'\x00=':"F3",
  b'\x00>':"F4",
  b'\x00?':"F5",
  b'\x00@':"F6",
  b'\x00A':"F7",
  b'\x00B':"F8",
  b'\x00C':"F9",
  b'\x00D':"F10",
  b'\xe0\x85':"F11",
  b'\xe0\x86':"F12",
  b'\x00S':"DELETE",
  b'\xe0S':"DELETE",
  b'\x00G':"HOME",
  b'\xe0G':"HOME",
  b'\x00I':"PAGE_UP",
  b'\xe0I':"PAGE_UP",
  b'\x00Q':"PAGE_DOWN",
  b'\xe0Q':"PAGE_DOWN",
  b'\x00O':"END",
  b'\xe0O':"END",
  b'\x00H':"ARROW_UP",
  b'\xe0H':"ARROW_UP",
  b'\x00P':"ARROW_DOWN",
  b'\xe0P':"ARROW_DOWN",
  b'\x00K':"ARROW_LEFT",
  b'\xe0K':"ARROW_LEFT",
  b'\x00M':"ARROW_RIGHT",
  b'\xe0M':"ARROW_RIGHT",
  b'\x1b':"ESCAPE",
  b'\x08':"BACKSPACE",
  b'\t':"TAB",
  b'\r':"ENTER"
}

def getChar():
  """Get a single character stdin"""
  return getch()

def convertByteInput(byteValue):
  """Converts byte input into a string"""
  try:
    string = byteStringDict[byteValue]
    if string == "SPECIAL":
      byteValue += getChar()
      string = byteStringDict[byteValue]
    return string
  except KeyError:
    return byteValue.decode("utf-8")

def getStringInput(prompt = None):
  """Gets single character string input.
  prompt - The value to prompt for"""
  if prompt != None:
    print(prompt, end="", flush=True)
  return convertByteInput(getChar())

def isCharacter(value):
  """Checks if a string is a regular character by checking if the byteStringDict contains a value equal to the passed value
  value - The string to check"""
  return value not in byteStringDict.values()