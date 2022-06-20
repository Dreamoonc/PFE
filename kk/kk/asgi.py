"""
ASGI config for kk project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
from authentification.consumers import *

from django.urls import re_path,path
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kk.settings')

ws_patterns = [
    path('ws/test/' ,TestConsumer.as_asgi() ),
    # path('ws/new/' , NewConsumer)
]

application = ProtocolTypeRouter({
    'websocket' : AuthMiddlewareStack(URLRouter(ws_patterns))
})