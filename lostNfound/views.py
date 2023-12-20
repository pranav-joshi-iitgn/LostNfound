from django.shortcuts import render
from django.http import HttpResponse
from .models import Item,Claim,Person
from django.utils import timezone
import datetime
from sklearn.feature_extraction.text import TfidfVectorizer

# Create your views here.

def similarity(d1,d2):
    documents = [d1,d2]
    tfidf = TfidfVectorizer().fit_transform(documents)
    ps = tfidf * tfidf.T
    s = ps[0,1]
    return float(s)

def distance(word1,word2):
    len_1=len(word1)
    len_2=len(word2)
    x =[[0]*(len_2+1) for _ in range(len_1+1)]#the matrix whose last element ->edit distance
    for i in range(0,len_1+1): #initialization of base case values
        x[i][0]=i
    for j in range(0,len_2+1):
        x[0][j]=j
    for i in range (1,len_1+1):
        for j in range(1,len_2+1):
            if word1[i-1]==word2[j-1]:
                x[i][j] = x[i-1][j-1]
            else :
                x[i][j]= min(x[i][j-1],x[i-1][j],x[i-1][j-1])+1
    d = x[i][j]
    d = d - abs(len_1-len_2)
    d = d/min(len_1,len_2)
    return d


def count_similar(k1,k2):
    L1 = k1.split(",")
    L2 = k2.split(",")
    count = 0
    l1 = len(L1)
    l2 = len(L2)
    i = 0
    j = 0
    while i<l1 and j<l2:
        if L1[i] > L2[j]:
            j += 1
        elif L1[i] < L2[j]:
            i += 1
        else:
            count += 1
            i += 1
            j += 1
    return count

def straighten(keywords):
    k = keywords.lower()
    k = k.split(",")
    k = [s.strip() for s in k]
    k = set(k)
    k = list(k)
    k.sort()
    keywords = ",".join(k)
    return keywords

def search(request):
    return HttpResponse(render(request,"lostNfound/search.html",{}))

def index(request):
    return HttpResponse(render(request,"lostNfound/index.html",{}))

def item(request,item_id):
    try:
        i = Item.objects.get(pk=item_id)
        context = {"i":i}
        return HttpResponse(render(request, "lostNfound/item.html",context))
    except:
        return HttpResponse("item number "+str(item_id)+"doesn't exist")

def see_claim(request,item_id,claim_id):
    try:
        i = Item.objects.get(pk=item_id)
        c = i.claim_set.get(pk=claim_id)
        context = {"i":i,"c":c}
        return HttpResponse(render(request,"lostNfound/see_claim.html",context))
    except:
        return HttpResponse("claim number "+str(claim_id)+" for item "+str(item_id)+" doesn't exist.")

def see_Claim(request,claim_id):
    try:
        c = Claim.objects.get(pk=claim_id)
        context = {"c":c}
        return HttpResponse(render(request,"lostNfound/see_Claim.html",context))
    except:
        return HttpResponse("claim number "+str(claim_id)+" doesn't exist.")

def see_Person(request,person_id):
    try:
        person = Person.objects.get(pk=person_id)
        context = {"p":person, "login":False}
        return HttpResponse(render(request,"lostNfound/see_Person.html",context))
    except:
        return HttpResponse("Person with id "+str(person_id)+" doesn't exist.")

def login(request):
    username = request.POST["username"]
    password = request.POST["password"]
    if not username:
        return HttpResponse("Please enter the username.")
    try:
        person = Person.objects.get(username=username)
    except:
        return HttpResponse("This username is not registered")
    if not password:
        context = {"p":person, "login":False}
    elif password != person.password :
        return HttpResponse("Incorrect Password")
    context = {"p":person, "login":True}
    return HttpResponse(render(request,"lostNfound/see_Person.html",context))

def claim(request, item_id):
    i = Item.objects.get(pk=item_id)
    context = {"i":i}
    return HttpResponse(render(request,"lostNfound/claim.html",context))

def Request(request):
    return HttpResponse(render(request,"lostNfound/Request.html",{}))

def initiate_dissolve(request, item_id):
    i =Item.objects.get(pk=item_id)
    context={"i":i}
    return HttpResponse(render(request,"lostNfound/initiate_dissolve.html",context))

def Registration(request):
    return HttpResponse(render(request,"lostNfound/Registration.html",{}))

def file_report(request, criminal_id):
    criminal = Person.objects.get(pk=criminal_id)
    context = {"criminal":criminal}
    return HttpResponse(render(request,"lostNfound/Report.html",context))

