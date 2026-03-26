from django.shortcuts import render
from .models import Election, Candidate

# ฟังก์ชันหน้าแรกที่เราเพิ่งสร้างเพื่อตอบโจทย์เทสต์
def home(request):
    return render(request, 'home.html')

def vote(request):
    # ดึงข้อมูลการเลือกตั้งเขตแรก
    election = Election.objects.first()
    
    # ถ้ามีการกดปุ่ม Submit ส่งข้อมูลมา (POST)
    if request.method == 'POST':
        candidate_id = request.POST.get('candidate') # ดึง id ของผู้สมัครจากฟอร์ม
        selected_candidate = Candidate.objects.get(id=candidate_id)
        
        # ส่งข้อมูลไปแสดงผลที่หน้า confirm
        context = {
            'election': election,
            'candidate': selected_candidate
        }
        return render(request, 'confirm.html', context)
    
    # ถ้าแค่เปิดหน้าเว็บเข้ามาธรรมดา (GET)
    candidates = Candidate.objects.filter(election=election)
    context = {
        'election': election,
        'candidates': candidates
    }
    return render(request, 'vote.html', context)

def results(request):
    pass