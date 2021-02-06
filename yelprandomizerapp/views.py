from django.shortcuts import render, redirect, HttpResponse
from .models import User
from django.contrib import messages
import requests
import json
from django.http import JsonResponse
import random
from django.core.mail import send_mail
from django.conf import settings
import secret

def welcome(request):
    if 'userid' in request.session:
        return redirect ("/search")
    return render(request, "welcome.html")

def createuser(request):
    errors = User.objects.user_validator(request.POST)

    if len(errors) > 0:
        for key,value in errors.items():
            messages.error(request,value,extra_tags="name")
        return redirect('/')
    
    errors = User.objects.email_validator(request.POST)

    if len(errors) > 0:
        for key,value in errors.items():
            messages.error(request,value,extra_tags="email")
        return redirect('/')
    if request.method == "POST":
        new_name = request.POST['name']
        new_email = request.POST['email']
        new_user = User.objects.create(name = new_name, email = new_email)
        print("User created")
        request.session['userid'] = new_user.id
        subject = 'Hey! Thanks for using yelp_but_random!'
        message = f'Thank you for using yelp_but_random, {new_name}!\n\nPlease be sure to recommend yelp_but_random to others if you enjoyed my app!\n\nBest,\n\n\nMichael Lin\n\nCheck me out on GitHub! https://github.com/michaelwlin\nCheck me out on LinkedIn! https://www.linkedin.com/in/michaelwlin/ '
        from_email = settings.EMAIL_HOST_USER
        to_list = [new_user.email]
        send_mail(subject,message,from_email,to_list,fail_silently=False) 
        print("Email Sent to",to_list)
        return redirect("/search")

def searchpage(request):
    if 'userid' not in request.session:
        return redirect('/')
    context = {
        "user_now" : User.objects.get(id=request.session['userid']) 
    }
    return render(request,"search.html",context)

def search_randomize(request):
    errors = User.objects.term_validator(request.POST)

    if len(errors) > 0:
        for key,value in errors.items():
            messages.error(request,value,extra_tags="term")
        return redirect('/search')
    errors = User.objects.location_validator(request.POST)

    if len(errors) > 0:
        for key,value in errors.items():
            messages.error(request,value,extra_tags="location")
        return redirect('/search')

    api_key = secret.api_key
    headers = {'Authorization':'Bearer %s' % api_key}

    url = 'https://api.yelp.com/v3/businesses/search'
    request.session['term'] = request.POST['term']
    request.session['location'] = request.POST['location']
    request.session['radius'] = float(request.POST['radius'])*1609.34
    print(request.session['radius'])
    request.session ['price'] = request.POST['price']
    print(request.session['price'])

    params = {'term':request.session['term'],'location':request.session['location'],'price':request.session['price'],'radius':int(request.session['radius'])}

    req = requests.get(url, params = params, headers = headers)
    if req.status_code != 200:
        return redirect('/noresult')
    print("The status code is {}".format(req.status_code))
    parsed = json.loads(req.text)
    businesses = parsed["businesses"]
    if len(businesses) < 1:
        return redirect('/noresult') 
    random_business = random.choice(businesses)
    request.session['one_business'] = random_business
    print(random_business)
    # print(json.loads(req.text))
    # for business in businesses:
    #     print(business)
    #     print("Name:",business['name'])
    #     print("Rating:",business['rating'])
    #     print("Address:", " ".join(business['location']['display_address']))
    #     print("Phone::",business['phone'])
    #     print("\n")
    return redirect("/result")

def randomize_again(request): 
    api_key = secret.api_key
    headers = {'Authorization':'Bearer %s' % api_key} #checks to see who this key belongs to and if its valid,(me)

    url = 'https://api.yelp.com/v3/businesses/search' #now using this url, we are searching for a specific business
    params = {'term':request.session['term'],'location':request.session['location'],'price':request.session['price'],'radius':int(request.session['radius']),'limit':50} #passing in params that I got from the form earlier, it's stored in session

    req = requests.get(url, params = params, headers = headers)
    if req.status_code != 200:
        return redirect('/noresult')
    print("The status code is {}".format(req.status_code))
    parsed = json.loads(req.text)
    businesses = parsed["businesses"]
    if len(businesses) < 1:
        return redirect('/noresult') 
    random_business = random.choice(businesses)
    request.session['one_business'] = random_business
    print(random_business)
    # print(json.loads(req.text))
    # for business in businesses:
    #     print(business)
    #     print("Name:",business['name'])
    #     print("Rating:",business['rating'])
    #     print("Address:", " ".join(business['location']['display_address']))
    #     print("Phone::",business['phone'])
    #     print("\n")
    return redirect("/result")

def result(request):
    if 'one_business' not in request.session:
        return redirect ('/search')
    context = {
        'user_now' : User.objects.get(id=request.session['userid']),
        'final_result' : request.session['one_business'],
        "address" : " ".join(request.session['one_business']['location']['display_address']),
        "distance" : round(request.session['one_business']['distance']*0.000621371,2),
        'categories' : request.session['one_business']['categories'],
    } 
    return render(request,"result.html",context)

def noresult(request):
    return render(request,"noresult.html")

def clear(request):
    request.session.clear()
    return redirect('/')