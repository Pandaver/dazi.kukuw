import time
import random
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()


def openPage(url, myTime, errorRate, timeSleep, username, password, desiredWPM):
    global driver
    # 打开网址
    driver.get(url)

    # 登陆
    if username.strip() != '':
        name = driver.find_element_by_id("name")
        name.click()
        newUsername = driver.find_element_by_id("new_username")
        newUsername.send_keys(username)
        driver.find_element_by_link_text("修改").click()
        if password.strip() != '':
            passw = driver.find_element_by_name("pass")
            passw.send_keys(password)
            driver.find_element_by_class_name("login_button").click()
            clickAccept = driver.switch_to.alert
            clickAccept.accept()
    # 随机选择一片文章
    # randomButtom = driver.find_element_by_id('suiji_a')
    # randomButtom.click()

    # 打字时间
    wastTime = driver.find_element_by_id('time')
    wastTime.clear()
    wastTime.send_keys(myTime)
    # 点击打字按钮
    clickTest = driver.find_element_by_name('start_button')
    clickTest.click()
    # 进入打字页面

    for x in range(0, 30):
        divId = 'i_' + str(x)
        # 选中对应序号的一组元素
        dataString = driver.find_element_by_id(divId)
        # 使用空格进行文本分词
        contentList = dataString.text.split(" ")
        # 选中输入框
        inputClick = dataString.find_element_by_class_name('typing')
        # 遍历每个单词
        for y in contentList:
            for a in y:
                # print(random.randint(1,100))
                # 出错
                if random.randint(1, 100) <= errorRate:
                    inputClick.send_keys("+")
                    # time.sleep(speed)
                    inputClick.send_keys(Keys.BACK_SPACE)
                    time.sleep(timeSleep)
                    inputClick.send_keys(a)
                # 正确
                else:
                    inputClick.send_keys(a)
                    time.sleep(timeSleep)

            # 速度调整，使WPM无限贴近desiredWPM
            try:
                wpmText = driver.find_element_by_class_name("sudu").text
            except:
                print()
            else:
                wpm = int(re.findall("\d+", wpmText)[0])
                if wpm > desiredWPM:
                    timeSleep += 0.001
                elif wpm < desiredWPM:
                    timeSleep -= 0.001
            # 词末空格
            inputClick.send_keys(Keys.SPACE)
            time.sleep(timeSleep)
            # print(timeSleep)

def main():
    # 打字网站
    url = "https://dazi.kukuw.com/"
    # 打字时间，单位分钟，请填入整数
    myTime = 1
    # 错误率，百分之五，调低容易被检测
    errorRate = 5
    # 用户名、密码
    # 用户名为空则不登录
    username = "游客133853633"
    # 未设置密码请留空
    password = "abc123"
    # 打字速度，越低越快
    # 打榜建议0.052左右
    timeSleep = 0.0520
    # WPM期望值
    desiredWPM = 799

    openPage(url, myTime, errorRate, timeSleep, username, password, desiredWPM)


if __name__ == '__main__':
    main()

