from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    taisan = {"Dien thoai", "May Tinh", "Gai"}
    context = {"name" : "Cuong", "taisan" : taisan}
    return render(request, "polls/index.html", context)


def sanpham(request):
    return HttpResponse("Chúng tôi hiện chưa có sản phẩm nào !")
