from libs.argParser import args
import os
import shutil
from config import *

def format(peoplelist):
  csv = []
  Preconditions('results')

  dot_removed = False
  if args.input[0] == ".":
      args.input = args.input[1:]
      dot_removed = True

  outputfilename = "results/" + args.input.replace("\"", "").replace("/", "-") + "-social.csv"
  phishingoutputfilename = "results/" + args.input.replace("\"", "").replace("/", "-")
  if args.format == "imagefolder":
      outputfilename = "results/results-social.csv"
      phishingoutputfilename = "results/results"
  filewriter = open(outputfilename.format(outputfilename), 'w')
  titlestring = "Full Name,"

  titlestring = titlestring[:-1]
  # filewriter.write("Full Name,LinkedIn,Facebook,Twitter,Pinterest,Instagram,Google Plus,Vkontakte,Weibo,Douban\n")
  filewriter.write(titlestring)
  filewriter.write("\n")
  print("")
  for person in peoplelist:
      writestring = '"%s",' % (person.full_name)

      writestring = writestring[:-1]
      filewriter.write(writestring)
      # filewriter.write('"%s","%s","%s","%s","%s","%s","%s","%s","%s"' % (person.full_name, person.linkedin, person.facebook, person.twitter, person.pinterest, person.instagram, person.vk, person.weibo, person.douban))
      filewriter.write("\n")

      terminalstring = ""
      # print "\n" + person.full_name
      if person.instagram != None:
          terminalstring = terminalstring + "\tInstagram: " + person.instagram + "\n"

  print("\nResults file: " + outputfilename)
  filewriter.close()

  # Code for generating HTML file
  htmloutputfilename = "results/" + args.input.replace("\"", "").replace("/", "-") + "-social.html"
  if args.format == "imagefolder":
      htmloutputfilename = "results/results-social.html"
  filewriter = open(htmloutputfilename.format(htmloutputfilename), 'w')

  # background-color: #4CAF50;
  css = """<meta charset="utf-8" />
  <style>
      #employees {
          font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
          border-collapse: collapse;
          width: 100%;
      }

      #employees td, #employees th {
          border: 1px solid #ddd;
          padding: 8px;
      }

      #employees td {
          height: 100px;
      }

      #employees tbody:nth-child(even){
          background-color: #f2f2f2;
      }

      #employees th {
          padding-top: 12px;
          padding-bottom: 12px;
          text-align: left;
          background-color: #12db00;
          color: white;
      }


      #employees .hasTooltipleft span {
          visibility: hidden;
          background-color: black;
          color: #fff;
          text-align: center;
          border-radius: 6px;
          padding: 5px 0;

          /* Position the tooltip */
          position: absolute;
          left:15%;
          z-index: 1;

      }

      #employees .hasTooltipcenterleft span {
          visibility: hidden;
          background-color: black;
          color: #fff;
          text-align: center;
          border-radius: 6px;
          padding: 5px 0;

          /* Position the tooltip */
          position: absolute;
          left:20%;
          z-index: 1;

      }

      #employees .hasTooltipcenterright span {
          visibility: hidden;
          background-color: black;
          color: #fff;
          text-align: center;
          border-radius: 6px;
          padding: 5px 0;

          /* Position the tooltip */
          position: absolute;
          left:25%;
          z-index: 1;

      }

      #employees .hasTooltipright span {
          visibility: hidden;
          background-color: black;
          color: #fff;
          text-align: center;
          border-radius: 6px;
          padding: 5px 0;

          /* Position the tooltip */
          position: absolute;
          left:30%;
          z-index: 1;

      }

      #employees .hasTooltipfarright span {
          visibility: hidden;
          background-color: black;
          color: #fff;
          text-align: center;
          border-radius: 6px;
          padding: 5px 0;

          /* Position the tooltip */
          position: absolute;
          left:35%;
          z-index: 1;

      }

      #employees .hasTooltipleft:hover span {
          visibility: visible;
      }

      #employees .hasTooltipcenterleft:hover span {
          visibility: visible;
      }

      #employees .hasTooltipcenterright:hover span {
          visibility: visible;
      }

      #employees .hasTooltipright:hover span {
          visibility: visible;
      }

      #employees .hasTooltipfarright:hover span {
          visibility: visible;
      }

      #employees tbody:hover {
          background-color: #aaa;
      }
  }

  </style>
  """
  foot = "</table></center>"
  header = """<center><table id=\"employees\">
              <tr>
                  <th rowspan=\"2\">Photo</th>
                  <th rowspan=\"2\">Name</th>
                  <th>Instagram</th>
              </tr>
              """
  filewriter.write(css)
  filewriter.write(header)
  for person in peoplelist:
      local_image_link = person.person_imagelink
      if args.format == "imagefolder":
          outputfoldername =  args.input.replace("\"","").replace("/","-") + "-social"
          local_image_link = "./" + outputfoldername + "/" + person.full_name + ".jpg"
      
      body = "<tbody>" \
            "<tr>" \
            "<td class=\"hasTooltipleft\" rowspan=\"2\"><img src=\"%s\" width=auto height=auto style=\"max-width:200px; max-height:200px;\"><span>%s</span></td>" \
            "<td rowspan=\"2\">%s</td>" \
            "<td rowspan=\"2\" class=\"hasTooltipcenterleft\"><a href=\"%s\"><img src=\"%s\" onerror=\"this.style.display=\'none\'\" width=auto height=auto style=\"max-width:100px; max-height:100px;\"><span>Instagram:<br>%s</span></a></td>" \
            "</tr>" \
            "</tbody>" % (local_image_link, local_image_link, person.full_name, person.instagram, person.instagramimage, person.instagram)
      filewriter.write(body)

  filewriter.write(foot)
  print("HTML file: " + htmloutputfilename + "\n")
  filewriter.close()

  # copy images from Social to output folder
  outputfoldername = "results/" + args.input.replace("\"","").replace("/","-") + "-social"
  if args.format == "imagefolder":
      if dot_removed == True:
          args.input = "." + args.input
      if os.path.exists(outputfoldername):
          try:
              shutil.rmtree(outputfoldername)
          except:
              logging.error("output folder for images for .html already exists and for some reason couldnt be removed and replaced")
              print("output folder for images for .html already exists and for some reason couldnt be removed and replaced")
      shutil.copytree(args.input, outputfoldername)
  else:
      os.rename('temp-targets',outputfoldername)
      print("Image folder: " + outputfoldername + "\n")
