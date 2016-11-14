#Seeding images of cities scrapped from Tripadvisor


from bs4 import BeautifulSoup
import urllib

# from sqlalchemy import func
from model import City_img, connect_to_db, db
from server import app

import csv

# r = urllib.urlopen('https://www.tripadvisor.com/Attractions-g60713-Activities-San_Francisco_California.html').read()
# soup = BeautifulSoup(r, "html.parser")

#for src in soup.find_all('img'):
#     print (src.get('src'))

# mydivs = soup.findAll("div", { "class" : "stylelistrow" })

# div.poi >div.detail > div."item name" title
#         >div >div >div >img src 

# img_divs = soup.find_all("div", { "class" : "poi" })

# firstdiv = mydivs[0]
# pic = firstdiv.find_all('img')[0].get('src')
# title = firstdiv.find_all("div", { "class" : "item name" })[0].get('title')

# for i in range(len(img_divs)):
#     current_div = img_divs[i]
#     img_url = current_div.find_all('img')[0].get('src')
#     img_title = current_div.find_all("div", { "class" : "item name" })[0].get('title')
#     print img_title,img_url


def load_city_img():
    """Load city links from city_link.csv and save images and titles into database"""

    #prevent duplicate record when re-seeding data
    City_img.query.delete()

    # # Read airports.csv file and insert data
    # counter = 0
    # dictairports = {}

    with open('city_links.csv', 'rb') as citylinksfile:
        citylinks = csv.reader(citylinksfile)
        for row in citylinks:
            airport_code, city_link= row[0], row[1]
            read_url = urllib.urlopen(city_link).read()
            soup = BeautifulSoup(read_url, "html.parser")
            img_divs = soup.find_all("div", { "class" : "poi" })


            for i in range(len(img_divs)):
                current_div = img_divs[i]
                img_url = current_div.find_all('img')[0].get('src')
                img_title = current_div.find_all("div", { "class" : "item name" })[0].get('title')
    
                img = City_img(city_airportcode=airport_code,
                                  img_url=img_url,
                                  img_title=img_title,
                                  )

                db.session.add(img)

            db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)

    db.create_all

    load_city_img()