# Import necessary packages
import swat, os
# Add certificate location to operating system's list of trusted certs.
os.environ['CAS_CLIENT_SSL_CA_LIST']=os.environ['SSLCALISTLOC']
# Connect to CAS
conn = swat.CAS(hostname="sas-cas-server-default-client",port=5570, password=os.environ['SAS_SERVICES_TOKEN'])

# Create caslib
r = conn.dropCaslib(caslib="Opendata", quiet=True)
r = conn.table.addCaslib(name="Opendata", session=False, path="/home/sasdemo/opendata/", createDirectory=True)

# Terminate session
conn.terminate()