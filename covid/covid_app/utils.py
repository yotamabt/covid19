from .models import PCRTestsSymptoms ,AllTests, deaths_no_date,covid19apidata ,hospitalization
import requests
import datetime
import sqlite3


def initPrepTables():
    database = sqlite3.connect('db.sqlite3', check_same_thread=False)
    tbls = ["covid_app_alltests","covid_app_pcrtestssymptoms"]
    for name in tbls:
        q =database.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{name}'")
        database.execute(q.fetchall()[0][0].replace(name,name+"_prep"))




# import first tests with symptoms data from https://data.gov.il/dataset/covid-19/resource/d337959a-020a-4ed3-84f7-fca182292308
def fullDataImportPCRTests():

    #connect to database
    database = sqlite3.connect('db.sqlite3', check_same_thread=False)
    database.execute('pragma journal_mode=wal')

    # delete old data from preparation table
    database.execute('DELETE FROM covid_app_pcrtestssymptoms_prep;')
    database.commit()
    database.execute("UPDATE SQLite_sequence SET seq=0 where name ='covid_app_pcrtestssymptoms_prep' ")
    database.commit()

    #make the first request and get the size
    req = requests.get("https://data.gov.il/api/3/action/datastore_search?resource_id=d337959a-020a-4ed3-84f7-fca182292308&limit=32000&include_total=true").json()
    indx = 0
    round = 1
    qlist = []
    size = req["result"]["total"]
    # help dict to transform data
    helpdict = {
        "1": True,
        "0": False,
        "חיובי": True,
        "שלילי": False,
        "זכר": "Male",
        "נקבה": "Female",
        "Yes": True,
        "No": False,
        "אחר": None,
        "NULL": None,
        'לא ודאי ישן': None

    }
    for row in req["result"]["records"]:
        test_date = datetime.datetime.strptime(row['test_date'], "%Y-%m-%d")
        cough = helpdict[row["cough"]]
        fever = helpdict[row["fever"]]
        sore_throat = helpdict[row["sore_throat"]]
        shortness_of_breath = helpdict[row["shortness_of_breath"]]
        head_ache = helpdict[row["head_ache"]]
        corona_result = helpdict[row["corona_result"]]
        age_60_and_above = helpdict[row["age_60_and_above"]]
        gender = helpdict[row["gender"]]
        test_indication = row["test_indication"]

        qlist.append((test_date, cough, fever, sore_throat, shortness_of_breath, head_ache, corona_result,
                      age_60_and_above, gender, test_indication))

    print("executing query")

    # execute query
    database.executemany('''insert into covid_app_pcrtestssymptoms_prep (test_date,
                                      cough,
                                      fever,
                                      sore_throat,
                                      shortness_of_breath,
                                      head_ache,
                                      corona_result,
                                      age_60_and_above,
                                      gender,
                                      test_indication) values (date(?),?,?,?,?,?,?,?,?,?)  ''', qlist)
    database.commit()

    # incrementally get all the data (the limit is 32,000 per api call)
    while indx < size:
        qlist = []
        print("ROUND" + str(round))
        indx = indx + 32000
        req = requests.get(
            "https://data.gov.il/api/3/action/datastore_search?resource_id=d337959a-020a-4ed3-84f7-fca182292308&limit=32000&include_total=true&offset=" + str(
                indx)).json()
        round = round + 1
        # prepare the query
        for row in req["result"]["records"]:
            test_date = datetime.datetime.strptime(row['test_date'], "%Y-%m-%d")
            cough = helpdict[row["cough"]]
            fever = helpdict[row["fever"]]
            sore_throat = helpdict[row["sore_throat"]]
            shortness_of_breath = helpdict[row["shortness_of_breath"]]
            head_ache = helpdict[row["head_ache"]]
            corona_result = helpdict[row["corona_result"]]
            age_60_and_above = helpdict[row["age_60_and_above"]]
            gender = helpdict[row["gender"]]
            test_indication = row["test_indication"]

            qlist.append((test_date, cough, fever, sore_throat, shortness_of_breath, head_ache, corona_result,
                          age_60_and_above, gender, test_indication))

        print("executing query")

        # execute query
        database.executemany('''insert into covid_app_pcrtestssymptoms_prep (test_date,
                                   cough,
                                   fever,
                                   sore_throat,
                                   shortness_of_breath,
                                   head_ache,
                                   corona_result,
                                   age_60_and_above,
                                   gender,
                                   test_indication) values (date(?),?,?,?,?,?,?,?,?,?)  ''', qlist)
        database.commit()






    print("replace old data")
    #clear old data from production table and copy the updated data
    database.execute('DELETE FROM covid_app_pcrtestssymptoms;')
    database.commit()
    database.execute("UPDATE SQLite_sequence SET seq=0 where name ='covid_app_pcrtestssymptoms'")
    database.commit()
    database.execute("insert into covid_app_pcrtestssymptoms select * from covid_app_pcrtestssymptoms_prep")
    database.commit()
    print("done")


