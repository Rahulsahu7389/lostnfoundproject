from django.urls import path ,re_path
from . import consumers
#this page is same as urls 

websocket_urlpatterns = [
    re_path('ws/sc',consumers.MySyncConsumer.as_asgi()), # last me maine / ye daal diya tha to error aaya
    re_path('ws/ac',consumers.MyAsyncConsumer.as_asgi())
]

