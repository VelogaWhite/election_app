from django.shortcuts import render
from .models import Election, Candidate, Vote

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
    if request.method == 'POST':
        candidate_id = request.POST.get('candidate_id')
        selected_candidate = Candidate.objects.get(id=candidate_id)
        
        # บันทึกคะแนนเสียงลง Database
        # (สมมติ voter_id เป็นไอดีจำลองไปก่อนสำหรับการทดสอบนี้)
        Vote.objects.create(candidate=selected_candidate, voter_id='voter_12345')
        
        return render(request, 'results.html')

    return render(request, 'results.html')