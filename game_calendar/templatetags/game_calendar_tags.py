from calendar import HTMLCalendar
from django import template
from datetime import datetime, date
from itertools import groupby

from django.utils.html import conditional_escape as esc

register = template.Library()

def do_event_calendar(parser, token):
    """
    template tag's syntax is {% event_calendar year month, event_list %}
    """

    try:
        tag_name, year, month, event_list = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError()
    return EventCalendarNode(year, month, event_list)


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
                    body.append(esc(event.series.primary_name))
                    body.append('</a></li>')
                body.append('</ul>')
                return self.day_cell(cssclass, '<span class="dayNumber">%d</span> %s' % (day, ''.join(body)))
            return self.day_cell(cssclass, '<span class="dayNumberNoEvents">%d</span>' % (day))
        return self.day_cell('noday', '&nbsp;')

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

    def group_by_day(self, events):
        field = lambda event: event.date_and_time.day
        return dict(
            [(day, list(items)) for day, items in groupby(events, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)

# Register the template tag so it is available to the Templates
register.tag("event_calendar", do_event_calendar)

# DOING:0 write HTMLCalendar ovveride functions
