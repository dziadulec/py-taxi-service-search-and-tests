from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car
from django.db.utils import IntegrityError

# ---------------------------------------------------------
# MODEL TESTS
# ---------------------------------------------------------

class ModelsTest(TestCase):

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="Dacia", country="Romania")
        self.assertEqual(str(manufacturer), "Dacia Romania")

    def test_manufacturer_meta(self):
        self.assertEqual(Manufacturer._meta.ordering, ["name"])

    def test_Car_str(self):
        manufacturer = Manufacturer.objects.create(name="Dacia", country="Romania")
        car = Car.objects.create(model="Duster", manufacturer=manufacturer)
        self.assertEqual(str(car), "Duster")

    def test_driver_str(self):
        driver = Driver.objects.create(
            username="Marianos",
            last_name="Dziad",
            first_name="Marek"
        )
        self.assertEqual(str(driver), "Marianos (Marek Dziad)")

    def test_driver_meta(self):
        self.assertEqual(Driver._meta.verbose_name, "driver")
        self.assertEqual(Driver._meta.verbose_name_plural, "drivers")

    def test_driver_get_absolute_url(self):
        driver = Driver.objects.create(
            username="Marianos",
        )
        expected_url = reverse("taxi:driver-detail", kwargs={"pk": driver.pk})
        self.assertEqual(driver.get_absolute_url(), expected_url)


    def test_driver_license_number_is_unique_false(self):

        driver_one = Driver.objects.create(
            username="Sariano",
            last_name="Dziad",
            first_name="Marek",
            license_number="ABC12347"
        )

        with self.assertRaises(IntegrityError):(
            Driver.objects.create(
            username="Mariano",
            last_name="Dziad",
            first_name="Marek",
            license_number="ABC12347"
            )
        )

# ---------------------------------------------------------
# VIEVs TESTS
# ---------------------------------------------------------


class IndexViewTests(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="testuser",
            password="test12345"
        )


    def test_Index_logout(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 302)


    def test_Index_login(self):
        self.client.login(username="testuser", password="test12345")
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)


    def test_index_context(self):
        self.client.login(username="testuser", password="test12345")

        manufacturer =  Manufacturer.objects.create(name="Dacia", country="Romania")
        Car.objects.create(model="Duster", manufacturer=manufacturer)
        response = self.client.get(reverse("taxi:index"))

        self.assertEqual(response.context["num_drivers"],12)
        self.assertEqual(response.context["num_cars"], 17)
        self.assertEqual(response.context["num_manufacturers"], 15)
