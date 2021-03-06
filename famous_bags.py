# documentation at  https://google-images-download.readthedocs.io/en/latest/index.html
#from google_images_download import google_images_download   #importing the library
import bing_scraper
#response = google_images_download.googleimagesdownload()

response = bing_scraper.bingimagesdownload()   #class instantiation
arguments = {"config_file":"Famous_bags.json"}  #creating list of arguments
paths = response.download(arguments)   #passing the arguments to the function
file = open("images.json", "w")
file.write(str(paths))
file.close()
print(paths)   #printing absolute paths of the downloaded images
