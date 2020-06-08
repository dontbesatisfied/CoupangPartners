from scrapy.selector import Selector
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pyperclip
from time import sleep


# 클립보드에 input을 복사한 뒤
# 해당 내용을 actionChain을 이용해 로그인 폼에 붙여넣기
def copy_input(driver, xpath, input):
    pyperclip.copy(input)
    driver.find_element_by_xpath(xpath).click()
    # 클립보드 내용 붙여넣기
    ActionChains(driver).key_down(Keys.CONTROL).send_keys(
        'v').key_up(Keys.CONTROL).perform()
    is_control_key = driver.find_element_by_xpath(
        xpath).get_attribute('value')

    if is_not_blank(is_control_key):
        pass
    else:
        # 클립보드 내용 붙여넣기
        ActionChains(driver).key_down(Keys.COMMAND).send_keys(
            'v').key_up(Keys.COMMAND).perform()

    return sleep(1)


def is_not_blank(input):
    return bool(input and input.strip())


def parse_detail_content(details=list):
    contents = []
    for detail in details:
        for vendorItemContentDescription in detail['vendorItemContentDescriptions']:
            if vendorItemContentDescription['imageType']:
                contents.append(
                    'https://' + vendorItemContentDescription['content'])
            else:
                s = Selector(text=vendorItemContentDescription['content'])
                contents = s.xpath('//img/@src').extract()
    return contents
