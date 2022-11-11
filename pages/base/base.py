import re
import time
import allure
from selenium import webdriver
from common.wrapper import handle_black
from common.utils import get_logger, get_config_data


class BasePage:
    _params = {}
    _driver = None
    logger = get_logger()
    config = get_config_data()

    def __init__(self, driver: webdriver = None):
        self._driver = driver

    def set_implicitly(self, wait_time):
        self._driver.implicitly_wait(wait_time)

    def screenshot(self, name):
        self._driver.get_screenshot_as_file(name)

    def allure_screenshot(self, filename, file_path):
        self.screenshot(file_path)
        with open(file_path, "rb") as f:
            content = f.read()
        allure.attach(content, name=filename, attachment_type=allure.attachment_type.PNG)

    def switch_to_window(self, index):
        handles = self._driver.window_handles
        self._driver.switch_to.window(handles[index])

    def keep_windows(self, keep_windows_tuple: tuple):
        handles = self._driver.window_handles
        if len(handles) <= len(keep_windows_tuple):
            raise ValueError
        for index in range(len(handles)):
            if not keep_windows_tuple.__contains__(index):
                self.switch_to_window(index)
                self._driver.close()

    @handle_black
    def finds(self, locator, value: str = None):
        elements: list
        if isinstance(locator, tuple):
            elements = self._driver.find_elements(*locator)
        else:
            elements = self._driver.find_elements(locator, value)
        return elements

    @handle_black
    def find(self, locator, value: str = None):
        if isinstance(locator, tuple):
            element = self._driver.find_element(*locator)
        else:
            element = self._driver.find_element(locator, value)
        return element

    @handle_black
    def find_and_get_text(self, locator, value: str = None):
        if isinstance(locator, tuple):
            element_text = self._driver.find_element(*locator).text
        else:
            element_text = self._driver.find_element(locator, value).text
        return element_text

    def find_js_click(self, ele):
        self._driver.execute_script('arguments[0].click();', ele)

    def window_vertical_scroll_to_by_js(self, height_start=0,
                                        height_stop='document.body.scrollHeight', scroll_to_nums=1):
        for i in range(scroll_to_nums):
            if height_stop == 1:
                height_stop = 'document.body.scrollHeight'
            self._driver.execute_script(f'window.scrollTo({height_start}, {height_stop})')

    def check_text_in_page(self, text: str, page: str):
        target_string = re.sub('[./]+', '', text)
        target_string_sub_list = re.split('[^\u4e00 -\u9fa5]+', target_string)
        print('target_string', target_string)
        print('target_string_sub_list', target_string_sub_list)

        for target_string_sub in target_string_sub_list:
            if not page.__contains__(target_string_sub):
                return False
        return True

    def before_exec_action_prepare(self, before_exec_action):
        if 'switch_window' in before_exec_action:
            self.switch_to_window(before_exec_action['switch_window'])
        if 'scroll_vertical_to' in before_exec_action:
            self.window_vertical_scroll_to_by_js(**before_exec_action['scroll_vertical_to'])

    def check_points_params_process(self, after_exec_action, element):
        print('check_points----------', after_exec_action)
        print('element---------------', element.text)
        if "check_points" in after_exec_action:
            check_points = after_exec_action['check_points']
            for index in range(len(check_points)):
                if check_points[index]['type'] == 'text_in_page':
                    if check_points[index]['is_action_element'] == 1:
                        text = element.text
                        check_points[index]['text'] = text
        return after_exec_action

    def check_points_process(self, after_exec_action):
        if "check_points" in after_exec_action:
            for check in after_exec_action['check_points']:
                if check['type'] == 'text_in_page':
                    if check['text'].count("${") == 1 and check['is_action_element'] == 0:
                        element = self.find(check['element']['by'], check['element']['locator'])
                        time.sleep(2)
                        page = self._driver.page_source
                        text = element.text
                        self.allure_screenshot('before_assert_screenshot',
                                               self.config['screenshots_path'] + 'assert.PNG')
                        assert self.check_text_in_page(text, page) == True
                    else:
                        time.sleep(2)
                        page = self._driver.page_source
                        self.allure_screenshot('before_assert_screenshot',
                                               self.config['screenshots_path'] + 'assert.PNG')
                        assert self.check_text_in_page(check['text'], page) == True

    def after_exec_action_process(self, after_exec_action):
        if "switch_window" in after_exec_action:
            self.switch_to_window(after_exec_action["switch_window"])
        if "sleep" in after_exec_action:
            time.sleep(after_exec_action["sleep"])
        self.check_points_process(after_exec_action)
        if "is_screenshot" in after_exec_action:
            if after_exec_action['is_screenshot'] == 1:
                screenshot_path = self.config['screenshots_path'] + after_exec_action['screenshot_name'] + '.PNG'
                self.allure_screenshot(after_exec_action["screenshot_name"], screenshot_path)

    def process_steps(self, steps):
        for step in steps:
            self.before_exec_action_prepare(step['before_exec_action'])
            if "action" in step.keys():
                action = step["action"]
                if "index" in step["locator"]:
                    element = self.finds(step["locator"]["by"],
                                         step["locator"]["locator"])[int(step["locator"]["index"])]
                else:
                    element = self.find(step["locator"]["by"], step["locator"]["locator"])
                step['after_exec_action'] = self.check_points_params_process(step['after_exec_action'], element)
                print("link is :" + element.get_attribute('href'))
                if "click" == action:
                    element.click()
                if "send" == action:
                    element.send_keys(step["value"])
            self.after_exec_action_process(step['after_exec_action'])

    def back(self):
        self._driver.back()
