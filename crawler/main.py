import os
import requests

from datetime import datetime
from pytz import timezone
# from github_utils import get_github_repo, upload_github_issue
from github import Github
from bs4 import BeautifulSoup


def parsing_beautifulsoup(url):
    data = requests.get(url)

    html = data.text
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def extract_book_data(soup):
    upload_contents = ''
    new_books = soup.select(".goodsTxtInfo")
    url_prefix = "http://www.yes24.com"

    for new_book in new_books:
        book_name = new_book.select("a")[0].text
        url_suffix = new_book.select("a")[1].attrs['href']
        url = url_prefix + url_suffix
        price = new_book.select(".priceB")[0].text

        content = f"<a href={url}>" + book_name + "</a>" + ", " + price + "<br/>\n"
        upload_contents += content

    return upload_contents


if __name__ == "__main__":

    seoul_timezone = timezone("Asia/Seoul")
    today = datetime.now(seoul_timezone)
    today_date = today.strftime("%Y년 %m월 %d일")

    yes24_it_new_product_url = "http://www.yes24.com/24/Category/NewProductList/001001003?sumGb=01"

    soup = parsing_beautifulsoup(yes24_it_new_product_url)

    issue_title = f"YES24 IT 신간 도서 알림 ({today_date})"
    upload_contents = extract_book_data(soup)
    print(upload_contents)

    access_token = os.environ['MY_GITHUB_TOKEN']
    repository_name = "action-test"

    g = Github(access_token)
    repo = g.get_user().get_repo(repository_name)
    repo.create_issue(title=issue_title, body=upload_contents)
    print("Upload Github Issue Success!")
