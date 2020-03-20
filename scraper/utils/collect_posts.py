from utils.collect_posts_functions.parse_post import *
import re, time, json, tqdm

def collect_posts(driver, profile_url, n_pages = 2,
                  profile_details = False):
    """
    Function scans a profile's recent activity and records profiles, posts and links from the recent posts

    """
    posts_dict = {}

    driver.get(profile_url + 'detail/recent-activity')

    search_xpath = "//div[@id='voyager-feed']/div"
    post_index = 0
    for page in range(n_pages):
        time.sleep(3)

        ### Get elements then IDs of items in the current feed
        feed_elements = driver.find_elements_by_xpath(search_xpath)
        feed_ids = [item.get_attribute('id') for item in feed_elements]
        ### Restrict list to unseen items
        feed_ids = feed_ids[post_index:]

        for post_id in feed_ids:
            ### Check if `post_id` is a valid element
            post_test_class = driver.find_elements_by_xpath(search_xpath[:-4] + f'/div[@id="{post_id}"]//div')
            if len(post_test_class) <= 1:
                ### If its not, sleep for a few seconds so the page finishes loads
                ### then skip the element
                time.sleep(3)
                continue
            post_dict = parse_post(driver, post_id, search_xpath, '7')

            posts_dict[post_id] = post_dict
            post_index += 1

    if profile_details == True:
        output_dict = posts_dict.copy()
        for (key, post_dict) in tqdm(posts_dict.items(), total=len(posts_dict.items())):

            post_dict['profile_link'] = post_dict['profile_link'].split('?')[0]
            print(post_dict['profile_link'])

            details_dict = scrape_profile(driver, post_dict['profile_link'])

            post_dict['profile_details'] = details_dict
            output_dict[key] = post_dict

    return posts_dict
