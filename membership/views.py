from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# from django.core.paginator import Paginator
from membership.models import MemberInfo, AuthUser
import math
import time
from uuid import uuid1



def is_login(request):
    if request.session.get('is_login', False):
        pass
    else:
        redirect('/membership/login')


# @login_required
def index(request):
    is_login(request)
    request.encoding = 'utf-8'
    if request.method == 'POST':
        phone = request.POST['phone']
        due = int(request.POST['due'])
        note = request.POST['note']

        if MemberInfo.objects(phone__exact=phone):
            # 数据库中有该会员
            user = MemberInfo.objects(phone=phone)[0]
            print(user.phone)
            payment = calculate(user, due, note)
            context = {
                'due': due,
                'payment': payment,
                'discounts': due - payment,
                'balance': user.balance
            }
            return render(request, 'membership/result.html', context=context)
        else:
            # 数据库中无该会员
            new_member = MemberInfo.objects.create(
                phone=phone,
                balance=due,
                first_order=time.strftime("%Y-%m-%d %H:%M", time.localtime()),
                recent_order = [{
                    'uuid': str(uuid1()),
                    'order_time': time.strftime("%Y-%m-%d %H:%M", time.localtime()),
                    'note': note,
                    'payment': due,
                     }]
            )
            new_member.save()
            context = {
                'due': due,
                'payment': due,
                'discounts': 0,
                'balance': due
            }
            return render(request, 'membership/result.html', context=context)
    else:
        return render(request, 'membership/index.html')

def calculate(user, due, note):
    discounts = math.ceil(due * 0.15)                       # 最大折扣 85折, 向上取整
    if user.balance >= discounts:
        user.balance = user.balance - discounts     # 余额扣去本次消费折扣
        payment = due - discounts
    else:
        payment = due - user.balance
        user.balance=0
    user.recent_order.append({
        'uuid': str(uuid1()),
        'order_time': time.strftime("%Y-%m-%d %H:%M", time.localtime()),
        'note': note,
        'payment': payment,
         })
    user.save()
    return payment




# @login_required
def table(request):
    is_login(request)
    if request.method == 'POST':
        try:
            index_data = request.POST['search']
            memberInfo = MemberInfo.objects(phone__icontains=index_data)
        except:
            memberInfo = MemberInfo.objects
        try:
            # if request.POST['delete']:
            #     check_box_list = request.getlist('check_box_list')
            phone = request.POST['phone']
            print(phone)
            MemberInfo.objects.filter(phone=phone).delete()
        except:
            print('ERROR')
            pass
    else:
        request.encoding = 'utf-8'
        memberInfo = MemberInfo.objects

    # paginator = Paginator(memberInfo, 5)
    # page = request.GET.get('page', 1)
    # loaded = paginator.page(page)
    return render(request, 'membership/table.html', context={
        'memberInfo': memberInfo,
        # 'memberInfo': loaded,
        # 'memberNum': memberInfo.count(),
    })

def record(request):
    is_login(request)
    phone = request.GET.get('phone')
    user = MemberInfo.objects(phone__exact=phone)[0]
    context = {
        'recent_order': user.recent_order,
    }
    # if request.method == 'POST':
    #     uuid = request.POST.get('uuid')
    #     print(user.recent_order.index(uuid))
    return render(request, 'membership/record.html', context=context)


# def result(request):
#     return render(request, 'membership/result.html')

def login(request):
    if request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        print(username, password)
        if username and password:  # 确保用户名和密码都不为空
            username = username.strip()
            try:
                user = AuthUser.objects.get(name=username)
            except:
                return render(request, 'membership/login.html')
            if user.password == password:
                print('success')
                # user = AuthUser.objects.get(name=username)
                request.session["is_login"] = True
                return redirect('/membership')
    return render(request, 'membership/login.html')
