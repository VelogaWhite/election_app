from django.shortcuts import render

# ฟังก์ชันหน้าแรกที่เราเพิ่งสร้างเพื่อตอบโจทย์เทสต์
def home(request):
    return render(request, 'home.html')

# ฟังก์ชันเปล่าๆ (Dummy) เพื่อไม่ให้ urls.py พัง
def vote(request):
    pass

def results(request):
    pass