# Minwoo Lee
# Mar. 25th 2016
# Pyzapi: Zoho API module for Python
# ver 3.0.0

import http.client, urllib, json, getpass

datafile = "profile.json"
 
def _pyzapiRequest(host, method, url, params={}):
    params = urllib.parse.urlencode(params)
    headers = {"Content-type": "application/x-www-form-urlencoded",  "Accept": "text/plain"}
    pyzapiConn = http.client.HTTPSConnection(host)

    # request HTTPS connection
    print (__name__ + ".connection: requesting to " + host + "...")
    if method == "GET":
        pyzapiConn.request(method, url + "?" + params)
    elif method == "POST":
        pyzapiConn.request(method, url, params, headers)
    else:
        raise NotImplementedError("Methods other than GET/POST are not supported!")
    response = pyzapiConn.getresponse()
    print (__name__ + ".connection: received response!")
    data = response.read().decode()
    pyzapiConn.close()
    return data

##  Creates datafile for storing authentication token and organizations info
def createProfileJSON(email, overwrite = False):
    # check if profile.json exists, and if so, should overwrite
    profileExists = True
    try:
        print (__name__ + ".createProfileJSON: checking if " + datafile + " exists...")
        with open(datafile) as data_file:
            data = json.load(data_file)
            print (__name__ + ".createProfileJSON: " + datafile + " for user <" + data['email'] + "> already exists!")
            print (__name__ + ".createProfileJSON: Using the existing profile. Call the function with overwrite=true to overwrite and create a new profile.")
#            overwritePrompt = "There's an existing profile for user <"+ data['email'] +">, do you want to continue and create a new token for user <"+ email + ">?(y/n)"
#            overwrite = True if input(overwritePrompt) == "y" else False
    except:
        print (__name__ + ".createProfileJSON: " + datafile + " doesn't exist.")
        profileExists = False

    # create datafile
    if (not profileExists) or overwrite:
        print (__name__ + ".createProfileJSON: Creating a new " + datafile + "...")
        authtoken = retrieveAuthtoken(email)
        organizations = retrieveOrganizations(authtoken)
        data = {"email": email, "token": authtoken, "organizations": organizations};
        with open(datafile, 'w') as outfile:
            json.dump(data, outfile)
        print(__name__ + ".createProfileJSON: File successfully created!")

##  Retrieves authentication token from accounts.zoho.com
def retrieveAuthtoken(email):
    print (__name__ + ": Retrieving a new authentication token for <"+email+">...")
    # Get password input
    password = getpass.getpass("Password for Zoho user {0}:".format(email))

    # Request API
    params = {'SCOPE': 'ZohoInventory/inventoryapi', 'EMAIL_ID': email, 'PASSWORD': password}
    data = _pyzapiRequest("accounts.zoho.com", "POST", "/apiauthtoken/nb/create", params)

    # Format resulting HTML output into dictionary
    dataline = data.splitlines()
    results = dict()
    for line in dataline:
        if line.find("=") != -1:
            query = line.split("=")
            results[query[0]] = query[1]

    # Return result if successful, or else raise ValueError
    if results['RESULT'] != 'FALSE':
        print (__name__ + ": successfully created a new authorization token!")
        return results['AUTHTOKEN']
    else:
        raise ConnectionError(results['CAUSE'])

##  Retrieves organizations from inventory.zoho.com
def retrieveOrganizations(authtoken):
    print (__name__ + ": Retrieving organizations for <"+email+">...")
    params = {'authtoken': authtoken};
    data = _pyzapiRequest("inventory.zoho.com", "GET", "/api/v1/organizations", params)
    print (__name__ + ": successfully retrieved organizations data!")
    return json.loads(data)['organizations']

###
### Below functions rely on authtoken and organization data saved in datafile
###

def getAuthtoken():
    with open(datafile) as data_file:
        data = json.load(data_file)
    return data["token"]


def listOrganizations():
    with open(datafile) as data_file:
        data = json.load(data_file)
    orgs = dict()
    for org in data['organizations']:
        orgs[org["name"]] = org["organization_id"]
    return orgs


def listSalesOrders(orgName = ''):
    # select first organization name for default
    orgs = listOrganizations()
    if not orgName:
        orgName = list(orgs.keys())[0]
    print (__name__ + ".listSalesOrders: Function called for org " + orgName)

    # call API
    orgID = orgs[orgName]
    authtoken = getAuthtoken()
    params = {'organization_id': orgID, 'authtoken': authtoken}
    data = _pyzapiRequest("inventory.zoho.com", "GET", "/api/v1/salesorders", params)

    print (__name__ + ".listSalesOrders: Successfully returning sales order list! Check https://www.zoho.com/inventory/api/v1/#sales-orders for details on returned sales order data.")
    return json.loads(data)["salesorders"]

def getSalesOrder(salesOrderID, orgName = ''):
    # select first organization name for default
    orgs = listOrganizations()
    if not orgName:
        orgName = list(orgs.keys())[0]
    print (__name__ + ".getSalesOrder: Function called for org " + orgName)

    # call API
    orgID = orgs[orgName]
    authtoken = getAuthtoken()
    params = {'organization_id': orgID, 'authtoken': authtoken}
    data = _pyzapiRequest("inventory.zoho.com", "GET", "/api/v1/salesorders/{0}".format(salesOrderID), params)

    print (__name__ + ".getSalesOrder: Successfully returning a sales order.")
    return json.loads(data)
