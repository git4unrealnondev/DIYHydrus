'''
Scraper that will scraper mangakalot
'''
USER_AGENT = "DIYHydrus/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 DIYHydrus/10.0"
RATE_LIMIT = 3
SELF_HANDLE_CONNECTION = True

from bs4 import BeautifulSoup, SoupStrainer
import cfscrape
import re
global re
global BeautifulSoup
global cfscrape
global SoupStrainer




class useless():

    def __init__(self):
        self.scraper = cfscrape.create_scraper()

    def rate_limiter(self, url):
        with web_data[1]:

            return self.scraper.get(url).content

    def pull_blocked_images(self, url):
        with web_data[1]:
            cookie_arg, user_agnt = cfscrape.get_cookie_string(url)
            
            return self.scraper.get(url, cookies=cookie_arg, user_agent=user_agnt).content
            
    def create_file_list(self, file_url, img_page):
        url_list = file_url.split('/')
    
        print("fileurl", file_url)
        file_name = url_list[-1]
        chapter = url_list[-2]
        print("filename", file_name)
        print("chapter", chapter)
        for imgs in img_page.findAll('p', {'class': ['_3w1ww']}):
            num = imgs.text.split('/')[1]
        download_list = []
        del url_list[-1]
        del url_list[-1]
        url = ""
        for each in url_list:
            print(each)
            url += each + '/'
        for i in range(1, int(num) + 1):

            download_list.append(url[:-1] + '/' + chapter + '/' + str(i) + '.' + str(file_name.split('.')[1]))
        for each in download_list:
            print(each)
    def handle_manga(self, url):
        '''
        Gets the first page of the manga for viewing.
        '''
        pulled_data = self.rate_limiter(url)

        soup = BeautifulSoup(pulled_data, 'html.parser')

        for tag in soup.findAll('a', {'class': 'btn btn-primary'}, href=True):
        
            img_page = BeautifulSoup(self.rate_limiter(tag['href']), 'html.parser')
            
            #print(img_page)
            temp = None
            for imgs in img_page.findAll('img', {'class': ['PB0mN']}):
                temp = ""
                file_url = imgs['src']
                
            if not temp is None:
                self.create_file_list(file_url, img_page)
            
            for imgs in img_page.findAll('div', {'class': ['KCqLv']}):
                for img in imgs.findAll('img', {'class': ['PB0mN']}):
                    print(img)
            #for deeper in img_page.findAll('div', {'class': 'KCqLv'}):
            #    for imgs in deeper.findAll('img', {'class': 'PB0mN'}):
            #        print(imgs)
            #print("Tag", tag['href'])

    def web_data_check(self):
        '''
        Parses data from website
        '''
        pulled_data = self.rate_limiter(web_data[0])

        #web_data = scraper.get()

        soup = BeautifulSoup(pulled_data)

        image_list = [tag.findAll('a') for tag in soup.findAll('div', id="mangalist")]

        data_to_return = {}
        for media in soup.findAll('div', {'class': 'media-body'}):
            for link in media.findAll('h4', {'class': 'media-heading'}):
                for href in link.findAll('a', href=True):
                    print("link", href.string, href['href'])
                    self.handle_manga(href['href'])
                    #data_to_return[href.string]
                    try:
                        print(link.find('small').contents[0])
                    except AttributeError:
                      print("Could not find small tag for: ", link)
            for labels in media.findAll('a', {'class': 'label genre-label'}):
              print("labels", labels.string)

        return ''

if 'web_data' in globals():
    print("I am getting called from fileDownloaderRateLimited")
    useless_storage = useless()
    stored_data = useless_storage.web_data_check()
else:
    print("I am getting called from scraper.py . My variables are getting read.")
    # Empty Pass back for laziness
    stored_data = ''