def report(request):
    criminal = request.POST["criminal"]
    reportee = request.POST["reportee"]
    password = request.POST["password"]
    description = request.POST["description"]
    if (not criminal) or (not reportee) or (not password) or (not description) :
        return HttpResponse("Please complete the form. Every field is necessary.")
    try:
        criminal = Person.objects.get(username=criminal)
    except:
        return HttpResponse("The person you want to report doesn't exist")
    try:
        reportee = Person.objects.get(username=reportee)
    except:
        return HttpResponse("Your username is not registered.")
    if reportee.password != password:
        return HttpResponse("Incorrect password.")
    if request.POST.get("make"):
        report = reportee.reports.create(
            criminal = criminal,
            description = description,
        )
        report.save()
        criminal.crimes.add(report)
        return HttpResponse("The report has been made. You can view it on your dashboard. Dont worry. Noone else will be be able to see the report.")
    elif request.POST.get("clear"):
        report = reportee.reports.get(criminal=criminal)
        report.delete()
        return HttpResponse("The report has been cleared. Check your dashboard to see if it is reflected.")

def search_result(request):
    sus_name=request.POST["name"]
    sus_owner=request.POST["owner"]
    sus_date=request.POST["date"]
    sus_keywords=request.POST["keywords"]
    sus_location=request.POST["location"]
    sus_description=request.POST["description"]
    if request.POST.get("items"):
        L = Item.objects.all()
        isclaim = False
    elif request.POST.get("claims"):
        L = Claim.objects.all()
        isclaim = True
    else:
        return HttpResponse("error")
    if sus_name:
        sus_name = sus_name.lower()
        for token in sus_name.split():
            L = L.filter(name__icontains=token)
    if sus_date:
        L = L.filter(date__lte=sus_date)
    if sus_owner:
        sus_owner = sus_owner.lower()
        for token in sus_owner.split():
            L = [i for i in L if (token in i.person.name.lower().split())]
    if sus_keywords:
        sus_keywords = straighten(sus_keywords)
        threshold = len(sus_keywords.split(",")) * 0.5
        L = [i for i in L if count_similar(i.keywords,sus_keywords) >= threshold]
    if sus_location:
        sus_location = sus_location.lower().split(",")
        newL = []
        for i in L:
            location = i.location.lower().split(",")
            for loc in location:
                good = False
                for sloc in sus_location:
                    if distance(loc,sloc) < 0.3:
                        good = True
                        break
                if good:
                    newL.append(i)
                    break
        L = newL
    if sus_description:
        threshold = 0.5
        L = [i for i in L if similarity(sus_description,i.description) >= threshold]

    context = {"L":L,"isclaim":isclaim}
    return HttpResponse(render(request, "lostNfound/search_result.html",context))

def dissolve_Request(request):
    item_id=request.POST["id"]
    password=request.POST["password"]
    try:
        i = Item.objects.get(pk=item_id)
    except:
        return HttpResponse("The id "+str(i.id)+" does not exist.")
    return HttpResponse(i.dissolve(password))

def dissolve_claim(request):
    item_id = request.POST['item_id']
    claim_id = request.POST['claim_id']
    password = request.POST['password']
    if not item_id:
        return HttpResponse("please write the item id in the form")
    if not claim_id:
        return HttpResponse("please write the claim_id in the form")
    i = Item.objects.get(pk=item_id)
    if request.POST.get("dissolve"):
        c = i.claim_set.get(pk=claim_id)
        return HttpResponse(c.dissolve(password))
    return HttpResponse(i.unlink(claim_id,password))

