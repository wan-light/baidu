import selenium.webdriver.common.devtools.v85.profiler
from selenium.webdriver.common.by import By

from pages.base.base import BasePage
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOption
from selenium.webdriver.firefox.options import Options as FirefoxOption
from selenium.webdriver.edge.options import Options as EdgeOption

from pages.base.base import BasePage


class App(BasePage):
    def start(self):
        if self._driver is None:
            options = globals()[self.config['browser']['options']]()
            for content in self.config['browser']['optionsContent']:
                options.add_argument(content)
            self._driver = getattr(webdriver, self.config['browser']['type'], None)(options=options)
            self._driver.get(self.config['baseUrl'])
            self._driver.maximize_window()
            self._driver.implicitly_wait(3)
        else:
            self._driver.launch_app()
        self.allure_screenshot('main_page', self.config['screenshots_path'] + 'main_page.PNG')
        return self

    def restart(self):
        self.stop()
        self.start()

    def stop(self):
        self._driver.quit()

    def back(self):
        self._driver.back()

    def main(self):
        from pages.main.main import Main
        return Main(self._driver)
