import datetime
from .models import AllTests,PCRTestsSymptoms ,deaths_no_date , covid19apidata,agg_Alltests,agg_PCRTestsSymptoms,hospitalization
from django.db.models import Count ,Q
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import statistics

'''
functions in this file pull data from the database and make charts to be displayed on the clientside

'''



#helper function to name chart files
def imgprefix(plot_type):
    return str(int(datetime.datetime.utcnow().timestamp())) +"_"+plot_type +".png"


#this function plots two graphs depicting relations between tests and positive results
def testsVsPosReport(fdate = None , todate = None):
    #set filename
    filename = imgprefix("TestVsPos")

    # if there are no date filters get the max & min date
    if fdate is None or fdate == "":
        fdate = AllTests.objects.filter(test_date__isnull= False).earliest('test_date').test_date.strftime('%Y-%m-%d')
    if todate is None or todate == "":
        todate = AllTests.objects.latest('test_date').test_date.strftime('%Y-%m-%d')

    #get the data from the database
    data = agg_Alltests.objects.filter(test_date__gte=fdate, test_date__lte=todate)

    # extract lists from the data
    date = [d.test_date for d in data]
    total_tests = [d.total_tests for d in data]
    total_pos = [d.total_pos for d in data]
    perc = [round(d.total_pos / d.total_tests , 2) for d in data]

    # plot 1st graph (tests - numbers , positives - numbers)
    fig,tests = plt.subplots()
    tests.plot(date,total_tests, label = 'Daily Tests', color="mediumturquoise")
    tests.tick_params(axis='y',color="mediumturquoise")
    tests.set_ylabel("Daily Positives",color="mediumturquoise")
    pos=tests.twinx()
    pos.plot(date, total_pos, label = 'Total Positives',color="lightsalmon")
    pos.tick_params(axis='y',color="lightsalmon")
    pos.set_ylabel("Daily Positives", color="lightsalmon")
    tests.legend(loc=0)
    pos.legend(loc=9)
    plt.tight_layout()
    fig.tight_layout()

    # save versions for pc & mobile for responsiveness
    dpi = fig.get_dpi()
    plt.setp(tests.xaxis.get_majorticklabels(), rotation=18)
    plt.savefig("./static/mob_" + filename)
    plt.setp(tests.xaxis.get_majorticklabels(), rotation=0)
    fig.set_size_inches(1200/ float(dpi), 610/ float(dpi))
    plt.savefig("./static/"+filename)

    #clear plot
    plt.clf()

    # plot 2nd graph (tests - numbers , positives - percentages )
    fig, tests = plt.subplots()
    pos_per = tests.twinx()
    tests.tick_params(axis='y', color="orchid")
    tests.set_ylabel("Total Tests", color="orchid")
    tests.plot(date, total_tests, label='Daily Tests', color="orchid")
    pos_per.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    pos_per.tick_params(axis='y', color="green")
    pos_per.set_ylabel("Daily Positives Percent", color="green")
    pos_per.plot(date, perc, label='Daily Positives Percent', color="green")

    # save versions for pc & mobile for responsiveness
    plt.setp(tests.xaxis.get_majorticklabels(), rotation=18)
    plt.savefig("./static/mob_perc_" + filename)
    plt.setp(tests.xaxis.get_majorticklabels(), rotation=0)
    fig.set_size_inches(1200 / float(dpi), 610 / float(dpi))
    plt.savefig("./static/perc_" + filename)
    plt.clf()

    #return objects with filenames
    return {"filename_pc": filename ,
            "filename_mob":"mob_" + filename,
            "perc_filename_pc": "perc_"+filename,
            "perc_filename_mob": "mob_perc_" + filename,
            }

# helper function to oreder age groups
def orderDict(d):
    newd = {}
    knownkeys = ['<65','65-74', '75-84', '85+']
    for key in d.keys():
        if key not in knownkeys:
            knownkeys.append(key)
    for key in knownkeys:
        newd[key] = d[key]
    return newd

