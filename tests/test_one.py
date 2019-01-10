from selenium import webdriver
from selenium.webdriver import FirefoxOptions

def test_facebook_on():
    capabilities = FirefoxOptions()
    desired_caps = capabilities.to_capabilities()
    desired_caps['enableVNC'] = True

    driver = webdriver.Remote(
    command_executor="http://selenoid:4444/wd/hub",
    desired_capabilities=desired_caps)

    driver.get("https://www.facebook.com")
    driver.quit()