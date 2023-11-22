from django.http import HttpResponse 
from django.template import Template, Context
from django.views.decorators.csrf import csrf_exempt
#import gramatica as g
#import ts as TS
#from expresiones import *
#from instrucciones import *

class CrearInterprete:
    @csrf_exempt
    def interprete(request):
        docExterno=open("C:/Users/lgniw/OneDrive/Documents/GitHub/InterpreteSoftware/Interprete/vista/static/interprete.html")
        plt=Template(docExterno.read())
        docExterno.close()
        ctx=Context()
        documento=plt.render(ctx)
        return HttpResponse(documento)