# import all tests with  no symptoms data from https://data.gov.il/dataset/covid-19/resource/dcf999c1-d394-4b57-a5e0-9d014a62e046
def TestsFullUpdateNoSymptoms():

    # help dict to transform data
    helpdict = {
        "1": True,
        "0": False,
        "חיובי": True,
        "שלילי": False,
        "זכר": "Male",
        "נקבה": "Female",
        "Yes": True,
        "No": False,
        "אחר": None,
        "NULL": None,
        "בעבודה": None,
        "לא ודאי": None,
        'לא בוצע/פסול 999': None,
        'חיובי גבולי': True,
        'לא ודאי ישן': None

    }
    # connect to database
    database = sqlite3.connect('db.sqlite3', check_same_thread=False)
    database.execute('pragma journal_mode=wal')
    # delete old data from preparation table
    database.execute('DELETE FROM covid_app_alltests_prep;')
    database.commit()
    database.execute("UPDATE SQLite_sequence SET seq=0 where name ='covid_app_alltests_prep' ")
    database.commit()

    # make the first request and get the size
    req = requests.get(
        "https://data.gov.il/api/3/action/datastore_search?resource_id=dcf999c1-d394-4b57-a5e0-9d014a62e046&limit=32000&include_total=true").json()

    indx = 0
    round = 1
    qlist = []
    size = req["result"]["total"]
    for row in req["result"]["records"]:
        test_date = None
        if row['test_date'] != 'NULL':
            test_date = datetime.datetime.strptime(row['test_date'], "%Y-%m-%d")
        result_date = None
        if row['result_date'] != 'NULL':
            result_date = datetime.datetime.strptime(row['result_date'], "%Y-%m-%d")
        corona_result = helpdict[row["corona_result"]]
        lab_id = row['lab_id']
        test_for_corona_diagnosis = helpdict[row["test_for_corona_diagnosis"]]
        is_first_Test = helpdict[row["is_first_Test"]]

        qlist.append((test_date, result_date, corona_result, lab_id, test_for_corona_diagnosis, is_first_Test))
    print("done Looping , creating query")
    database.executemany('''insert into covid_app_alltests_prep(test_date,
        result_date,
        corona_result,
        lab_id,
        test_for_corona_diagnosis,
        is_first_Test) values (date(?),date(?),?,?,?,?)  ''', qlist)
    print("executing query")

    # incrementally get all the data (the limit is 32,000 per api call)
    while indx < size:
        qlist = []
        print("ROUND" + str(round))
        indx = indx + 32000
        req = requests.get(
            "https://data.gov.il/api/3/action/datastore_search?resource_id=dcf999c1-d394-4b57-a5e0-9d014a62e046&limit=32000&include_total=true&offset=" + str(
                indx)).json()


        round = round + 1
        # prepare the query
        for row in req["result"]["records"]:
            test_date = None
            if row['test_date'] != 'NULL':
                test_date = datetime.datetime.strptime(row['test_date'], "%Y-%m-%d")
            result_date = None
            if row['result_date'] != 'NULL':
                result_date = datetime.datetime.strptime(row['result_date'], "%Y-%m-%d")
            corona_result = helpdict[row["corona_result"]]
            lab_id = row['lab_id']
            test_for_corona_diagnosis = helpdict[row["test_for_corona_diagnosis"]]
            is_first_Test = helpdict[row["is_first_Test"]]

            qlist.append((test_date, result_date, corona_result, lab_id, test_for_corona_diagnosis, is_first_Test))
        print("done Looping , creating query")
        database.executemany('''insert into covid_app_alltests_prep(test_date,
            result_date,
            corona_result,
            lab_id,
            test_for_corona_diagnosis,
            is_first_Test) values (date(?),date(?),?,?,?,?)  ''', qlist)
        print("executing query")




    # clear old data from production table and copy the updated data
    print("Tranfering from prep table to prod table")
    database.execute('DELETE FROM covid_app_alltests;')
    database.commit()
    database.execute("UPDATE SQLite_sequence SET seq=0 where name ='covid_app_alltests'")
    database.commit()
    database.execute("insert into covid_app_alltests select * from covid_app_alltests_prep")
    database.commit()
    print("done")

