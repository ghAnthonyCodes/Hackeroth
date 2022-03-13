import math
import time
# from termcolor import colored
import numpy as np

def colored(m, a):
   return m

XP_CURVE = 1.055
HP_CURVE = 1.03
AP_CURVE = 1.028

class Avatar:

   def __init__(self, name, friendly=True):
      self.name = name
      self.xCoord = np.random.randint(50)
      self.level = 1
      self.needed = 50
      self.xp = 0
      self.hp = 100
      self.ap = 10
      self.hpMax = 100
      self.energy = 100
      self.energyMax = 100
      self.hpRegen = 0.012 # % HP per second
      self.energyRegen = 0.25 # % Energy per second
      self.friendly = friendly
      self.critChance = 0.15
      self.piece = name[0]

      # Ability
      self.punchCd = 1.0
      self.punchMult = 1.0
      self.lastPunch = time.time() - self.punchCd
      self.punchEnergy = 40.0

   def punch(self):
      stamp = time.time()
      crit = False
      damage = 0.0
      if stamp - self.lastPunch >= self.punchCd and self.energy >= self.punchEnergy:
         self.lastPunch = stamp
         self.energy -= self.punchEnergy
         damage = self.ap*self.punchMult*(0.9 + np.random.randint(20)/100)
         if np.random.randint(100)/100.0 <= self.critChance:
            damage = damage*1.5
            crit = True
         return True, damage, crit
      return False, damage, crit

   def addExperience(self, xp):
      self.xp += xp
      while self.xp >= self.needed:
         self.xp -= self.needed
         self.level += 1
         self.needed = round(self.needed*XP_CURVE)
      self.updateStats()

   def updateStats(self):
      self.hp = int(round(100*HP_CURVE**(self.level-1)))
      self.hpMax = int(round(100*HP_CURVE**(self.level-1)))
      self.ap = int(round(10*AP_CURVE**(self.level-1)))

   def info(self):
      print("Name: %s (lvl %d)\n  HP: %d (%d%%)\n  AP: %d" % (self.name, self.level, self.hp, int(self.hp/self.hpMax*100), self.ap))

   def showNameplate(self):
      print("")
      self.showName()
      self.showHealthbar()
      self.showEnergyBar()
      self.showXp()

   def showName(self,width=20):
      if self.friendly:
         color = 'green'
      else:
         color = 'red'
      print(colored('        %s - lvl. %d' % (self.name, self.level), color))

   def showHealthbar(self):
      self.showBar('Health', self.hp, self.hpMax, 'green', 20)

   def showEnergyBar(self):
      self.showBar('Energy', self.energy, self.energyMax, 'yellow', 20)

   def showXp(self):
      self.showBar('XP    ', self.xp, self.needed, 'cyan', 20)

   def showBar(self, lbl, cur, maxi, color, width=20):
      bar = colored('%s |' % lbl, 'white')
      pct = cur/maxi
      for i in range(width):
         if pct*width > i:
            bar += colored('*', color)
         else:
            bar += ' '
      bar += colored('| (%d/%d - %d%%)' % (cur, maxi, pct*100), 'white')
      print(bar)

   def regen(self, elapsed):
      self.energy = min(self.energy + elapsed*self.energyRegen*self.energyMax, self.energyMax)
      self.hp= min(self.hp + elapsed*self.hpRegen*self.hpMax, self.hpMax)
      
      
      