#this function plots three graphs depicting cumulative deathrates by age group
def deathsBarChart():
    # set filename
    filename = imgprefix("deathsCumulative")

    #get data from database
    deathsbyagegroup = list(deaths_no_date.objects.values("age_group").annotate(count = Count('id'),vent= Count("id" ,filter=Q(Ventilated=True))))
    count = deaths_no_date.objects.count()

    # extract lists from the data
    bar_dict = orderDict({d["age_group"]: d["count"] for d in deathsbyagegroup})
    bar_dict_perc = orderDict({d["age_group"]: round(d["count"] / count, 2) for d in deathsbyagegroup})
    bar_dict_perc_vent = orderDict({d["age_group"]: round(d["vent"] / d["count"], 2) for d in deathsbyagegroup})

    # plot 1st graph deaths by age group - numbers
    plt.bar(range(len(bar_dict.keys())),bar_dict.values(), label = "Death by age group")
    plt.xticks(range(len(bar_dict.keys())),bar_dict.keys())
    fig = plt.gcf()
    plt.tight_layout()
    fig.tight_layout()
    dpi = fig.get_dpi()
    ax = fig.add_subplot(1, 1, 1)
    ax.yaxis.set_major_formatter(mtick.ScalarFormatter())
    plt.legend()

    # save versions for pc & mobile for responsiveness
    plt.savefig("./static/mob_" + filename)
    fig.set_size_inches(1200 / float(dpi), 610 / float(dpi))
    plt.savefig("./static/" + filename)


    plt.clf()

    # plot 2nd graph deaths by age group - percentages
    ax = fig.add_subplot(1, 1, 1)
    plt.bar(range(len(bar_dict_perc.keys())),bar_dict_perc.values(), color="orange",label = "Death % out of all deaths by age group")
    plt.xticks(range(len(bar_dict.keys())), bar_dict.keys())
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    plt.legend()

    # save versions for pc & mobile for responsiveness
    plt.savefig("./static/mob_perc_" + filename)
    fig.set_size_inches(1200 / float(dpi), 610 / float(dpi))
    plt.savefig("./static/perc_" + filename)
    plt.clf()

    # plot 3rd graph Ventilated out of deaths by age group - percentages
    ax = fig.add_subplot(1, 1, 1)
    plt.bar(range(len(bar_dict_perc_vent.keys())), bar_dict_perc_vent.values(), color="indianred",label = "% Ventilated out of deaths in age group")
    plt.xticks(range(len(bar_dict.keys())), bar_dict.keys())
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    plt.legend()

    # save versions for pc & mobile for responsiveness
    plt.savefig("./static/mob_perc_vent_" + filename)
    fig.set_size_inches(1200 / float(dpi), 610 / float(dpi))
    plt.savefig("./static/perc_vent_" + filename)
    plt.clf()

    return {
            "filename_pc": filename,
            "filename_mob": "mob_" + filename,
            "perc_filename_pc": "perc_" + filename,
            "perc_filename_mob": "mob_perc_" + filename,
        "perc_vent_filename_pc": "perc_vent_" + filename,
        "perc_vent_filename_mob": "mob_perc_vent_" + filename
            }

