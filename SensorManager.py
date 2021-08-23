def registerNewSensorClass(data):
    s={'success_status': 'True', 'msg': 'Sensor Class Created!!!!!'}
    return str(s)

def makeSensorInstances(data):
    s=[{'success_status': 'True', 'msg': 'Sensor instance registered successfully!!!'}, {'success_status': 'True', 'msg': 'Sensor instance registered successfully!!!'}, {'success_status': 'True', 'msg': 'Sensor instance registered successfully!!!'}]
    return str(s)

def validateAppSensors(data):
    s=[True, True, True]
    return str(s)

def getSensorIdByLocation(data):
    s=["1","2"]
    return str(s)

def installNewBarricades(data):
	return True

def bus_list():
	return ["B1","B2","B3","B4"]