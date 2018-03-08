#!/usr/bin/python3


import webapp

listurl = {}
invlisturl = {}

formulario = """
    <form action = " " method="POST">
    Url:<br>
    <input type = "text" name = "url" value = " "><br>
    <input type = "submit" value = "Enviar">
</form>
"""

class acortarurlApp(webapp.webApp):
    
    def parse(self, request):
        return (request.split()[0], request.split()[1], request)
        
    def process(self, parsedRequest):  
        metodo, recurso, peticion = parsedRequest
        if metodo == "POST":
            cuerpo = peticion.split('/')[1]
            listurl[recurso] = cuerpo.split('=')[0]
        try:
            print(listurl)
            print(recurso)      
            return ("200 OK", "<html>" + listurl[recurso] + "<html>")
        except KeyError:
            return ("404 Not Found", "<html> Not Found!" + formulario + "<html>")
        
        
if __name__ == "__main__":
    testWebApp = acortarurlApp("localhost", 1234)
