from multiprocessing import context
from unittest import result
from urllib import request
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from flask import session
from .models import *
from django.contrib.sessions.models import Session
from django.template import loader
from django.urls import reverse
from .forms import AccountForm, SearchForm


""" Scrap imports """
import requests
import pandas as pd
from bs4 import BeautifulSoup  
import json



def index(request):
    json_data = open("JobScraper/templates/JobScraper/cities.json",encoding="utf8")   
    data1 = json.load(json_data)
    json_data.close()
    context={
        'cities':data1
    }
    return render(request,'JobScraper/index.html',context)

import random
    

def scrapByTerm(request):
    myForm = SearchForm(request.POST)
    print(myForm)
    if myForm.is_valid():   
        term = myForm.cleaned_data['term']
        page = myForm.cleaned_data['page']
        print(page)
        print(term)
        formLocation = myForm.cleaned_data['location']
        jobType = myForm.cleaned_data['jobType']
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}

        if formLocation=='noLocation':
            JobfindUrl = "https://www.jobfind.gr/JobAds/all/all/GR/Theseis_Ergasias?cnt=1&st="+term+"&pageid="+page+"&jt="+jobType
            if jobType==0:
                IndeedUrl = "https://gr.indeed.com/jobs?q="+term+"&start="+page
            else:
                IndeedUrl = "https://gr.indeed.com/jobs?q="+term+"&sc=0kf%3Ajt(fulltime)%3B"+"&start="+page
            JoobleUrl = "https://gr.jooble.org/SearchResult?jt="+jobType+"&ukw="+term
        else:            
            JobfindUrl = "https://www.jobfind.gr/JobAds/all/"+formLocation+"/GR/Theseis_Ergasias?st="+term+"&pageid="+page+"&jt="+jobType
            if jobType==0:
                IndeedUrl = "https://gr.indeed.com/jobs?q="+term+"&l="+formLocation+"&start="+page
            else:
                IndeedUrl = "https://gr.indeed.com/jobs?q="+term+"&l="+formLocation+"&sc=0kf%3Ajt(fulltime)%3B"+"&start="+page
            JoobleUrl = "https://gr.jooble.org/SearchResult?jt="+jobType+"&rgns="+formLocation+"&ukw="+term

        JobfindRequest = requests.get(JobfindUrl, headers=headers)
        JobfindSoup = BeautifulSoup(JobfindRequest.content, "html.parser")

        IndeedRequst = requests.get(IndeedUrl, headers=headers)
        IndeedSoup = BeautifulSoup(IndeedRequst.content, "html.parser")

        rows = JobfindSoup.find_all("div",class_="jobitem")
        rows += IndeedSoup.find_all("div", class_="job_seen_beacon")

        results = {     
        }
        
        if page == '1':
            JoobleRequest = requests.get(JoobleUrl, headers=headers)
            JoobleSoup = BeautifulSoup(JoobleRequest.content, "html.parser")
            rows += JoobleSoup.find_all("article", class_="FxQpvm yKsady")
        else:
            if formLocation=='noLocation':
                JoobleUrl = "https://gr.jooble.org/SearchResult?p="+page+"&ukw="+term
            else:
                JoobleUrl = "https://gr.jooble.org/SearchResult?p="+page+"rgns="+formLocation+"&ukw="+term

            JoobleRequest = requests.get(JoobleUrl, headers=headers)
            JoobleSoup = BeautifulSoup(JoobleRequest.content, "html.parser")
            tracker=(int(page)*20)-20
            obj=[]
            for i in range(0,20) :
                obj += JoobleSoup.select_one('article:nth-child('+str(tracker)+')')
                tracker = int(tracker)+1
                results[i]={'id':i,'title':JoobleSoup.select_one('article:nth-child('+str(tracker)+')').find("span",class_="_3862j6").text,'location':JoobleSoup.select_one('article:nth-child('+str(tracker)+')').find("div",class_="caption _2_Ab4T").text, 'source': "Jooble", 'link':JoobleSoup.select_one('article:nth-child('+str(tracker)+')').find("a",class_="_3qfVeS _3fnsFH _2dWEc6")['datahref'],"term":term,'page':int(page)+1, 'details':JoobleSoup.select_one('article:nth-child('+str(tracker)+')').find("div",class_="_9jGwm1").text}
        if page == '1':
            i=0
        else:
            i=tracker 

            
        for job in rows:
            findSource =  job.find("h3",class_="title")
            if findSource is None:
                findSource = job.find("span",class_="_3862j6")
                if findSource is None:
                    findSource = job.find("a",class_="jcs-JobTitle")
                    if findSource is None:
                        break
                    else:
                        source = 'Indeed'
                else:
                    source = 'Jooble'
            else:
                source = 'Jobfind'
                
            if source == 'Jobfind':
                title = job.find("h3",class_="title")
                location =  job.find("div",class_="city")
                link = job.find("a")
                JobfindDetailsUrl = "https://www.jobfind.gr"+link['href']
                JobfindDetailsRequest = requests.get(JobfindDetailsUrl, headers=headers)
                JobfindDetailsSoup = BeautifulSoup(JobfindDetailsRequest.content, "html.parser")
                details = JobfindDetailsSoup.find("div",class_='adtext')
                if title is None:
                    title="no title"
                if location is None:
                    location="no location"
                if link is None:
                    link="no link"
                if details is None:
                    details="no details"
                results[i]={'id':i,'title':title.text, 'location':location.text, 'source': source, 'link': "https://www.jobfind.gr"+link['href'],"term":term,'page':int(page)+1, 'details':details.text}
                    
            else: 
                if source == 'Jooble' and page == '1':
                    title = job.find("span",class_="_3862j6")
                    location = job.find("div",class_="caption _2_Ab4T") 
                    link = job.find("a",class_="_3qfVeS _3fnsFH _2dWEc6")
                    details = job.find("div",class_="_9jGwm1")
                    if title is None:
                        title="no title"
                    if location is None:
                        location="no location"
                    if link is None:
                        link="no link"
                    if details is None:
                        details="no details"
                    results[i]={'id':i,'title':title.text,'location':location.text, 'source': source, 'link':link['datahref'],"term":term,'page':int(page)+1, 'details':details.text}
                else:
                    title = job.find("a",class_="jcs-JobTitle")
                    location = job.find("div",class_="companyLocation")
                    link = job.find("a")
                    details = job.find("div",class_="job-snippet")
                    if title is None:
                        title="no title"
                    if location is None:
                        location="no location"
                    if link is None:
                        link="no link"
                    if details is None:
                        details="no details"
                    results[i]={'id':i,'title':title.text,'location':location.text, 'source': source, 'link': "https://gr.indeed.com"+link['href'],"term":term,'page':int(page)+1, 'details':details.text}
            i+=1
        user=request.user
        lists={}
        if user.is_authenticated:
            lists=Lists.objects.filter(user__exact=user)
            
        customLists={}
        i=0
        for list in lists:
            customLists[i]={'listName':list.listName}
            i+=1

        context={
            'results':results,
            'lists':customLists,
            'jobType':jobType,
            'location':formLocation
        }
        return render(request,'JobScraper/results.html',context)
    else:
        return HttpResponse('Sas')


 #Lists
