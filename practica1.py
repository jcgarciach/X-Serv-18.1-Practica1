#!/usr/bin/python3

import webapp
import csv

def Formulario():
    formulario = """
    <form action="" method="POST">url:<br><input type="text" name="url" placeholder="URL a acortar"><br><input type="submit" value="Enviar"></form> 
    """
    return formulario
    
class URLshortApp (webapp.webApp):
	
	list_urls = ""
	url_sinnum = ""
	num = 0
	dicturl = {}
	dicturlshort = {}
	
	def parse(self,request):
		method = request.split()[0] 
		resource = request.split()[1][1:] 
		if method == "POST" :
			body = request.split('\r\n\r\n', 1)[1].split('=')[1]
			if len(body.split("%3A%2F%2F")) == 1:
				url = "http://" + body.split('%', 1)[0]
			else:
				url = "http://" + body.split("%3A%2F%2F", 1)[1].split('%', 1)[0]
		else:
			body = ""
			url = body
		print (url)
		return (method, resource, url)
	
	def process(self,parsedRequest):
		method, resource, url = parsedRequest
		formulario = Formulario()
		if method == "GET":
			if resource == "":
				code = "200 OK"
				#creamos una tabla de html usando table tb td 
				body = "<html>" + formulario + "<table><tr><td>URL</td><td>short_url</td></tr><tr><td>" + self.list_urls + "</td><td>" + self.url_sinnum + "</td></tr></table>" + "</html>"
			elif resource == "favicon.ico":
				code = "404 Not Found"
				body = "<html><body>favicon</html>"
			else:
			# en este caso nos va a redirigir la pagina se refrescara en el caso de que yo pido "nº" y eso es menor que el contador
				if int(resource) < self.num :
					code = "307 Temporary Redirect"
					body = "<html><body><h1>Redirigir</h1><meta http-equiv='Refresh' content='0; url= " + str(self.dicturlshort[int(resource)]) + "></body></html>"
				else:
					code = "400 Not Found"
					body = "<html><body><h1>error </h1></body></html>"
		if method == "POST" :
			if url == "":
				code = "400 Not Found"
				body = "<html><body><h1> Error </h1></body></html>"
			if url not in self.dicturl.keys(): #dict.keys() se usa mucho en los dicturls
				self.dicturl[self.num] = url
				self.dicturl[url] = self.num
				self.list_urls = self.list_urls + "<p>" + str(url) + "</p>"
				self.url_sinnum = self.url_sinnum + "<p>http://localhost:1234/" + str(self.num) + "</p>"
				self.num = self.num + 1
			#el dicturl en un fichero
			#buscado en google
			with open('listurl.csv', 'a', newline = '') as myfich:
				fichUrl = csv.writer(myfich)
				fichUrl.writerow([self.num,url])
			code = "200 OK"
			body = '<html><body>' + "<p><h4>url_orig<a href=" + url + ">" + str(url) + "</a></h4></p><p><h4>url_short<a href=" + "http://localhost:1234/" + str(self.num - 1) + ">" + str("http://localhost:1234/" + str(self.num - 1)) + "</a></h4></p>" + "<p><a href='http://localhost:1234/'>formulario</a></p>" + "</body></html>"
		
		return(code,body)
	
	def __init__(self, hostname, port):
		archi = open('listurl.csv', 'a')
		archi.close()
		super().__init__(hostname,port)

if __name__ == "__main__":
    testWebApp = URLshortApp("localhost", 1234)
