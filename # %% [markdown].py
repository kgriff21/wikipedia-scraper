
import requests
root_url = 'https://country-leaders.onrender.com'
status_url = 'https://country-leaders.onrender.com/status/'
r = requests.get(status_url)
status_code = r.status_code
if status_code == 200:
    print(f'Text response of status code: {r.reason}')
else:
    print(f'Status code: {status_code}')

countries_url = 'https://country-leaders.onrender.com/countries'
r = requests.get(countries_url)
countries = r.json()
print(countries, r.status_code)

cookie_url = 'https://country-leaders.onrender.com/cookie'
response_cookie = requests.get(cookie_url)
cookies = response_cookie.cookies # Returns a dictionary of cookies
print(cookies)

countries = requests.get(countries_url, cookies=cookies)
countries_list = countries.json()
print(countries, countries.reason)
print(countries.content)
print(f"countries list: {countries_list}")

leaders_url = 'https://country-leaders.onrender.com/leaders'
leaders = requests.get(leaders_url, cookies=cookies)
print(leaders.text)

params = {
    "country": "be"
}
leaders = requests.get(leaders_url, params=params, cookies=cookies)
print(leaders, leaders.json())

leaders_per_country = {}
for country in countries_list:
    print(country)
    params = {
        "country": country
    }
    leaders_response = requests.get(leaders_url, params=params, cookies=cookies)
    print(leaders_response.json())
    leaders_per_country[country] = leaders_response.json()
print(f"Leaders per country dict: {leaders_per_country}")

leaders_per_country = {x : requests.get(leaders_url, params={ "country" : x}, cookies=cookies).json() for x in countries_list}
print(leaders_per_country)

def get_leaders():
    root_url = 'https://country-leaders.onrender.com'
    cookies = requests.get(f"{root_url}/cookie").cookies  # Getting the cookies
    countries = requests.get(f"{root_url}/countries", cookies=cookies).json()
    leaders_per_country = {country : requests.get(f"{root_url}/leaders", {"country": country}, cookies=cookies).json() for country in countries}
    return leaders_per_country

print(get_leaders())

leaders_data = get_leaders()
wiki_url_ru = leaders_data['ru'][0]['wikipedia_url']
print(wiki_url_ru)
for data in leaders_data[countries][leaders_per_country]:
    print(data)


from bs4 import BeautifulSoup
response = requests.get(wiki_url_ru).text
soup = BeautifulSoup(response, 'html.parser')
print(soup.get_text())


paragraphs = soup.find_all('p')
for paragraph in paragraphs:  # Need to apply prettify() to individual elements within the list, not to the entire list itself.
    print(paragraph.prettify())


for para in paragraphs:
    



















