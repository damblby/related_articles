import requests
from bs4 import BeautifulSoup


def main():
    url1 = 'https://link.springer.com/journal/12202/volumes-and-issues'
    response = requests.get(url1)
    soup = BeautifulSoup(response.text, features='html.parser')
    issues = soup.find_all('li', class_='c-list-group__item')
    issues_links = []
    text = open('keywords.txt', 'w', encoding='utf-8')
    for issue in issues:
        start = str(issue).find('href="') + 6
        end = start + 39 if str(issue)[start + 39] == '"' else start + 38
        issues_links.append(str(issue)[start:end])
    for issue_link in issues_links:
        url2 = 'https://link.springer.com' + issue_link
        response = requests.get(url2)
        soup = BeautifulSoup(response.text, features='html.parser')
        articles = soup.find_all('h3', class_='c-card__title')
        links = []
        for article in articles:
            a = str(article)
            start = a.find('https')
            end = int(start) + 59
            links.append(a[start:end])
        for link in links:
            keywords_in_article = ''
            url = link
            response = requests.get(url)
            soup = BeautifulSoup(response.text, features='html.parser')
            keywords = soup.find_all('li', class_='c-article-subject-list__subject')
            for words in keywords:
                words = words.text
                new_words = ''
                new = ''
                if words.find('\xa0') != -1:
                    for word in words.split('\xa0'):
                        new_words += ' ' + word
                    words = new_words[1:]
                for word in words.split(' '):
                    new += word + '_'
                keywords_in_article += new[:-1] + ' '

            text.write(keywords_in_article + '\n')
            print(keywords_in_article)

if __name__ == '__main__':
    main()
