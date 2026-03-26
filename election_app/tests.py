from django.test import TestCase
from django.urls import resolve
from election_app.views import home, vote, results
from election_app.models import Election, Candidate 

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

class VotePageTest(TestCase):

    def setUp(self):
        # จำลองข้อมูลใน Database เพราะหน้าเว็บต้องดึง "ราชบุรี เขต 1" มาแสดง
        self.election = Election.objects.create(name='ราชบุรี เขต 1', date='2026-03-12')
        Candidate.objects.create(name='ผู้สมัครคนที่ 1', election=self.election)

    def test_vote_url_resolves_to_vote_view(self):
        # เช็คว่า /vote/ วิ่งไปหาฟังก์ชัน vote
        found = resolve('/vote/')
        self.assertEqual(found.func, vote)

    def test_vote_page_returns_correct_html(self):
        # ลองเข้าหน้า /vote/
        response = self.client.get('/vote/')
        
        # คาดหวังว่าจะใช้เทมเพลต vote.html
        self.assertTemplateUsed(response, 'vote.html')
        
        # ตรวจสอบคำบนหน้าเว็บตามที่ FT คาดหวัง
        self.assertContains(response, 'เลือก สส เขต')
        self.assertContains(response, 'ราชบุรี เขต 1')
        self.assertContains(response, 'เลือกผู้สมัคร')