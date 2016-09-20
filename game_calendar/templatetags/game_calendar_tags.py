from calendar import HTMLCalendar
from django import template
from datetime import datetime, date
from itertools import groupby
from django.middleware import locale as _locale
#from django.conf.urls import url

from django.utils.html import conditional_escape as esc

register = template.Library()
month_names = ['', 'January', 'Feburary', 'March', 'April', 'May', 'June', 'July',
'August', 'September', 'October', 'November', 'December']

def do_event_calendar(parser, token):
    """
    template tag's syntax is {% event_calendar year month, event_list %}
    """
    try:
        tag_name, year, month, events_list = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError()
    return EventCalendarNode(year, month, events_list)


class EventCalendarNode(template.Node):
    """
    Process a particular node in the template.
    """

    def __init__(self, year, month, event_list):
        try:
            self.event_list = template.Variable(event_list)
            self.year = template.Variable(year)
            self.month = template.Variable(month)
        except ValueError:
            raise template.TemplateSyntaxError

    def render(self, context):
        try:
            # Get the variable from the context so the method is thread-safe.
            my_event_list = self.event_list.resolve(context)
            my_year = self.year.resolve(context)
            my_month = self.month.resolve(context)
            cal = EventCalendar(my_event_list)
            return cal.formatmonth(int(my_year), int(my_month))
        except ValueError:
            return
        except template.VariableDoesNotExist:
            return

class EventCalendar(HTMLCalendar):
    """
    Overload Python's calender.HTMLCalendar to add the appropriate events to
    each day's table cell.
    """

    def __init__(self, events):
        super(EventCalendar, self).__init__()
        self.events = self.group_by_day(events)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.events:
                cssclass += ' filled'
                body = ['<ul>']
                for event in self.events[day]:
                    body.append('<li>')
                    body.append('<a href="%s">' % event.get_absolute_url())
                    body.append((event.title))
                    body.append('</a></li>')
                body.append('</ul>')
                return self.day_cell(cssclass, '<span class="dayNumber">%d</span> %s' % (day, ''.join(body)))
            return self.day_cell(cssclass, '<span class="dayNumberNoEvents">%d</span>' % (day))
        return self.day_cell('noday', '&nbsp;')

    # TODO:10 Make in-calendar link better.

    def formatmonthname(self, year, month, withyear=True):
        """
        Return a month name as a table row.
        """
        self.year, self.month = year, month
        if withyear:
            s = '%s %s' % (month_names[self.month], self.year)
        else:
            s = '%s' % month_names[self.month]
        return '<tr><th colspan="7" class="monthname text-center">%s</th></tr>' % s

    def formatmonth(self, year, month):
        """
        Return a formatted month as a table.
        """
        self.year, self.month = year, month
        v = []
        a = v.append
        a('<table class="table table-bordered">')
        a('\n')
        a(self.formatmonthname(self.year, self.month, withyear=True))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(self.year, self.month):
            a(self.formatweek(week))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)

        # DONE:40 add navigation links to previous and next month in the calendar.

    def group_by_day(self, events):
        field = lambda event: event.date_and_time.day
        return dict(
            [(day, list(items)) for day, items in groupby(events, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)

# Register the template tag so it is available to the Templates
register.tag("event_calendar", do_event_calendar)

# DONE:60 write HTMLCalendar ovveride functions
