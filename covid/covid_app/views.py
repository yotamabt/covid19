from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from .ReportMaker import initPage ,testsVsPosReport

# Create your views here.


def index(request):
    if request.method == "POST":
        fdate = request.POST["fdate"]
        todate = request.POST['todate']
        dat = initPage(str(fdate),str(todate))
        return HttpResponse(render(request, "covid_app/index.html",dat))
    else:
        dat = initPage()

        print(dat)
        return HttpResponse(render(request, "covid_app/index.html",dat))


def makeTestVsPosReport(request):
    test = testsVsPosReport()
    return JsonResponse(test)
def testpath(request):
    return HttpResponse(render(request, "covid_app/test.html"))
