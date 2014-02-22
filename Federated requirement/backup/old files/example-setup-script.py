import urllib
import urllib2
import json

BASE_URL=http://localhost

""" Make a request to keystone """
def keystoneRequest(endpoint, data = {}, method = "GET"):
    headers = {'X-Auth-Token': 'password'}
    if method == "GET":        
        req = urllib2.Request(endpoint, headers = headers)
        response = urllib2.urlopen(req)
    elif method == "PUT":
        req = urllib2.Request(endpoint, headers = headers)        
        req.get_method = lambda: 'PUT'
        response = urllib2.urlopen(req)
        return
    elif method == "POST":
        data = json.dumps(data)
        headers['Content-Type'] = 'application/json'
        req = urllib2.Request(endpoint, data, headers)
        response = urllib2.urlopen(req)
    return json.loads(response.read())



print "Adding Identity Providers"
kentproxy = {"service":{"name":"Kent Proxy Identity Service", "description": "Kent Proxy Identity Service", "type":"idp.saml"}}
serviceEndpoint = BASE_URL+":5000BASE_URL+"/v3/services"
proxy = keystoneRequest(serviceEndpoint, kentproxy, "POST")
print "OK"

print "Adding Endpoints"
kentendpoint = "https://persistence.kent.ac.uk/simplesaml/saml2/idp/SSOService.php"
proxycertdata = "MIIDXDCCAsWgAwIBAgIJANHDiJSSuTu+MA0GCSqGSIb3DQEBBQUAMH0xCzAJBgNVBAYTAkdCMQ0wCwYDVQQIEwRLZW50MRMwEQYDVQQHEwpDYW50ZXJidXJ5MRswGQYDVQQKExJVbml2ZXJzaXR5IG9mIEtlbnQxCzAJBgNVBAsTAkNTMSAwHgYDVQQDExdpZHAuc2hpbnRhdTIua2VudC5hYy51azAeFw0xMDExMDgxMzI4MDVaFw0yMDExMDcxMzI4MDVaMH0xCzAJBgNVBAYTAkdCMQ0wCwYDVQQIEwRLZW50MRMwEQYDVQQHEwpDYW50ZXJidXJ5MRswGQYDVQQKExJVbml2ZXJzaXR5IG9mIEtlbnQxCzAJBgNVBAsTAkNTMSAwHgYDVQQDExdpZHAuc2hpbnRhdTIua2VudC5hYy51azCBnzANBgkqhkiG9w0BAQEFAAOBjQAwgYkCgYEAqMJSgjGNS9f/T2jyU3ort+vzY29hEMXjJPgtQEvM2ms/QsaNEIMCkH32duA6zpw37EdpWj3Zkd23+1YNELFPkXA8AKP8LKKoVMeyvBmVwddsfAQsQVSBP6wD9rAGxsRX4+ZiMD7Pr/W9z2oH4VHLO+3dhKN/jKs0i0X+pqfmDe8CAwEAAaOB4zCB4DAdBgNVHQ4EFgQURPhSdGQW7H3QDKx4uyPxLEEc5J4wgbAGA1UdIwSBqDCBpYAURPhSdGQW7H3QDKx4uyPxLEEc5J6hgYGkfzB9MQswCQYDVQQGEwJHQjENMAsGA1UECBMES2VudDETMBEGA1UEBxMKQ2FudGVyYnVyeTEbMBkGA1UEChMSVW5pdmVyc2l0eSBvZiBLZW50MQswCQYDVQQLEwJDUzEgMB4GA1UEAxMXaWRwLnNoaW50YXUyLmtlbnQuYWMudWuCCQDRw4iUkrk7vjAMBgNVHRMEBTADAQH/MA0GCSqGSIb3DQEBBQUAA4GBAJJfj3BOWxtZGm/4tnIyRNMINBZfMAz9GS5/9np16mVYVsKHX+ZSxnZkXVNouzaZnQmsAy+L9yeccaETEOvo8tKmUkV9YTIKRABq7Sb95ELkf7BVXSX/8hCpTRz84edBwE9Zppu2S1t+1bfhfDak0enqXCJ5P6fKdTmrdjPn0eoo"

kentproxyendpoint = {"endpoint":{}}
kentproxyendpoint["endpoint"]["service_id"] = proxy["service"]["id"]
kentproxyendpoint["endpoint"]["publicurl"]=kentendpoint
kentproxyendpoint["endpoint"]["internalurl"]=kentendpoint
kentproxyendpoint["endpoint"]["adminurl"]=kentendpoint
kentproxyendpoint["endpoint"]["certdata"]=proxycertdata

endpointEndpoint = BASE_URL+":35357/v2.0/endpoints"

kpep = keystoneRequest(endpointEndpoint, kentproxyendpoint, "POST")
print "OK"

print "Adding Org Attributes"
orgattEndpoint = BASE_URL+"/v3/org_attributes"

# For SAML


# Google
att6 = {"org_attribute":{}}
att6["org_attribute"]["type"] = "idp"
att6["org_attribute"]["value"] = "google"
orgatt6 = keystoneRequest(orgattEndpoint, att6, "POST")

