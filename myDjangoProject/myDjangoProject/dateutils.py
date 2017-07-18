import datetime

def getcurrentdate():
	now = datetime.datetime.now()
	return now.strftime("%Y%m%d")
