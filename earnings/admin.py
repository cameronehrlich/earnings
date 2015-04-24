from django.contrib import admin
from django.db.models import Q
from models import Stock
from datetime import date, timedelta

SUNDAY = 6
SATURDAY = 5

class ReportDateFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'report date'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'report_date'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('Any Date', ''),
            ('-week', 'Last 1 week'),
            ('yesterday', 'Yesterday'),
            ('today', 'Today'),
            ('tomorrow', 'Tomorrow'),
            ('week', 'Next 1 Week'),
            ('month', 'Next 1 Month'),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == '-week':
            return queryset.filter(report_date__gte=date.today() - timedelta(days=7), report_date__lt=date.today())
        if self.value() == 'yesterday':
            d = date.today() - timedelta(days=1)
            while d.weekday() in [SATURDAY, SUNDAY]:
                d -= timedelta(days=1)
            return queryset.filter(report_date=d)
        if self.value() == 'today':
            d = date.today()
            while d.weekday() in [SATURDAY, SUNDAY]:
                d += timedelta(days=1)
            return queryset.filter(report_date=d)
        if self.value() == 'tomorrow':
            d = date.today() + timedelta(days=1)
            while d.weekday() in [SATURDAY, SUNDAY]:
                d += timedelta(days=1)
            return queryset.filter(report_date=d)
        if self.value() == 'week':
            return queryset.filter(report_date__gte=date.today(), report_date__lt=date.today() + timedelta(days=7))
        if self.value() == 'month':
            return queryset.filter(report_date__gte=date.today(), report_date__lt=date.today() + timedelta(days=30))


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'company', 'time', 'report_date', 'quarter', 'recommendation', 'number', 'cap', 'eps', 'last_eps', 'cnb_img', 'surprise_img']
    list_filter = [ReportDateFilter, "recommendation"]
    ordering = ['report_date', '-recommendation', '-number']
    readonly_fields = ('recommendation_img', 'cnb_img', 'surprise_img')
