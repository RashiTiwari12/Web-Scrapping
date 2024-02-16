import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
}
data = requests.get("https://www.imdb.com/chart/top/?ref_=nv_mv_250", headers=headers)

soup = BeautifulSoup(data.text, "html.parser")
movies = soup.select(
    "#__next > main > div > div.ipc-page-content-container.ipc-page-content-container--center > section > div > div.ipc-page-grid.ipc-page-grid--bias-left > div > ul"
)
# print()
for movie in movies:
    movieTitle = movie.select(".ipc-title__text")
    for title_element in movieTitle:
        movie_title = title_element.text
        print(movie_title)
