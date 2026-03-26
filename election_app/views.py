from django.shortcuts import render
from .models import Election, Candidate

# ฟังก์ชันหน้าแรกที่เราเพิ่งสร้างเพื่อตอบโจทย์เทสต์
def home(request):
    return render(request, 'home.html')

# ฟังก์ชันเปล่าๆ (Dummy) เพื่อไม่ให้ urls.py พัง
def vote(request):
    # ดึงข้อมูลการเลือกตั้งเขตแรก
    election = Election.objects.first()
    # ดึงผู้สมัครทั้งหมดที่อยู่ในเขตนี้
    candidates = Candidate.objects.filter(election=election)
    
    # ส่งข้อมูลไปที่ vote.html
    context = {
        'election': election,
        'candidates': candidates
    }
    return render(request, 'vote.html', context)

def results(request):
    pass