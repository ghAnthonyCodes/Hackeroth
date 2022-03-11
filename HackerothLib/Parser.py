import requests
import numpy as np

RATELIMIT = True

class Parser:

   def __init__(self, user, repos):
      self.user = user
      self.repos = repos
      self.total = 0
      self.additions = 0
      self.deletions = 0

   def analyzeRepos(self):
      if RATELIMIT:
         self.additions = np.random.randint(0, 1000)
         self.deletions = np.random.randint(0, 1000)
         self.total = self.additions + self.deletions
         return

      self.additions = 0
      self.deletions = 0
      self.total = 0
      for repo in self.repos:
         baseUrl = 'https://api.github.com/repos/%s/%s/commits' % (self.user, repo)
         print(baseUrl)
         response = requests.get(baseUrl)
         commits = response.json()
         print(len(commits))

         for commit in commits:
            sha = commit['sha']
            url = '%s/%s' % (baseUrl, sha)
            data = requests.get(url).json()
            print(data['stats'])

            # XP
            self.additions += data['stats']['additions']
            self.deletions += data['stats']['deletions']
            self.total += data['stats']['total'] 
