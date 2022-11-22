# from django.contrib import admin
from django.urls import path
from . import views, admin_view

urlpatterns = [

    # Pages
    path('', views.home,name="home"),
    
    path('searchPage', views.searchPage,name="search_page"),
    path('displayPDF/<int:file_id>', views.displayPDF,name="displayPDF"),
    path('search_store', views.search_store,name="search_store"),

    path('file_like', views.file_like,name="file_like"),
    path('file_unlike', views.file_unlike,name="file_unlike"),
    path('add_bookmark', views.add_bookmark,name="add_bookmark"),
    path('remove_bookmark', views.remove_bookmark,name="remove_bookmark"),
    path('report_submit', views.report_submit,name="report_submit"),

    path('upload_page', views.upload_page,name="upload_page"),
    path('uploadTC', views.uploadTC,name="uploadTC"),

    path('loginpage', views.loginpage , name="loginpage"),
    path('forgetPassword', views.forgetPassword , name="forgetPassword"),
    path('logout', views.logout , name="logout"),

    path('signuppage', views.signuppage , name="signuppage"),
    path('otp_page', views.otp_page , name="otp_page"),

    path('profile', views.profile , name="profile"),
    
    path('contact', views.contact , name="contact"),
    path('about', views.about,name="about"),
    path('team', views.team,name="team"),
    path('faq', views.faq,name="faq"),

    path('adminsite', admin_view.adminfeed , name="adminfeed"),
    # path('getAllSearches', admin_view.getAllSearches , name="getAllSearches"),
    path('getAllClickedFiles', admin_view.getAllClickedFiles , name="getAllClickedFiles"),
    path('getOpenedFiles', admin_view.getOpenedFiles , name="getOpenedFiles"),
    path('changeRole', admin_view.changeRole , name="changeRole"),
    path('banUser', admin_view.banUser , name="banUser"),
    path('unBanUser', admin_view.unBanUser , name="unBanUser"),
    path('adminUserReports', admin_view.admin_user_reports , name="admin_user_reports"),
]
