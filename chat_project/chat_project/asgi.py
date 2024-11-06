"""
ASGI config for chat_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""
#connection start krne k liye
import os
from channels.routing import ProtocolTypeRouter,URLRouter
from django.core.asgi import get_asgi_application
import Home.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_project.settings')

application = get_asgi_application()
# ws_pattern = []

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        'websocket':URLRouter(
            Home.routing.websocket_urlpatterns
        )
    }
)