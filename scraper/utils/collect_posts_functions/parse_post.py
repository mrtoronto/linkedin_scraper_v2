from selenium.webdriver.common.action_chains import ActionChains
from utils.scrape_profile import scrape_profile

from datetime import datetime

def parse_post(driver, post_id, search_xpath, scroll_px):
    post_dict = {}

    ### XPaths for interesting sections
    profile_xpath = f'/div[@id="{post_id}"]//div[@class="display-flex feed-shared-actor display-flex ember-view"]/a'
    post_xpath = f'/div[@id="{post_id}"]//div[@class="feed-shared-update-v2__description-wrapper ember-view"]//span[@class="ember-view"]'
    article_xpath = f'/div[@id="{post_id}"]//article//a'

    ### Grab original poster's profile link
    try:
        post_dict['profile_link'] = driver.find_element_by_xpath(search_xpath[:-4] + profile_xpath).get_attribute('href')
    except:
        ### If you fail the first time, try a different XPath
        alt_profile_xpath = f'/div[@id="{post_id}"]/div[@class="display-flex feed-shared-actor display-flex ember-view"]/a'
        print(f'Used alternative profile XPath for {post_id}')
        try:
            post_dict['profile_link'] = driver.find_element_by_xpath(search_xpath[:-4] + alt_profile_xpath).get_attribute('href')
        except:
            post_dict['profile_link'] = ''


    try:
        post_dict['post_time'] = driver.find_element_by_xpath(search_xpath[:-4] + profile_xpath + '//span[@aria-hidden="true"]').text
        post_dict['post_time'] = post_dict['post_time'].split('•')[0].strip()
    except:
        post_dict['post_time'] = ''

    try:
        body = driver.find_element_by_xpath(search_xpath[:-4] + post_xpath).text
        body = re.sub('[ \n\s]+', ' ', body)
        post_dict['post_body'] = re.sub('(\\nhashtag\\n)', '', body)
    except:
        post_dict['post_body'] = ''
    try:
        post_dict['post_link'] = driver.find_element_by_xpath(search_xpath[:-4] + article_xpath).get_attribute('href')
    except:
        post_dict['post_link'] = ''

    ### Scroll page down `scroll_px` pixels
    actions = ActionChains(driver)
    coordinates = driver.find_element_by_xpath(search_xpath[:-4] + f'/div[@id="{post_id}"]').location_once_scrolled_into_view # returns dict of X, Y coordinates
    driver.execute_script(f"window.scrollBy(0, -{scroll_px});")

    post_dict['current_date'] = datetime.now().strftime("%m/%d/%Y")

    return post_dict
