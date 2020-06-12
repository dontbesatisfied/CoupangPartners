from scrapy.selector import Selector
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pyperclip
from time import sleep
from glob import glob
from PIL import Image
from os import path, getcwd


def merge_images(folder_dir, image_name):
    files = sorted(glob(folder_dir + '/{image_name}'), key=path.getmtime)
    resized_xy = []
    resized_list = []
    max_y = 0
    # 가로를 693으로 고정하고 비율에 맞춰 세로크기 조정
    for file in files:
        image = Image.open(file)
        resized_y = int((693/image.size[0]) * image.size[1])
        max_y += resized_y
        resized_xy.append((693, resized_y))
        resized_list.append(image.resize((693, resized_y)))

    # 합병할 총 사이즈만큼의 도화지(?) 생성
    merged_image = Image.new("RGB", (693, max_y), (256, 256, 256))

    # 합병
    cursor_y = 0
    for i in range(len(resized_xy)):
        area = (0, cursor_y, 693, cursor_y+resized_xy[i][1])
        cursor_y += resized_xy[i][1]
        merged_image.paste(resized_list[i], area)

    saved_path = getcwd()+'/images/total.png'
    merged_image.save(saved_path)

    return saved_path


def read_file(filename):
    with open(filename) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    return [x.strip() for x in content]


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
                    'https:' + vendorItemContentDescription['content'])
            else:
                s = Selector(text=vendorItemContentDescription['content'])
                contents = s.xpath('//img/@src').extract()
    return contents
