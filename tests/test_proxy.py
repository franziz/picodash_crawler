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

	assert len(proxy) == 3

def test_browser_proxy(proxy):
	browser = Browser(proxy=proxy)
	browser.get("http://whatismyipaddress.com/")
	
	ip_element = browser.driver.find_element_by_xpath('//*[@id="section_left"]/div[2]/a')
	ip_address = ip_element.text
	
	assert proxy.proxy["ip"] == ip_address