#this function plots two graphs depicting cumulative confirmed ,active ,recovered and CFR as well as daily change in confirmed ,active and recovered
def confDeathRecoverActive(fdate = None,todate = None):
    # set filname
    filename = imgprefix("confDeathRecoverActive")

    # if there are no date filters get the max & min date
    if fdate is None or fdate == "":
        fdate = covid19apidata.objects.filter(Date__gte="2020-02-21").earliest("Date").Date.strftime('%Y-%m-%d')
    if todate is None or todate == "":
        todate = covid19apidata.objects.latest("Date").Date.strftime('%Y-%m-%d')

    #get data from database
    data = covid19apidata.objects.filter(Date__gte=fdate, Date__lte=todate)

    #ectract lists from data
    Date = [d.Date for d in data]
    Confirmed =[d.Confirmed for d in data]
    Recovered = [d.Recovered for d in data]
    Active = [d.Active for d in data]
    Deaths_rate = [d.Deaths/d.Confirmed for d in data]
    daily_Confirmed =[d.daily_Confirmed for d in data]
    daily_Recovered = [d.daily_Recovered for d in data]
    daily_Active = [d.daily_Active for d in data]

    # plot 1st graph (confirmed ,active ,recovered - numbers , CFR - %)
    fig,cnf= plt.subplots()
    drate = cnf.twinx()
    drate.tick_params(axis='y')
    drate.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    drate.plot(Date, Deaths_rate, label="CFR", color="red")
    cnf.plot(Date, Confirmed, label="Confirmed")
    cnf.plot(Date, Recovered, label="Recovered")
    cnf.plot(Date, Active, label="Active")
    drate.legend(loc="best")
    cnf.legend()
    plt.tight_layout()
    fig.tight_layout()

    # save versions for pc & mobile for responsiveness
    dpi = fig.get_dpi()
    plt.xticks(rotation=18)
    plt.savefig("./static/mob_" + filename)
    plt.xticks(rotation=0)
    fig.set_size_inches(1200 / float(dpi), 610 / float(dpi))
    plt.savefig("./static/" + filename)

    #clear plot
    plt.clf()

    # plot 2nd graph (confirmed ,active ,recovered - numbers , CFR - %)
    plt.plot(Date, daily_Confirmed, label="Confirmed")
    plt.plot(Date, daily_Recovered, label="Recovered")
    plt.plot(Date, daily_Active, label="Active")
    plt.legend()

    # save versions for pc & mobile for responsiveness
    fig = plt.gcf()
    plt.xticks(rotation=18)
    plt.savefig("./static/mob_change_" + filename)
    plt.xticks(rotation=0)
    fig.set_size_inches(1200 / float(dpi), 610 / float(dpi))
    plt.savefig("./static/change_" + filename)
    plt.clf()
    return {"filename_pc": filename,
            "filename_mob": "mob_" + filename,
            "change_filename_pc": "change_" + filename,
            "change_filename_mob": "mob_change_" + filename}

#this function plots two graphs depicting the ratio between daily tests to tests with symptoms and positives and positives with symptoms
def symptomsPCR(fdate = None , todate = None):

    #set filname
    filename = imgprefix("symptomsPCR")

    #if there are no date filters get min and max date
    if fdate is None or fdate == "":
        fdate = PCRTestsSymptoms.objects.filter(test_date__isnull=False).earliest('test_date').test_date.strftime('%Y-%m-%d')
    if todate is None or todate == "":
        todate = PCRTestsSymptoms.objects.filter(test_date__isnull=False).latest('test_date').test_date.strftime('%Y-%m-%d')

    #get data from database
    data = agg_PCRTestsSymptoms.objects.filter(test_date__gte=fdate, test_date__lte=todate)

    #extract lists from data
    Date = [d.test_date for d in data]
    alltests= [d.alltests for d in data]
    symptoms = [d.withsymptoms for d in data]
    allpos = [d.allpos for d in data]
    poswithwithsymptoms = [d.poswithwithsymptoms for d in data]

    # plot 1st graph (tests , tests with symptoms -numbers )
    plt.stackplot(Date ,symptoms , alltests, labels= ["Tested With Symptoms", "All Tests"], colors=["lightcoral","mediumpurple"])
    plt.legend(loc=2)
    fig = plt.gcf()
    dpi = fig.get_dpi()

    # save versions for pc & mobile for responsiveness
    plt.xticks(rotation=18)
    plt.savefig("./static/mob_" + filename)
    plt.xticks(rotation=0)
    fig.set_size_inches(1200 / float(dpi), 610 / float(dpi))
    plt.savefig("./static/" + filename)

    #clear plot
    plt.clf()

    # plot 2nd graph (positives ,positives with symptoms -numbers )
    plt.stackplot(Date, poswithwithsymptoms, allpos, labels=["Positive With Symptoms", "All Positives"],colors=["firebrick", "gold"])
    plt.legend(loc=2)
    plt.tight_layout()
    fig.tight_layout()

    # save versions for pc & mobile for responsiveness
    plt.xticks(rotation=18)
    plt.savefig("./static/mob_pos_" + filename)
    plt.xticks(rotation=0)
    fig.set_size_inches(1200 / float(dpi), 610 / float(dpi))
    plt.savefig("./static/pos_" + filename)

    # clear plot
    plt.clf()
    return {"filename_pc": filename,
     "filename_mob": "mob_" + filename,
     "pos_filename_pc": "pos_" + filename,
     "pos_filename_mob": "mob_pos_" + filename}


