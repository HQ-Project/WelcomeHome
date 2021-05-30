import time
import ibmiotf.application
import ibmiotf.device

organization = "7lke3y"
deviceType = "raspi"
deviceId = "dca632b2337e"
authMethod = "token"
authToken = "z0&s36wdlAL-+A*tUd"

# Initialize the device client.
deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
deviceCli = ibmiotf.device.Client(deviceOptions)