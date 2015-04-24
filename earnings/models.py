from django.db import models

class Stock(models.Model):
    symbol = models.CharField(max_length=256, primary_key=True)
    company = models.CharField(max_length=1024)
    cap = models.FloatField()
    recommendation = models.FloatField(verbose_name='rcmd')
    eps = models.FloatField()
    number = models.IntegerField(verbose_name='num')
    report_date = models.DateField()
    last_report_date = models.DateField()
    last_eps = models.FloatField()
    time = models.CharField(max_length=256)
    quarter = models.CharField(max_length=256)
    def recommendation_img(self):
        return '<img src="http://www.nasdaq.com/charts/%s_rm.jpeg"/>' % self.symbol.lower()
    recommendation_img.allow_tags = True

    def cnb_img(self):
        return '<a href="http://www.nasdaq.com/symbol/%s/analyst-research"><img src="http://www.nasdaq.com/charts/%s_cnb.jpeg" height="100" /></a>' \
            % (self.symbol.lower(), self.symbol.lower())
    cnb_img.allow_tags = True

    def surprise_img(self):
        return '<img src="http://www.nasdaq.com//charts/%s_sur.jpeg" height="100"/>' % self.symbol
    surprise_img.allow_tags = True
