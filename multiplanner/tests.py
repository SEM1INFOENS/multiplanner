
# Integration tests

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.touch_actions import TouchActions


class AccountTestCase(LiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Firefox()
        super(AccountTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(AccountTestCase, self).tearDown()

    def test_register(self):
        selenium = self.selenium
        #Opening the link we want to test
        selenium.get(self.live_server_url+'/signup')
        #find the form element
        username = selenium.find_element_by_id('id_username')
        password1 = selenium.find_element_by_id('id_password1')
        password2 = selenium.find_element_by_id('id_password2')

        submit = selenium.find_element_by_id('submit')

        #Fill the form with data
        username.send_keys('unary2')
        password1.send_keys('cavacava')
        password2.send_keys('cavacava')
        
        submit.click()
        #check the returned result
        assert 'Your current balance is' in selenium.page_source