att7 = {"org_attribute":{}}
att7["org_attribute"]["type"] = "facebook.id"
orgatt7 = keystoneRequest(orgattEndpoint, att7, "POST")

print "OK"

print "Adding Authorised Issuers for Attributes"
#Proxy can issue org atts 6-7

keystoneRequest(orgattEndpoint+"/"+orgatt6["org_attribute"]["id"]+"/issuers/"+proxy["service"]["id"], method="PUT")
keystoneRequest(orgattEndpoint+"/"+orgatt7["org_attribute"]["id"]+"/issuers/"+proxy["service"]["id"], method="PUT")


print "OK"

print "Adding roles"
roleEndPoint = BASE_URL+"/v3/roles"
# Google member
gm= {"role":{}}
gm["role"]["name"] = "googlemember"
gmem = keystoneRequest(roleEndPoint, gm, "POST")
# Facebook member
fm= {"role":{}}
fm["role"]["name"] = "facebookmember"
fmem = keystoneRequest(roleEndPoint, fm, "POST")

print "OK"


print "Adding Projects"
projectEndPoint = BASE_URL+"/v3/projects"
# Google project
gp= {"project":{}}
gp["project"]["name"] = "Google User's Project"
gp["project"]["description"] = "Google User's Project"
gpro = keystoneRequest(projectEndPoint, gp, "POST")
# Facebook project
fp= {"project":{}}
fp["project"]["name"] = "Facebook User's Project"
fp["project"]["description"] = "Facebook User's Project"
fpro = keystoneRequest(projectEndPoint, fp, "POST")

print "OK"

print "Organising Org Sets"
orgsetEndpoint = BASE_URL+"/v3/org_attribute_sets"


# Google  Sets
# Set 1 contains idp=google(orgatt6) 
# Create the set
gs1 = {"org_attribute_set":{}}
gs1["org_attribute_set"]["name"] = "GoogleSet1"
gset1 = keystoneRequest(orgsetEndpoint, gs1, "POST")
# Add the attributes
keystoneRequest(orgsetEndpoint+"/"+gset1["org_attribute_set"]["id"]+"/attributes/"+orgatt6["org_attribute"]["id"], method="PUT")

# Facebook  Sets
# Set 1 contains idp=facebook(orgatt7) 
# Create the set
fs1 = {"org_attribute_set":{}}
fs1["org_attribute_set"]["name"] = "FacebookSet1"
fset1 = keystoneRequest(orgsetEndpoint, fs1, "POST")
# Add the attributes
keystoneRequest(orgsetEndpoint+"/"+fset1["org_attribute_set"]["id"]+"/attributes/"+orgatt7["org_attribute"]["id"], method="PUT")

print "OK"

print "Organising Os Sets"
ossetEndpoint = BASE_URL+"/v3/os_attribute_sets"
# Google Sets
# Set 1 contains role=googlemember (gmem) and project=google users (gpro) 
# Create the set
gos1 = {"os_attribute_set":{}}
gos1["os_attribute_set"]["name"] = "GoogleSet1"
goset1 = keystoneRequest(ossetEndpoint, gos1, "POST")
# Add the attributes
keystoneRequest(ossetEndpoint+"/"+goset1["os_attribute_set"]["id"]+"/projects/"+gpro["project"]["id"], method="PUT")
keystoneRequest(ossetEndpoint+"/"+goset1["os_attribute_set"]["id"]+"/roles/"+gmem["role"]["id"], method="PUT")

# Facebook Sets
# Set 1 contains role=facebookmember (fmem) and project=facebook users (fpro) 
# Create the set
fos1 = {"os_attribute_set":{}}
fos1["os_attribute_set"]["name"] = "FacebookSet1"
foset1 = keystoneRequest(ossetEndpoint, fos1, "POST")
# Add the attributes
keystoneRequest(ossetEndpoint+"/"+foset1["os_attribute_set"]["id"]+"/projects/"+fpro["project"]["id"], method="PUT")
keystoneRequest(ossetEndpoint+"/"+foset1["os_attribute_set"]["id"]+"/roles/"+fmem["role"]["id"], method="PUT")

print "OK"

print "Mapping Sets"

amEndpoint = BASE_URL+"/v3/attribute_set_mappings"
basicMap = {"attribute_set_mapping":{"org_attribute_set_id":"", "os_attribute_set_id":""}}
# Google: goset1 -> gset1
googleMap = basicMap.copy()
googleMap["attribute_set_mapping"]["org_attribute_set_id"] = gset1["org_attribute_set"]["id"]
googleMap["attribute_set_mapping"]["os_attribute_set_id"] = goset1["os_attribute_set"]["id"]
keystoneRequest(amEndpoint, googleMap, "POST")
# Facebook: foset1 -> fset1
facebookMap = basicMap.copy()
facebookMap["attribute_set_mapping"]["org_attribute_set_id"] = fset1["org_attribute_set"]["id"]
facebookMap["attribute_set_mapping"]["os_attribute_set_id"] = foset1["os_attribute_set"]["id"]
keystoneRequest(amEndpoint, facebookMap, "POST")

print "OK"
print "Success, all entities created, demo ready"

