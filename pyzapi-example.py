# Minwoo Lee
# Mar. 25th 2016
# Example usage of pyzapi module
import pyzapi, json
# Use pprint() instead of print() to display JSON output as formatted string
from pprint import pprint

# To use pyzapi, first create a profile.json file using the following command.
# createProfileJSON creates a new authentication token and stores it in profile.json file.
# it also stores available organizations
# if this function is called when there is already profile.json, then the function is ignored, unless overwrite parameter is set to true.
pyzapi.createProfileJSON("johnsmith@gmail.com")


# listOrganizations() returns a list of dictionary format of organzation names and ids
# Use this function to identify the names of available organizations
print(pyzapi.listOrganizations())


# listSalesOrders() returns a list of dictionary format of sales order.
# You can optionally pass an organization name as a parameter to get data for specific organization
salesOrders = pyzapi.listSalesOrders()
salesOrders = pyzapi.listSalesOrders('Aurender America Inc.')

# Also possible to call without any arguments, and it will automatically use default authtoken and orgID.
#pprint(pyzapi.getSalesOrder('244857000000065757'))
pyzapi.getSalesOrder('244857000000065757')
