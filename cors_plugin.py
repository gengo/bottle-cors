# -*- coding: utf-8 -*-

# Copyright 2011 Florian von Bock (f at mygengo dot com)
#
# CORS preflighting and header plugin for bottle

__author__ = "Florian von Bock"
__email__ = "f at mygengo dot com"
__version__ = "0.0.9"

from bottle import request, response, Route

def options_preflight_method( methods, allow_origin = '*', ttl = 300 ):
    """ Takes the methods/verbs from the 'original' endpoint and returns the
        endpoint function that serves the preflight OPTIONS request.

        """
    def endpoint( *args, **kwargs ):
        """ This is the actual endpoint that gets inserted for all routes/rules
            that are to be preflighted.

            """
        preflight_headers = { 'Access-Control-Allow-Methods': ', '.join( methods ),
                              'Access-Control-Max-Age': ttl,
                              'Content-Type': 'plain/text' }
        if request.headers.get( 'Access-Control-Request-Headers' ):
            preflight_headers[ 'Access-Control-Allow-Headers' ] = request.headers[ 'Access-Control-Request-Headers' ]
        for header_name in preflight_headers.iterkeys():
            response.headers[ header_name ] = preflight_headers[ header_name ]
        return []
    return endpoint


def enable_cors_hook( origin = '*' ):
    """ This is the hook that sends the `Allow-Origin` header for _all_ endpoints.
        Some endpoints might not be preflighted, but the `Allow-Origin` will be
        sent on all endpoints. This is taken from the CORS-hook example in the
        bottle documentation. Not 100% sure it makes sense, but i stick with it -
        for now at least.

        """
    def enable_cors_header():
        response.headers[ 'Access-Control-Allow-Origin' ] = origin
    return enable_cors_header


class RequestPreflightPlugin( object ):
    """ This plugin registers OPTIONS endpoints for CORS related request preflighting."""

    name = 'RequestPreflight'
    api = 2

    def __init__( self, allow_origin = '*',
                  preflight_methods = [ 'GET', 'POST', 'PUT', 'DELETE' ], ttl = 300 ):
         self.allow_origin = allow_origin
         self.preflight_methods = preflight_methods
         self.ttl = ttl
         self.method_registry = {}

    def setup( self, app ):
        """ Check that the plugin does not get installed twice."""
        for other in app.plugins:
            if not isinstance( other, RequestPreflightPlugin ):
                continue
            raise PluginError( "RequestPreflightPlugin is already installed." )
        hook_registered = False
        for func in app.hooks.hooks[ 'after_request' ]:
            if isinstance( func, enable_cors_header ):
                hook_registered = True
        if not hook_registered:
            app.hooks.add( 'after_request', enable_cors_hook( self.allow_origin ) )

    def apply( self, callback, context ):
        for plugin in context.app.plugins:
            plugins = []
            if not isinstance( plugin, RequestPreflightPlugin ):
                plugins.append( plugin )
            else:
                skip_self = plugin
        if context.method in self.preflight_methods:
            self.method_registry.setdefault( context.rule, [] ).append( context.method )
            route = Route( context.app, context.rule, 'OPTIONS',
                           globals()[ 'options_preflight_method' ]( self.method_registry[ context.rule ],
                                                                    self.allow_origin,
                                                                    self.ttl ),
                           name = None, plugins = plugins, skiplist = [ skip_self ] )
            context.app.router.add( context.rule, 'OPTIONS', route, name = None )

        return callback
