import os
import sys

TEST_DIR   = os.path.abspath(os.path.dirname(__file__))
PARENT_DIR = os.path.join(TEST_DIR, '..')
sys.path.insert(0, PARENT_DIR)

from lib.model.proxy   import Proxy
from lib.model.browser import Browser
import pytest

@pytest.fixture
def proxy():
	return Proxy()

def test_get_proxy(proxy):	
	proxy = proxy.get_proxy()

	assert proxy.ip 	  is not None
	assert proxy.port 	  is not None
	assert proxy.username is not None
	assert proxy.password is not None

def test_browser_proxy(proxy):
	browser = Browser(proxy=proxy)
	browser.get("http://ip.my-proxy.com/")
	browser.driver.save_screenshot("proxy.jpg")
	
	ip_element = browser.driver.find_element_by_xpath('//*[@id="findipinfo"]/div[1]/b')
	ip_address = ip_element.text
	
	assert browser.proxy.ip == ip_address