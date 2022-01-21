import unittest
import helpers

class FormYearsTestCase(unittest.TestCase):
    """Tests that get form years returns correct list of years and returns empty list for invalid entries"""
    def test_form_years(self):
        assert helpers.get_form_years_from_year_range("") == []
        assert helpers.get_form_years_from_year_range("1990") == [1990]
        assert helpers.get_form_years_from_year_range("199") == []
        assert helpers.get_form_years_from_year_range("199-199") == []
        assert helpers.get_form_years_from_year_range("1990-1993") == [1990, 1991, 1992, 1993]


class ProductDataTestCase(unittest.TestCase):
    """Tests that product data returns correct dictionary or empty dict for invalid entries"""
    def test_get_product_data(self):
        self.assertFalse(helpers.get_product_data("Form Wxyz"))
        self.assertTrue(helpers.get_product_data("Form W-2"))
        

class ScrapeProductDataTestCase(unittest.TestCase):
    """Tests that scrape prod data returns list of products"""
    def test_scrape_product_data(self):
        self.assertFalse(helpers.scrape_product_data("Form Wxyz"))
        self.assertTrue(helpers.scrape_product_data("Form W-2"))


if __name__ == "__main__":
    unittest.main()