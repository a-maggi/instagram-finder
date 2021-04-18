import argparse

# Setup Argument parser to print help and lock down options
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='Instagram finder',
    usage='%(prog)s -f <format> -i <input> -t <threshold> <options>')
parser.add_argument('-v', '--version', action='version',
                    version='%(prog)s 0.0.1 : Instagram finder')
parser.add_argument('-vv', '--verbose', action='store_true', dest='vv', help='Verbose Mode')
parser.add_argument('-f', '--format', action='store', dest='format', required=True,
                    choices=set(("csv", "imagefolder", "company", "social")),
                    help='Specify if the input file is either a \'company\',a \'CSV\',a \'imagefolder\' or a HTML file to resume')
parser.add_argument('-i', '--input', action='store', dest='input', required=True,
                    help='The name of the CSV file, input folder or company name to use as input')
parser.add_argument('-t', '--threshold', action='store', dest='thresholdinput', required=False,
                    choices=set(("loose", "standard", "strict", "superstrict")),
                    help='The strictness level for image matching, default is standard but can be specified to loose, standard, strict or superstrict')

args = parser.parse_args()