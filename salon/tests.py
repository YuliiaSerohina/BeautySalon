from django.test import TestCase
from datetime import timedelta, datetime, date, time
from salon.period_calculation import convert_time_to_set
from salon.period_calculation import calc_free_time_for_test


class TestPeriodCalculation(TestCase):
    def test_convert_time_to_set(self):
        date_day = date(2023, 5, 6)
        time_start = time(10, 0)
        time_finish = time(12, 0)
        date_time_start = datetime.combine(date_day, time_start)
        date_time_finish = datetime.combine(date_day, time_finish)
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
        result = convert_time_to_set(date_time_start, date_time_finish)
        self.assertSetEqual(result, expected_result)

    def test_convert_time_to_set2(self):
        date_day = date(2023, 5, 6)
        time_start = time(10, 0)
        time_finish = time(12, 0)
        date_time_start = datetime.combine(date_day, time_start)
        date_time_finish = datetime.combine(date_day, time_finish)
        expected_result = set()
        result = convert_time_to_set(date_time_finish, date_time_start)
        self.assertSetEqual(result, expected_result)

    def test_convert_time_to_set3(self):
        date_day = date(2023, 5, 6)
        time_start = time(10, 0)
        time_finish = time(10, 0)
        date_time_start = datetime.combine(date_day, time_start)
        date_time_finish = datetime.combine(date_day, time_finish)
        expected_result = {datetime(2023, 5, 6, 10, 0)}
        result = convert_time_to_set(date_time_finish, date_time_start)
        self.assertSetEqual(result, expected_result)

    def test_calc_free_time(self):
        bookings = [{'date': datetime(2023, 4, 9, 10, 0), 'service_time': 30}]
        service_time = 30
        date_day_time_start = datetime(2023, 4, 9, 10, 0)
        date_day_time_finish = datetime(2023, 4, 9, 11, 0)
        result = calc_free_time_for_test(bookings, date_day_time_start, date_day_time_finish, service_time)
        expected_result = [
            datetime(2023, 4, 9, 10, 30),
        ]
        self.assertListEqual(result, expected_result)

    def test_calc_free_time2(self):
        bookings = [{'date': datetime(2023, 4, 9, 10, 0), 'service_time': 30}]
        service_time = 30
        date_day_time_start = datetime(2023, 4, 9, 10, 0)
        date_day_time_finish = datetime(2023, 4, 9, 12, 0)
        result = calc_free_time_for_test(bookings, date_day_time_start, date_day_time_finish, service_time)
        expected_result = [
            datetime(2023, 4, 9, 10, 30),
            datetime(2023, 4, 9, 10, 45),
            datetime(2023, 4, 9, 11, 0),
            datetime(2023, 4, 9, 11, 15),
            datetime(2023, 4, 9, 11, 30)
        ]
        self.assertListEqual(result, expected_result)

    def test_calc_free_time3(self):
        bookings = [
            {'date': datetime(2023, 4, 9, 10, 0), 'service_time': 30},
            {'date': datetime(2023, 4, 9, 12, 0), 'service_time': 30}
        ]
        service_time = 30
        date_day_time_start = datetime(2023, 4, 9, 10, 0)
        date_day_time_finish = datetime(2023, 4, 9, 13, 0)
        result = calc_free_time_for_test(bookings, date_day_time_start, date_day_time_finish, service_time)
        expected_result = [
            datetime(2023, 4, 9, 10, 30),
            datetime(2023, 4, 9, 10, 45),
            datetime(2023, 4, 9, 11, 0),
            datetime(2023, 4, 9, 11, 15),
            datetime(2023, 4, 9, 11, 30),
            datetime(2023, 4, 9, 12, 30)
        ]
        self.assertListEqual(result, expected_result)

    def test_calc_free_time4(self):
        bookings = [
            {'date': datetime(2023, 4, 9, 10, 0), 'service_time': 30},
            {'date': datetime(2023, 4, 9, 12, 0), 'service_time': 30},
            {'date': datetime(2023, 4, 9, 12, 30), 'service_time': 15}
        ]
        service_time = 30
        date_day_time_start = datetime(2023, 4, 9, 10, 0)
        date_day_time_finish = datetime(2023, 4, 9, 14, 0)
        result = calc_free_time_for_test(bookings, date_day_time_start, date_day_time_finish, service_time)
        expected_result = [
            datetime(2023, 4, 9, 10, 30),
            datetime(2023, 4, 9, 10, 45),
            datetime(2023, 4, 9, 11, 0),
            datetime(2023, 4, 9, 11, 15),
            datetime(2023, 4, 9, 11, 30),
            datetime(2023, 4, 9, 12, 45),
            datetime(2023, 4, 9, 13, 0),
            datetime(2023, 4, 9, 13, 15),
            datetime(2023, 4, 9, 13, 30)
        ]
        self.assertListEqual(result, expected_result)

    def test_calc_free_time5(self):
        bookings = [
            {'date': datetime(2023, 4, 9, 10, 0), 'service_time': 30},
            {'date': datetime(2023, 4, 9, 12, 0), 'service_time': 30},
            {'date': datetime(2023, 4, 9, 12, 30), 'service_time': 15}
        ]
        service_time = 30
        date_day_time_start = datetime(2023, 4, 9, 10, 0)
        date_day_time_finish = datetime(2023, 4, 9, 13, 1)
        result = calc_free_time_for_test(bookings, date_day_time_start, date_day_time_finish, service_time)
        expected_result = [
            datetime(2023, 4, 9, 10, 30),
            datetime(2023, 4, 9, 10, 45),
            datetime(2023, 4, 9, 11, 0),
            datetime(2023, 4, 9, 11, 15),
            datetime(2023, 4, 9, 11, 30)
        ]
        self.assertListEqual(result, expected_result)
