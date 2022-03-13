from django.shortcuts import render
from django.http import HttpResponse
from .HackerothLib import Avatar, Parser

# Create your views here.
def index(request):
   return HttpResponse("Hello, world")

def parse(request):
   repos = ['TopCoder']
   S = ""
   player = Avatar.Avatar('Anthony')
   parser = Parser.Parser('ghAnthonyCodes', repos)
   parser.analyzeRepos()
   for repo in repos:
      player.addExperience(parser.stats[repo][0])
      S = 'Repo: %s<br>' % repo
      S = 'Added %d XP<br>' % parser.stats[repo][0]
   S += "Level: %d<br>" % player.level
   S += "Health: %d<br>" % player.hp
   S += "AP: %d<br>" % player.ap
   return HttpResponse(S)
   
