from selenium import webdriver


class TestMainPage:

    def setup_method(self, method):
        #TODO: Add database setup code when we add more complicated tests
        self.driver = webdriver.Firefox()

    def test_can_hit_main_page(self):
        self.driver.get("http:localhost:5000")
        assert "GTD App" in self.driver.title

    def teardown_method(self, method):
        #TODO: Add database teardown code when we add more complicated tests
        self.driver.quit()

