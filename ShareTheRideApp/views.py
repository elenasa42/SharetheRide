from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user,allowed_users
import reverse_geocoder as rg
from django.contrib.auth.models import User

from .forms import CreateUserForm,CustomerForm,CreateRouteForm,FindRouteForm
from .models import Customer,Route
# Create your views here.

#On createPage and findPage i do some transformations with the objects i save and take from the mysql db in order to be in the
#form i want.That is because the latitude in the longitude when stored in the db they change order in a certain way.So when i want to retrieve
# them i have to to do some transformations in order to have them back in the original order.

def signupPage(request):
    form = CreateUserForm()
           
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CreateUserForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            user = form.save()
            
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(
            user = user,
            
            )
            
            
            messages.success(request,'Account was created successfully')
            return redirect('signin')
            
          
                     
    return render(request, 'ShareTheRideApp/signup.html', {'form':form})
    

def signinPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request,user)
            return redirect('dashboard')
        else:
            messages.info(request,'Username OR password was incorrect')
            
    context = {}    
    return render(request, 'ShareTheRideApp/signin.html', context)
    
def logoutUser(request):
    logout(request)
    return redirect('signin')
    
    
def indexPage(request):
    
    context = {}    
    return render(request, 'ShareTheRideApp/index.html', context)
    
def dashPage(request):
    current_user = User.objects.get(pk=request.user.id)
    ob = Customer.objects.get(user_id = current_user.id)
    context = {'prof':ob}    
    return render(request, 'ShareTheRideApp/dashboard.html', context)
    
    
    
@login_required(login_url = 'login')    
def profilePage(request):
    context={}
    temp1=[]
    temp11=[]
    temp2=[]
    temp22=[]
    current_user = User.objects.get(pk=request.user.id)
    ob = Customer.objects.get(user_id = current_user.id)
    r = Route.objects.filter(user_id_id = ob.id)
    for i in range(0,len(r)):
        routF = r[i].routFrom
        routT = r[i].routTo
        temp = ""
        
        
        routFrom = str(routF[0]) + ',' + str(routF[1]).replace(" ", "")
        routTo = str(routT[0]) + ',' + str(routT[1]).replace(" ", "")
        
        
        i = 0
        while routFrom[i] != ',' :
            i+=1
        rF1 = routFrom[i+1:len(routFrom)]
        rF2 = routFrom[0:i]
        rF = (rF1,rF2)
        
        i = 0
        while routTo[i] != ',' :
            i+=1
        rT1 = routTo[i+1:len(routTo)]
        rT2 = routTo[0:i]
        rT = (rT1,rT2)
        
            
        
            
                         
        result1 = rg.search(rF)
        result2 = rg.search(rT)
        
        
        
        res1 = [ sub['name'] for sub in result1 ]
        res11 = [ sub['admin1'] for sub in result1 ]
        res2 = [ sub['name'] for sub in result2 ]
        res22 = [ sub['admin1'] for sub in result2 ]
        
        temp1.append(res1)
        temp11.append(res11)
        temp2.append(res2)
        temp22.append(res22)
    
   
        
    context = {'r1' : temp1,'r11' : temp11, 'r2' : temp2, 'r22' : temp22, 'prof' : ob}
    
    
    
   
    
    return render(request, 'ShareTheRideApp/profile.html',context )
    
    
    
@login_required(login_url = 'login')
def settingsPage(request):
    
    current_user = User.objects.get(pk=request.user.id)
    ob = Customer.objects.get(user_id = current_user.id)
    
    customer = request.user.customer
    form = CustomerForm(instance = customer)
    
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance = customer)
        if form.is_valid():
            form.save()
            
    
    
    context = {'form':form,'prof':ob}    
    return render(request, 'ShareTheRideApp/settings.html', context)    

    
    
@login_required(login_url = 'login')    
def createPage(request):
    
    current_user = User.objects.get(pk=request.user.id)
    ob = Customer.objects.get(user_id = current_user.id)
    
    form = CreateRouteForm()
    
    if request.method == 'POST':
        form = CreateRouteForm(request.POST)
        if form.is_valid():
            instance = form.save(commit = False)
            instance.user_id = request.user.customer
            instance.save()
            messages.success(request,'Route was created successfully')
    
    
    context = {'form':form,'prof':ob}    
    return render(request, 'ShareTheRideApp/create.html', context) 
    
    
    
