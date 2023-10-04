from datetime import datetime, timedelta, timezone
import pytz

class DateHelper:
    @staticmethod
    def now():
        today = datetime.now(timezone.utc)
        timezone_offset = today.utcoffset().seconds / 3600 if today.utcoffset() else 0
        today -= timedelta(hours=timezone_offset)
        return today

    @staticmethod
    def UTCKTime():
        today = DateHelper.now()
        parsed_date = today.strftime('%A, %Y %B %d')
        parsed_time = today.strftime('%H:%M:%S')
        return (parsed_date, parsed_time)

    @staticmethod
    def windowTime():
        today = DateHelper.now()
        #! 여기 하나 부족함 -> 여기 time_def.py 수정해야함
        parsed_date = today.strftime('%Y-%m-%d')
        parsed_time = today.strftime('%H:%M')
        return (parsed_time, parsed_date)

    @staticmethod
    def fileName(includeTime=True):
        today = DateHelper.now()
        date = today.strftime('%Y-%m-%d')
        time = today.strftime('%H%M%S')
        return f"{date}_{time}" if includeTime else date