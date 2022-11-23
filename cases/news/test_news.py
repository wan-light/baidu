import allure
from common.utils import get_test_page_data
from pages.base.app import App
import pytest

page_test_data = get_test_page_data('test_news')


@allure.epic(page_test_data['Test_news']['allure']['epic'])
class Test_news:
    def setup_class(self):
        with allure.step(page_test_data['Test_news']['setup_steps'][0]):
            self.app = App().start()
            self.news = self.app.main().goto_news()
            print("--------------------------------------------", page_test_data['Test_news']['allure']['epic'])

    def setup(self):
        with allure.step(page_test_data['Test_news']['setup_steps'][1]):
            self.news.switch_to_window(1)

    @allure.feature(page_test_data['test_click_one_hot_new']['allure']['feature'])
    @allure.story(page_test_data['test_click_one_hot_new']['allure']['story'])
    @pytest.mark.parametrize('index', page_test_data['test_click_one_hot_new']['select_index_new_click'])
    @pytest.mark.highs
    def test_click_one_hot_new(self, index):
        with allure.step(page_test_data['test_click_one_hot_new']['allure']['steps'][0]):
            self.news.click_a_appoint_new_on_special_news_item(
                page_test_data['test_click_one_hot_new']['news_item'], index)

    @allure.feature(page_test_data['test_click_one_local_new']['allure']['feature'])
    @allure.story(page_test_data['test_click_one_local_new']['allure']['story'])
    @pytest.mark.parametrize('index', page_test_data['test_click_one_local_new']['select_index_new_click'])
    @pytest.mark.lows
    def test_click_one_local_new(self, index):
        with allure.step(page_test_data['test_click_one_local_new']['allure']['steps'][0]):
            self.news.click_a_appoint_new_on_special_news_item(
                page_test_data['test_click_one_local_new']['news_item'], index)

    def teardown(self):
        with allure.step(page_test_data['Test_news']['teardown_steps'][0]):
            self.news.keep_windows((0, 1))

    def teardown_class(self):
        self.app.stop()
