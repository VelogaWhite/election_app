from django.test import TestCase
from django.urls import resolve
from election_app.views import home, vote, results
from election_app.models import Election, Candidate, Vote
from election_app.setup_data import create_test_data

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

    @classmethod
    def setUpTestData(cls):
        cls.election, cls.candidate = create_test_data()

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

    def test_vote_post_renders_confirm_page(self):
        response = self.client.post('/vote/', data={'candidate': self.candidate.id})
        self.assertTemplateUsed(response, 'confirm.html')
        
        # ตรวจสอบว่ามีชื่อผู้สมัครและชื่อเขตปรากฏอยู่ในหน้าเว็บ
        self.assertContains(response, 'ผู้สมัครคนที่ 1')
        self.assertContains(response, 'ราชบุรี เขต 1')
        
        self.assertContains(response, 'id_final_confirm_button')

class ResultsPageTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.election, cls.candidate = create_test_data()

    def test_results_url_resolves_to_results_view(self):
        # ตรวจสอบว่า url /results/ วิ่งไปที่ฟังก์ชัน results
        found = resolve('/results/')
        self.assertEqual(found.func, results)

    def test_results_post_saves_vote_and_returns_correct_html(self):
        # จำลองการส่งข้อมูล (กดปุ่มยืนยันครั้งสุดท้าย) โดยส่ง candidate_id ไปที่ /results/
        response = self.client.post('/results/', data={'candidate_id': self.candidate.id})
        
        # คาดหวังว่าคะแนนโหวตจะถูกบันทึกลง Database (ต้องมี Vote โผล่มา 1 record)
        self.assertEqual(Vote.objects.count(), 1)
        
        # ตรวจสอบว่า Vote ที่บันทึก เป็นของการเลือก Candidate คนที่ 1 จริงๆ
        new_vote = Vote.objects.first()
        self.assertEqual(new_vote.candidate, self.candidate)
        
        # คาดหวังว่าจะใช้เทมเพลต results.html
        self.assertTemplateUsed(response, 'results.html')
        
        # คาดหวังข้อความ "เลือกตั้งสำเร็จ" ตามที่ Functional Test ระบุไว้เป๊ะๆ
        self.assertContains(response, 'เลือกตั้งสำเร็จ')