def make_Request(request):
    password=request.POST["password"]
    username=request.POST["username"]
    if not password:
        return HttpResponse("Please enter the password. <br> It helps us make sure someone else won't dissolve your request accidently.")
    if not username:
        return HttpResponse("Please enter your username")
    L = Person.objects.filter(username=username)
    if not L.count():
        return HttpResponse("You are not registered!")
    L = L.filter(password=password)
    if not L.count():
        return HttpResponse("Wrong password!")
    if L.count()!=1:
        return HttpResponse("More than 1 users with same passwords. This shouldn't be happening")
    person = L.get(password=password)
    keywords = request.POST["keywords"] or ""
    keywords = straighten(keywords)
    today = timezone.now().date()
    date=request.POST["date"]
    if not date:
        date = today
    else:
        date = [int(x) for x in date.split('-')]
        year,mont,day = date
        date = datetime.date(day=day,month=mont,year=year)
    if date > today:
        return HttpResponse("Please enter a valid date ....and don't live in the future =)")
    if request.POST.get("item"):
        if (today - date).days > 4*365:
            return HttpResponse("We don't expect anyone to find something that you lost more than 4 years ago.")
        if person.item_set.count() > 50 :
            return HttpResponse("You cannot make more requests. Please remove one of the requests by your name to make more.")
        i = person.item_set.create(
            name=(request.POST["name"] or "unknown").lower(),
            date=request.POST["date"] or timezone.now().date(),
            description=request.POST["description"] or "",
            keywords=keywords,
            image=request.POST["image"] or "media/default.png",
            location=request.POST["location"] or "unknown",
        )
        i.save()
        return HttpResponse("Your request has been made. View it <a href='https://pranavjoshi.pythonanywhere.com/lostNfound/"+str(i.id)+"'> here </a>.")
    elif request.POST.get("claim"):
        if person.claim_set.count() > 50 :
            return HttpResponse("You cannot make more claims. Please remove one of them by your name to make more.")
        c = person.claim_set.create(
            name=(request.POST["name"] or "unknown").lower(),
            date=request.POST["date"] or timezone.now().date(),
            description=request.POST["description"] or "",
            keywords=keywords,
            image=request.POST["image"] or "media/default.png",
            location=request.POST["location"] or "unknown",
        )
        c.save()
        return HttpResponse("Your claim has been made. View it <a href='https://pranavjoshi.pythonanywhere.com/lostNfound/claim/"+str(c.id)+"'> here </a>.")

def make_claim(request, item_id):
    i = Item.objects.get(pk=item_id)
    username=request.POST["username"]
    password=request.POST["password"]
    username=request.POST["username"]
    if not username :
        return HttpResponse("Please tell us your username.")
    if not password :
        return HttpResponse("Please enter a password")
    L = Person.objects.filter(username=username)
    if not L.count():
        return HttpResponse("You are not registered!")
    L = L.filter(password=password)
    if not L.count():
        return HttpResponse("Wrong password!")
    if L.count()!=1:
        return HttpResponse("More than 1 users with same passwords. This shouldn't be happening")
    person = L.get(password=password)
    L =  i.claim_set.filter(person=person)
    if L.count()>10:
        return HttpResponse("You have already made many claims. You need to delete one of them first.")
    if request.POST.get("make"):
        keywords=request.POST["keywords"] or ""
        keywords = straighten(keywords)
        today = timezone.now().date()
        date= request.POST["date"]
        if not date:
            date = today
        else:
            date = [int(x) for x in date.split('-')]
            year,month,day = date
            if year<2000:
                return HttpResponse("Year less than 2000.")
            date = datetime.date(day=day,month=month,year=year)
        if date > today:
            return HttpResponse("Please enter a valid date ....and don't live in the future =)")
        c = person.claim_set.create(
            name=i.name,
            date=date,
            description=request.POST["description"] or "",
            keywords=keywords,
            image=request.POST["image"] or "default.png",
            location=request.POST["location"] or "unknown",
        )
        c.save()
        i.claim_set.add(c)
        return HttpResponse("Your claim has been made. View it <a href='https://pranavjoshi.pythonanywhere.com/lostNfound/"+str(i.id)+"/"+str(c.id)+"'> here </a>.")
    elif request.POST.get("link"):
        claim_id = request.POST["claim_id"]
        if not claim_id:
            return HttpResponse("please enter the claim id")
        try:
            c = Claim.objects.get(pk=claim_id)
        except:
            return HttpResponse("This Claim id doesn't exist.")
        if c.person.username != username:
            return HttpResponse("You have never made this claim. Make sure the id is typed correctly.")
        if c.person.password != password:
            return HttpResponse("incorrect password")
        i.claim_set.add(c)
        return HttpResponse("done")
    else:
        return HttpResponse("error")

def Register(request):
    username = request.POST['username']
    name = request.POST['name'] or "unknown"
    password = request.POST['password']
    password_conf = request.POST["password_conf"]
    contact = request.POST['contact'] or "unknown"
    email = request.POST['email'] or "unknown"
    address = request.POST['address'] or "unknown"
    image = request.POST['image'] or "/media/default.png"
    if not username:
        return HttpResponse("Please type your username")
    if Person.objects.filter(username=username).count():
        return HttpResponse("This username is already taken.")
    if not password:
        return HttpResponse("Please enter the password")
    if password != password_conf:
        return HttpResponse("Please retype the password correctly")
    person = Person(
        username=username,
        name=name,
        password=password,
        contact=contact,
        email=email,
        image=image,
        address=address,
    )
    person.save()
    return HttpResponse("You are Registered! View yourself <a href='https://pranavjoshi.pythonanywhere.com/lostNfound/person/"+str(person.id)+"'> here </a>.")