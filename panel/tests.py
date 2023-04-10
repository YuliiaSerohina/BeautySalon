from django.test import TestCase
from django.test import Client
from salon.models import Services, Specialist, ScheduleSpecialist


class TestPanelEndpoints(TestCase):

    def test_services_add(self):
        client = Client()
        response = client.post('/panel/services/', {'name': 'haircut', 'time': '30', 'price': '300'})
        self.assertEqual(response.status_code, 200)
        service = Services.objects.filter(name='haircut')
        self.assertEqual(len(service), 1)

    def test_specialist_handler(self):
        client = Client()
        service = Services(name='haircut', time=30, price=300)
        service.save()
        response = client.post(
            f'/panel/specialist/',
            {
                'name': 'Tamara',
                f'services_{service.pk}': f'{service.pk}',
                'level': '3',
                'phone': '+380676767670',
                'status': '1'
            }
        )
        self.assertEqual(response.status_code, 200)
        specialist = Specialist.objects.filter(name='Tamara')
        self.assertEqual(len(specialist), 1)

    def test_specialist_id_handler(self):
        service = Services(name='haircut', time=30, price=300)
        service.save()
        specialist = Specialist(name='Tamara', level=3, phone='+380676767670', status=1)
        specialist.save()
        specialist.services.add(service)
        specialist.save()
        client = Client()
        response = client.post(f"/panel/specialist/{specialist.pk}/",
                               {
                                   'specialist': f"{specialist.pk}",
                                   'date': '2023-04-11',
                                   'time_start': '10:00',
                                   'time_finish': '17:00'
                               })
        self.assertEqual(response.status_code, 200)
        schedule_specialist = ScheduleSpecialist.objects.filter(specialist=specialist)
        self.assertEqual(len(schedule_specialist), 1)