# import deaths data from https://data.gov.il/dataset/covid-19/resource/a2b2fceb-3334-44eb-b7b5-9327a573ea2c
def deathsNoDateUpdate():
    # connect to database
    database = sqlite3.connect('db.sqlite3', check_same_thread=False)
    database.execute('pragma journal_mode=wal')
    # delete old data from table
    database.execute('DELETE FROM covid_app_deaths_no_date;')
    database.commit()
    database.execute("UPDATE SQLite_sequence SET seq=0 where name ='covid_app_deaths_no_datep' ")
    database.commit()


    req = requests.get("https://data.gov.il/api/3/action/datastore_search?resource_id=a2b2fceb-3334-44eb-b7b5-9327a573ea2c&limit=32000&include_total=true").json()
    finalList = req["result"]["records"].copy()
    indx = len(finalList)
    round = 1

    size = req["result"]["total"]

    # incrementally get all the data (the limit is 32,000 per api call)
    while indx < size:
        print("ROUND" + str(round))

        req = requests.get(
            "https://data.gov.il/api/3/action/datastore_search?resource_id=a2b2fceb-3334-44eb-b7b5-9327a573ea2c&limit=32000&include_total=true&offset=" + str(
                indx)).json()
        indx = indx + 32000
        finalList = finalList + req["result"]["records"].copy()
        round = round + 1

    # help dict to transform data
    helpdict = {
        "1": True,
        "0": False,
        "חיובי": True,
        "שלילי": False,
        "זכר": "Male",
        "נקבה": "Female",
        "Yes": True,
        "No": False,
        "אחר": None,
        "NULL": None,
        "בעבודה": None,
        "לא ודאי": None,
        'לא בוצע/פסול 999': None,
        'חיובי גבולי': True,

    }
    qlist = []

    # prepare the query
    for row in finalList:
        gender = helpdict[row["gender"]]
        age_group = row["age_group"]
        Ventilated = helpdict[row['Ventilated']]
        Time_between_positive_and_hospitalization = None
        if row['Time_between_positive_and_hospitalization'] != "NULL":
            Time_between_positive_and_hospitalization = float(row['Time_between_positive_and_hospitalization'])
        Length_of_hospitalization = None
        if row['Length_of_hospitalization'] != "NULL":
            Length_of_hospitalization = float(row['Length_of_hospitalization'])
        Length_of_hospitalization = None
        if row['Time_between_positive_and_death'] != "NULL":
            Time_between_positive_and_death = float(row['Time_between_positive_and_death'])

        dbrow = deaths_no_date(gender =gender,
                         age_group=age_group,
                         Ventilated=Ventilated,
                         Time_between_positive_and_hospitalization=Time_between_positive_and_hospitalization,
                         Length_of_hospitalization=Length_of_hospitalization,
                         Time_between_positive_and_death =Time_between_positive_and_death
                         )
        qlist.append(dbrow)

    print("done Looping , creating query")

    print("executing query")

    # execute query
    deaths_no_date.objects.bulk_create(qlist)

# get aggregated confirmed,recovered,active and deaths from https://covid19api.com/
def covid19APIUpdate():
    # connect to database
    database = sqlite3.connect('db.sqlite3', check_same_thread=False)
    database.execute('pragma journal_mode=wal')
    # delete old data from table
    database.execute('DELETE FROM covid_app_covid19apidata;')
    database.commit()
    database.execute("UPDATE SQLite_sequence SET seq=0 where name ='covid_app_covid19apidata' ")
    database.commit()
    req = requests.get("https://api.covid19api.com/country/israel?from=2020-02-22T00:00:00Z").json()

    qlist = []

    # add daily change to cumulative data and prepare query
    for index , row in enumerate(req):
        Date = row["Date"].split("T")[0]
        Deaths = row["Deaths"]
        Recovered = row["Recovered"]
        Active = row["Active"]
        Confirmed = row["Confirmed"]
        daily_Deaths = 0
        daily_Recovered = 0
        daily_Active = 0
        daily_Confirmed=0
        if index > 0:
            daily_Deaths =  row["Deaths"] - req[index-1]["Deaths"]
            daily_Recovered = row["Recovered"] - req[index-1]["Recovered"]
            daily_Active = row["Active"] - req[index-1]["Active"]
            daily_Confirmed = row["Confirmed"]- req[index - 1]["Confirmed"]
        else:
            daily_Deaths = row["Deaths"]
            daily_Recovered = row["Recovered"]
            daily_Active = row["Active"]
            daily_Confirmed = row["Confirmed"]
        qlist.append(covid19apidata(Date=Date,
                                    Confirmed=Confirmed,
                                    Deaths=Deaths,
                                    Recovered=Recovered,
                                    Active=Active,
                                    daily_Confirmed=daily_Confirmed,
                                    daily_Deaths=daily_Deaths,
                                    daily_Recovered=daily_Recovered,
                                    daily_Active= daily_Active
                                    ))

    #execute query
    covid19apidata.objects.bulk_create(qlist)

