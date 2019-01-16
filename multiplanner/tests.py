
# Integration tests

from groups.models import Group
from accounting.models import Transaction, TransactionPart

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.touch_actions import TouchActions
from django.test.utils import override_settings
from django.conf import settings
import time



class AccountTestCase(StaticLiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Firefox()
        super(AccountTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(AccountTestCase, self).tearDown()

    def sub_test_register(self):
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
        assert 'Your current balance' in selenium.page_source

    def sub_test_create_group(self):
        selenium = self.selenium
        selenium.find_element_by_xpath('//*[@id="navbarSupportedContent"]/ul[1]/li[2]/a').click()
        element = selenium.find_element_by_link_text("create a new group")
        element.click()

        name = selenium.find_element_by_name('name')
        name.send_keys('test_group')

        selenium.find_element_by_xpath("//*[@id='id_currency']/option[3]").click()

        #selenium.find_element_by_xpath('//*[@id="id_members_field"]/option[2]').click()

        selenium.find_element_by_xpath('//*[@id="content"]/form/input[3]').click()
        selenium.find_element_by_xpath('//*[@id="content"]/a[1]').click()
        selenium.find_element_by_xpath('//*[@id="content"]/form/input[3]').click()

        assert len(Group.objects.all()) == 1


    def sub_test_create_transaction(self):
        selenium = self.selenium

        selenium.find_element_by_xpath('//*[@id="content"]/button').click()
        selenium.find_element_by_xpath('//*[@id="id_payer"]/option[2]').click()
        selenium.find_element_by_xpath('//*[@id="id_amount_0"]').send_keys('1.00')
        selenium.find_element_by_xpath('//*[@id="exampleModal"]/div/div/div[2]/form/input[3]').click()
        selenium.find_element_by_xpath('//*[@id="content"]/form/input[6]').click()

        assert Transaction.objects.get(pk=1).amount.amount == 1.00

    @override_settings(DEBUG=True)
    def test_integration(self):
        self.sub_test_register()
        self.sub_test_create_group()
        #self.sub_test_create_transaction()
