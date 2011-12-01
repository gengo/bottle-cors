bottle-cors
===========

An _alpha_ version of a plugin for bottle to handle CORS (Cross Origin
Resource Sharing). It adds a `Access-Control-Allow-Origin` header and
registeres routes to serve OPTIONS requests for your endpoints (request
preflighting).

# Usage #

Copy the cors_plugin.py somewhere into your project. ie:

    cp cors_plugin.py <your_project>/plugins

then you have to import and register the plugin:

    from plugins.cors_plugin import RequestPreflightPlugin

    request_preflight_plugin = RequestPreflightPlugin( allow_origin = '*',
                                                       preflight_methods = [ 'GET', 'POST', 'PUT', 'DELETE' ],
                                                       ttl = 3600 )
    request_handler.install( request_preflight_plugin )

`allow_origin` will be the value of the `Access-Control-Allow-Origin` header.
`preflight_methods` lists the methods/HTTP verbs that you want to have preflighted by default.
`ttl` will be the value of the `Access-Control-Max-Age` in the OPTIONS response.

All routes that you have will get an OPTIONS route registered that will serve the preflight response.

If you want to exclude a route from preflighting you have to skip the plugin:

    @route( "/path",
            skip = [ request_preflight_plugin ] )
    def do_stuff:
        pass

# TODO #

* make the OPTION preflighting optional?
