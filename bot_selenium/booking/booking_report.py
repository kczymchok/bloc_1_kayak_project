#this file is going to include methods that will parse
#the specific data that we need for each on of the deal boxes

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd



class BookingReport:

    def __init__(self, boxes_section_element:WebElement, city:str ):
        self.boxes_section_element = boxes_section_element
        self.deal_boxes = self.pull_deal_section()
        self.city = city
        
    
        
    def pull_deal_section(self):
        
        return  self.boxes_section_element.find_elements(By.CSS_SELECTOR,'[data-testid="property-card"]')
        
    def pull_deal_box_attributes(self):

        results = []
        
        for deal_box in self.deal_boxes:
            
            hotel_name=deal_box.find_element(By.CSS_SELECTOR, 
                    '[data-testid="title"]'
            ).get_attribute('innerHTML').strip()

            hotel_prices= deal_box.find_element(By.CSS_SELECTOR, 
                    '[data-testid="price-and-discounted-price"]'
            ).get_attribute('innerHTML').strip()
            
            time.sleep(1)

            try:
            # Explicitly wait for the review score element to be present
                review_score_element = deal_box.find_element(By.CSS_SELECTOR, 'div[data-testid="review-score"]')
                print("Review Score Element HTML:")
                print(review_score_element.get_attribute('innerHTML'))

                score_element = review_score_element.find_element(By.CSS_SELECTOR, "div.c617a39cca")
                score = score_element.get_attribute('innerHTML').strip()

                reviews_element = review_score_element.find_element(By.CSS_SELECTOR, "div.b290e5dfa6.a5cc9f664c.c4b07b6aa8")
                reviews = reviews_element.get_attribute('innerHTML').strip()
            except NoSuchElementException:
                score = "No rating"
                reviews = "No reviews"

            #retrieve the hotel link
            try:
                hotel_link = deal_box.find_element(By.CSS_SELECTOR, 'a[data-testid="title-link"]').get_attribute('href')
            except NoSuchElementException:
                hotel_link = "URL not found"
            

            # # Click on the hotel link
            # try:
            #     deal_box.find_element(By.CSS_SELECTOR, 'a[data-testid="title-link"]').click()
            #     time.sleep(2)  # Adding a delay to ensure the page loads properly, adjust as needed
            #     # Now you can perform operations on the new page if needed
            #     # Example: Switch to new window or handle the new page
            #     # self.switch_to.window(self.window_handles[-1])  # Switch to the new tab

            #     try:
            #         map_link_element = deal_box.find_element(By.ID, 'hotel_address')

            #         latlng = map_link_element.get_attribute('data-atlas-latlng')
            #         print(latlng)

            #     except NoSuchElementException:
            #         latlng = "Latitude and longitude not found"

            #     deal_box.close()  # Close the new tab
            #     deal_box.switch_to.window(self.window_handles[0])  # Switch back to the original tab

            # except NoSuchElementException:
            #     print(f"Failed to click on the URL for {hotel_name}")
            
        


            results.append({
                
                "city": self.city,
                "name": hotel_name,
                "hotel_prices":hotel_prices,
                "rating": score,
                'number of review': reviews,
                "hotel_link": hotel_link,
            
            })
        print(f"Total number of results: {len(results)}")
        results_df=pd.DataFrame(results)
        print(results_df)
        return results_df
