""" Python script to test the WordPress profile page """

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)


def test_login():
    """ Test if login to profile page works """
    browser.get('https://wordpress.com/me')
    user_textbox = wait.until(EC.visibility_of_element_located((By.ID, "usernameOrEmail")))
    assert user_textbox.is_enabled(), "User textbox was not enabled in a timely manner."
    user_textbox.send_keys("tomaigner@gmail.com", Keys.ENTER)
    password_textbox = wait.until(EC.visibility_of_element_located((By.ID, "password")))
    assert password_textbox.is_enabled(), "Password textbox was not enabled in a timely manner."
    password_textbox.send_keys("Testing123!", Keys.ENTER)
    try:
        logged_in = wait.until(EC.url_matches("https://wordpress.com/me"))
    except TimeoutException:
        logged_in = False
    assert logged_in is True, "Profile page failed to load."


def test_learn_more():
    """ Test that support page loads correctly"""
    learn_more = browser.find_element(By.CSS_SELECTOR, ".inline-support-link__nowrap")
    learn_more.click()
    try:
        support_url = wait.until(EC.url_contains("support-article"))
    except TimeoutException:
        support_url = False
    assert support_url is True, "Profile support page didn't display."
    close = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, ".support-article-dialog__base > .button:nth-child(1)")))
    close.click()
    try:
        profile_page = wait.until(EC.url_matches("https://wordpress.com/me"))
    except TimeoutException:
        profile_page = False
    assert profile_page is True, "Profile page failed to load."


def test_public_display_name():
    """ Test that public display name changes when textbox is changed """
    display_name_textbox = browser.find_element(By.NAME, "display_name")
    display_name_display = browser.find_element(By.CSS_SELECTOR,
                                                ".profile-gravatar__user-display-name")
    assert display_name_display.text == display_name_textbox.get_attribute("value"), \
        "Display names don't match."
    name = "TheAutomator"
    if display_name_textbox.get_attribute("value") == name:
        name = "TheMarketingAutomator"
    display_name_textbox.clear()
    display_name_textbox.send_keys(name, Keys.ENTER)
    success_button = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, ".notice__dismiss > .gridicon")))
    success_button.click()
    assert display_name_display.text == name, "Display name didn't change."


def add_profile_link():
    """ Helper method to add profile link """
    add_button = browser.find_element(By.CSS_SELECTOR, ".section-header__actions > .button")
    add_button.click()
    add_url = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, ".popover__menu-item:nth-child(2)")))
    add_url.click()
    url_textbox = wait.until(EC.visibility_of_element_located((By.NAME, "value")))
    url_textbox.send_keys("https://www.aweber.com")
    description_textbox = wait.until(EC.visibility_of_element_located((By.NAME, "title")))
    description_textbox.send_keys("powerfully-simple email marketing software")
    add_site = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, ".profile-links-add-other__add")))
    add_site.click()


def test_add_profile_link():
    """ Test that profile link is added and can be clicked to load new tab from the link"""
    add_profile_link()
    wordpress_window = browser.current_window_handle
    aweber_link = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, ".profile-link__url")))
    aweber_link.click()
    while True:
        window_handles = browser.window_handles
        if len(window_handles) > 1:
            break
    for window_handle in window_handles:
        if wordpress_window != window_handle:
            browser.switch_to.window(window_handle)
    try:
        aweber = wait.until(EC.url_contains("aweber"))
    except TimeoutException:
        aweber = False
    assert aweber is True, "Profile page failed to load."
    browser.close()
    browser.switch_to.window(wordpress_window)


def test_add_duplicate_profile_link():
    """ Test to check if duplicate link message is displayed correctly """
    add_profile_link()
    notice = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".notice__text")))
    assert notice.text == "That link is already in your profile links. No changes were made.", \
        "Duplicate error not displayed correctly."
    notice_close = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, ".notice__dismiss use")))
    notice_close.click()
    try:
        notice = browser.find_element(By.CSS_SELECTOR, ".notice__text")
        assert notice.is_displayed() is False, "Duplicate notice not deleted correctly."
    except NoSuchElementException:
        pass


def test_delete_profile_link():
    """ Test to check if a link can be deleted """
    browser.find_element(By.CSS_SELECTOR, ".profile-link__url")
    link_close = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, ".profile-link__remove > .gridicon")))
    link_close.click()
    sleep(1)
    try:
        aweber_link = browser.find_element(By.CSS_SELECTOR, ".profile-link__url")
        assert aweber_link.is_displayed() is False, "AWeber link not deleted correctly"
    except NoSuchElementException:
        pass
