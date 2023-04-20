from django.test import TestCase
from django.test import Client
from salon.models import Services, Specialist, ScheduleSpecialist


class TestPanelEndpoints(TestCase):
    fixtures = ['fixture_base.json']

    def setUp(self):
        client = Client()

    def test_services_add(self):
        self.client.login(username='admin', password='123456')
        response = self.client.post('/panel/services/', {'name': 'haircut', 'time': '30', 'price': '300'})
        self.assertEqual(response.status_code, 200)
        service = Services.objects.filter(name='haircut')
        self.assertEqual(len(service), 1)

    def test_specialist_handler(self):
        self.client.login(username='admin', password='123456')
        service = Services.objects.filter(name="eyebrow trimming")
        for one_service in service:
            idx = one_service.pk
        response = self.client.post(
            f'/panel/specialist/',
            {
                'name': 'Tamara',
                f'services_{idx}': f'{idx}',
                'level': '3',
                'phone': '+380676767670',
                'status': '1'
            }
        )
        self.assertEqual(response.status_code, 200)
        specialist = Specialist.objects.filter(name='Tamara', phone='+380676767670')
        self.assertEqual(len(specialist), 1)

    def test_specialist_id_handler(self):
        self.client.login(username='admin', password='123456')
        specialist = Specialist.objects.filter(name='Katy')
        for one_specialist in specialist:
            idx = one_specialist.pk
        response = self.client.post(f"/panel/specialist/{idx}/",
                               {
                                   'specialist': f"{idx}",
                                   'date': '2023-04-11',
                                   'time_start': '10:00',
                                   'time_finish': '17:00'
                               })
        self.assertEqual(response.status_code, 200)
        schedule_specialist = ScheduleSpecialist.objects.filter(specialist=idx)
        self.assertEqual(len(schedule_specialist), 1)



