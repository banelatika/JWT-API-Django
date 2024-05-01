from rest_framework import renderers
import json

class UserRenders(renderers.JSONRenderer):
    charset= 'utf-8'
    def render(self, data, accepted_media_type=None, renderer_context=None):
        respose = ''
        if 'ErrorDetail' in str(data):
            respose= json.dumps({'errors':data})
        else:
            respose =json.dumps(data)
        return respose