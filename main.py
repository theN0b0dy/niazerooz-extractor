import requests
from scrapy import Selector
import logging
from niazrooz import ExtractDetail
import threading 
import time 


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logging.disable(logging.INFO)


class NiazRooz:

	def __init__(self):
		self._result = []*30
		self.url = str(input(" pls enter page url : "))
		pages = int(input(" how many pages should i extract for you ? "))
		self.main(pages)

	def sendRequest(self, url):
		try:
			logging.debug("Sending request seccessfully")
			return requests.get(url) 
		except Exception as e:
			logging.error("error in sending Request :: Exception ::=> {0}".format(e))

	def __getLinks(self, response):
		logging.debug("getLinks Called")
		links = Selector(response).css('a.order-link::attr(href)').extract()
		logging.debug("the links are : {0}".format(links))
		return ["https://www.niazerooz.com" + link for link in links]


	def __getData(self, link):
		obj = ExtractDetail(link)
		title = obj.getTitle()
		owner = obj.getSenderInformation()
		phone_numbers = obj.getContactInformation()
		website = obj.getWebsite()
		# print({"owner": owner, "phone_numbers": phone_numbers, "website": website})
		self._result.append({"title": title, "link": link, "owner": owner, "phone_numbers": phone_numbers, "website": website})

	def extractor(self, response):
		threads = list()
		for link in self.__getLinks(response):
			x = threading.Thread(target=self.__getData, args=(link,), daemon=True)
			threads.append(x)
			x.start()
		for _ in threads:
			_.join()

	def main(self, pages):
		html = """<!DOCTYPE html>
					<html lang="en">
					  <head>
					    <title></title>
					    <!-- Required meta tags -->
					    <meta charset="utf-8" />
					    <meta
					      name="viewport"
					      content="width=device-width, initial-scale=1, shrink-to-fit=no"
					    />

					    <!-- Bootstrap CSS -->
					    <link
					      rel="stylesheet"
					      href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
					      integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T"
					      crossorigin="anonymous"
					    />
					  </head>
					  <body>
					    <div class="container">
					      <table class="table table-striped">
					        <thead>
					          <tr>
					            <th>#</th>
					            <th>Title</th>
					            <th>owner</th>
					            <th>phone numbers</th>
					            <th>website</th>
					          </tr>
					        </thead>
					        <tbody>"""
		i = 1
		for page_number in range(1, pages + 1):
			url = self.url + "page-" + str(page_number)
			print(url)
			response = self.sendRequest(url)
			self.extractor(response)
			result_list = self._result
			for row in result_list:
				html += """<tr>
					            <td scope="row">{0}</td>
					            <td><a href="{1}">{2}</a></td>
					            <td>{3}</td>
					            <td>{4}</td>
					            <td>
					              <a href="{5}">{6}</a>
					            </td>
					          </tr>""".format(
					          		i,
					          		row['link'],
					          		row['title'],
					          		row['owner'],
					          		row['phone_numbers'],
					          		row['website'],
					          		row['website']
					          	)
				i+=1
				self._result = []
		html += """</tbody>
			      </table>
			      <!-- Optional JavaScript -->
			      <!-- jQuery first, then Popper.js, then Bootstrap JS -->
			      <script
			        src="https://code.jquery.com/jquery-3.3.1.slim.min.js"
			        integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo"
			        crossorigin="anonymous"
			      ></script>
			      <script
			        src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"
			        integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1"
			        crossorigin="anonymous"
			      ></script>
			      <script
			        src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"
			        integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM"
			        crossorigin="anonymous"
			      ></script>
			    </div>
			  </body>
			</html>
			"""
		with open('result.html', 'a+') as f:
			f.write(html)
			


if __name__ == '__main__':
	NiazRooz()