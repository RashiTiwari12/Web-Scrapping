from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import requests
from bs4 import BeautifulSoup

uri = "<your uri>"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi("1"))

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
}

url = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"

data = requests.get(url=url, headers=headers)
soup = BeautifulSoup(data.text, "html.parser")

movies = soup.select_one(
    "#__next > main > div > div.ipc-page-content-container.ipc-page-content-container--center > section > div > div.ipc-page-grid.ipc-page-grid--bias-left > div > ul"
)

db = client.MyCollection

for movie in movies:
    title = movie.select_one(
        "div.ipc-metadata-list-summary-item__c > div > div > div.ipc-title.ipc-title--base.ipc-title--title.ipc-title-link-no-icon.ipc-title--on-textPrimary.sc-be6f1408-9.srahg.cli-title > a > h3"
    ).text
    year = movie.select_one(
        "div.ipc-metadata-list-summary-item__c > div > div > div.sc-be6f1408-7.iUtHEN.cli-title-metadata > span:nth-child(1)"
    ).text
    rating_with_votes = str(
        movie.select_one(
            "div.ipc-metadata-list-summary-item__c > div > div > span > div > span"
        ).text
    )
    rating = rating_with_votes.split()[0]

    movie = title.split(". ")[1]
    db.imdb_movies.insert_one(
        {
            "movie": movie,
            "year": year,
            "rating": rating,
        }
    )
