from django.db import models

# Create your models here.
class PCRTestsSymptoms(models.Model):
    test_date = models.DateField(auto_now_add=False , auto_now= False , blank= True ,null= True)
    cough = models.BooleanField(null= True)
    fever= models.BooleanField(null= True)
    sore_throat = models.BooleanField(null= True)
    shortness_of_breath = models.BooleanField(null= True)
    head_ache = models.BooleanField(null= True)
    corona_result = models.BooleanField(null= True)
    age_60_and_above = models.BooleanField(null= True)
    gender = models.CharField(max_length=200,null= True)
    test_indication = models.CharField(max_length=200,)


    def __str__(self):
        return str(self.corona_result)

class AllTests(models.Model):
    test_date = models.DateField(auto_now_add=False , auto_now= False , blank= True ,null= True)
    result_date = models.DateField(auto_now_add=False , auto_now= False , blank= True ,null= True)
    corona_result = models.BooleanField(null= True)
    lab_id = models.IntegerField(null=True)
    test_for_corona_diagnosis = models.BooleanField(null= True)
    is_first_Test = models.BooleanField(null= True)

    def __str__(self):
        return str(self.corona_result)


class deaths_no_date(models.Model):
    gender = models.CharField(max_length=200, null=True)
    age_group = models.CharField(max_length=200, null=True)
    Ventilated = models.BooleanField(null= True)
    Time_between_positive_and_hospitalization = models.FloatField(null = True)
    Length_of_hospitalization = models.FloatField(null = True)
    Time_between_positive_and_death = models.FloatField(null = True)

    def __str__(self):
        return str(self.corona_result)


class covid19apidata(models.Model):
    Date = models.DateField(auto_now_add=False, auto_now=False, blank=True, null=True)
    Confirmed = models.IntegerField(null=True)
    Deaths = models.IntegerField(null=True)
    Recovered = models.IntegerField(null=True)
    Active = models.IntegerField(null=True)
    daily_Confirmed = models.IntegerField(null=True)
    daily_Deaths = models.IntegerField(null=True)
    daily_Recovered = models.IntegerField(null=True)
    daily_Active = models.IntegerField(null=True)


    def __str__(self):
        return self.Date.strftime('%Y-%m-%d')

class agg_Alltests(models.Model):
    test_date = models.DateField(auto_now_add=False, auto_now=False, blank=True, null=True)
    total_tests= models.IntegerField(null=True)
    total_pos = models.IntegerField(null=True)


    def __str__(self):
        return self.Date.strftime('%Y-%m-%d')

class agg_PCRTestsSymptoms(models.Model):
    test_date = models.DateField(auto_now_add=False , auto_now= False , blank= True ,null= True)
    alltests = models.IntegerField(null=True)
    withsymptoms = models.IntegerField(null=True)
    allpos = models.IntegerField(null=True)
    poswithwithsymptoms = models.IntegerField(null=True)

    def __str__(self):
        return self.Date.strftime('%Y-%m-%d')
class hospitalization(models.Model):
    date=models.DateField(auto_now_add=False , auto_now= False , blank= True ,null= True)
    total_hospitalised = models.IntegerField(null=True)
    perc_hospitalised_female = models.FloatField(null = True)
    avg_age = models.FloatField(null = True)
    std_div_age = models.FloatField(null = True)
    ventilated = models.IntegerField(null=True)
    perc_female_ventilated = models.FloatField(null = True)
    avg_age_ventilated = models.FloatField(null = True)
    std_div_age_ventilated = models.FloatField(null = True)
    mild = models.IntegerField(null=True)
    perc_mild_female = models.FloatField(null = True)
    avg_age_mild = models.FloatField(null = True)
    std_div_age_mild = models.FloatField(null = True)
    modarate = models.IntegerField(null=True)
    perc_modarate_female = models.FloatField(null = True)
    avg_age_modarate = models.FloatField(null = True)
    std_div_age_modarate = models.FloatField(null = True)
    severe = models.IntegerField(null=True)
    perc_severe_female = models.FloatField(null = True)
    avg_age_severe = models.FloatField(null = True)
    std_div_age_severe = models.FloatField(null = True)
    severe_cumulative = models.IntegerField(null=True)

    def __str__(self):
        return self.date.strftime('%Y-%m-%d')