@login_required(login_url = 'login')    
def findPage(request):
    
    current_user = User.objects.get(pk=request.user.id)
    ob = Customer.objects.get(user_id = current_user.id)
    
    form = FindRouteForm()
    custom = 0
    cu = 0
    temp1 = ""
    deiktis = 0
    j = 0
    radius = []
    t1=[] 
    t2=[]
    temp_r = [];
   
  
    
    if request.method == 'POST':
        form = FindRouteForm(request.POST)
        if form.is_valid():
            
            form.save()
            routFrom1 = request.POST.get('routFrom')
            routTo1 = request.POST.get('routTo')
            rout_category = 'create'
            if routFrom1[2] == '.' :
                temp = routFrom1[0:2]
                i = 3
                while routFrom1[i] != ',' :
                    temp1 += routFrom1[i]
                    i+=1
                temp2 = routFrom1[i+1 : len(routFrom1) + 1]
                routFrom = temp2 + routFrom1[i] + temp + '.' + temp1
            else :
                temp = routFrom1[0:2]
                routFrom = routFrom1[3:len(routFrom1) + 1] + routFrom1[2] + temp + '.' + '0'
            
            
            if routTo1[2] == '.' :
                temp = routTo1[0:2]
                i = 3
                while routTo1[i] != ',' :
                    temp1 += routTo1[i]
                    i+=1
                temp2 = routTo1[i+1 : len(routTo1) + 1]
                routTo = temp2 + routTo1[i] + temp + '.' + temp1
            else :
                temp = routTo1[0:2]
                routTo = routTo1[3:len(routTo1) + 1] + routTo1[2] + temp + '.' + '0'
            
            
            
            ob = Route.objects.filter(routFrom=routFrom,routTo=routTo,rout_category=rout_category)
            
            for i in range(0,len(ob)-1):
                
                cust = [ob[i].user_id_id]
                custom = Customer.objects.filter(pk=cust[i])
                
            
            
            temp_radius = Route.objects.all().filter(rout_category='create')
                              
                        
            for i in range(0,len(temp_radius)):
                j = 0
                
                while j <= len(str((temp_radius[i].routFrom)))-1:
                    if str(temp_radius[i].routFrom)[j] == ',':
                        deiktis = j
                        
                    j = j+1
                
                if (str(temp_radius[i].routFrom))[deiktis+5] == routFrom1[3] :
                    if((str(temp_radius[i].routFrom))[deiktis+6] != ')'):
                        
                        if int((str(temp_radius[i].routFrom))[deiktis+6]) == int(routFrom1[4]) :
                            radius += [temp_radius[i]]
                            
                        elif int((str(temp_radius[i].routFrom))[deiktis+6]) + 1 == int(routFrom1[4]) :
                            radius += [temp_radius[i]]
                            
                        elif int((str(temp_radius[i].routFrom))[deiktis+6]) -1 == int(routFrom1[4]) :
                            radius += [temp_radius[i]]
                            
            
            
            
            if radius != 0:
                if len(radius) == 1:
                    for i in range(0,len(radius)):
                       
                        
                        temp_r = Route.objects.filter(routFrom=radius[i].routFrom,rout_category='create')
                        
                        c = [temp_r[i].user_id_id]
                        cu = Customer.objects.filter(pk=c[i])
                        
                else :
                    for i in range(0,len(radius)):
                        
                        
                        temp_r += Route.objects.filter(routFrom=radius[i].routFrom,rout_category='create')
                        c = radius[i].user_id_id
                        cu = Customer.objects.filter(pk=c)
                       
                        
            
            if(temp_r != 0):
                for i in range(0,len(temp_r)):
                    
                    routF = temp_r[i].routFrom
                    routT = temp_r[i].routTo
                    temp = ""
                                    
                    routFrom = str(routF[0]) + ',' + str(routF[1]).replace(" ", "")
                    routTo = str(routT[0]) + ',' + str(routT[1]).replace(" ", "")
                    
                    
                    i = 0
                    while routFrom[i] != ',' :
                        i+=1
                    rF1 = routFrom[i+1:len(routFrom)]
                    rF2 = routFrom[0:i]
                    rF = (rF1,rF2)
                    
                    i = 0
                    while routTo[i] != ',' :
                        i+=1
                    rT1 = routTo[i+1:len(routTo)]
                    rT2 = routTo[0:i]
                    rT = (rT1,rT2)
                    
                        
                    
                        
                                     
                    result1 = rg.search(rF)
                    result2 = rg.search(rT)
                    
                    
                    
                    res1 = [ sub['name'] for sub in result1 ]
                    res11 = [ sub['admin1'] for sub in result1 ]
                    res2 = [ sub['name'] for sub in result2 ]
                    res22 = [ sub['admin1'] for sub in result2 ]
                    
                    t1.append(res1)
                    
                    t2.append(res2)
                    
                    
                   
               
            
           
                
          
           
    
    
     
    
    return render(request, 'ShareTheRideApp/find.html', {'form': form, 'customer': custom, 'c': cu,'r1': t1,'r2': t2,'prof':ob })  
