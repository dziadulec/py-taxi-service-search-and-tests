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


