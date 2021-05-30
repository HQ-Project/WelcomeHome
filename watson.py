import time
import ibmiotf.application
import ibmiotf.device

organization = "7lke3y"
deviceType = "raspi"
deviceId = "dca632b2337e"
authMethod = "token"
authToken = "z0&s36wdlAL-+A*tUd"

# Initialize the device client.
try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
except Exception as e:
	print(str(e))
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()
# deviceCli.commandCallback = myCommandCallback

while(1):
	data = {"bebegim": "<3"}
	deviceCli.publishEvent(event="status", data=data, msgFormat="json")
	time.sleep(2)

deviceCli.disconnect()