#this function plots four graphs depicting the ratio between levels of severity in hospitalized cases
def hospitalizationsCharts(fdate = None , todate = None):

    #set filename
    filename = imgprefix("hospitalizationsCharts")

    #if there are no filters get the max and min dates
    if fdate is None or fdate == "":
        fdate = hospitalization.objects.filter(date__isnull=False).earliest('date').date.strftime('%Y-%m-%d')
    if todate is None or todate > hospitalization.objects.filter(date__isnull=False).latest('date').date.strftime('%Y-%m-%d') :
        todate = hospitalization.objects.filter(date__isnull=False).latest('date').date.strftime('%Y-%m-%d')
    #get data from database
    covidapiDat = covid19apidata.objects.values("Date","Confirmed","Deaths").filter(Date__gte=fdate, Date__lte=todate).order_by("Date")
    data= hospitalization.objects.filter(date__gte=fdate, date__lte=todate).order_by("date")

    #extract lists
    total_cases = [d["Confirmed"] for d in covidapiDat]
    total_deaths = [d["Deaths"] for d in covidapiDat]
    total_hospitalised  = [d.total_hospitalised for d in data]
    date = [d.date for d in data]
    mild = [d.mild for d in data]
    modarate =[d.modarate for d in data]
    severe = [d.severe for d in data]
    severe_acc = [d.severe_cumulative for d in data]
    perc_hosp_mild = [d.mild/d.total_hospitalised for d in data]
    perc_hosp_modarate = [d.modarate / d.total_hospitalised for d in data]
    perc_hosp_severe  = [d.severe  / d.total_hospitalised for d in data]
    perc_case_mild = [(mild[index] if index < len(data) else 0)/d for index ,d in enumerate(total_cases)]
    perc_case_modarate = [(modarate[index] if index < len(data) else 0 )/ d for index, d in enumerate(total_cases)]
    perc_case_severe = [(severe[index] if index < len(data) else 0 )/ d for index, d in enumerate(total_cases)]
    perc_case_total_hospitalised = [(total_hospitalised[index] if index < len(data) else 0) / d for index, d in enumerate(total_cases)]
    perc_severe_deaths = [((total_deaths[index] if index < len(data)  else 0)/d ) if d > 0 else 0 for index ,d in enumerate(severe_acc)]

    #plot 1st graph cumulative hospitalizations by severity
    plt.plot(date , mild , label = "Mild",color="green")
    plt.plot(date, modarate, label="Modarate")
    plt.plot(date, severe, label="Severe",color = "red")
    plt.plot(date,total_hospitalised,label="Total Hospitalised")
    fig = plt.gcf()
    dpi = fig.get_dpi()
    plt.legend()

    # save versions for pc & mobile for responsiveness
    plt.xticks(rotation=18)

    plt.savefig("./static/mob_" + filename)
    plt.xticks(rotation=0)
    fig.set_size_inches(1200 / float(dpi), 610 / float(dpi))
    plt.savefig("./static/" + filename)
    plt.clf()

    # plot 1st graph daily hospitalizations by severity
    fig = plt.gcf()
    ax = fig.add_subplot(1, 1, 1)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    plt.plot(date, perc_hosp_mild, label="Mild % of Hospitalised",color="green")
    plt.plot(date, perc_hosp_modarate, label="Modarate % of Hospitalised")
    plt.plot(date, perc_hosp_severe, label="Severe % of Hospitalised" ,color = "red")
    plt.legend()
    fig = plt.gcf()
    dpi = fig.get_dpi()
    plt.legend()
    plt.xticks(rotation=18)
    plt.savefig("./static/mob_perc_hosp_" + filename)
    plt.xticks(rotation=0)
    fig.set_size_inches(1200 / float(dpi), 610 / float(dpi))
    plt.savefig("./static/perc_hosp_" + filename)
     
    plt.clf()

    # plot 2nd graph daily % of total hospitalizations by severity
    fig = plt.gcf()
    ax = fig.add_subplot(1, 1, 1)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    plt.plot(date, perc_case_mild, label=" Daily Mild % of Daily Cumulative Cases", color="green")
    plt.plot(date, perc_case_modarate, label=" Daily Modarate % of Daily Cumulative Cases")
    plt.plot(date, perc_case_severe, label="Severe % Daily Cumulative Cases", color="red")
    plt.plot(date, perc_case_total_hospitalised, label="Daily Total Hospitalised % Daily Cumulative Cases")
    plt.legend()
    fig = plt.gcf()

    # save versions for pc & mobile for responsiveness
    dpi = fig.get_dpi()
    plt.legend()
    plt.xticks(rotation=18)
    plt.savefig("./static/mob_perc_case_" + filename)
    plt.xticks(rotation=0)
    fig.set_size_inches(1200 / float(dpi), 610 / float(dpi))
    plt.savefig("./static/perc_case_" + filename)


    plt.clf()

    # plot 3rd graph daily % hospitalizations of total cases by severity
    plt.bar(date, perc_severe_deaths, label="Cumulative Daily Death % out of Daily Cumulative Severe", color="red")
    fig = plt.gcf()
    ax = fig.add_subplot(1, 1, 1)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    plt.legend()

    # save versions for pc & mobile for responsiveness
    plt.xticks(rotation=18)
    plt.savefig("./static/mob_perc_severe_death_" + filename)
    plt.xticks(rotation=0)
    fig.set_size_inches(1200 / float(dpi), 610 / float(dpi))
    plt.savefig("./static/perc_severe_death_" + filename)
    plt.clf()
    return {
    "filename_pc": filename,
     "filename_mob": "mob_" + filename,
     "perc_hosp_filename_pc": "perc_hosp_" + filename,
     "perc_hosp_filename_mob": "mob_perc_hosp_" + filename,
    "perc_case_filename_pc": "perc_case_" + filename,
     "perc_case_filename_mob": "mob_perc_case_" + filename,
     "perc_severe_death_filename_pc": "perc_severe_death_" + filename,
     "perc_severe_death_filename_mob": "mob_perc_severe_death_" + filename
     }


