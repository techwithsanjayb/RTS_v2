from django.shortcuts import render ,redirect
from rts.logger import *
from .forms import UserLoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .utils import *
from .models import *
#####################################################################


def home(request):
    record(request,"home view called")
    return render(request,'core/home.html',{'name':"Sanjay"})

####-----####-----####-----####------####-----####-----####-----####

def resolver_dashboard(request):
    record(request,"resolver_dashboard view called")
    return render(request,'core/resolver_dashboard.html')

####-----####-----####-----####------####-----####-----####-----####

def raiser_dashboard(request):
    record(request,"raiser_dashboard view called")
    return render(request,'core/raiser_dashboard.html')

####-----####-----####-----####------####-----####-----####-----####

def administrator_dashboard(request):
    record(request,"administrator_dashboard view called")
    # System_list_obj = System.objects.filter(is_active=True).all()
    # context = {
    #     'System_list_obj':System_list_obj
    # }
    return render(request,'core/administrator_dashboard.html')

####-----####-----####-----####------####-----####-----####-----####

def login_view(request):
    record(request, "login_view View Called")
    
    if request.user.is_authenticated:
        record(request, "User already authenticated. Redirecting to check role.")
        dashboard_url = redirect_based_on_role(request.user)
        
        if dashboard_url:
            return redirect(dashboard_url)
        else:
            logout(request)
            record(request, f"SECURITY WARNING: user authenticated but no role assigned")
            messages.error(request, "Role not assigned. Contact Administrator.")
            return redirect("core:login_view")
        
    
    UserLoginForm_obj = UserLoginForm(request.POST or None)
    
    if request.method == "POST":
        record(request,"POST Method calling --- User has filled form and posted data")
        
        if UserLoginForm_obj.is_valid():
            username = UserLoginForm_obj.cleaned_data['username']
            password = UserLoginForm_obj.cleaned_data['password']    
            
            record(request,"Form data is valid--Now sending request for authentication")
            user = authenticate(request,username=username,password=password)
            
            if user is None:
                record(request,"Authentication Failed. Invalid User Name or Password")
                messages.error(request,"Authentication Failed.Invalid User Name or Password")
                return render(request,"core/login_view.html",{'UserLoginForm_obj':UserLoginForm_obj})
            
            elif not user.is_active:
                record(request,"Inactive user tried to login")
                messages.error(request,"Account is not active. Please contact administrator")
                return render(request,"core/login_view.html",{'UserLoginForm_obj':UserLoginForm_obj})
                
            
            else:
                record(request,f"Authentication Passed-- logged in successfully ")
                login(request,user)
                request.session.set_expiry(0)  # browser close → logout
                record(request,"Role is being checked for redirection")
                
                # Role-based redirection
                dashboard_url = redirect_based_on_role(user)
                
                if dashboard_url:
                    record(request,f"Received dashboard Role is -- {dashboard_url}. Now Logged in User is being redirected to his Dashboard")
                    messages.success(request,f"Welcome {user.username} . You are logged in successfully")
                    return redirect(dashboard_url)
                else:
                    logout(request)
                    record(request,"Role not assigned. Contact Administrator")
                    messages.error(request, "Role not assigned. Contact Administrator.")
                    return redirect("core:login_view")
        else:
            record(request,"Form Data is invalid. User should fill valid data")
            messages.error(request, "Form Data is not valid. Please fill correct data")
            return render(request,"core/login_view.html",{'UserLoginForm_obj':UserLoginForm_obj})
    
    record(request,"GET Method calling --- Blank Form has been rendered to user for filling")
    return render(request,"core/login_view.html",{'UserLoginForm_obj':UserLoginForm_obj})
                    
####-----####-----####-----####------####-----####-----####-----####
   
    
def user_logout(request):
    record(request, "user_logout View Called")
    username = request.user.username
    logout(request)
    request.session.flush()
    record(request, f"{username} logged out successfully . Session has been flushed ")
    messages.success(request,"Logged out successfully !")
    return redirect('core:login_view')  # Redirect to the login page after logging out

####-----####-----####-----####------####-----####-----####-----####



####-----####-----####-----####------####-----####-----####-----####



####-----####-----####-----####------####-----####-----####-----####



####-----####-----####-----####------####-----####-----####-----####



####-----####-----####-----####------####-----####-----####-----####



####-----####-----####-----####------####-----####-----####-----####



####-----####-----####-----####------####-----####-----####-----####



####-----####-----####-----####------####-----####-----####-----####



####-----####-----####-----####------####-----####-----####-----####



####-----####-----####-----####------####-----####-----####-----####



####-----####-----####-----####------####-----####-----####-----####
