import logging
from colorama import Fore, Style
from agorios.utils.Scraper import Scraper

OCADO_WEBSITE = 'https://www.ocado.com/browse'
OCADO_SEARCH_URL = 'https://www.ocado.com/search?entry='
OCADO_POPUP_BUTTON_XPATH = '//button[@id="onetrust-accept-btn-handler"]'
OCADO_SEARCH_INPUT_TEXT_XPATH = '//header//input[@id="search"]'
OCADO_MAIN_COLUMN_PRODUCTS_XPATH = '//div[@class="main-column"]//div[@class="fop-contentWrapper"]'
OCADO_CATEGORIES_XPATH = '//div[contains(@class, "grocery-section")]/ul/li'
OCADO_NUMBER_OF_PRODUCTS_IN_SEARCH = '//span[@class="bc-mobileBreadcrumbs__itemsCount"]'


def main():
    print(Fore.GREEN + "--Scraping-initialized--" + Style.RESET_ALL)
    scrapy = Scraper(headless=False, browser_detached=True)

    # Sample test with oil
    search_product(scrapy, 'oil')
    scrapy.wait(1)
    check_close_popup(scrapy)
    scrapy.scroll_and_load_page(20)
    products = scrapy.get_elements(OCADO_MAIN_COLUMN_PRODUCTS_XPATH)
    print(Fore.LIGHTGREEN_EX + "Number of products found: " + str(len(products)) + Style.RESET_ALL)
    product_list = (get_products(scrapy, products))
    #print(product_list)
    print(Fore.LIGHTGREEN_EX + "Number of products fetched: " + str(len(product_list)) + Style.RESET_ALL)

def search_product(scrapy: Scraper, search_string: str)->Scraper:
    formatted_query = '%20'.join(search_string.split())
    scrapy.get(OCADO_SEARCH_URL + formatted_query)
    pass

def check_close_popup(scrapy: Scraper)->None:
    if scrapy.check_if_exists(OCADO_POPUP_BUTTON_XPATH):
        scrapy.click_element(OCADO_POPUP_BUTTON_XPATH)
    pass

def get_number_of_products_in_search(scrapy: Scraper)->str:
    if (scrapy.get_elements(OCADO_NUMBER_OF_PRODUCTS_IN_SEARCH)):
        return scrapy.get_elements(OCADO_NUMBER_OF_PRODUCTS_IN_SEARCH).text
    return ''


def get_categories(scrapy:Scraper)->list:
    categories = scrapy.get_elements(OCADO_CATEGORIES_XPATH)
    categories_list = []
    for c in categories:
        categories_list.append({'name':c.text,
                                'link': scrapy.return_children(c)[0].get_attribute('href')
                                })
    return categories_list

def get_products(scrapy: Scraper, products:list):
    product_list = []
    for key,p in enumerate(products):
        product_name = scrapy.get_elements(strategy='class name', value='fop-title', element=p)[0]
        product_catch_weight = scrapy.get_elements(strategy='class name', value='fop-catch-weight', element=p)[0]
        product_price = scrapy.get_elements(OCADO_MAIN_COLUMN_PRODUCTS_XPATH + '//span[contains(@class,"fop-price")]')[key]
        product_link = scrapy.get_elements(OCADO_MAIN_COLUMN_PRODUCTS_XPATH + '/a')[key].get_attribute('href')
        product_list.append({
            'product_name': product_name.text if product_name else '',
            'product_catch_weight': product_catch_weight.text if product_catch_weight else '',
            'product_price': product_price.text if product_price else '',
            'product_link': product_link if product_link else ''
        })
    return product_list

if __name__ == "__main__":
    main()
