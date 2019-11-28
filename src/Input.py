from msvcrt import getch

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
  return getch()

def convertByteInput(byteValue):
  try:
    string = byteStringDict[byteValue]
    if string == "ARROW":
      byteValue += getChar()
      string = byteStringDict[byteValue]
    if string == "SPECIAL":
      byteValue += getChar()
      string = byteStringDict[byteValue]
    return string
  except KeyError:
    return byteValue.decode("utf-8")

def getStringInput(prompt = None):
  if prompt != None:
    print(prompt, end="", flush=True)
  return convertByteInput(getChar())

def isCharacter(value):
  return value not in byteStringDict.values()