def saveListing(request):
    if request.method == 'POST':
        title=request.POST.get('title')
        location=request.POST.get('location')
        source=request.POST.get('source')
        link=request.POST.get('link')
        details=request.POST.get('details')
        user = request.user
        new = JobListing(title=title,location=location,source=source,link=link,details=details)
        new.save()
        saved = Saved(JobListing=new,user=user)
        saved.save()
    return render(request,"JobScraper/results.html")


#adds listing to custom list
def saveCustomListing(request):
    if request.method == 'POST':
        title=request.POST.get('title')
        location=request.POST.get('location')
        source=request.POST.get('source')
        link=request.POST.get('link')
        details=request.POST.get('details')
        listName=request.POST.get('listName')
        print(listName)
        user = request.user
        new = JobListing(title=title,location=location,source=source,link=link,details=details)
        new.save()
        customList=Lists.objects.get(listName__exact=listName)
        saved = CustomListings(JobListing=new,user=user,listName=customList)
        saved.save()
    return render(request,"JobScraper/results.html")

def addToHistory(request):
    if request.method == 'POST':
        title=request.POST.get('title')
        location=request.POST.get('location')
        source=request.POST.get('source')
        link=request.POST.get('link')
        details=request.POST.get('details')
        user = request.user
        new = JobListing(title=title,location=location,source=source,link=link,details=details)
        new.save()
        saved = History(JobListing=new,user=user)
        saved.save()
    return render(request,"JobScraper/results.html")

