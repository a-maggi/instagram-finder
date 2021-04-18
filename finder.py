'''
Functions for fetching profiles and face recognition
'''
from config import *
from libs.argParser import args
from modules import instagramfinder
import face_recognition.api as face_recognition
from django.utils import encoding
import multiprocessing
import concurrent.futures
import itertools
import urllib

def compare_faces(profile,person,target_encoding,threshold=0.6):
  profilelink, profilepic, distance = profile
  match = None
  try:
    image = urllib.request.urlopen(profilepic)
    unknown_image = face_recognition.load_image_file(image)
    unknown_encoding = face_recognition.face_encodings(unknown_image)

    if len(unknown_encoding) > 0:
      results = face_recognition.face_distance(target_encoding, unknown_encoding[0])
      for result in results:
          if result < float(threshold):
              person.instagram = encoding.smart_str(profilelink, encoding='ascii', errors='ignore')
              person.instagramimage = encoding.smart_str(profilepic, encoding='ascii',
                                                        errors='ignore')
              logging.info("Match found: " + person.full_name +" ,Instagram: " + person.instagram)
              if args.vv == True:
                  print("\tMatch found: " + person.full_name)
                  print("\tInstagram: " + person.instagram)
              match = person

  except Exception as e:
    logging.error("compare_faces: " + str(e))
    print("ERROR")
    print(e)
  
  return match


def run_recognition(profilelist,person,threshold):
  early_break = False
  known_face_image = face_recognition.load_image_file(person.person_image)
  known_face_encodings = face_recognition.face_encodings(known_face_image)

  context = multiprocessing
  if "forkserver" in multiprocessing.get_all_start_methods():
      context = multiprocessing.get_context("forkserver")

  pool = context.Pool(processes=4)

  function_parameters = zip(
      profilelist,
      itertools.repeat(person),
      itertools.repeat(known_face_encodings),
      itertools.repeat(threshold)
  )

  multi_result = pool.starmap(compare_faces, function_parameters)
  results = [i for i in multi_result if i]
  if(len(results) > 0):
    person = results[0]
 
  return person


def get_instagram(person,threshold):
  logging.info("Searching for profile "+person.full_name)
  if args.vv == True:
    print("Searching for profile "+person.full_name)
  profiles = instagramfinder.Instagramfinder(person)
  profiles.search()
  persona = run_recognition(profiles.candidates,person,threshold)
  logging.info("Finished search for "+person.full_name)
  if args.vv == True:
    print("Finished search for "+person.full_name)
  return persona



def fill_instagram(peoplelist,threshold):

  with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
      peoplelist = list(executor.map(get_instagram, peoplelist,itertools.repeat(str(threshold))))

  return peoplelist