#get hospitalization data from  https://data.gov.il/dataset/covid-19/resource/e4bf0ab8-ec88-4f9b-8669-f2cc78273edd
def hospitalizationUpdate():
    # connect to database
    database = sqlite3.connect('db.sqlite3', check_same_thread=False)
    database.execute('pragma journal_mode=wal')
    # delete old data from table
    database.execute('DELETE FROM covid_app_hospitalization')
    database.commit()
    database.execute("UPDATE SQLite_sequence SET seq=0 where name ='covid_app_hospitalization' ")
    database.commit()

    #helpdict to deal with hebrew keys
    helpdict = {"תאריך":"date",
                "מאושפזים":"total_hospitalised",
                "אחוז נשים מאושפזות":"perc_hospitalised_female",
                "גיל ממוצע מאושפזים":"avg_age",
                "סטיית תקן גיל מאושפזים" :"std_div_age",
                "מונשמים":"ventilated",
                "אחוז נשים מונשמות":"perc_female_ventilated",
                "גיל ממוצע מונשמים":"avg_age_ventilated",
                "סטיית תקן גיל מונשמים":"std_div_age_ventilated",
                "חולים קל":"mild",
                "אחוז נשים חולות קל":"perc_mild_female",
                "גיל ממוצע חולים קל":"avg_age_mild",
                "סטיית תקן גיל חולים קל":"std_div_age_mild",
                "חולים בינוני":"modarate",
                "אחוז נשים חולות בינוני":"perc_modarate_female",
                "גיל ממוצע חולים בינוני":"avg_age_modarate",
                "סטיית תקן גיל חולים בינוני":"std_div_age_modarate",
                "חולים קשה":"severe",
                "אחוז נשים חולות קשה":"perc_severe_female",
                "גיל ממוצע חולים קשה":"avg_age_severe",
                "סטיית תקן גיל חולים קשה":"std_div_age_severe",
                "חולים קשה מצטבר": "severe_cumulative"}

    # make the first request and get the size
    req = requests.get("https://data.gov.il/api/3/action/datastore_search?resource_id=e4bf0ab8-ec88-4f9b-8669-f2cc78273edd&limit=32000&include_total=true").json()
    heblist = req["result"]["records"].copy()
    indx = len(heblist)
    round = 1
    size = req["result"]["total"]

    # incrementally get all the data (the limit is 32,000 per api call)
    while indx < size:
        print("ROUND" + str(round))
        req = requests.get("https://data.gov.il/api/3/action/datastore_search?resource_id=a2b2fceb-3334-44eb-b7b5-9327a573ea2c&limit=32000&include_total=true&offset=" + str(indx)).json()
        indx = indx + 32000
        heblist = heblist+req

    # translate the hebrew keys
    finallist = [{helpdict[key]:row[key] for key in helpdict.keys()} for row in heblist]

    # prepare query
    qlist =[]
    for row in finallist:
        hosp = hospitalization(
            date=row["date"].split("T")[0],
            total_hospitalised= row["total_hospitalised"] if row["total_hospitalised"]!= 'NULL' else None ,
            perc_hospitalised_female=row["perc_hospitalised_female"] if row["perc_hospitalised_female"]  != 'NULL' else None  ,
            avg_age=row["avg_age"] if row["avg_age"] != 'NULL' else None ,
            std_div_age=row["std_div_age"] if row["std_div_age"] != 'NULL' else None ,
            ventilated=  float(row["ventilated"] if row["ventilated"] not in ['<15','NULL'] else 0),
            perc_female_ventilated=row["perc_female_ventilated"] if row["perc_female_ventilated"] != 'NULL' else None,
            avg_age_ventilated=row["avg_age_ventilated"] if row["avg_age_ventilated"] != 'NULL' else None,
            std_div_age_ventilated=row["std_div_age_ventilated"] if row["std_div_age_ventilated"]!= 'NULL' else None,
            mild=float(row["mild"] if row["mild"]!= 'NULL' else None),
            perc_mild_female=row["perc_mild_female"] if row["perc_mild_female"] != 'NULL' else None,
            avg_age_mild=row["avg_age_mild"] if row["avg_age_mild"] != 'NULL' else None,
            std_div_age_mild=row["std_div_age_mild"] if row["std_div_age_mild"] != 'NULL' else None,
            modarate=float(row["modarate"] if row["modarate"] not in ['<15','NULL'] else 0),
            perc_modarate_female=row["perc_modarate_female"] if row["perc_modarate_female"]!= 'NULL' else None,
            avg_age_modarate=row["avg_age_modarate"] if row["avg_age_modarate"] != 'NULL' else None,
            std_div_age_modarate=row["std_div_age_modarate"] if row["std_div_age_modarate"] != 'NULL' else None,
            severe=float(row["severe"] if row["severe"] not in ['<15','NULL'] else 0),
            perc_severe_female=row["perc_severe_female"] if row["perc_severe_female"] != 'NULL' else None,
            avg_age_severe=row["avg_age_severe"] if row["avg_age_severe"] != 'NULL' else None,
            std_div_age_severe=row["std_div_age_severe"] if row["std_div_age_severe"] != 'NULL' else None,
            severe_cumulative=float(row["severe_cumulative"] if row["severe_cumulative"]  not in ['<15','NULL'] else 0)

        )
        qlist.append(hosp)

    #execute query
    hospitalization.objects.bulk_create(qlist)





