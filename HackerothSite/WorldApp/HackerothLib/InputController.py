import sys
import select
import tty
import termios
import time
import os

class InputController:

   def __init__(self):
      old_settings = termios.tcgetattr(sys.stdin)
      tty.setcbreak(sys.stdin.fileno())

   def isData(self):
      return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

   def sampleInput(self):
      if not self.isData():
         return False
      self.lastInput = sys.stdin.read(1)
      return True
