from django.db import models

class Stock(models.Model):
    symbol = models.CharField(max_length=256, primary_key=True)
    company = models.CharField(max_length=1024)
    cap = models.FloatField()
    recommendation = models.FloatField()
    eps = models.FloatField()
    number = models.IntegerField()
    report_date = models.DateField()
    last_report_date = models.DateField()
    last_eps = models.FloatField()
    time = models.CharField(max_length=256)
    quarter = models.CharField(max_length=256)
    def recommendation_img(self):
        return '<img src="http://www.nasdaq.com/charts/%s_smallrm.jpeg"/>' % self.symbol.lower()
    recommendation_img.allow_tags = True