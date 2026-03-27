from django.shortcuts import render
from django.db.models import Count
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
    # ดึงข้อมูลการเลือกตั้ง (ในที่นี้คือเขตแรกตามตัวอย่างเดิม)
    election = Election.objects.first()
    
    # ดึงรายชื่อผู้สมัครและนับจำนวนโหวต (Vote) ที่เชื่อมโยงกับผู้สมัครแต่ละคน
    candidates = Candidate.objects.filter(election=election).annotate(total_votes=Count('vote')).order_by('-total_votes')
    
    success_message = False
    if request.method == 'POST':
        candidate_id = request.POST.get('candidate_id')
        selected_candidate = Candidate.objects.get(id=candidate_id)
        
        # บันทึกคะแนนเสียง
        Vote.objects.create(candidate=selected_candidate, voter_id='voter_12345')
        success_message = True
        
        # อัปเดตข้อมูลคะแนนใหม่หลังจากบันทึกแล้ว
        candidates = Candidate.objects.filter(election=election).annotate(total_votes=Count('vote')).order_by('-total_votes')

    context = {
        'election': election,
        'candidates': candidates,
        'success_message': success_message
    }
    return render(request, 'results.html', context)

    return render(request, 'results.html')