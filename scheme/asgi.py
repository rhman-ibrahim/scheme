import os
# Django
from django.core.asgi import get_asgi_application
from django.urls import path
# Channels
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
# Spaces
from spaces.consumers import ChatConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scheme.settings")


application = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests
    "http": get_asgi_application(),

    # WebSocket chat handler
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                path('spaces/<str:serial>/', ChatConsumer.as_asgi()),
            ])
        )
    ),

})