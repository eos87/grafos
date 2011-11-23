# -*- coding: UTF-8 -*-
from PIL import Image
import commands
from django.core.files import File
from django.http import HttpResponse
from django.utils.hashcompat import sha_constructor
from grafos.settings import *
import random
BATIK_PATH = MEDIA_ROOT + 'batik/batik-rasterizer.jar '

def index(request):    
    if request.method == 'POST':
        tmpName = sha_constructor(str(random.random())).hexdigest()
        tipo = request.POST['type']
        svg = request.POST['svg']
        filename = request.POST['filename']
        width = request.POST['width']

        if tipo == 'image/png':
            typeString = 'image/png'
            ext = '.png'
        elif tipo == 'image/jpeg':
            typeString = 'image/jpg'
            ext = '.jpg'
        elif tipo == 'application/pdf':
            typeString = 'application/pdf'
            ext = '.pdf'	    
        else:
            typeString = 'image/svg+xml'
            ext = '.svg'
    else:
        return HttpResponse('<h1>GTFO!!</h1>', mimetype='text/html')

    outfile = MEDIA_ROOT + tmpName + ext
    #return the url not the image
    try:    
        img_url = request.POST['img_url']
    except:
        img_url = None
        
    try:
        f = open('%s%s%s' % (MEDIA_ROOT,tmpName,'.svg'), 'w')
        svgObj = File(f)
        svgObj.write(svg.encode('utf-8'))
        svgObj.close()
        string = 'java -jar '+ str(BATIK_PATH) + ' -m ' + str(tipo) +' -d '+ str(outfile) +' -w '+ str(width) + ' ' + str(svgObj.name)        
        convert = commands.getoutput(string)
        salida = open(outfile)
        #only url not the image
        if img_url:
            return HttpResponse(tmpName + ext)   
                
    	response = HttpResponse(salida, mimetype=tipo)
    	response['Content-Disposition'] = 'attachment; filename=grafico'+ext
    	return response
    except Exception:
        return HttpResponse(str(Exception))
