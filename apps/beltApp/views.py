from django.shortcuts import render, HttpResponse, redirect
from django.db.models import Count
from .models import User, Job, Category
import bcrypt
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'beltApp/index.html')


def register(request):
    print('in register method')

    if request.method == "POST":
        errors = User.objects.registration_validator(request.POST)

        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, key)
            return redirect('/')

        else:
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            email = request.POST['email']
            password = request.POST['password']

            hashpassword = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            print(hashpassword)
            
            user = User.objects.create(first_name = firstname, last_name = lastname, email = email, password = hashpassword)
            request.session['id'] = user.id
            user = User.objects.get(id=request.session['id'])
            print(user.id, user.first_name, user.last_name, user.email, user.password)
            messages.success(request, "User registration successfully completed!")
            uJobs = user.jobs.all()
            print(uJobs)
            context = {
                "usr": user,
                "uJobs": uJobs,
                "allJobs": Job.objects.all()
            }
            return render(request,'beltApp/dashboard.html', context)


def login(request):
    print('in login method')

    if request.method == "POST":        
        print(f'in login method - POST {request.POST}')
        errors = User.objects.login_validator(request.POST)
        
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, key)
            return redirect('/')
        else:
            email = request.POST['loginemail']

            user = User.objects.get(email = email)
            print(user.id, user.first_name, user.last_name, user.email, user.password)
            request.session['id'] = user.id            
            messages.success(request, "User Login was successfull!")
            # orderedthots = Thought.objects.annotate(num_like=Count('like')).order_by('-num_like')
            print('User login was successfull!')
            uJobs = user.jobs.all()
            print(uJobs)
            context = {
                "usr": user,
                "uJobs": uJobs,
                "allJobs": Job.objects.all()
            }
            return render(request,'beltApp/dashboard.html', context)            
    else:
        return redirect('/')


def logout(request):
    print('In Logout method')

    if 'id' not in request.session:
        return redirect('/')

    if 'id' in request.session:
        print(request.session['id'])
        del request.session['id']

    if 'id' not in request.session:
        print("session-id has been deleted")

    return redirect('/')


def dashboard(request):
    print('in Dashboard method')
    
    user = User.objects.get(id=request.session['id'])
    uJobs = user.jobs.all()
    print(uJobs)
    context = {
        "usr": user,
        "uJobs": uJobs,
        "allJobs": Job.objects.all()
    }
    return render(request,'beltApp/dashboard.html', context)


def newJob(request):
    print('in newJob method')    
    user = User.objects.get(id=request.session['id'])

    context = {
            "usr": user,
    }
    return render(request,'beltApp/new.html', context)


def createJob(request):
    print('in createJob method')

    if request.method == "POST":
        errors1 = Job.objects.job_validator(request.POST)
        errors2 = Category.objects.category_validator(request.POST)
        print(f"ERRORS1 = {errors1}")
        print(f"ERRORS2 = {errors2}")
        if len(errors1) > 0:
            for key, value in errors1.items():
                messages.error1(request, value, key)
            return redirect('/newJob')
        elif len(errors2) > 0:
            for key, value in errors2.items():
                messages.error2(request, value, key)
            return redirect('/newJob')
        else:
            title = request.POST['title']
            description = request.POST['desc']
            location = request.POST['location']
            category = request.POST['category']
            other = request.POST['other']
            user = User.objects.get(id=request.session['id'])

            job = Job.objects.create(title = title, description = description, location = location, creator = user)  
            print(job.id, job.title, job.description, job.location, job.creator.id)
            cat1 = Category.objects.create(title=category)
            job.categories.add(cat1)
            if other:
                cat2 = Category.objects.create(title=other)
                job.categories.add(cat2)
            print(job)
            messages.success(request, "Job Creation successfully completed!")
            uJobs = user.jobs.all()
            print("Job Creation successfully completed!")

            context = {
                    "usr": user,
                    "uJobs": uJobs,
                    "allJobs": Job.objects.all()
            }
            return render(request,'beltApp/dashboard.html', context)


def removeJob(request, job_id):
    print('in removeJob method')
    print(f"JobId: {job_id}")
    user = User.objects.get(id=request.session['id'])
    jobToRemove = Job.objects.get(id=job_id)
    jobToRemove.delete()
    print(f"Logged in user: {user.first_name} {user.last_name} removed the job {job_id}")
    return redirect('/dashboard')

def jobDetail(request, job_id):
    print('in jobDetail method')
    print(f"Job Id: {job_id}")
    jv = Job.objects.get(id=job_id)
    print(jv.id, jv.title, jv.description, jv.location, jv.creator.id)
    user = User.objects.get(id=request.session['id'])
    uJobs = user.jobs.all()
    context = {
        "usr": user,
        "uJobs": uJobs,
        "j": jv,   
    }
    return render(request, 'beltApp/jobdetail.html', context)
    # return HttpResponse("this job to view")

def editJob(request, job_id):
    print('in editJob method')
    print(f"JobId: {job_id}")
    user = User.objects.get(id=request.session['id'])
    jed = Job.objects.get(id=job_id)
    print(jed.id, jed.title, jed.description, jed.location, jed.creator.id)
    # jobToRemove.delete()
    print(f"Launching web interface, so that logged in user: {user.first_name} {user.last_name} can edit the job {job_id}")
    context = {
        "usr": user,
        "j": jed,   
    }
    return render(request, 'beltApp/edit.html', context)


def submitEditJob(request, job_id):
    print('in submitEditJob method')
    print(f"JobId: {job_id}")
    jed = Job.objects.get(id=job_id)
    print(jed.id, jed.title, jed.description, jed.location, jed.creator.id)

    if request.method == "POST":
        print(f"In IF")
        errors = Job.objects.job_validator(request.POST)
        print(f"ERRORS = {errors}")
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, key)
            return redirect(f"/editJob/{job_id}")

        else:
            title = request.POST['title']
            description = request.POST['desc']
            location = request.POST['location']
            user = User.objects.get(id=request.session['id'])

            jed.title = title
            jed.description = description
            jed.location = location
            jed.save()
            messages.success(request, "Job Update successfully completed!")
            print("Job Update successfully completed!")
            return redirect('/dashboard')

def addJob(request, job_id):
    print('in addJob method')
    print(f"JobId: {job_id}")
    user = User.objects.get(id=request.session['id'])
    jed = Job.objects.get(id=job_id)
    print(jed.id, jed.title, jed.description, jed.location, jed.creator.id)
    user.jobs.add(jed)
    print(f"Job {jed.id} ADDED to the cart of user {user.first_name} {user.last_name}")
    return redirect('/dashboard')

def dropJob(request, job_id):
    print('in dropJob method')
    print(f"JobId: {job_id}")
    user = User.objects.get(id=request.session['id'])
    jed = Job.objects.get(id=job_id)
    print(jed.id, jed.title, jed.description, jed.location, jed.creator.id)
    user.jobs.remove(jed)
    print(f"Job {jed.id} REMOVED from the cart of user {user.first_name} {user.last_name}")
    return redirect('/dashboard')
