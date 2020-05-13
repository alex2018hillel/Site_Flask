import bs4
import time
import lxml.html as lxml
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('wb')


class Driver:
    def __init__(self):
#         chrome_options = Options()
#         chrome_options.add_argument("--headless")
#         chrome_options.add_argument("--window-size=1920x1080")
#         chrome_driver = "C:\Intel\geckodriver.exe"
#         self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
#         self.driver.get("https://www.google.com")
#         lucky_button = self.driver.find_element_by_css_selector("[name=btnI]")
#         lucky_button.click()
# # capture the screen
#         self.driver.get_screenshot_as_file("capture.png")

        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(options=options)
        self.driver.get("https://auto.ria.com/car/nissan//")

        # ua = dict(DesiredCapabilities.PHANTOMJS)
        # ua["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36")
        # self.driver = webdriver.PhantomJS(desired_capabilities=ua)
        # self.driver.set_window_size(1920, 1080)

        ## self.driver.get('https://rozetka.com.ua/drills/c152496/producer=proton/')
    # def __init__(self, browser = 'firefox'):
    #     desired_capabilites = None
    #     comand_executor = "http://localhost:5556"
    #     #comand_executor = "http://192.168.1.106:4444/wd/hub"
    #
    #     if browser == "chrome":
    #         desired_capabilites =  {
    #             "browserName": "chrome",
    #             "maxInstances": 5
    #         }
    #     elif browser == "firefox":
    #         desired_capabilites = {
    #             "browserName": "firefox",
    #             "maxInstances": 5
    #         }
    #
    #     self.driver = webdriver.Remote(
    #         command_executor=comand_executor,
    #         desired_capabilities=desired_capabilites)
# class Client:
#     def __init__(self):
        ###!!!self.driver = webdriver.Firefox(executable_path=r'C:\Intel\geckodriver.exe')
        #####  !!!!!!!!!!!!!  self.navigate()
        # self.session = requests.Session()
        # self.session.headers = {
        #     'user-agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.17 Safari/537.36 OPR/68.0.3609.0 (Edition developer)'
        # }
        # self.result = []
        self.text = self.driver.page_source
        #print(self.text)
        #self.images = self.driver.find_element_by_xpath("//div[@id='__PWS_ROOT__']//div[@class='gridCentered']//img").get_attribute()
        #self.images = self.driver.find_element_by_xpath("//div[@id='__PWS_ROOT__']").find_element_by_xpath("//div[@class='gridCentered']").find_element_by_tag_name('img').text


    def navigate(self):
        res =self.driver.get('https://auto.ria.com/car/nissan/')
        #time.sleep(2)
        return res


    # def parse_page(self):
    #     print('============parse_page========')
    #     soup = bs4.BeautifulSoup(self.text, 'lxml')
    #     # soup = bs4.BeautifulSoup(self.text, 'html.parser')
    #     time.sleep(0.5)
        #container = soup.select('div.__PWS_ROOT__')
        #container = soup.select('div.goods-tile')#class="catalog-grid
        #container = soup.select('ul.catalog-grid')#class="catalog-grid
        #container = soup.select('div.OpenSearchForm')#class="catalog-grid
        #els = soup.xpath("//div[@class='gridCentered']/div/div/div/div/div/div/div/div/div/div/div/a")
        #els = soup.xpath("//div[@class='gridCentered']")
        ###   els = soup.xpath("//div[@class='qiB']/div/div/div/div/div/div/div/span").text
        # for g in els:
        #     link1 = g.find_all('a')
        #     url = [link['href'] for link in link1 if link.get('href')]

        ###print(els)
        #container = soup.select("//div[@id='__PWS_ROOT__']//div[@class='gridCentered']//img")
        # for i in self.images:
        #     print(i)
        # for each_div in soup.findAll('div',{'class':'Grid__Container'}):
        #     print(each_div)



        #soup.('a') # [<a ..>, ..]
        # d = soup.find_all('div', class='XiG zI7 iyn Hsu')

        # for link in soup.find_all('img'):
        #     print(link.get('href'))
        # soup.find_all(href=re.compile("elsie"), id='link1')
        # container = soup.find_all('div', {'class': ['Yl-', 'MIw','Hb7']})
        # print(container)
        # for block in container:
        #     self.parse_block(block=block)
    # def parse_block(self,block):
    #     logger.info(block)
    #     logger.info('='*100)
    #
    #     url_block = block.select_one('img.hCL kVc L4E MIw')
    #     if not url_block:
    #         logger.error('no url_block')
    #         return
    #
    #     url = url_block.get('href')
    #     if not url:
    #         logger.error('no href')
    #         return
    #
    #     logger.info('%s', url)

    def parser(self):
        #soup = BeautifulSoup(html, 'lxml')
        # els = self.driver.find_elements_by_xpath("//div[@class='qiB']")
        # els2 = self.driver.find_elements_by_xpath("//div[@class='qiB']/div/div/div/div/div/div/div/span")
        # print(els2)

        doc = lxml.document_fromstring(self.text)
        links= doc.xpath("//*[@id='catalogSearchAT']//div[@class='content-bar']//div[@class='price-ticket']/span/span[1]")
        for g in links:
            link = g.text
            print('link',link)


        texts= doc.xpath("//*[@id='catalogSearchAT']//div[@class='content-bar']//div[@class='price-ticket']/span/span[4]/span")
        for b in texts:
            text= b.text
            print('text',text)
        soup = bs4.BeautifulSoup(self.text, 'html.parser')
        print(soup)
        container = soup.select_all('section div.content-bar')
        # container = soup.select_all('div.ticket-item new__ticket t paid')
        # print('container',container)
    #container = soup.select(".//div[@class='offer-wrapper']//td[@class='photo-cell']//img")
        for g in container:
            images = g.find_all('img')['src']
        print('images',images)
        for g in container:
            links = g.find_all('a')
            url = [link['href'] for link in links if link.get('href')]

        for g in container:
            link_head = g.find('td', class_ = "title-cell").div.h3.a.strong.text
            print(link_head)
        for g in container:
            link_1 = g.find('td', class_ = "title-cell").div.h3.a['href']
            print('link_1',link_1)

    def run(self):
        self.parser()
        self.quit()

    def quit(self):
        time.sleep(10)
        self.driver.quit()


# if __name__ == '__main__':
parser = Driver()
parser.run()







'''
def __init__(self, browser):
    desired_capabilites = None
    comand_executor = "http://localhost:4444/wd/hub"

    if browser == "chrome":
        desired_capabilites =  {
                "browserName": "chrome",
                "maxInstances": 5
            }
    elif browser == "firefox":
        desired_capabilites = {
            "browserName": "firefox",
            "maxInstances": 5
        }

    self.driver = webdriver.Remote(
        command_executor=comand_executor,
        desired_capabilities=desired_capabilites)
'''