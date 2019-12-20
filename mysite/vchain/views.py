from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Account, Student
from django.core.files.storage import FileSystemStorage
from requests_toolbelt import MultipartEncoder
from datetime import datetime
import json
import requests
# Create your views here.

def index(request):
    request.session.flush()
    if(request.method == 'POST'):
        url = "http://178.128.217.110:8175/xmbc_DC2019_6_DC2019_6/get"
        parameters = {
            "id" : request.POST['id']
        }
        print(request.POST['id'])
        response = requests.get(url, params = parameters)
        if (response.status_code != 200):
            errors = "Truy vấn thực hiện không thành công!"
            return render(request, 'vchain/index.html', {"errors" : errors})
        elif (response.status_code == 200):
            if(response.json() == []):
                return render(request, 'vchain/index.html', {"errors" : "Không tồn tại id"})
            else:
                # file = open('data.txt', )
                data = response.json()
                first = data[0]


                #create file
                data = response.json()

                with open ('assets/files/sinhvien.txt', 'w+', encoding='utf-8') as outfile:
                    json.dump(data, outfile, ensure_ascii=False)

                return render(request, 'vchain/index.html', {"students" : data, 'name_student' : first['name_student'],
                                                             'mssv' : first['mssv']})

    else:
        return render(request, 'vchain/index.html')


def login(request):
    request.session.flush()
    if(request.method == 'POST'):
        account = Account.objects.filter(username = request.POST['username'], password = request.POST['password'])
        print(account)
        url = 'http://178.128.217.110:8175/authentication'
        data = {
            "username" : request.POST['v-n'],
            "password" :request.POST['v-p']
        }
        response = requests.post(url=url, json=data)
        request.session['v-n'] = request.POST['v-n']
        request.session['v-p'] = request.POST['v-p']
        if(len(account) == True and response.json()['statusCode'] == 0):
            return HttpResponseRedirect('/vchain/create')
        else:
            return render(request, 'vchain/login.html', {'error' : 'Đăng nhập thất bại!'})
    else:
        return render(request, 'vchain/login.html')


# def create(request):
#     if 'v-p' not in request.session:
#         return HttpResponseRedirect('login')
#     if request.method == "POST":
#         uploaded_file = request.FILES['image']
#         fs = FileSystemStorage()
#         name = fs.save(uploaded_file.name, uploaded_file)
#         img_url = fs.url(name)[1:]
#
#         #Authorization
#         url = 'http://178.128.217.110:8175/authentication'
#         data = {
#             "username": request.session['v-n'],
#             "password": request.session['v-p']
#         }
#         response = requests.post(url=url, json=data)
#         auth = response.json()['authorization']
#         print(auth)
#         # Create
#         url = 'http://178.128.217.110:8175/xmbc_DC2019_6_DC2019_6/create'
#
#         m = MultipartEncoder(
#             fields={
#             "name_student" : request.POST['name'],
#             "mssv" : request.POST['mssv'],
#             "date_provide" : request.POST['date_provide'],
#             "name_certification" : request.POST['name_cert'],
#             'image': ('filename', open(img_url, 'rb'))}
#         )
#
#         response = requests.post(url, data=m,
#                           headers={'Content-Type': m.content_type, 'Authorization' : auth})
#         print(response)
#         # print(json.dumps(response))
#         if("status" in response.json() and response.json()['status'] == 'Success'):
#
#             obj = Student.objects.create(public_key = response.json()['id'], mssv = request.POST['mssv'])
#             obj.save()
#             return render(request, 'vchain/create.html', {"id" : response.json()['id']})
#         else:
#             return render(request, 'vchain/create.html', {"error" : 1})
#     else:
#         return render(request, 'vchain/create.html')
def create(request):
    if 'v-p' not in request.session:
        return HttpResponseRedirect('login')
    if request.method == "POST" and "create" in request.POST:
        uploaded_file = request.FILES['file_info']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        img_url = fs.url(name)[1:]
        f = open(img_url, "r", encoding='utf-8')
        list_upload_ok = []
        for x in f:
            t = x.strip()
            o = json.loads(t)
            url = 'http://178.128.217.110:8175/authentication'
            data = {
                "username": request.session['v-n'],
                "password": request.session['v-p']
            }
            response = requests.post(url=url, json=data)
            auth = response.json()['authorization']
            print(auth)
            # Create
            url = 'http://178.128.217.110:8175/xmbc_DC2019_6_DC2019_6/create'
            m = MultipartEncoder(
                fields={
                    "name_student": o['name_student'],
                    "mssv": o['mssv'],
                    "date_provide": o['date_provide'],
                    "name_certification": o['name_certification'],
                    'image': ('filename', open('media/' + o['image'], 'rb'))}
            )
            response = requests.post(url, data=m,
                                     headers={'Content-Type': m.content_type, 'Authorization': auth})
            if ("status" in response.json() and response.json()['status'] == 'Success'):
                obj = Student.objects.create(public_key=response.json()['id'], mssv=o['mssv'])
                obj.save()
                list_upload_ok.append(response.json()['id'])

        f.close()
        if len(list_upload_ok) == 0:
            return render(request, 'vchain/create.html', {"error_all" : "Quá trình đưa dữ liệu thất bại"})
        else:
            return render(request, 'vchain/create.html', {"list" : list_upload_ok})

    if request.method == "POST" and "create" not in request.POST:
        uploaded_file = request.FILES['image']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        img_url = fs.url(name)[1:]

        print(img_url)
        #Authorization
        url = 'http://178.128.217.110:8175/authentication'
        data = {
            "username": request.session['v-n'],
            "password": request.session['v-p']
        }
        response = requests.post(url=url, json=data)
        auth = response.json()['authorization']
        print(auth)
        # Create
        url = 'http://178.128.217.110:8175/xmbc_DC2019_6_DC2019_6/create'

        m = MultipartEncoder(
            fields={
            "name_student" : request.POST['name'],
            "mssv" : request.POST['mssv'],
            "date_provide" : request.POST['date_provide'],
            "name_certification" : request.POST['name_cert'],
            'image': ('filename', open(img_url, 'rb'))}
        )

        response = requests.post(url, data=m,
                          headers={'Content-Type': m.content_type, 'Authorization' : auth})
        if("status" in response.json() and response.json()['status'] == 'Success'):
            obj = Student.objects.create(public_key = response.json()['id'], mssv = request.POST['mssv'])
            obj.save()
            return render(request, 'vchain/create.html', {"id" : response.json()['id']})
        else:
            return render(request, 'vchain/create.html', {"error" : 1})
    else:
        return render(request, 'vchain/create.html')


