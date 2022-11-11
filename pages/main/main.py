from pages.base.base import BasePage
from common.utils import get_page_data


class Main(BasePage):

    main_data = get_page_data('main')

    def goto_news(self):
        from pages.news.news import News
        self.process_steps(self.main_data['news'][0]['steps'])
        return News(self._driver)

    def goto_hao123(self):
        from pages.news.news import News
        self.process_steps(self.main_data['hao123'][0]['steps'])
        return News(self._driver)

    def goto_map(self):
        from pages.news.news import News
        self.process_steps(self.main_data['map'][0]['steps'])
        return News(self._driver)

    def goto_tieba(self):
        from pages.news.news import News
        self.process_steps(self.main_data['tieba'][0]['steps'])
        return News(self._driver)

    def goto_videos(self):
        from pages.news.news import News
        self.process_steps(self.main_data['videos'][0]['steps'])
        return News(self._driver)

    def goto_images(self):
        from pages.news.news import News
        self.process_steps(self.main_data['images'][0]['steps'])
        return News(self._driver)

    def goto_netdisk(self):
        from pages.news.news import News
        self.process_steps(self.main_data['netdisk'][0]['steps'])
        return News(self._driver)

    def goto_more(self):
        from pages.news.news import News
        self.process_steps(self.main_data['news'][0]['steps'])
        return News(self._driver)
