import time

def sign_in(driver, li_profile):
    """
    Function takes a webdriver object and a LinkedInProfile object and uses
    the credentials from the LinkedInProfile object to log the driver into LinkedIn.

    Args:
        driver - Selenium WebDriver: WebDriver created by Selenium
        li_profile - LinkedInProfile: Object from config file containing LinkedIn account credentials
    Returns:
        None
    """

    driver.get('https://www.linkedin.com')
    driver.find_element_by_xpath("//nav/a[@class='nav__button-secondary']").click()

    time.sleep(2)

    username = driver.find_element_by_xpath("//input[@id='username']")
    password = driver.find_element_by_xpath("//input[@id='password']")

    username.send_keys(li_profile.username)
    password.send_keys(li_profile.password)

    time.sleep(1)

    driver.find_element_by_xpath("//button[@type='submit']").click()