def savedListings(request):
    user = request.user
    listings= Saved.objects.filter(user__exact=user).values('JobListing_id')
    i=0
    results={}
    for listing in listings:
        saved_listing = JobListing.objects.get(id__exact=listing["JobListing_id"])
        results[i]={'id':i,'title':saved_listing.title,'location':saved_listing.location,'link':saved_listing.link,'source':saved_listing.source,'details':saved_listing.details}
        i+=1
    user=request.user
    lists={}
    if user.is_authenticated:
        lists=Lists.objects.filter(user__exact=user)
            
    customLists={}
    i=0
    for list in lists:
        customLists[i]={'listName':list.listName}
        i+=1

    context={
        'results':results,
        'lists':customLists
    }
    return render(request,'JobScraper/saved.html',context)

def history(request):
    user = request.user
    listings= History.objects.filter(user__exact=user).values('JobListing_id')
    i=0
    results={}
    for listing in listings:
        saved_listing = JobListing.objects.get(id__exact=listing["JobListing_id"])
        results[i]={'id':i,'title':saved_listing.title,'location':saved_listing.location,'link':saved_listing.link,'source':saved_listing.source,'details':saved_listing.details}
        i+=1
    user=request.user
    lists={}
    if user.is_authenticated:
        lists=Lists.objects.filter(user__exact=user)
            
    customLists={}
    i=0
    for list in lists:
        customLists[i]={'listName':list.listName}
        i+=1

    context={
        'results':results,
        'lists':customLists
    }
    return render(request,'JobScraper/history.html',context)  

#Loads a custom list and its listings
def customList(request,listName):
    user = request.user
    customList=Lists.objects.get(listName__exact=listName)
    listings= CustomListings.objects.filter(user__exact=user, listName__exact=customList).values('JobListing_id')
    i=0
    results={}
    for listing in listings:
        saved_listing = JobListing.objects.get(id__exact=listing["JobListing_id"])
        results[i]={'id':i,'title':saved_listing.title,'location':saved_listing.location,'link':saved_listing.link,'source':saved_listing.source,'details':saved_listing.details}
        i+=1
    user=request.user
    lists={}
    if user.is_authenticated:
        lists=Lists.objects.filter(user__exact=user)
            
    customLists={}
    i=0
    for list in lists:
        customLists[i]={'listName':list.listName}
        i+=1

    context={
        'results':results,
        'lists':customLists,
        'listName':listName
    }
    return render(request,'JobScraper/customList.html',context)

#Loads lists and template
def lists(request):
    user=request.user
    lists=Lists.objects.filter(user__exact=user)
    results={}
    i=0
    for list in lists:
        results[i]={'listName':list.listName}
        i+=1
    context={
    'results':results
    }
    return render(request,'JobScraper/lists.html',context)

#Creates Custom List
def createList(request):
    if request.method == 'POST':
        listName=request.POST.get('listName')
        user = request.user
        new = Lists(listName=listName,user=user)
        new.save()
    return render(request,"JobScraper/lists.html")

from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm


#Account
def loginPage(request):
    return render(request,'JobScraper/login.html')

def create_account(request):  
    if request.method == 'POST':
        myForm = AccountForm(request.POST)
        if myForm.is_valid():
            user = User.objects.create_user(myForm.cleaned_data['username'],myForm.cleaned_data['password'],myForm.cleaned_data['firstName'],myForm.cleaned_data['lastName'],myForm.cleaned_data['email'],)
            return HttpResponseRedirect('')
    else:
        return render(request,'JobScraper/create_account.html')

def authentication(request):
    if request.method == 'POST':
        myForm = LoginForm(request.POST)
        if myForm.is_valid():
            username = myForm.cleaned_data['username']
            password = myForm.cleaned_data['password']
            user = User.objects.get(username=username)
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return render(request,'JobScraper/index.html')
            else:
                return HttpResponse("Your username and password didn't match.")
    else:
        return render(request, 'JobScraper/login.html')  

def logoutPage(request):
    logout(request)
    json_data = open("JobScraper/templates/JobScraper/cities.json",encoding="utf8")   
    data1 = json.load(json_data)
    json_data.close()
    context={
        'cities':data1
    }
    return render(request,'JobScraper/index.html',context)
    