# function that plots all the graphs with the date filter from the frontend and reruns an objects with the filenames
def initPage(fdate = None , todate = None):
    start = datetime.datetime.now()
    if fdate is None or fdate == "":
        fdate = AllTests.objects.filter(test_date__isnull=False).earliest('test_date').test_date.strftime('%Y-%m-%d')
    if todate is None or todate == "":
        todate = AllTests.objects.latest('test_date').test_date.strftime('%Y-%m-%d')
    finalObj = {}
    tvp = testsVsPosReport(fdate=fdate,todate=todate)
    dbar = deathsBarChart()
    cnf = confDeathRecoverActive(fdate=fdate,todate=todate)
    sym = symptomsPCR(fdate=fdate,todate=todate)
    hospi = hospitalizationsCharts(fdate=fdate,todate=todate)
    for key in tvp.keys():
        finalObj[key.replace("filename" , "filename_tvp")] = tvp[key]
    for key in dbar.keys():
        finalObj[key.replace("filename" , "filename_dbar")] = dbar[key]
    for key in cnf.keys():
        finalObj[key.replace("filename" , "filename_cnf")] = cnf[key]
    for key in sym.keys():
        finalObj[key.replace("filename", "filename_sym")] = sym[key]
    for key in hospi.keys():
        finalObj[key.replace("filename", "filename_hospi")] = hospi[key]
    print(datetime.datetime.now() - start)
    return finalObj