def update(request):
    if 'v-p' not in request.session:
        return HttpResponseRedirect('login')
    if request.method == "POST" and "update" in request.POST:
        uploaded_file = request.FILES['file_info']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        img_url = fs.url(name)[1:]
        f = open(img_url, "r", encoding='utf-8')
        list_upload_ok = []
        count = 0
        for x in f:
            t = x.strip()
            o = json.loads(t)
            count += 1
            url = 'http://178.128.217.110:8175/authentication'
            data = {
                "username": request.session['v-n'],
                "password": request.session['v-p']
            }
            response = requests.post(url=url, json=data)
            auth = response.json()['authorization']
            print(auth)
            # Create
            url = 'http://178.128.217.110:8175/xmbc_DC2019_6_DC2019_6/update'
            m = MultipartEncoder(
                fields={
                    "id" : o['id'],
                    "date_provide": o['date_provide'],
                    "name_certification": o['name_certification'],
                    'image': ('filename', open('media/' + o['image'], 'rb'))}
            )
            response = requests.put(url, data=m,
                                     headers={'Content-Type': m.content_type, 'Authorization': auth})
            # if ("status" in response.json() and response.json()['status'] == 'Success'):

        f.close()
        return render(request, 'vchain/update.html', {"update_all" : 1, "count" : count})

    if request.method == "POST":
        uploaded_file = request.FILES['image']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        img_url = fs.url(name)[1:]

        # Authorization
        url = 'http://178.128.217.110:8175/authentication'
        data = {
            "username": request.session['v-n'],
            "password": request.session['v-p']
        }
        response = requests.post(url=url, json=data)
        auth = response.json()['authorization']
        print(auth)
        # Create
        url = 'http://178.128.217.110:8175/xmbc_DC2019_6_DC2019_6/update'

        m = MultipartEncoder(
            fields={
                "id" : request.POST['id'],
                "date_provide": request.POST['date_provide'],
                "name_certification": request.POST['name_cert'],
                'image': ('filename', open(img_url, 'rb'))}
        )

        response = requests.put(url, data=m,
                                 headers={'Content-Type': m.content_type, 'Authorization': auth})
        print(response.json())
        if ("status" in response.json() and response.json()['status'] == 'Success'):
            return render(request, 'vchain/update.html', {"success" : 1})
        else:
            return render(request, 'vchain/update.html', {"error": 1})
    else:
        return render(request, 'vchain/update.html')

