from django.http import HttpResponse
from django.shortcuts import redirect, render
from  django.contrib import messages
from backend.models import bookmarked_files, file_likes, file_upload, reported_file, searched_file, user_details,contact_us ,viewed_notes
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
import random
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail

def Context(request):
    user_id = request.session.get("user_unique_id")
    username = request.session.get("username")
    user_is_admin = False
    name = "user"
    print(user_id)
    if username != None:
        user_detail = user_details.objects.get(Q(pk=user_id))
        print(user_detail)
        user_is_admin = user_detail.is_admin
        name = user_detail.first_name + " " + user_detail.last_name

        context = {
            'current_user': user_id,
            'username': username,
            'is_admin': user_is_admin,
            'name': name
        }
        return context 
    else:
        context = {
            'current_user':None
        }
        return context

def home(request):
    # mailToNonActiveUsers() # Only use when wants to send mail to users who haven't verified their email id
    return render(request, 'pages/home/index.html', Context(request))


def profile(request):
    context = Context(request)
    user_id = request.session.get("user_unique_id")
    username = request.session.get("username")
    if username != None:
        user_detail = user_details.objects.get(Q(pk=user_id))
        total_likes = file_likes.objects.filter(Q(user_id=user_id)).count()
        uploaded_files = file_upload.objects.filter(Q(user_id=user_id))
        total_uploads = uploaded_files.count()
        bookmarked_file = bookmarked_files.objects.filter(Q(user_id=user_id))
        total_bookmarked_file = bookmarked_file.count()
        print(uploaded_files.count())
        user_is_admin = user_detail.is_admin
        context['uploaded_files'] = uploaded_files 
        context['total_likes'] = total_likes
        context['total_uploads'] = total_uploads
        context['total_bookmarked'] = total_bookmarked_file
        context['uploaded_files'] = uploaded_files
        context['bookmarked_file'] = bookmarked_file
        context['user_bio'] = user_detail.user_bio
        return render(request, 'pages/profile/user_profile.html', context)
    else:
        return redirect(error_404_view)

def uploadCountUpdate(user_id, upload_count):
    user_detail = user_details.objects.get(Q(pk = user_id))
    user_detail.total_uploads = int(upload_count)
    print(upload_count)
    user_detail.save()

def faq(request):
    context = Context(request)
    return render(request, 'pages/other/FAQ/faq.html', context)


