import requests
import icalendar

userName = "PARGALL2"
password = "***"

LoginURL = "https://student.uwo.ca/psp/heprdweb/EMPLOYEE/HRMS/c/UWO_WISG.WSA_STDNT_CENTER.GBL&languageCd=ENG";


payload = {'httpPort2' : '',
		'timezoneOffset2':0,
		'userid':userName.upper(),
		'pwd':password,
		'Submit':'Sign In'}

r = requests.post(LoginURL, params=payload);
print(r.text)