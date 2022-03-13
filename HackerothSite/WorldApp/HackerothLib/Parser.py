import requests
import numpy as np
from ..models import Repo, Commit
from django.contrib.auth.models import User

RATELIMIT = False

class Parser:

   def __init__(self, user, repos):
      self.user = user
      self.repos = repos
      self.total = {} 
      self.additions = {}
      self.deletions = {}

   def analyzeRepos(self):
      if RATELIMIT:
         self.additions = np.random.randint(0, 1000)
         self.deletions = np.random.randint(0, 1000)
         self.total = self.additions + self.deletions
         return

      self.stats = { }
      for repo in self.repos:

         self.stats[repo] = [0, 0, 0]

         # Check if repo object exists
         u = User.objects.get(username='anthony')
         r = None
         if not Repo.objects.filter(user=u).filter(name=repo).exists():
            print("Creating repository %s" % repo)
            r = Repo()
            r.user = u
            r.name = repo
            r.save()
         else:
            print("%s repo object already exists" % repo)
            r = Repo.objects.filter(user=u).get(name=repo)

         baseUrl = 'https://api.github.com/repos/%s/%s/commits' % (self.user, repo)
         response = requests.get(baseUrl)
         commits = response.json()
         print("%d commits to analyze" % len(commits))

         for commit in commits:
            shaStr = commit['sha']
            c = None
            if Commit.objects.filter(repo=r).filter(sha=shaStr).exists():
               print("Commit %s already exists in %s" % (shaStr, repo))
               c = Commit.objects.filter(repo=r).get(sha=shaStr)
               print(c.total)
               self.stats[repo][0] += c.total
               self.stats[repo][1] += c.additions
               self.stats[repo][2] += c.deletions
               continue

            print("Adding commit %s to %s" % (shaStr, repo))
            c = Commit()
            c.user = u
            c.repo = r
            c.sha = shaStr

            url = '%s/%s' % (baseUrl, shaStr)
            data = requests.get(url).json()
            print(data['stats'])

            # XP
            c.total = data['stats']['total'] 
            c.additions = data['stats']['additions']
            c.deletions = data['stats']['deletions']
            self.stats[repo][0] += c.total
            self.stats[repo][1] += c.additions
            self.stats[repo][2] += c.deletions
            c.save()
