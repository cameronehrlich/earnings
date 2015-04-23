from django.contrib import admin
from django.db.models import Q
from models import Stock
from datetime import date, timedelta
# Register your models here.


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
            ('today', 'Today'),
            ('week', 'One Week'),
            ('month', 'One Month'),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == 'today':
            return queryset.filter(report_date=date.today())
        if self.value() == 'week':
            return queryset.filter(report_date__gte=date.today(), report_date__lt=date.today() + timedelta(days=7))
        if self.value() == 'month':
            return queryset.filter(report_date__gte=date.today(), report_date__lt=date.today() + timedelta(days=30))


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'company', 'recommendation', 'number', 'report_date', 'time']
    list_filter = [ReportDateFilter, "recommendation"]
    ordering = ['report_date', '-recommendation', '-number']
    readonly_fields = ('recommendation_img', )
