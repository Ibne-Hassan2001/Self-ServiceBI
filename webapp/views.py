from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, CreateRecordForm, UpdateRecordForm
from django.utils import timezone
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from .task_processing import *
from django.contrib.auth.decorators import login_required

from . models import Record
from django.contrib import messages
import datetime

def home(request):

    return render(request, 'webapp/index.html')

# - Register a user

def register(request):

    form = CreateUserForm()

    if request.method == "POST":

        form = CreateUserForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, "Account created successfully!")

            return redirect("my-login")

    context = {'form':form}

    return render(request, 'webapp/register.html', context=context)



# - Login a user

def my_login(request):

    form = LoginForm()

    if request.method == "POST":

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:

                auth.login(request, user)

                messages.success(request, "You have logged")

                return redirect("dashboard")

    context = {'form':form}

    return render(request, 'webapp/my-login.html', context=context)



@staticmethod
def format_creation_date(creation_date):
        if creation_date:
            year = str(creation_date.year)
            month = str(creation_date.month).zfill(2)
            day = str(creation_date.day).zfill(2)
            hour = str(creation_date.hour).zfill(2)
            minute = str(creation_date.minute).zfill(2)
            return year + month + day + hour + minute
        return None
# - Dashboard

@login_required(login_url='my-login')
def dashboard(request):

    my_records = Record.objects.all()

    # Calculate end time based on status
    # for record in my_records:
    #     if record.status == 'complete':
    #         record.end_time = timezone.now()  # Set end time to current time for completed records
    #     else:
    #         record.end_time = None  # Set end time to None for records in progress

    my_records = Record.objects.filter(user=request.user)
    context = {'records': my_records}

    return render(request, 'webapp/dashboard.html', context=context)




# - Create a record 

# @login_required(login_url='my-login')
# def create_record(request):

#     form = CreateRecordForm()

#     if request.method == "POST":

#         form = CreateRecordForm(request.POST)

#         if form.is_valid():

#             now = datetime.datetime.now()

#             form.save()

            

#             messages.success(request, "Your record was created!")

#             return redirect("dashboard")

#     context = {'form': form}

#     return render(request, 'webapp/create-record.html', context=context)
import time
import threading
from django.template.defaultfilters import date
@login_required(login_url='my-login')
def create_record(request):
    form = CreateRecordForm()

    if request.method == "POST":
        form = CreateRecordForm(request.POST)
        if form.is_valid(): 
            time.sleep(3)
            # Set the user field to the current logged-in user
            record = form.save(commit=False)
            record.user = request.user
            record.save()
            
            task_id = date(record.creation_date, "YmdHis")

             # Start a background thread for updating status and generating CSV file
            thread = threading.Thread(target=update_status_and_generate_csv, args=(record, task_id))
            thread.start()
            
        
            messages.success(request, "Your record was created!")
            return redirect("dashboard")

    context = {'form': form}
    return render(request, 'webapp/create-record.html', context=context)
from django.utils import timezone


# - Update a record 

@login_required(login_url='my-login')
def update_record(request, pk):

    record = Record.objects.get(id=pk)

    form = UpdateRecordForm(instance=record)

    if request.method == 'POST':

        form = UpdateRecordForm(request.POST, instance=record)

        if form.is_valid():

            form.save()

            # messages.success(request, "Your record was updated!")

            return redirect("dashboard")
        
    context = {'form':form}

    return render(request, 'webapp/update-record.html', context=context)


# - Read / View a singular record

@login_required(login_url='my-login')
def singular_record(request, pk):

    all_records = Record.objects.get(id=pk)

    context = {'record':all_records}

    return render(request, 'webapp/view-record.html', context=context)



# - Delete a record

@login_required(login_url='my-login')
def delete_record(request, pk):

    record = Record.objects.get(id=pk)

    record.delete()

    messages.success(request, "Your record was deleted!")

    return redirect("dashboard")








# - User logout

def user_logout(request):

    auth.logout(request)

    messages.success(request, "Logout success!")

    return redirect("my-login")


import csv
import os
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, CreateRecordForm, UpdateRecordForm
from django.utils import timezone
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import Record
from django.contrib import messages
import datetime


def generate_csv(task_id):
    # Define your data to be written to CSV (matching the fieldnames)
    data = [
        {'Name': 'John', 'Age': 30, 'City': 'New York'}
    ]   
    print("Task ID received in generate_csv():", task_id)
    file_name = f"{task_id}.csv"
    file_path = f'D:\\file_generated\\{file_name}'
    # Write data to CSV file
    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['Name', 'Age', 'City']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    print("Generated file name:", file_path)
    return file_path  # Return the file path if needed



def update_status_and_generate_csv(record, task_id):
    # Simulate some processing time
    import time
    time.sleep(10)

    # Change status to 'file generated'
    record.status = 'File Generated'
    record.save()

    # Generate CSV file
    generate_csv(task_id)
    print("hello update_status_and_generate_csv ")
    # Update end time after generating CSV file
    print("tttt",timezone.now())
    record.end_time = timezone.now()
    record.save()

    return redirect("dashboard")