# function to aggragte data from data.gov.il
def agg():
    database = sqlite3.connect('db.sqlite3', check_same_thread=False)
    database.execute('pragma journal_mode=wal')
    database.execute('DELETE FROM covid_app_agg_alltests;')
    database.commit()
    database.execute("UPDATE SQLite_sequence SET seq=0 where name ='covid_app_agg_alltests';")
    database.commit()
    database = sqlite3.connect('db.sqlite3', check_same_thread=False)
    database.execute('DELETE FROM covid_app_agg_pcrtestssymptoms;')
    database.commit()
    database.execute("UPDATE SQLite_sequence SET seq=0 where name ='covid_app_agg_pcrtestssymptoms';")
    database.commit()
    database.execute('''
                           INSERT INTO covid_app_agg_alltests(test_date , total_tests, total_pos)
                            select * from
                            (select t1.test_date,count(*) as total_tests ,t2.total_pos
                            from covid_app_alltests t1
                            join (select result_date ,count(*) as total_pos
                                    from covid_app_alltests
                                    where corona_result =true 
                                    and test_for_corona_diagnosis = true
                                    group by result_date
                                    ) as t2
                            on t2.result_date = t1.test_date
                            where 
                            t1.test_for_corona_diagnosis = true
                            group by test_date)
                                                                        ''')
    database.commit()
    database.execute('''INSERT INTO covid_app_agg_pcrtestssymptoms(test_date ,alltests , withsymptoms ,allpos ,poswithwithsymptoms) select * from
                        (select t1.test_date,count(*) as alltests , withsymptoms ,allpos ,poswithwithsymptoms
                            from covid_app_pcrtestssymptoms as t1
                            join
                            (select test_date,count(*)  as withsymptoms 
                                from covid_app_pcrtestssymptoms
                                where cough =true or 
                                fever= true or 
                                sore_throat =true or 
                                shortness_of_breath =true or 
                                head_ache = true
                                group by test_date ) as t2
                             on t2.test_date = t1.test_date
                            join
                                (select test_date,count(*)  as allpos
                                from covid_app_pcrtestssymptoms
                                where corona_result = true
                                group by test_date ) as t3
                             on t3.test_date = t1.test_date
                            join
                            (select test_date,count(*)  as poswithwithsymptoms 
                                from covid_app_pcrtestssymptoms
                                where cough =true or 
                                fever= true or 
                                sore_throat =true or 
                                shortness_of_breath =true or 
                                head_ache = true
                                and corona_result = true
                                group by test_date ) as t4
                            on t4.test_date = t1.test_date
                            group by t1.test_date
                                                                                        )''')
    database.commit()


# function that runs the full update and aggregation can be executed periodically to keep data updated
def updateAll():
    start = datetime.datetime.now()
    deathsNoDateUpdate()
    print("deaths data.gov.il updated  " + str(datetime.datetime.now() - start))
    covid19APIUpdate()
    print("covid19api updated  " + str(datetime.datetime.now() - start))
    fullDataImportPCRTests()
    print("tests with symptoms data.gov.il updated  " + str(datetime.datetime.now() - start))
    TestsFullUpdateNoSymptoms()
    print("all tests with no symptoms data.gov.il updated  " + str(datetime.datetime.now() - start))
    hospitalizationUpdate()
    print("hospitalizations data.gov.il updated  " + str(datetime.datetime.now() - start))
    agg()


