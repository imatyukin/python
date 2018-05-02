#!/usr/bin/env python3
import sys
from selenium import webdriver
import time


def main():
    email = sys.argv[1]

    driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
    driver.get("https://mail.google.com/mail/")

    # Enter id
    idElem = driver.find_element_by_id('Email')
    idElem.send_keys('my_id')
    print("Successfully entered id")

    # Click next button
    nextElem = driver.find_element_by_id('next')
    nextElem.click()
    print("Successfully clicked next button")

    # wait for 3 seconds
    time.sleep(3)

    # Enter password
    passwordElem = driver.find_element_by_id('Passwd')
    passwordElem.send_keys('my_password')
    print("Successfully entered password")

    # Click sign in button
    signinElem = driver.find_element_by_id('signIn')
    signinElem.click()
    print("Successfully clicked sign-in button")

    # Click writing email button
    time.sleep(5)
    writeElem = driver.find_element_by_class_name("z0")
    writeElem.click()
    print("Successfully clicked writing button")

    # Write Receiver
    time.sleep(3)
    receiverElem = driver.find_element_by_class_name("eV")
    receiverElem.send_keys(email)
    print("Successfully wrote receiver")

    titleElem = driver.find_element_by_class_name("aoT")
    titleElem.send_keys("This is title")
    print("Successfully wrote title")

    # Write content
    content = driver.find_element_by_id(":md")
    content.send_keys("This is content")
    print("Successfully wrote content")

    # Click send button
    time.sleep(1)
    sendElem =driver.find_element_by_id(":sb")
    sendElem.click()

    driver.close()


if __name__ == "__main__":
    main()
