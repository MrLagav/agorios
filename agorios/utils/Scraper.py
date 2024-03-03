import selenium
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

class Scraper:
    """
    A class for web scraping using Selenium.

    Attributes:
        headless (bool): Whether to run the browser in headless mode.
    """

    def __init__(self, headless:bool = True, browser_detached:bool = False)->None:
        """
        Initializes the Scraper object.

        Args:
            headless : (bool, optional)
                Whether to run the browser in headless mode. Defaults to True.
            browser_detached : (bool, optional)
                Whether to detach the browser. Defaults to False.

        Returns:
            None
        """
        self.options = webdriver.ChromeOptions()
        if headless:
            self.options.add_argument("--headless=new")
        if browser_detached:
            self.options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=self.options)

    def get(self, url:str)->webdriver:
        """
        Open a webpage in the browser.

        Args:
            url : str
            The URL of the webpage to access.

        Returns:
            None
        """
        return self.driver.get(url)

    def wait(self, wait_time:int)->None:
        '''
        Args:
            wait_time : int
                Waiting time in seconds.
        Returns:
            None
        '''
        time.sleep(wait_time)
        pass

    def typein_field(self, input_xpath:str, input_value:str, enter_key:bool)->None:
        """
        Enters text into a field and optionally presses enter.

        Args:
            input_xpath : str
                The XPATH of the input field.
            input_value : str
                The value to be entered into the input field.
            enter_key : bool
                Whether to press the enter key after entering the value.

        Returns:
            None
        """
        el = self.driver.find_element(By.XPATH, input_xpath)
        el.clear()
        el.send_keys(input_value)
        if enter_key:
            el.send_keys(Keys.RETURN)
        pass

    def click_element(self, element_xpath:str)->None:
        """
        Clicks an element identified by its XPath.

        Args:
            element_xpath : str
                The XPATH of the element to click.

        Returns:
            None
        """
        el = self.driver.find_element(By.XPATH, element_xpath)
        el.click()
        pass

    def return_children(self, element:WebElement)->WebElement:
        """
        Returns the children of a given WebElement.

        Args:
            element : WebElement
                The parent element whose children are to be returned.

        Returns:
            WebElement: List of child elements.
        """
        child = element.find_elements(By.XPATH, './child::*')
        return child

    def get_elements(self, value:str, strategy:str = By.XPATH, element:WebElement = None)->list[WebElement]:
        """
        Finds and returns web elements based on the specified strategy and value.

        Args:
            value : str
                The value to search for.
            strategy : str, optional
                The search strategy, by default XPath.
            element : WebElement, optional
                The parent element to search within, by default None.

        Returns:
            list[WebElement]: List of found web elements.
        """
        if element:
            return element.find_elements(strategy, value)
        return self.driver.find_elements(strategy, value)

    def check_if_exists(self, element_xpath:str)->bool:
        """
        Checks if an element exists based on its XPath.

        Args:
            element_xpath : str
                The XPATH of the element to check.

        Returns:
            bool: True if the element exists, False otherwise.
        """
        return True if not len(self.driver.find_elements(By.XPATH, element_xpath)) == 0 else False

    def scroll_and_load_page(self, wait_time:int = 20)->None:
        """
        Scrolls to the bottom of the page and waits for dynamic content to load.

        Args:
            wait_time : int, optional
                The time to wait after scrolling, by default 20 seconds.

        Returns:
            None
        """
        smooth_scroll_script = """
            function smoothScrollToBottom(callback) {
                var height = document.documentElement.scrollHeight || document.body.scrollHeight;
                var scrollStep = height / 100;
                var currentScroll = 0;
                console.log('starting to scroll');
                var scrollInterval = setInterval(function(){
                    currentScroll += scrollStep;
                    window.scrollTo(0, currentScroll);
                    if(currentScroll >= height) {
                        clearInterval(scrollInterval);
                        if (callback && typeof callback === 'function') {
                            callback(); // Execute the callback function if provided
                        }
                    }
                }, 100);
            }

            smoothScrollToBottom(function(){
                console.log('finished scrolling');
            });
        """
        self.driver.execute_script(smooth_scroll_script)
        self.wait(wait_time)
        pass
