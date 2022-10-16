# Import Libraries
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd 

# Creating an instance of webdriver for google chrome
driver = webdriver.Chrome(executable_path='chromedriver.exe')

# Read data
df = pd.read_csv("file.csv")
isbn = df["ISBN"].tolist()

# store data in this empty list
isbnInSite_arr = []
age_arr = []
binding_arr = []
length_arr = []
breadth_arr = []
height_arr = []
weight_arr = []
publication_country_arr = []
nOfPages_arr = []
desc_arr = []
datePublished_arr = []
author_arr = []

# going through each ISBN through this 
for i in isbn:
    url = 'https://www.bookdepository.com/*/' + str(i)
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # default value
    isbnInSite = ""
    age = ""
    binding = ""
    length = ""
    breadth = ""
    height = ""
    weight = ""
    publication_country = ""
    nOfPages = ""
    desc = ""
    datePublished = ""
    author = ""

    # if a particular ISBN data is not found in site the it helps in skip all process
    if soup.find('body', {"class": "error-page-body"}):
        continue

    # from here we started to extracting and cleaning the data
    # for isbn
    isbnInSite = soup.find('span',{'itemprop':"isbn"})
    if isbnInSite:
        isbnInSite = isbnInSite.text

    # For description
    desc = soup.find('div',{'class':"item-description"})
    if desc:
        desc = desc.text.replace("\nDescription\n\n\n                            ", "").replace("  \nshow more\n\n","")

    # for number of pages
    nOfPages = soup.find('span',{'itemprop':"numberOfPages"})
    if nOfPages:
        nOfPages = int(nOfPages.text.replace(" pages\n", ""))

    # for the Published date
    datePublished = soup.find('span',{'itemprop':"datePublished"})
    if datePublished:
        datePublished = datePublished.text

    # For the auther name
    author = soup.find('span', {'itemprop':'author'})
    if author:
        author = author.text.replace('\n\n\n                                    ',"").replace("\n\n","")

    # for the basic details which is in list
    details = soup.find("ul", {"class": "biblio-info"})
    if details:
        details = details.find_all("li")

    # breaking keys with values so that easy to find respected value
    arr = list()
    for d in details:
        arr.append(d.text.strip())
        
    keys = []

    for k in arr:
        keys.append(k[:k.find("\n")])
        
    # set details according to key findings
    for x in range(len(keys)):
        if keys[x] == "For ages":
            age = arr[x][arr[x].find("\n")+1:] + " Y"
        elif keys[x] == "Format":
            binding = arr[x][arr[x].find("\n"):].strip()[:arr[x][arr[x].find("\n"):].strip().rfind("\n")]
        elif keys[x] == "Dimensions":
            dimension = arr[x][arr[x].find("\n")+2:].strip().split("\n                                    ")
            length = int(dimension[0])/10
            if len(dimension) >= 2:
                dimension[1] = dimension[1].replace('x ',"").replace("mm","")
                height = int(dimension[1])/10
            if len(dimension) >= 3:
                dimension[2] = dimension[2].replace('x ',"").replace("mm\n                                ","")
                breadth = int(dimension[2])/10
            if len(dimension) == 4:
                dimension[3] = dimension[3].replace('| ',"").replace("g","")
                weight = dimension[3]
            
        elif keys[x] == "Publication City/Country":    
            publication_country = arr[x][arr[x].find("\n")+2:].strip().split(", ")[1]
            
    # now store that data into that empty array
    isbnInSite_arr.append(isbnInSite)
    age_arr.append(age)
    binding_arr.append(binding)
    length_arr.append(length)
    breadth_arr.append(breadth)
    height_arr.append(height)
    weight_arr.append(weight)
    publication_country_arr.append(publication_country)
    nOfPages_arr.append(nOfPages)
    desc_arr.append(desc)
    datePublished_arr.append(datePublished)
    author_arr.append(author)

# create the dataframe so that able to store in spreadsheet
data = {'isbn': isbnInSite,
        'age': age_arr,
        'binding': binding_arr,
        'length': length_arr,
        'breadth': breadth_arr,
        'height': height_arr,
        'weight': weight_arr,
        'country': publication_country_arr,
        'pages': nOfPages_arr,
        'desc': desc_arr,
        'datePublished': datePublished_arr,
        'author': author_arr}
# Create the pandas DataFrame
dataframe = pd.DataFrame(data)

# export that data into a spreadsheet
# for csv
dataframe.to_csv("book-depository-data.csv", index=False)
# for excel
dataframe.to_excel("book-depository-data.xlsx", index=False)