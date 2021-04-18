# Instagram Finder

A basic project using face recognition to search and found profiles on Instagram by a photo and a full name.

It is based on Social Mapper but with many improvements like concurrent task feature and replaced selenium scrapping with the Instagram API.

## Getting Started

1) Install the required libraries:

```
git clone https://github.com/a-maggi/instagram-finder
cd instagram-finder/setup
python3 -m pip install --no-cache-dir -r requirements.txt
```

2) Provide with the cookies to allow the project use the instagram api:

```
Open the browser with the developer tools to see the network data, go to Instagram and from the request copy the cookie value header.
Open config.conf and enter that value in TOKEN variable
```

## Using Instagram Finder

It is run from the command-line using a mix of required and optional parameters.

### Required Parameters

To start up the tool 2 parameters must be provided, an input format and the input file or folder:

```
-f, --format	: Specify if the -i, --input is a 'name', 'csv', 'imagefolder' or 'socialmapper' resume file
-i, --input	: The company name, a CSV file, imagefolder or Social Mapper HTML file to feed into Social Mapper
```

### Optional Parameters

Additional optional parameters can also be set to add additional customisation to the way Social Mapper runs:

```
-t, --threshold		: Customises the facial recognition threshold for matches, this can be seen as the match accuracy. Default is 'standard', but can be set to 'loose', 'standard', 'strict' or 'superstrict'. For example 'loose' will find more matches, but some may be incorrect. While 'strict' may find less matches but also contain less false positives in the final report.
-vv, --verbose  : Verbose Mode (Useful for Debugging)
```

### Example

```
The basic for search profiles with a standard recognition value. The report with the results will going to results folder:
python3 main.py -f imagefolder -i ./Input-Examples/
```
