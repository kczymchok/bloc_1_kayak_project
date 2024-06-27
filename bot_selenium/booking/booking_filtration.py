#this file will includ a class with instance methods
#that wil be responsible to interact wit our website
#after we have some results, to apply filtration
from selenium.webdriver.common.by import By
from typing import List
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
import booking.constants as const
from typing import Type

class BookingFiltration:
    def __init__(self,driver:WebDriver):
        self.driver = driver

    def apply_star_rating(self, *star_values):
        star_filtration_box=self.driver.find_element(By.CSS_SELECTOR,  'div[data-filters-group="class"]')
        star_child_elements= star_filtration_box.find_elements(By.CSS_SELECTOR, '*')
        # print(len(star_child_elements))

        for star_value in star_values:
            for start_element in star_child_elements:
                if str(start_element.get_attribute('innerHTML')).strip() == f'{star_value} stars':
                    start_element.click()

    def apply_property_type(self, property_type_value=204):
        # Locate the property type filtration box
        property_filtration_box = self.driver.find_element(By.CSS_SELECTOR, 'div[data-filters-group="ht_id"]')
        
        # Get all child elements within the property filtration box
        property_child_elements = property_filtration_box.find_elements(By.CSS_SELECTOR, 'div[data-filters-item]')
        # print(len(property_child_elements))
        
        # Iterate over the child elements to find the matching property type
        for property_element in property_child_elements:
            # Check if the property type matches the provided value
            if property_element.get_attribute('data-filters-item') == f'ht_id:ht_id={property_type_value}':
                property_element.click()


    def sort_price_lowest_first(self):
        filtration_element=self.driver.find_element(By.CSS_SELECTOR, '[data-testid="sorters-dropdown-trigger"]' )
        filtration_element.click()
        
        button_low_to_high_prices= self.driver.find_element(By.CSS_SELECTOR, '[data-id="price"]')
        button_low_to_high_prices.click()