def loginpage(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        try:
            validate_userid = user_details.objects.get((Q(username__iexact =username)|Q(mail__iexact  = username)), Q(password=password))
            user_unique_id = validate_userid.unique_id
            user_is_active = validate_userid.is_active
            user_is_banned = validate_userid.is_banned
            if user_is_banned == False:
                if user_is_active:
                    request.session['user_unique_id'] = user_unique_id
                    request.session['username'] = username
                    context = {
                        'username': username,
                        'user_unique_id': user_unique_id
                    }
                    return redirect("/", args=context)
                else:
                    try:
                        request.session['new_user'] = username
                        request.session['new_user_id'] = validate_userid.unique_id
                        print(request.session.get('new_user_id'))
                        mailer(request,"Verify your account", "send otp",[validate_userid.mail])
                        return redirect("/otp_page")
                    except Exception as e:
                        print(e)
            else:
                messages.error(request, "Your account has been banned, if you think this is mistake please contact us!")
        except:
            messages.error(request, "Invalid credentials")
    return render(request, 'pages/login_page/login_page.html')

def forgetPassword(request):
    user_credentials = request.GET['user_credentials']  
    print(user_credentials)
    try:
        getUserCred = user_details.objects.get(Q(username__iexact = user_credentials) or Q(mail__iexact = user_credentials))
        user_mail = getUserCred.mail
        user_name = getUserCred.first_name 
        password = getUserCred.password
        # messages.success(request,"Please check your mail")
        print("sending mail")
        html_content = render_to_string("pages/other/mail_template/email_con.html", {'name': user_name, 'password': password})
        text_content = strip_tags(html_content)
        send_mail(
            "FindMyNotes Password requested",
            text_content,
            'FindMyNotes',
            [user_mail],
            fail_silently=False,
        )
        return HttpResponse("Please check your mail")
    except Exception as err:
        print("user not found:",err)
        # messages.error(request,"Please enter valid username or email")
        return HttpResponse("Please enter valid username or email")
    return redirect(loginpage)

def mailer(request,subject,content,mail_to):
    if content == 'send otp':
        random_num = random.randint(1000, 9999)
        request.session['new_otp'] = random_num
        content = str(random_num)
        send_mail(
            subject,
            content,
            'FindMyNotes',
            mail_to,
            fail_silently=False,
        )
        return random_num
    else:

        return mail_to

# def mailToNonActiveUsers():
#     mailTo = user_details.objects.filter(is_active = 0)
#     count = 0
#     for mails in mailTo: 
#         # print(mails.first_name)
#         print(mails.mail)
#         # try:
#         #     htmly = get_template('./non_active_mail.html')
#         #     contexts = {'name': mails.first_name}
#         #     subject, from_email, to = 'Only One step left...','findmynotes2022@gmail.com' ,mails.mail   
#         #     text_content = "Your details has been registered successfully. Please complete your registration by verfying your email."
#         #     html_content = htmly.render(contexts)
#         #     msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
#         #     msg.attach_alternative(html_content, "text/html")
#         #     msg.send()
#         #     count += 1
#         # except Exception as err:
#         #     print("Error sending mail to", mails.mail,"Error:",err)
#     print(count,"mails sent")



def about(request):
    return render(request, 'pages/other/about/aboutus.html', Context(request))


def team(request):
    return render(request, "pages/other/about/team.html",Context(request))

def contact(request):
    user_id = request.session.get("user_unique_id")
    return render(request, 'pages/other/contact/contact.html', Context(request))


# login & signup backend
def signuppage(request):

    if request.method == "POST":
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        gender = request.POST['gender']
        dob = request.POST['dob']
        mail = request.POST['mail']
        phone = request.POST['phone']
        username = request.POST['username']
        password = request.POST['password']
        print(username)

        exists_username = user_details.objects.filter(
            username=username).count()
        exists_email = user_details.objects.filter(mail=mail).count()

        if exists_username > 0:
            print("username error")
            messages.error(request, "Username Exist")

        elif exists_email > 0:
            print("email error")
            messages.error(request, "Email Exist")
        else:
            users = user_details.objects.create(
                first_name=first_name,
                last_name=last_name,
                gender=gender,
                dob=dob,
                mail=mail,
                phone=phone,
                username=username,
                password=password,
                total_uploads = 0,
            )
            users.save()
            print("User Created")
            # We will load the html content first
            random_num = random.randint(1000, 9999)

            html_content = render_to_string(
                "pages/other/mail_template/emailtemplate.html", {'name': first_name, 'otp': random_num})

            # html content jo load karenge usme se HTML tags nikal denge
            text_content = strip_tags(html_content)
            mail = EmailMultiAlternatives(  # Initialize a single email message (which can be sent to multiple recipients).
                # subject
                "Please Verify Your Account",
                # content
                text_content,
                # from email
                'findmynotes2002@gmail.com',
                # receipient list
                [mail]
            )

            # attach the html content
            mail.attach_alternative(html_content, "text/html")
            mail.send()
            request.session["new_user"] = username
            request.session["new_user_id"] = users.unique_id
            request.session["new_otp"] = random_num
            return redirect(otp_page)

    return render(request, 'pages/reg_page/reg_page.html')


def otp_page(request):
    if request.method == "POST":
        input_otp = request.POST['otp_input']
        if input_otp == str(request.session.get('new_otp')):
            set_active = user_details.objects.get(username=request.session.get("new_user"))
            set_active.is_active = True
            set_active.save()
            request.session['username'] = request.session.get("new_user")
            request.session['user_unique_id'] = request.session.get("new_user_id")
            print(request.session.get('username'))
            return redirect(home)
        else:
            messages.error(request, "Invalid OTP")
    return render(request, "pages/other/otp/otp_page.html")


def searchPage(request):
    user_id = request.session.get("user_unique_id")
    username = request.session.get("username")
    context= Context(request)
    #Get query from url
    category = str(request.GET.get('category'))
    query = str(request.GET.get('search_query'))
    print("searched Query:",query)
    name = ''
    resources = ""
    if username != None:
        user_detail = user_details.objects.get(Q(pk=user_id))
        user_is_admin = user_detail.is_admin
        name = user_detail.first_name
        context = Context(request)
        if category != '' and query != 'None':
            search_query = query
            # print(search_query)
            resources = file_upload.objects.filter((Q(description__icontains = search_query) | Q(file_title__icontains =search_query) | Q(file_name__icontains =search_query) | Q(tags__icontains =search_query)), (Q(is_verified = True)))
            context['resultFor'] = "Search Result for: "+query
            # creating list of liked files in search result bu user
        else:
            context['resultFor'] = "Recomended"
            searched_file_query = searched_file.objects.filter(Q(user_id=user_id))[0:3]
            searched_file_name = []
            for file in searched_file_query:
                searched_file_name.append(file.query)
                # print(searched_file_name)
                resources = file_upload.objects.filter((Q(description__icontains= searched_file_name) | Q(file_title__icontains =searched_file_name) | Q(file_name__icontains =searched_file_name) | Q(tags__icontains =searched_file_name)), (Q(is_verified = True)))
        print(resources)
        liked_resources = file_likes.objects.filter(Q(user=user_id), Q(file__in=resources))
        liked_by_user = []
        for dataset in liked_resources:
            if dataset.pk not in liked_by_user:
                liked_by_user.append(dataset.file.pk)

        bookmarked_resources = bookmarked_files.objects.filter(
            Q(user=user_id), Q(file__in=resources))

        # creating list of bookmarked files in search result bu user
        bookmarked_by_user = []
        for dataset in bookmarked_resources:
            if dataset.pk not in bookmarked_by_user:
                bookmarked_by_user.append(dataset.file.pk)

        context['all_resources'] = resources
        context['liked_by_user'] = liked_by_user
        context['bookmarked_by_user'] = bookmarked_by_user
    else:
        return redirect(loginpage)
    return render(request, "pages/search/search_page.html", context)


def search_store(request):
    context = Context(request)
    try:
        search_file_query = searched_file.objects.create(
            user_id=user_details.objects.get(unique_id=context['current_user']),
            query=request.GET['searched_query']
        )
        search_file_query.save()
        print("Search file stores")
        return HttpResponse(request,"1")
    except:
        print("Error storing search ")
        return HttpResponse(request,"0")

def searchClickInsert(request):
    user_id = request.session.get("user_unique_id")
    file_id = request.GET.get("file_id",None)
    print(file_id)
    try:
        storeClickedFileDetails = viewed_notes.objects.create(
            user_clicked=user_details.objects.get(unique_id=user_id),
            file=file_upload.objects.get(pk=file_id)
        )
        storeClickedFileDetails.save()
        return HttpResponse('Success')
    except Exception as er:
        print(er)
        return HttpResponse("Error: "+str(er))

def file_like(request):
    user_id = request.session.get("user_unique_id")
    if request.method == "POST":
        try:
            print(request.GET.get('file_id', None))
            file_id = request.GET.get('file_id', None)
            # print("File_id: ",file_id)
            create_file_like_object = file_likes.objects.create(
                user=user_details.objects.get(unique_id=user_id),
                file=file_upload.objects.get(pk=file_id)
            )
            create_file_like_object.save()

            like_count = count_likes(file_id)

            # print("count: ",count_likes(file_id))

            return HttpResponse('Success,'+str(like_count))

        except Exception as er:
            return HttpResponse("Error: "+str(er))


def file_unlike(request):
    user_id = request.session.get("user_unique_id")
    if request.method == "POST":
        try:
            file_id = request.GET.get('file_id', None)

            get_file_like_object = file_likes.objects.get(
                Q(file=file_id), Q(user=user_id))
            get_file_like_object.delete()

            like_count = count_likes(file_id)

            return HttpResponse('Success,'+str(like_count))

        except Exception as er:
            return HttpResponse("Error: "+str(er))


def count_likes(file_id):
    get_like_db_count = file_likes.objects.filter(Q(file=file_id)).count()
    file_db_update = file_upload.objects.get(pk=file_id)
    file_db_update.likes = int(get_like_db_count)
    file_db_update.save()
    return get_like_db_count


def add_bookmark(request):

    user_id = request.session.get("user_unique_id")
    if request.method == "POST":
        try:
            print(request.GET.get('file_id', None))
            file_id = request.GET.get('file_id', None)
            # print("File_id: ",file_id)
            create_bookmark_file_object = bookmarked_files.objects.create(
                user=user_details.objects.get(unique_id=user_id),
                file=file_upload.objects.get(pk=file_id)
            )
            create_bookmark_file_object.save()

            # print("count: ",count_likes(file_id))

            return HttpResponse("Success")
        except Exception as er:
            return HttpResponse("Error: "+str(er))


def remove_bookmark(request):
    user_id = request.session.get("user_unique_id")
    if request.method == "POST":
        try:
            file_id = request.GET.get('file_id', None)

            bookmark_file_object = bookmarked_files.objects.get(
                Q(file=file_id), Q(user=user_id))
            bookmark_file_object.delete()

            return HttpResponse("Success")
        except Exception as er:
            return HttpResponse("Error: "+str(er))


def report_submit(request):
    if request.method == "POST":
        try:

            file_id = request.GET.get('file_id', None)
            user_reported_issue = request.GET.get('user_reported_issue', None)
            user_posted = request.GET.get('user_posted', None)
            report_topic = request.GET.get('report_topic', None)
            reason_to_report = request.GET.get('reason_to_report', None)

            file_id = file_upload.objects.get(Q(pk=file_id))
            user_reported_issue = user_details.objects.get(
                Q(pk=user_reported_issue))
            user_posted = user_details.objects.get(Q(pk=user_posted))

            print("->", file_id, user_reported_issue, user_posted)

            report_file_objects = reported_file.objects.create(
                file=file_id,
                user_reported_issue=user_reported_issue,
                user_posted=user_posted,
                reason=report_topic,
                reason_message=reason_to_report,
            )
            report_file_objects.save()
            return HttpResponse("Success")

        except Exception as er:
            print("Error: "+str(er))
            return HttpResponse("Error: "+str(er))


def upload_page(request):
    user_id = request.session.get("user_unique_id")
    username = request.session.get("username")
    context = Context(request)
    if username != None:
        user_detail = user_details.objects.get(Q(pk=user_id))
        user_is_admin = user_detail.is_admin
        user_is_faculty = user_detail.is_faculty
        print(user_is_faculty)
        name = user_detail.first_name
        context['uploaded'] = "Upload"
        if request.method == "POST":
            try:
                file = request.FILES['file_data']
                # if file_type == "pdf":
                file_type = request.POST['file_type']
                file_description = request.POST['description']
                print(file_description)
                file_title = request.POST['title']
                tags = request.POST['tags']
                fs = FileSystemStorage(location='files/'+str(request.session['user_unique_id'])+"/"+file_type+"/")
                file_details = file_upload.objects.create(
                    file_type=file_type,
                    file_name=file.name,
                    description=file_description,
                    file_title=file_title,
                    tags=tags,
                    file_url=str(request.session['user_unique_id'])+"/"+file_type+"/"+file.name,user=user_details.objects.get(unique_id=request.session.get("user_unique_id")),
                    likes=0,
                    is_verified = user_is_faculty
                )
                success_message = "Notes Uploaded"
                if user_is_faculty:
                    success_message = "Your notes are uploaded and available to everyone"
                else:
                    success_message = "Your notes will get public after verification by our team"

                file_details.save()
                
                fs.save(file.name, file)

                messages.success(request, success_message)

                user_detail.total_uploads += 1 
                user_detail.save()
                context['uploaded'] = "Upload another"
            except Exception as err:
                print("error uploading file:", err)
                messages.success(request, "Error uploading file")
    else:
        return redirect(loginpage)
    return render(request, "pages/upload/old_upload.html", context)

#Terms and condition page to upload note
def uploadTC(request):
    return render(request, "pages/upload/terms_and_condition.html", Context(request))


def error_404_view(request, exception):
    return render(request,"pages/other/notfound/notfound.html")


def logout(request):
    request.session.flush()
    return redirect(loginpage)
