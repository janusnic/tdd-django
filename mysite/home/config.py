# config.py

from authomatic.providers import oauth2, oauth1 #, openid, gaeopenid

CONFIG = {
    
    'tw': { # Your internal provider name
        
        # Provider class
        'class_': oauth1.Twitter,
        
        # Twitter is an AuthorizationProvider so we need to set several other properties too:
        'consumer_key': 'gTVg6h1fPPK0qyUj2Z7M5lKmW',
        'consumer_secret': 'EGNPWNHuYqZ74sK08EtsKwIzA4I5HIbpXhcdeFfe1DainSuApL',
    },
    
    'fb': {
           
        'class_': oauth2.Facebook,
        
        # Facebook is an AuthorizationProvider too.
        'consumer_key': '########################',
        'consumer_secret': '########################',
        
        # But it is also an OAuth 2.0 provider and it needs scope.
        'scope': ['user_about_me', 'email', 'publish_stream'],
    },
    
    'oi': {
           
        # OpenID provider dependent on the python-openid package.
        #'class_': openid.OpenID,
    }
}