from scrapy import Selector
import requests
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logging.disable(logging.INFO)


class ExtractDetail():

	def __init__(self, url):
		self.url = url
		self.sendRequest()

	def sendRequest(self):
		try:
			self.response = requests.get(self.url)
			logging.info("Sending request seccessfully")
			return self.response
		except Exception as e:
			logging.error("error in sending Request :: Exception ::=> {0}".format(e))

	def getTitle(self):
		logging.info("getTitle Called ")
		title = Selector(self.response).css('header.has-star > h1::text').extract_first()
		logging.debug("the title is : {0}".format(title))
		return title

	def getSenderInformation(self):
		logging.info("getSenderInformation Called ")
		owner=Selector(self.response).css(
		    'div.order-owner > p.order-info-value > strong::text').extract_first()
		logging.debug("the ownre is : {0}".format(owner))
		return owner

	def getContactInformation(self):
		logging.info("getContactInformation Called ")
		phone_numbers=Selector(self.response).css(
		    'div.order-phone > p.order-info-value > strong::text').extract_first()
		logging.debug("the phone numbers are/is : {0}".format(phone_numbers))
		return phone_numbers

	def getWebsite(self):
		logging.info("getWebsite Called ")
		website=Selector(self.response).css(
		    'div.order-owner > p.order-info-value > a.order-weblink::attr(href)').extract_first()
		logging.debug("the website is : {0}".format(website))
		return website
