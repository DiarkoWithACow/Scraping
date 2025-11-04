import requests
from bs4 import BeautifulSoup
url = "https://stackoverflow.com/questions/5338979/scraping-a-web-page-with-java-script-in-python"
response = requests.get(url)
soup = BeautifulSoup (response.text, "html.parser")
first_paragraph = soup.find("p")
print (first_paragraph)