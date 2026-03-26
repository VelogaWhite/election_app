from django.test import TestCase
from django.urls import resolve
from election_app.views import home

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        # ทดสอบว่า URL '/' (หน้าแรก) วิ่งไปหาฟังก์ชัน home ใน views.py หรือไม่
        found = resolve('/')
        self.assertEqual(found.func, home)

    def test_home_page_returns_correct_html(self):
        # จำลองการส่ง GET request ไปที่ '/'
        response = self.client.get('/')
        
        # ทดสอบว่า response ใช้เทมเพลตที่ชื่อว่า home.html (หรือ base.html ตามโครงสร้าง)
        self.assertTemplateUsed(response, 'home.html')
        
        # ทดสอบว่าในหน้าเว็บมีคำว่า 'election_app' และ 'เลือกตั้ง' ตามที่ Functional Test คาดหวัง
        self.assertContains(response, 'election_app')
        self.assertContains(response, 'เลือกตั้ง')