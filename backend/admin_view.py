from datetime import datetime
import json
from backend.models import bookmarked_files, file_likes, file_upload, reported_file, user_details, searched_file,viewed_notes
from django.db.models import Q
from .views import error_404_view, uploadCountUpdate
from django.shortcuts import redirect, render
from .helper_functions import mergeDict
import asyncio
from asgiref.sync import sync_to_async

def Context(request):
    user_id = request.session.get("user_unique_id")
    username = request.session.get("username")

    user_is_admin = False
    name = "User"
    if username != None:
        user_detail = user_details.objects.get(Q(pk = user_id))
        user_is_admin = user_detail.is_admin
        name = user_detail.first_name 
        
    context = {
        'current_user': user_id,
        'username': username,
        'is_admin': user_is_admin,
        'name':name
    }

    return context


# admin pages where he can approve and decline uploaded contents 
@sync_to_async  
def adminfeed(request):
    context = Context(request)
    if context['is_admin'] == True:
        users = user_details.objects.all().exclude(Q(is_active = False) | Q(is_admin = True) | Q(is_banned = True))
        user_count = users.count()
        banned_users = user_details.objects.filter(Q(is_banned = True))
        banned_users_count = banned_users.count()
        uploads = file_upload.objects.all()
        upload_count = uploads.count()
        # For getting total upload and storing in database 
        # -->>
        # for user in users:
        #     getFileDetails = file_upload.objects.filter( Q(user = user.pk) ).count()
        #     print(getFileDetails)
        #     uploadCountUpdate(user.pk, getFileDetails)
        # <<--
        reports = reported_file.objects.all()
        report_count = reports.count()
        bookmarked = bookmarked_files.objects.all()
        bookmarked_count = bookmarked.count()
        likes = file_likes.objects.all()
        likes_count = likes.count()
        user_id = request.session.get("user_unique_id")
        username = request.session.get("username")
        if username != None:
            user_detail = user_details.objects.get(Q(pk = user_id))
            user_is_admin = user_detail.is_admin
            name = user_detail.first_name
        chart_data = json.dumps(chartData())
        # print(type(json.dumps(chart_data)))
            
        context2 = {
            'current_user': user_id,
            'user_count':user_count,
            'banned_users_count':banned_users_count,
            'report_count':report_count,
            'file_count':upload_count,
            'list_of_users':users,
            'list_of_banned_users':banned_users,
            'list_of_reports':reports,
            'list_of_uploads':uploads,
            'username':username,
            'name':name,
            'chart_data':chart_data
        }
        context = mergeDict(Context(request),context2)

        return render(request,'pages/Admin/admin_panel.html',context)
    else:
        return redirect(error_404_view)

def changeRole(request):
    user_id = request.GET['user_id']
    role = request.GET['role']

    print("User: ",user_id)
    print("role: ",role)

    user_data = user_details.objects.get(Q(pk = user_id)) 
    if role == "Admin":

        user_data.is_content_writer = 0
        user_data.is_faculty = 0
        user_data.is_student = 0
        user_data.is_admin = 1

    elif role == "Student":

        user_data.is_student = 1
        user_data.is_content_writer = 0
        user_data.is_faculty = 0
        user_data.is_admin = 0

    elif role == "Faculty":

        user_data.is_faculty = 1
        user_data.is_content_writer = 0
        user_data.is_student = 0
        user_data.is_admin = 0
    
    elif role == "Content Writer":  

        user_data.is_content_writer = 1
        user_data.is_faculty = 0
        user_data.is_student = 0
        user_data.is_admin = 0

    user_data.save()
    return redirect(adminfeed)

def admin_user_reports(request):    
    return render(request,'pages/Admin/user_reports.html',Context(request))

def banUser(request):
    user_to_ban = int(request.GET['user_to_ban'])
    print("backend ban user",user_to_ban)
    get_user = user_details.objects.get(Q(unique_id = user_to_ban))
    get_user.is_banned = True
    get_user.save()
    return redirect(adminfeed)

def unBanUser(request):
    user_to_ban = int(request.GET['user_to_ban'])
    print("backend ban user",user_to_ban)
    get_user = user_details.objects.get(Q(unique_id = user_to_ban))
    get_user.is_banned = False
    get_user.save()
    return redirect(adminfeed)


# def getAllSearches(request):
#     context = Context(request)
#     if context['is_admin'] == True:
#         searchQuery = searched_file.objects.all()
#         context['searched_file_data'] = searchQuery
#         return render(request,'pages/Admin/getAllSearches.html',context)
#     else:
#         return redirect(error_404_view)



@sync_to_async
def getAllClickedFiles(request):
    context = Context(request)
    if context['is_admin'] == True:
        searchQuery = viewed_notes.objects.all()
        context['clicked_file_data'] = searchQuery
        return render(request,'pages/Admin/getAllClickedFiles.html',context)
    return render(request,'pages/Admin/getAllClickedFiles.html',context)
    # else:
    #     return redirect(error_404_view)


user_Joined_data_for_chart = {}

def chartData():
    users = user_details.objects.all().exclude(Q(is_active = False) and Q(is_admin = True) and Q(is_banned = True)).order_by('-timestamp')

    count_year = 0
    count_month = 0

    secondary_year = datetime.now().date().year
    secondary_month = datetime.now().date().month
    month_data_dict = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0}

    for user in users:
        user_joining_date = user.timestamp.date()
        primary_year = user_joining_date.year
        primary_month = user_joining_date.month
        # print(user.unique_id,user.timestamp)
        # print(user.timestamp.date().day, " " ,user.timestamp.date().month , user.timestamp.date())

        if primary_year == secondary_year:
            if count_year == 0:
                user_Joined_data_for_chart[primary_year] = {'count':0}
            count_year += 1
            if primary_month == secondary_month:
                count_month +=1
                month_data_dict[primary_month] = count_month
            else:
                secondary_month = primary_month
                count_month = 1
                month_data_dict[primary_month] = count_month
            addDataToUserJoinedDataForChart(primary_year,month_data_dict,count_year)
        else:
            count_year = 1
            count_month = 0
            month_data_dict = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0}
            if primary_month == secondary_month:
                count_month +=1
                month_data_dict[primary_month] = count_month
            else:
                secondary_month = primary_month
                count_month = 1
                month_data_dict[primary_month] = count_month
            addDataToUserJoinedDataForChart(primary_year,month_data_dict,count_year)
    return user_Joined_data_for_chart

def addDataToUserJoinedDataForChart(year,month_data_dict , count_year):
    user_Joined_data_for_chart[year] = {'month':month_data_dict,'count':count_year}

