from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,logout,login
from .models import *

def index(request):
    return render(request,'index.html')

def login(request):
    error=""
    if request.method=='POST':
        u=request.POST['uname']
        p=request.POST['pswd']
        user = auth.authenticate(username=u,password=p)
        try:
            if user.is_staff:
                auth.login(request,user)
                error="no"
            elif user is not None:
                auth.login(request,user)
                error="not"
            else:
                error="yes"
        except:
            error="yes"
    d={'error':error}
    return render(request,'login.html',d)

def signup(request):
    error = ""
    if request.method=='POST':
        f=request.POST['fname']
        l=request.POST['lname']
        e=request.POST['email']
        con=request.POST['contact']
        gen=request.POST['gender']
        d=request.POST['dob']
        p=request.POST['pwd']
        i=request.FILES['profile_pic']
        try:
            user=User.objects.create_user(first_name=f,last_name=l,username=e,password=p)
            Signup.objects.create(user=user,mobile=con,image=i,gender=gen,dob=d)
            error="no"
        except:
            error="yes"
    d={'error':error}
    return render(request,'signup.html',d)

def contact_us(request):
    error=""
    if request.method=="POST":
        n=request.POST['fname']
        e=request.POST['email']
        m=request.POST['mobile']
        p=request.POST['purpose']
        try:
            Contact.objects.create(c_name=n,c_email=e,c_mobile=m,c_purpose=p)
            error="no"
        except:
            error="yes"
    d={'error':error}
    return render(request,'contact_us.html',d)


def admin_home(request):
    return render(request,'admin_home.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def user_home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request,'user_home.html')

def add_room(request):
    error=""
    if not request.user.is_staff:
        return redirect('login')
    if request.method=='POST':
        pn=request.POST['pname']
        ps=request.POST['pstate']
        pc=request.POST['pcity']
        tp=request.POST['tprice']
        st=request.POST['status']
        i=request.FILES['image']
        act = request.POST['activity']
        ph = request.POST['phistory']
        try:
            Room.objects.create(p_name=pn,p_state=ps,p_city=pc,t_price=tp,status=st,
                                activity=act,image=i,history=ph)
            error="no"
        except:
            error="yes"
    d={'error':error}
    return render(request,'add_room.html',d)


def view_room_admin(request):
    if not request.user.is_authenticated:
        return redirect('login')
    data=Room.objects.all()
    d={'data':data}
    return render(request,'view_room_admin.html',d)


def delete_room(request,id):
    data=Room.objects.get(id=id)
    data.delete()
    return redirect('view_room_admin')

def edit_room(request,pid):
    error=""
    data = Room.objects.get(id=pid)
    if request.method=='POST':
        pn = request.POST['pname']
        ps = request.POST['pstate']
        pc = request.POST['pcity']
        tp = request.POST['tprice']
        st = request.POST['status']
        act = request.POST['activity']
        ph = request.POST['phistory']
        data.p_name=pn
        data.p_state=ps
        data.p_city=pc
        data.t_price=tp
        data.status=st
        data.activity=act
        data.history=ph
        try:
            data.save()
            error="no"
        except:
            error="yes"
        try:
            i = request.FILES['image']
            data.image=i
            data.save()
            error="no"
        except:
            pass
    d={'data':data,'error':error}
    return render(request,'edit_room.html',d)

def view_booking_admin(request):
    data = Booked.objects.all()
    d={'data':data}
    return render(request,'view_booking_admin.html',d)

def view_room_user(request):
    data=Room.objects.all()
    d={'data':data}
    return render(request,'view_room_user.html',d)

def change_password_user(request):
    error=""
    if request.method=='POST':
        c=request.POST['currentpassword']
        n=request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error="no"
            else:
                error="not"
        except:
            error="yes"
    d={'error':error}
    return render(request,'change_password_user.html',d)

def change_password_admin(request):
    error=""
    if request.method=='POST':
        c=request.POST['currentpassword']
        n=request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error="no"
            else:
                error="not"
        except:
            error="yes"
    d={'error':error}
    return render(request,'change_password_admin.html',d)

def edit_profile(request):
    error=""
    data=User.objects.get(id=request.user.id)
    data2=Signup.objects.get(user=data)
    if request.method=='POST':
        f = request.POST['fname']
        l = request.POST['lname']
        c = request.POST['contact']
        g = request.POST['gender']
        do = request.POST['dob']
        data.first_name=f
        data.last_name=l
        data2.mobile=c
        data2.gender=g
        data2.dob=do
        try:
            data.save()
            data2.save()
            error="no"
        except:
            error="yes"
        try:
            i=request.FILES['image']
            data2.image=i
            data2.save()
            error="no"
        except:
            pass
    d={'data':data,'data2':data2,'error':error}
    return render(request,'edit_profile.html',d)


def user_booking(request):
    data = Booked.objects.all()
    d={'data':data}
    return render(request,'user_booking.html',d)


def book_room(request,id):
    error=""
    data=Room.objects.get(id=id)
    data2=Signup.objects.get(user=request.user)
    if request.method=='POST':
        f=request.POST['fname']
        l=request.POST['lname']
        name=f+" "+l
        e=request.POST['email']
        c=request.POST['contact']
        c2=request.POST['contact2']
        b=request.POST['booking_date']
        d=request.POST['select_days']
        tt=request.POST['total_ticket']
        p=request.POST['price']
        np=int(p)*int(d)*int(tt)
        add=request.POST['address']
        try:
            Booked.objects.create(full_name=name,email=e,contact=c,contact2=c2,bookint_date=b,days=d,gender=tt,price=np,dob=add,status="Pending")
            error="no"
        except:
            error="yes"
    dd={'data':data,'data2':data2,'error':error}
    return render(request,'book_room.html',dd)

def change_status(request,id):
    error=""
    data=Booked.objects.get(id=id)
    if request.method=='POST':
        s=request.POST['rstatus']
        data.status=s
        try:
            data.save()
            error="no"
        except:
            error="yes"
    d={'data':data,'error':error}
    return render(request,'change_status.html',d)


def view_user(request):
    if not request.user.is_authenticated:
        return redirect('login')
    data=Signup.objects.all()
    d={'data':data}
    return render(request,'view_user.html',d)

def delete_user(request,id):
    data=User.objects.get(id=id)
    data.delete()
    return redirect('view_user')

def delete_booking(request,id):
    data=Booked.objects.get(id=id)
    data.delete()
    return redirect('view_booking_admin')

def cancel_booking(request,id):
    data = Booked.objects.get(id=id)
    data.delete()
    return redirect('user_booking')

def view_contact(request):
    data = Contact.objects.all()
    d={'data':data}
    return render(request,'view_contact.html',d)

def delete_contact(request,id):
    data = Contact.objects.get(id=id)
    data.delete()
    return redirect('view_contact')


def search(request):
    n=request.POST['name']
    data = Room.objects.filter(type__icontains=n)
    d={'data':data}
    return render(request,'view_room_user.html',d)

def searchh(request):
    n=request.POST['name']
    data = Booked.objects.filter(email__icontains=n)
    d={'data':data}
    return render(request,'view_booking_admin.html',d)


def more_detail(request,id):
    data = Room.objects.get(id=id)
    d = {'data':data}
    return render(request,'more_detail.html',d)

