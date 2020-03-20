from selenium.webdriver.common.action_chains import ActionChains


def click_all_see_more_buttons(driver):
    """
    Scrolls through page and clicks all the "See more" buttons possibly found in Experiences, Education,
    Volunteer Experiences and Licenses & Certifications

    Args:
        driver - Selenium WebDriver: WebDriver created by Selenium
    """
    see_more_button_xpath = "//button[@class='pv-profile-section__see-more-inline pv-profile-section__text-truncate-toggle link link-without-hover-state']"
    show_more_elements = driver.find_elements_by_xpath(see_more_button_xpath)
    for button in show_more_elements:
        actions = ActionChains(driver)
        coordinates = button.location_once_scrolled_into_view # returns dict of X, Y coordinates
        driver.execute_script(f"window.scrollTo({coordinates['x']}, {coordinates['y']});")
        try:
            button.click()
        except:
            pass

def check_for_see_more_buttons(driver):
    """
    Checks webpage currently loaded in `driver` to see if there are still "See more" buttons remaining.

    Args:
        driver - Selenium WebDriver: WebDriver created by Selenium
    Returns:
        Boolean - TRUE/FALSE depending on whether there are more buttons
    """
    see_more_button_xpath = "//section[@class='pv-profile-section pv-profile-section--reorder-enabled background-section artdeco-container-card ember-view']//button[@class='pv-profile-section__see-more-inline pv-profile-section__text-truncate-toggle link link-without-hover-state']"
    show_more_elements = driver.find_elements_by_xpath(see_more_button_xpath)
    if len(show_more_elements) > 0:
        return True
    else:
        return False



def open_read_about_me(driver, profile_data):
    try:
        about_show_more_element = driver.find_element_by_xpath("//a[@id='line-clamp-show-more-button']")

        actions = ActionChains(driver)
        coordinates = about_show_more_element.location_once_scrolled_into_view # returns dict of X, Y coordinates
        driver.execute_script(f"window.scrollTo({coordinates['x']}, {coordinates['y']});")

        about_show_more_element.click()
    except Exception as e:
        pass

    about_me_xpath = "//div[@class='application-outlet ']//div[@class='profile-detail']/div/section/p/span"
    about_me_lines = driver.find_elements_by_xpath(about_me_xpath)
    profile_data['profile_about_me'] = " ".join([line.text for line in about_me_lines])

    return profile_data
