from pages.base.base import BasePage
from common.utils import get_page_data, yaml_content_param_replace
from pages.main.main import Main


class News(BasePage):
    news_data = get_page_data('news')

    def click_a_appoint_new_on_special_news_item(self, news_item, index):
        step = yaml_content_param_replace(self.news_data[news_item][0]['steps'], param_dict={'index': str(index)})
        self.process_steps(step)

    def goto_main_from_news(self):
        self.steps(self.news_data['wangye'])
        return Main(self._driver)

    def goto_tieba_from_news(self):
        self.steps(self.news_data['tieba'])
        return Main(self._driver)

    def goto_zhidao_from_news(self):
        self.steps(self.news_data['zhidao'])
        return Main(self._driver)

    def goto_music_from_news(self):
        self.steps(self.news_data['music'])
        return Main(self._driver)

    def goto_images_from_news(self):
        self.steps(self.news_data['images'])
        return Main(self._driver)

    def goto_videos_from_news(self):
        self.steps(self.news_data['videos'])
        return Main(self._driver)

    def goto_map_from_news(self):
        self.steps(self.news_data['map'])
        return Main(self._driver)

    def goto_wenku_from_news(self):
        self.steps(self.news_data['wenku'])
        return Main(self._driver)
