from utils.scrape_profile_functions.interaction_functions import *
from utils.scrape_profile_functions.parsing_functions import *
import re, time, json
from datetime import datetime

def scrape_profile(driver, profile_url):
    """
    Function will use the provided driver and URL to scrape data from a LinkedIn page. Random notes below:

        - Program essentially goes in the order of the content on the page.
        - There are lots of hardcoded class names and ids here so there's a large chance something eventually breaks.
        - In headless mode, the section which expands the "about me" section and the experiences data collection does not work.
            - Neither are problems while running non-headless.
        - Right now function only gets data from Experiences and Education and skips Volunteer Experiences and Licenceses
            but this only happens because I'm lazy

    Args:
        driver - Selenium WebDriver: WebDriver created by Selenium
        profile_url - Str: URL of profile to scrape data from
    Returns:
        profile_data - Dict: Data from the profile...
    """

    ### Skip companies for now
    if re.search('company', profile_url):
        return {}

    ### Prevents chat from blocking anything
    driver.maximize_window()

    profile_data = {}
    now = datetime.now()

    try:
        driver.get(profile_url)
    except:
        print(f'Failed to get URL in `scrape_profile()`: {profile_url}\nReturning NA.')
        return {}
    ### Extract data from header box
    profile_data = header_box_parsing(driver, profile_data)
    ### Expand and read 'About Me' section
    profile_data = open_read_about_me(driver, profile_data)

    ### Check for 'See More' buttons under Work Experience sections and
    ### click them until there are no more buttons to click
    while check_for_see_more_buttons(driver):
        click_all_see_more_buttons(driver)
    print(f'Buttons clicked for URL : {profile_url}')
    ### XPath to container with work experience sections
    work_exp_xpath = '//section[@class="pv-profile-section pv-profile-section--reorder-enabled background-section artdeco-container-card ember-view"]'
    experience_dict = {}
    education_dict = {}
    #lic_certif_dict = {}
    #volunteer_dict = {}

    for section_index, section in enumerate(driver.find_elements_by_xpath(work_exp_xpath + '/div')):
        ### Grab the title of the section
        section_title = driver.find_elements_by_xpath(work_exp_xpath + '/div/section/header')[section_index].text
        ### Grab the section's "ember ID" to use in later XPaths
        section_id = driver.find_elements_by_xpath(work_exp_xpath + '/div/section')[section_index].get_attribute('id')
        ### Grab the items in the section and their IDs
        section_items = driver.find_elements_by_xpath(work_exp_xpath + f'/div/section[@id="{section_id}"]/ul/li')
        item_ids = [item.get_attribute('id') for item in section_items]

        print(f'Section : {section_title} starting items for URL : {profile_url}')

        for item_index, item_id in enumerate(item_ids):
            print(f'Item : {item_id} starting item for URL : {profile_url}')
            item_xpath_base = work_exp_xpath + f'/div/section[@id="{section_id}"]/ul/li[@id="{item_id}"]'
            if section_title == 'Experience':
                ### Extract experience data
                item_dict = experience_reader(driver, item_xpath_base)
                experience_dict[item_id] = item_dict

            if section_title == 'Education':
                ### Extract education data
                item_dict = education_reader(driver, item_xpath_base)
                education_dict[item_id] = item_dict
                
    profile_data['experience'] = experience_dict
    profile_data['education'] = education_dict

    return profile_data
