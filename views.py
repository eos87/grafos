from django.utils.hashcompat import sha_constructor
from django.core.files import File
from django.http import HttpResponse
from PIL import Image
import random
import commands

from grafos.settings import *
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
            typeString = 'image/jpeg'
            ext = '.jpg'
        elif tipo == 'application/pdf':
            typeString = 'application/pdf'
            ext = '.pdf'
        else:
            typeString = 'image/svg+xml'
            ext = '.svg'
    else:
        return HttpResponse('<h1>GTFO!!</h1>', mimetype='text/html')

    outfile =  MEDIA_ROOT + tmpName + ext

    try:
        f = open('%s%s%s' % (MEDIA_ROOT,tmpName,'.svg'), 'w')
        svgObj = File(f)
        svgObj.write(svg)
        svgObj.close()
        string = 'gij --jar '+ BATIK_PATH + ' -m ' + typeString +' -d '+ outfile +' -w '+ width + ' ' + svgObj.name +'        
        convert = commands.getoutput(string)
        resultado = Image.open(outfile)
        return HttpResponse(resultado, mimetype=tipo)
    except:
        return HttpResponse(convert)

    return HttpResponse(svgObj.name)

