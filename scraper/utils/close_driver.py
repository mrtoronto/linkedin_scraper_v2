def close_driver(driver):
    """
    Function will try to close any pages open with Driver.

    Doesn't always work but is never bad to run.

    Args:
        driver - Selenium WebDriver: WebDriver created by Selenium

    """
    try:
        driver.close()
    except:
        pass
    driver.quit()
    
