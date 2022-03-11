from HackerothLib import Avatar, Parser, InputController
import time
from datetime import datetime as dt
import os
from termcolor import colored
import numpy as np

FRAMES_PER_SECOND = 10

# Create Avatar
player = Avatar.Avatar('Anthony')

# Parse the lines of code
parser = Parser.Parser('ghAnthonyCodes', ['CodeChef', 'TopCoder', 'Hackeroth'])
parser.analyzeRepos()

# Level character based on lines of code
player.addExperience(parser.total)

# Create enemy
enemy = Avatar.Avatar('Disheveled Goblin', friendly = False)
enemy.addExperience(100)

def showFrame(player, enemy):
   os.system('clear')
   player.showNameplate()
   enemy.showNameplate()

def showCombatLog(log):
   print("")
   print(colored("Combat Log", "white"))
   for line in log:
      print(line)

def showMap(player, enemy):
   mapStr = ""
   for m in range(50):
      if m == int(player.xCoord):
         mapStr += player.piece
      elif m == int(enemy.xCoord):
         mapStr += enemy.piece
      else:
         mapStr += "_"
   print(colored(mapStr, "blue"))

combatLog = []
def addToLog(message):
   global combatLog
   combatLog.append(colored("[t = %6.2f] " % ts, 'white') + message)

# Create input controller
inputController = InputController.InputController()
start = dt.now()
while True:

   # Render
   showFrame(player, enemy)
   showMap(player, enemy)
   showCombatLog(combatLog)

   # Regen stats
   player.regen(1/FRAMES_PER_SECOND)

   # Poll input
   if inputController.sampleInput():
      latestInput = inputController.lastInput
      if latestInput == 'h':
         player.xCoord -= 1
      if latestInput == 'l':
         player.xCoord += 1
      elif enemy.hp == 0:
         combatLog.append('There are no enemies to attack')
      elif latestInput == 'p':
         success, damage, crit =  player.punch()
         if success:
            elapsed = dt.now() - start
            ts = elapsed.total_seconds()
            if crit:
               addToLog(colored("Punched enemy for %f damage (CRITICAL)" % damage, 'yellow'))
            else:
               addToLog(colored("Punched enemy for %f damage" % damage, 'white'))
            enemy.hp = max(0, enemy.hp - damage)
            if enemy.hp == 0:
               player.addExperience(100)
               addToLog(colored("Enemy killed", 'red'))
               addToLog(colored("Gained %d xp" % 112, 'cyan'))
   enemy.xCoord += -0.1 + np.random.randint(20)/100

   # Wait for net frame
   time.sleep(1/FRAMES_PER_SECOND)
