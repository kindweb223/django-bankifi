"""
# Xero API OAUTH handler

Provides the OAUTH handling routines used by the Cashflow Application (aka Bankifi demo).
This utilises the [pyxero 3rd partyh project](https://github.com/freakboy3742/pyxero) where additional
usage documentation can be found.

The Django session capabilities are utilised to store tokens between calls to the Xero API and Web Page refreshes.

"""
"""
**Public Methods:**

1. ***get_xero_credentials***: Receives Xero credentials to be used for the initial login and authorisation_url.
2. ***get_xero***: returns Xero connection handler that allows the Xero api to be called.

**Internal Methods:**

1. ***json_serial***: JSON serializer for objects not serializable by default json code.
2. ***save_temp_credentials***: Temporarily save Xero credentials in the Django session state for subsequent use.
3. ***verify_credentials***: Verify with Xero that the credentials are valid.
4. ***save_credentials***: Save Xero credentials in the Django session state for subsequent use.
"""

# === Imports ===

# Import Python modules
from datetime import datetime
import logging

# Import pyxero modules
from xero.auth import PublicCredentials
from xero import Xero

# Import Django modules
from django.conf import settings
from django.http import Http404


# === Logging ===

# Setup loggers
infolog = logging.getLogger('infologger')
errorlog = logging.getLogger('prodlogger')

# === Methods ===

def json_serial(obj):
    """
    **json_serial(obj)**

    JSON serializer for objects not serializable by default json code.

    **Parameters:**

    ***obj***: python object to be converted.

    **Returns**:

    Serialized object or TypeError exception.
    """
    # Serialize datetime objects used correctly
    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial

    raise TypeError ("Type not serializable")


def get_xero_credentials(request, callback=settings.XERO_CALLBACK_URI):
    """
    **get_xero_credentials(request, callback=settings.XERO_CALLBACK_URI)**

    Receives Xero credentials to be used for the initial login and authorisation_url.

    Saves a temporary copy of the pyxero credentials that are used following the callback from Xero.

    **Parameters:**

    ***request***: Django request object.

    ***callback***: Callback URI to be used by Xero.

    **Returns:**

    Pyxero credentials object.
    """
    # Reset session state
    request.session['temp_credentials'] = None
    # Login to Xero to generate credentials to access the authorization URL
    credentials = PublicCredentials(settings.XERO_CLIENT_KEY, settings.XERO_CLIENT_SECRET, callback)
    # Save initial request credentials pre-URL call as these are needed post the call too
    save_temp_credentials(request, credentials)
    infolog.info("Getting Credentials {0}".format(credentials.state))
    return credentials


def save_temp_credentials(request, credentials):
    """
    **save_temp_credentials(request, credentials)**

    Temporarily save Xero credentials in the Django session state for subsequent use.

    **Parameters:**

    ***request***: Django request object.

    ***credentials***: pyxero credentials object.

    **Returns:**

    Nothing
    """
    tmp = credentials.state
    tmp['oauth_authorization_expires_at'] = str(tmp.get('oauth_authorization_expires_at'))
    tmp['oauth_expires_at'] = str(tmp.get('oauth_expires_at'))
    infolog.info("save TEMP credentials stats: {0}".format(credentials.state))
    request.session['temp_credentials'] = tmp


def verify_credentials(request):
    """
    **verify_credentials(request)**

    Verify the pyxero credentials with Xero.

    **Parameters:**

    ***request***: Django request object.

    **Returns**:

    Nothing
    """
    # Recreate the credential objects from the saved credentials
    temp_credentials = request.session.get('temp_credentials', None)
    credentials = PublicCredentials(**temp_credentials)

    infolog.info("Pre-Verify Credentials: {0}".format(credentials.state))

    # Verify the credentials using the passed in 'oauth_verifier' parameter
    credentials.verify( request.GET.get('oauth_verifier', None))
    # Important we save the verified credentials for future use
    if credentials.state.get('verified', False) == True:
        tmp = credentials.state
        tmp['oauth_authorization_expires_at'] = str(tmp.get('oauth_authorization_expires_at'))
        tmp['oauth_expires_at'] = str(tmp.get('oauth_expires_at'))
        request.session['credentials'] = tmp
        infolog.info("Credentials Now Verified {0}".format(credentials.state))
    else:
        infolog.info("Failed to Verify Credentials {0}".format(credentials.state))

def save_credentials(request, credentials):
    """
    **save_credentials(request, credentials)**

    Save the verifie pyxero credentials in the Django session state for subsequent use.

    **Parameters:**

    ***request***: Django request object.

    ***credentials***: pyxero credentials object.

    **Returns:**

    Nothing
    """
    tmp = credentials.state
    tmp['oauth_authorization_expires_at'] = str(tmp.get('oauth_authorization_expires_at'))
    tmp['oauth_expires_at'] = str(tmp.get('oauth_expires_at'))
    infolog.info("Before Session: {0}".format(request.session['credentials']))
    infolog.info("save_credentials stats: {0}".format(credentials.state))
    request.session['credentials'] = tmp
    infolog.info("After Session: {0}".format(request.session['credentials']))


def get_xero(request):
    """
    **get_xero(request)**

    Retrieves the Xero connection object to allow access to Xero API.

    **Parameters:**

    ***request***: Django request object.

    **Returns**:

    Xero connection object that allows api access.
    """
    try:
        saved_credentials = request.session.get('credentials', None)
        credentials = PublicCredentials(**saved_credentials)
        infolog.info("session credentials: {0}".format(credentials.state))
        return Xero(credentials)
    except:
        errorlog.error("Failed to retrieve the connection object. Perhaps user not logged in.")
        raise Http404("Failed to connect to Xero. Ensure you are signed in.")
        
