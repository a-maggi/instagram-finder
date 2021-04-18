'''
Main file that includes all functions in appropriate order
'''
from config import *
from datetime import datetime
import finder
import os
import csv
import multiprocessing
from django.utils import encoding
import itertools
from libs.argParser import args
from libs.formatter import format
class Person(object):
    first_name = None
    last_name = None
    full_name = None
    person_image = None
    person_imagelink = None
    instagram = None
    instagramimage = None
    def __init__(self, first_name, last_name, full_name, person_image):
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = full_name
        self.person_image = person_image


if __name__ == '__main__':
  ## Main section
  startTime = datetime.now()
  Logging()
  Remove_folder('results')

  # Set up face matching threshold
  threshold = 0.6
  try:
      if args.thresholdinput == "superstrict":
          threshold = 0.4
      if args.thresholdinput == "strict":
          threshold = 0.5
      if args.thresholdinput == "standard":
          threshold = 0.6
      if args.thresholdinput == "loose":
          threshold = 0.7
  except:
      pass

  exit = True
  # remove targets dir for remaking
  Remove_folder('temp-targets')
  # people list to hold people in memory
  peoplelist = []

  # Fill people list from document with just name + image link
  if args.format == "csv":
      exit = False
      file = open(args.input, 'rb')
      data = file.read()
      file.close()
      try:
          os.remove('temp.csv')
      except OSError:
          pass
      tempcsv = open('temp.csv', 'wb')

      tempcsv.write(data.rstrip(b'\x00'))
      tempcsv.close()
      if not os.path.exists('temp-targets'):
          os.makedirs('temp-targets')
      filereader = csv.reader(open('temp.csv', 'r'), delimiter=",")
      for full_name, person_image in filereader:
          try:
              full_name = encoding.smart_str(full_name, encoding='ascii', errors='ignore')
              person_image = encoding.smart_str(person_image, encoding='ascii', errors='ignore')
              urllib.request.urlretrieve(person_image, "temp-targets/" + full_name + ".jpg")
              first_name = full_name.split(" ")[0]
              last_name = full_name.split(" ", 1)[1]
              person = Person(first_name, last_name, full_name, "temp-targets/" + full_name + ".jpg")
              person.person_imagelink = person_image
              peoplelist.append(person)
          except Exception as e:
              logging.error("Error getting image or creating person structure, skipping:" + full_name)
              print("Error getting image or creating person structure, skipping:" + full_name)

  # Parse image folder full of images and names into
  if args.format == "imagefolder":
      if not args.input.endswith("/"):
          args.input = args.input + "/"
      exit = False
      for filename in os.listdir(args.input):
          if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg"):
              full_name = filename.split(".")[0]
              first_name = full_name.split(" ")[0]
              try:
                  last_name = full_name.split(" ")[1]
              except:
                  last_name = ""
              first_name = encoding.smart_str(first_name, encoding='ascii', errors='ignore')
              last_name = encoding.smart_str(last_name, encoding='ascii', errors='ignore')
              full_name = encoding.smart_str(full_name, encoding='ascii', errors='ignore')
              person = Person(first_name, last_name, full_name, args.input + filename)
              person.person_imagelink = args.input + filename
              peoplelist.append(person)

  if exit:
      logging.error("Input Error, check options relating to format and input")
      print("Input Error, check options relating to format and input")
      sys.exit(1)

  # Start look on Instagram
  peoplelist = finder.fill_instagram(peoplelist,threshold)
  logging.info("Founded {} profiles on Instagram".format(sum(x.instagram is not None for x in peoplelist)))
  print("Founded {} profiles on Instagram".format(sum(x.instagram is not None for x in peoplelist)))

  # Write out updated people list to a CSV file along with other output if
  format(peoplelist)
  logging.info("Task Duration: " + str(datetime.now() - startTime))
  print("Task Duration: " + str(datetime.now() - startTime))
