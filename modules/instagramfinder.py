from config import TOKEN, Time_delay, API_USER
import requests

class Instagramfinder:
  timeout = int(Time_delay)
  headers = {'cookie': TOKEN}

  def __init__(self, person):
    self.candidates = []
    self.person = person

  def search(self):
    self.fetch(self.person.first_name+" "+self.person.last_name) # Looking profiles
    self.fetch(self.person.first_name+self.person.last_name) # Looking profiles without spaces

  def fetch(self, searchstring):
    try:
      response = requests.get(API_USER, params={'context': 'user','query': searchstring}, headers=self.headers, timeout=self.timeout)
    except Exception as e:
      print("ERROR Fetch profiles from Instagram")
      print(e)
    else:
      data = response.json()
      for user in data.get('users'):
        profile_link = "https://instagram.com/"+user.get('user').get('username')
        if not any(x[0] == profile_link for x in self.candidates):
          self.candidates.append([profile_link, user.get('user').get('profile_pic_url'), 1.0])
