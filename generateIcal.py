import requests
import icalendar

userName = "PARGALL2"
password = "***"

LoginURL = 'https://student.uwo.ca/psp/heprdweb/EMPLOYEE/HRMS/c/UWO_WISG.WSA_STDNT_CENTER.GBL&languageCd=ENG';
schedURL = 'https://student.uwo.ca/psc/heprdweb/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSR_SSENRL_LIST.GBL';

payload = {'httpPort2' : '',
		'timezoneOffset2':0,
		'userid':userName.upper(),
		'pwd':password,
		'Submit':'Sign In'}
s = requests.Session();

#login in
s.post(LoginURL, params=payload);

#get Sched
r = s.post(schedURL, {'Page':'SSR_SSENRL_LIST'})

print(r.text)