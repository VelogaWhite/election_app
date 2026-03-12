from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import time
import os

MAX_WAIT = 10

class NewElectionTest(StaticLiveServerTestCase):
    
    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def logout(self):
        self.browser.delete_all_cookies()


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

        # สมชายเห็นหน้า แล้วมีหัวข้อล็อกไว้ให้อยู่แล้วว่า เป็น "ราชบุรี เขต 1" ตรงกับข้อมูลที่เขาจำได้
        self.assertIn('ราชบุรี เขต 1', self.browser.page_source)

        # สมชายเห็น Dropdown ให้เลือกผู้สมัคร และเลือกผู้สมัครคนที่ 1
        self.assertIn('เลือกผู้สมัคร', self.browser.page_source)
        dropdown = self.browser.find_element(By.ID, 'id_candidate')  
        dropdown.click()
        option = dropdown.find_element(By.XPATH, "//option[@value='1']")
        option.click()

        # สมชายเห็นปุ่ม "ยืนยันการเลือกตั้ง" และคลิกเข้าไป
        self.assertIn('ยืนยันการเลือกตั้ง', self.browser.page_source)
        button = self.browser.find_element(By.ID, 'id_confirm_button')
        button.click()

        # เมื่อเขากด ยันยัน ระบบได้แสดงหน้าว่า สมชายได้เลือกผู้สมัครคนที่ 1 ในเขต "ราชบุรี เขต 1" แล้วมีให้กดยืนยันอีกครั้ง
        self.assertIn('คุณได้เลือกผู้สมัครคนที่ 1 ในเขต ราชบุรี เขต 1', self.browser.page_source)
        confirm_button = self.browser.find_element(By.ID, 'id_final_confirm_button')
        confirm_button.click()

        # เมื่อกดยืนยันครั้งสุดท้ายแล้ว ระบบก็ได้แสดงหน้าว่า "เลือกตั้งสำเร็จ"
        self.assertIn('เลือกตั้งสำเร็จ', self.browser.page_source)

        # สมชายก็ได้ปิดแอบลงไป
        self.logout()
