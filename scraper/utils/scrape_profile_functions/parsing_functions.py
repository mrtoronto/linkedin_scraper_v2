import time, re
from datetime import datetime

def diff_month(end_date, start_date):
    return (end_date.year - start_date.year) * 12 + end_date.month - start_date.month

def parse_years(years):
    len_of_exp = ''

    """print(f'''`years` value : {years}
    `years.strip()` value : {years.strip()}
    `years.split(' - ') valie : {years.split(" - ")}`
    `len(years.split(' - ')[0]) || len(years.strip())` : {len(years.split(' - ')[0])} || {len(years.strip())}''')
    """


    ### One year
    try:
        ### Example: 2018
        if (not re.search('-', years)) and \
        (len(years.strip()) == 4):
            len_of_exp = '<=12'
        ### Example: Aug 2018
        elif (not re.search('-', years)) and \
        (len(years.strip()) == 8):
            len_of_exp = '<=1'
        ### Example 2017 - Aug 2018
        elif (re.search('-', years)) and \
        (len(years.split(' - ')[0].strip()) != len(years.split(' - ')[1].strip())):
            years = years.split(' - ')
            try:
                end_date = datetime.strptime(years[1].strip(), '%Y')
                start_date = datetime.strptime(years[0].strip(), '%b %Y')
            except:
                end_date = datetime.strptime(years[1].strip(), '%b %Y')
                start_date = datetime.strptime(years[0].strip(), '%Y')

            len_of_exp = diff_month(end_date, start_date)

        elif (re.search(' - ', years)) and \
        (len(years.split(' - ')[0].strip()) == len(years.split('-')[1].strip())) and \
        (len(years.split(' - ')[0].strip()) == 4):
            start_year = years.split('-')[0].strip()
            end_year = years.split('-')[1].strip()
            len_of_exp = (int(end_year) - int(start_year)) * 12

        elif (re.search(' - ', years)) and \
        (len(years.split(' - ')[0].strip()) == len(years.split('-')[1].strip())) and \
        (len(years.split(' - ')[0].strip()) == 8):
            years = years.split(' - ')
            end_date = datetime.strptime(years[1].strip(), '%b %Y')
            start_date = datetime.strptime(years[0].strip(), '%b %Y')
            len_of_exp = diff_month(end_date, start_date)
        elif len(years.strip()) == 0:
            pass
        else:
            print(f'Could not parsed the following value for `years` : {years.strip()}')
    except Exception as e:
        print(e)
        print(f'Could not parse this `years` value : {years}')
    return len_of_exp

def experience_reader(driver, item_xpath_base):
    """

    """
    now = datetime.now()
    item_dict = {}
    ### Multi-position experience
    if driver.find_elements_by_xpath(item_xpath_base + '/section/ul'):
        multi_item_flag = 1
        titles = driver.find_elements_by_xpath(item_xpath_base + '/section/ul/li//h3[@class="t-14 t-black t-bold"]')
        titles = [title.text.split('\n')[1] for title in titles]
        expr_title = '|'.join(titles)

        try:
            years = driver.find_element_by_xpath(item_xpath_base + '/section/ul/li//h4[@class="pv-entity__date-range t-14 t-black--light t-normal"]').text
        except:
            years = ''
        expr_company = driver.find_element_by_xpath(item_xpath_base + '//div/h3[@class="t-16 t-black t-bold"]').text
        expr_company = expr_company.split('\n')[1]
    ### Single position experience
    else:
        expr_title = driver.find_element_by_xpath(item_xpath_base + '//h3[@class="t-16 t-black t-bold"]').text

        expr_company = driver.find_element_by_xpath(item_xpath_base + '//p[@class="pv-entity__secondary-title t-14 t-black t-normal"]').text
        try:
            years = driver.find_element_by_xpath(item_xpath_base + '//h4[@class="pv-entity__date-range t-14 t-black--light t-normal"]').text
        except:
            years = ''

    try:
        years = years.split('\n')[1]
    except:
        years = years
    years = re.sub('\u2013', '-', years)
    item_dict['title'] = expr_title
    item_dict['company'] = expr_company
    item_dict['years'] = re.sub('Present', f'{now.strftime("%b %Y")}', years)
    item_dict['len_of_experience'] = parse_years(item_dict['years'])
    return item_dict



def education_reader(driver, item_xpath_base):
    """
    Function extracts relevant data from
    """
    item_dict = {}
    institution, years, degree, len_of_exp = '', '', '', ''
    institution = driver.find_element_by_xpath(item_xpath_base + '//h3').text
    edu_p_list = driver.find_elements_by_xpath(item_xpath_base + '//p')


    try:
        years = driver.find_element_by_xpath(item_xpath_base + '//p[@class="pv-entity__dates t-14 t-black--light t-normal"]').text
    except:
        years = ''
    years = re.sub('\u2013', '-', years)
    try:
        years = years.split('\n')[1]
    except:
        pass
    degree = driver.find_elements_by_xpath(item_xpath_base + '//div[@class="pv-entity__degree-info"]/p/span[@class="pv-entity__comma-item"]')

    degree = ", ".join([item.text for item in degree])

    item_dict['institution']= institution
    item_dict['years'] = years
    item_dict['degree'] = degree
    item_dict['len_of_experience'] = parse_years(item_dict['years'])
    return item_dict


def header_box_parsing(driver, profile_data):
    """
    Function takes in list elements from a profile's header box along with the in-progress
    profile_data dictionary and updates the dictionary to include data from the profile header.

    Args:

    Returns:

    """
    base_xpath = "//div[@class='application-outlet ']//div[@class='ph5 pb5']/div[@class='display-flex mt2']/div[@class='flex-1 mr5']"
    #header_box_elements = driver.find_elements_by_xpath(f"{base_xpath}//ul/li")

    ### Try to grab user's name,
    try:
        profile_data['profile_name'] = driver.find_element_by_xpath(f"{base_xpath}//ul/li[@class='inline t-24 t-black t-normal break-words']").text
    ### If failed, remove the double slash in the XPath and try again.
    except:
        profile_data['profile_name'] = driver.find_element_by_xpath(f"{base_xpath}/ul/li[@class='inline t-24 t-black t-normal break-words']").text

    ### Check if user is a connection
    try:
        conn_degree = driver.find_element_by_xpath(f"{base_xpath}//ul/li/span[@class='distance-badge separator']").text
        profile_data['connection_degree'] = conn_degree.split('\n')[1]
    except: ### If not,
        profile_data['connection_degree'] = 'NA'

    profile_data['profile_location'] = driver.find_element_by_xpath(f"{base_xpath}//ul/li[@class='t-16 t-black t-normal inline-block']").text

    profile_data['profile_n_conn'] = driver.find_element_by_xpath(f"{base_xpath}//ul/li[@class='inline-block']").text.split(' ')[0]

    profile_data['profile_header'] = driver.find_element_by_xpath(f"{base_xpath}//h2").text
    return profile_data
