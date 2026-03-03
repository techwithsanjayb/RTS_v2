from django.shortcuts import render ,redirect
from rts.logger import *
from .forms import UserLoginForm, TicketCreateForm
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

@login_required
def raise_ticket(request):
    record(request, "raise_ticket view called")
    form = TicketCreateForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.raised_by = request.user
            ticket.reported_date = timezone.now()
            initial_status = TicketStatus.objects.filter(code='OPEN').first()
            if initial_status:
                ticket.status = initial_status
            ticket.complaint_id = generate_complaint_id()
            resolver = auto_assign_ticket(ticket)
            print("###########",resolver)
            if resolver:
                # ticket.assigned_to = resolver # Assigning the resolver here
                messages.success(request, f"Ticket #{ticket.complaint_id} assigned to {resolver.user.username}")
            else:
                messages.warning(request, f"Ticket #{ticket.complaint_id} raised. Pending assignment.")

            ticket.save()

            return redirect('core:raiser_dashboard')
        
        else:
            messages.error(request, "Please correct the errors in the form below.")

    return render(request, 'core/raise_ticket.html', {'form': form})

####-----####-----####-----####------####-----####-----####-----####

def get_categories(request):
    """AJAX endpoint to get categories for selected department"""
    from django.http import JsonResponse
    dept_id = request.GET.get('department_id')
    if dept_id:
        categories = Category.objects.filter(department_id=dept_id).values('id', 'name')
        return JsonResponse(list(categories), safe=False)
    return JsonResponse([], safe=False)

####-----####-----####-----####------####-----####-----####-----####

def get_issues(request):
    """AJAX endpoint to get issues for selected category"""
    from django.http import JsonResponse
    cat_id = request.GET.get('category_id')
    if cat_id:
        issues = List_of_Issue.objects.filter(Issue_category_id=cat_id).values('id', 'name')
        return JsonResponse(list(issues), safe=False)
    return JsonResponse([], safe=False)

####-----####-----####-----####------####-----####-----####-----####

def administrator_dashboard(request):
    record(request,"administrator_dashboard view called")
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
