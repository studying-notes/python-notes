from selenium import webdriver


def add_attribute(driver, element_obj, attribute, value):
    driver.execute_script(
        "arguments[0].%s=arguments[1]" % attribute, element_obj, value)


def set_attribute(driver, element_obj, attribute, value):
    driver.execute_script(
        "arguments[0].setAttribute(arguments[1], arguments[2])", element_obj, attribute, value)


def get_attribute(element_obj, attribute):
    return element_obj.get_attribute(attribute)


def remove_attribute(driver, element_obj, attribute):
    driver.execute_script(
        "arguments[0].removeAttribute(arguments[1])", element_obj, attribute)


driver = webdriver.Chrome()

driver.get('html/operate.html')
element = driver.find_element_by_xpath('//input')

add_attribute(driver, element, 'name', 'search')
get_attribute(element, 'name')
get_attribute(element, 'value')
set_attribute(driver, element, 'value', '这是更改后的文字')
