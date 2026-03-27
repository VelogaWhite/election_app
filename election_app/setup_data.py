import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'election.settings')
django.setup()
from election_app.models import Election, Candidate

def create_test_data():
    """
    ฟังก์ชันสำหรับสร้างข้อมูลจำลองจำนวนมาก
    """
    #print("กำลังสร้างข้อมูลการเลือกตั้ง...")
    
    # เคลียร์ข้อมูลเก่าทิ้งก่อน (ถ้าต้องการรันซ้ำหลายรอบจะได้ข้อมูลไม่ซ้ำซ้อนซ้อน)
    Election.objects.all().delete()
    Candidate.objects.all().delete()

    # สร้างการเลือกตั้ง 2 เขต
    election_rb = Election.objects.create(name='ราชบุรี เขต 1', date='2026-03-12')
    election_bkk = Election.objects.create(name='กรุงเทพมหานคร เขต 1', date='2026-04-01')

    # สร้างผู้สมัครของ ราชบุรี เขต 1 จำนวน 10 คน
    first_candidate = None
    for i in range(1, 11):
        c = Candidate.objects.create(name=f'ผู้สมัครคนที่ {i}', election=election_rb)
        if i == 1:
            first_candidate = c

    # สร้างผู้สมัครของ กทม. เขต 1 จำนวน 5 คน
    for i in range(1, 6):
        Candidate.objects.create(name=f'นายใจดี เบอร์ {i}', election=election_bkk)

    #print("สร้างข้อมูลสำเร็จแล้ว!")
    return election_rb, first_candidate

if __name__ == '__main__':
    create_test_data()