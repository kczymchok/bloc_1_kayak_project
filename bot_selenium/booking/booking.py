from types import TracebackType
from typing import Type
from selenium import webdriver
import booking.constants as const
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from booking.booking_filtration import BookingFiltration
import time
from booking.booking_report import BookingReport
import pandas as pd


class Booking(webdriver.Firefox):
    def __init__(self, driver_path="/usr/local/bin/geckodriver", teardown=False):
        self.driver_path= driver_path
        self.teardown=teardown
        os.environ['PATH'] += self.driver_path
        super(Booking, self).__init__()
        self.implicitly_wait(30)
        self.maximize_window()
        self.wait = WebDriverWait(self, 100)
    
    def __exit__(self, exc_type: type[BaseException] | None, exc: BaseException | None, traceback: TracebackType | None):
        if self.teardown:
            self.quit()
    
    def land_first_page(self):
        self.get(const.BASE_URL)

    def close_signin_booking(self):
        wait = WebDriverWait(self, 10)
        try:
            # Locate the dismiss button using the aria-label attribute
            close_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Dismiss sign-in info.']"))
            )
            close_button.click()
        except TimeoutException:
            print("Timed out waiting for the sign-in dismiss button to be clickable.")

    # def close_ggle_signin(self): NOT WORKING
    #     # close_button=self.find_element(By.ID, "close")
    #     # close_button.click()
    #     try:
    #         # Wait for the close button to be clickable
    #         close_button = WebDriverWait(self, 10).until(
    #             EC.element_to_be_clickable((By.ID, "close"))
    #         )
    #         close_button.click()
    #     except TimeoutException:
    #         print("Timed out waiting for the close button to be clickable.")
    
    # def change_currency(self, currency=None): #can not find
    #     currency_element=self.find_element(By.CSS_SELECTOR, 'button[data-testid="header-currency-picker-trigger"]' 
                          
    #                       )
        
    #     currency_element.click()

    #     selected_currency_element = self.find_element(By.CSS_SELECTOR, )
    
    def select_city(self, place_to_go):
        search_field = self.find_element(By.NAME, "ss")
        search_field.clear()
        search_field.send_keys(place_to_go)

         # Define a WebDriverWait instance
        wait = WebDriverWait(self, 10)
        
        try:
            # Wait until the autocomplete result contains the desired city name
            first_result = wait.until(
                EC.text_to_be_present_in_element(
                    (By.ID, "autocomplete-result-0"), place_to_go
                )
            )
            # Click on the first result after it contains the desired city name
            self.find_element(By.ID, "autocomplete-result-0").click()
        except TimeoutException:
            print(f"Timed out waiting for autocomplete result to contain '{place_to_go}'.")


    def select_date(self, check_in_date, check_out_date):
        check_in_element = self.find_element(By.CSS_SELECTOR, f"span[data-date='{check_in_date}']" )
        check_in_element.click()

        check_out_element = self.find_element(By.CSS_SELECTOR, f"span[data-date='{check_out_date}']" )
        check_out_element.click()

    
    def select_number_occupancy(self,count=1):
        selection_element= self.find_element(By.CSS_SELECTOR, '[data-testid="occupancy-config"]')
        selection_element.click()

        while True:
            decrease_adults_element=self.find_element(By.CSS_SELECTOR, 'button.bf33709ee1.becc918b37')
            decrease_adults_element.click()
            #if the value of adults reach one we should get out
            adults_value_element= self.find_element(By.ID, 'group_adults')
            adults_value= adults_value_element.get_attribute(
                'value'
            ) #should give back the adult count

            if int(adults_value) ==1:
                break
        
        increase_button_element = self.find_element(By.CSS_SELECTOR, 'button.bf33709ee1.f22ffed92e')

        for i in range(count -1):
            increase_button_element.click()

    def click_search(self):
        search_button=self.find_element(
            By.CSS_SELECTOR, "button[type='submit']"

        )
        search_button.click()
    
    def apply_filtration(self):

        filtration = BookingFiltration(driver=self)
        filtration.apply_star_rating(3,4,5)
        time.sleep(5)
        filtration.apply_property_type()
        time.sleep(5)
        filtration.sort_price_lowest_first()
        time.sleep(5)


    def report_resutls(self):
        city_element = self.find_element(By.CSS_SELECTOR, 'input[name="ss"]')
        city = city_element.get_attribute('value')

        hotel_container =self.find_element(By.CLASS_NAME, "fb4e9b097f")
        report=BookingReport(hotel_container,city)

        # print(report.pull_deal_box_attributes())

        results_df = report.pull_deal_box_attributes()
        results_df=pd.DataFrame(results_df)
        csv_file_path = f'/Users/kechok/Documents/kayak_project/bot/data/each_city/{city}_hotel_deals.csv'

        # Save the DataFrame to a CSV file
        results_df.to_csv(csv_file_path, index=False)

        print(f"Data saved to {csv_file_path}")

        return results_df
    





