from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from config import LinkedInProfile
from datetime import datetime
import re, time, json

from utils.linkedin_sign_in import sign_in
from utils.scrape_profile import scrape_profile
from utils.collect_posts import collect_posts
from utils.close_driver import close_driver




def datetime_handler(x):
    if isinstance(x, datetime):
        return x.isoformat()
    raise TypeError(f"Unknown type : {x}")

def main():
    
    n_pages = 50
    export_path = 'output/test_prof_3.json'
    li_profile = LinkedInProfile()
    ### Checks if you have a driver open, if not, makes it == ''
    driver = webdriver.Firefox()

    driver = webdriver.Firefox()
    ### Sign it into LinkedIn
    sign_in(driver, li_profile)

    ### Scrape a specific profile
    return_dict = scrape_profile(driver, profile_url)
    """
    ### Collect posts from a specific user's activity
    return_dict = collect_posts(driver, profile_url, n_pages, \
                        profile_details = True)

                        """
    close_driver(driver)

    if export_path:
        with open(export_path, 'w') as f:
            json.dump(return_dict, f, default=datetime_handler, indent=4)

if __name__ == "__main__":
    main()
