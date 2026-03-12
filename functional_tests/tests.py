from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import time
import os

MAX_WAIT = 10

class NewVisitorTest(StaticLiveServerTestCase):
    
    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, 'id_list_table')
                rows = table.find_elements(By.TAG_NAME, 'tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_elect(self):
        # เป็นวันเลือกตั้งแอพได้เปิดให้ user ใช้ Feature เลือกตั้งออนไลน์ได้
        # สมชายจึงเปิดแอพขึ้นมา
        self.browser.get(self.live_server_url)

        # สมชายเจอหน้าแรกที่มีหัวข้อต่างๆ สมชายเห็นหัวข้อ "เลือกตั้ง" และคลิกเข้าไป
        self.assertIn('เลือกตั้ง', self.browser.page_source)
        link = self.browser.find_element(By.LINK_TEXT, 'เลือกตั้ง')
        link.click()

        # เมื่อเขากด Enter เขาจะถูกนำไปยังหน้าใหม่ที่มีหัวข้อว่า "เลือกตั้ง"
        self.assertIn('เลือกตั้ง', self.browser.title)

        # สมชายจำได้ว่าจะเลือกใครเป็น สส เขต
        # ในหน้าเลือกตั้งเขาเห็นหัวข้อ "เลือก สส เขต" และคลิกเข้าไป
        self.assertIn('เลือก สส เขต', self.browser.page_source)
        link = self.browser.find_element(By.LINK_TEXT, 'เลือก สส เขต')
        link.click()

        # เมื่อเขากด Enter เขาจะถูกนำไปยังหน้าใหม่ที่มีหัวข้อว่า "เลือก สส เขต"
        self.assertIn('เลือก สส เขต', self.browser.title)

        # สมชายเห็น Dropdown 
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # She types "Buy peacock feathers" into a text box (Edith's hobby
        # is tying fly-fishing lures)
        inputbox.send_keys('Buy peacock feathers')

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list table
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')