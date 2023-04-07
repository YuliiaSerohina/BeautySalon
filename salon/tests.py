from django.test import TestCase
from salon.period_calculation import convert_time_to_set
from datetime import timedelta, datetime, date, time


class Test(TestCase):
    def test_convert_time_to_set(self):
        date_day = date(2023, 5, 6)
        time_start = time(10, 0)
        time_finish = time(12, 0)
        expected_result = {
            datetime(2023, 5, 6, 10, 0),
            datetime(2023, 5, 6, 10, 15),
            datetime(2023, 5, 6, 10, 30),
            datetime(2023, 5, 6, 10, 45),
            datetime(2023, 5, 6, 11, 0),
            datetime(2023, 5, 6, 11, 15),
            datetime(2023, 5, 6, 11, 30),
            datetime(2023, 5, 6, 11, 45),
            datetime(2023, 5, 6, 12, 0)
        }
        result = convert_time_to_set(date_day, time_start, time_finish)
        self.assertSetEqual(result, expected_result)






