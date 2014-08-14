import requests
import icalendar
from datetime import date
from lxml import html

class Course:
	name = ""
	sections = []

	def __init__(self, n):
		name = n

class Section:
	name =""
	times = []
	startDate = date.today()
	endDate = date.today()

courseList = []
userName = "PARGALL2"
password = '***'

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


tree = html.fromstring(r.text)
courses = tree.xpath("//div[starts-with(@id,'win0divDERIVED_REGFRM1_DESCR20$')]")

#Parse the raw HTML into objects
for course in courses:
	#Get the course title
	name = course.xpath("descendant::td[@class = 'PAGROUPDIVIDER']")
	c = Course(name[0].text) 

	#Find the sections we're signed uo for
	sections =  course.xpath("descendant::tr[starts-with(@id,'trCLASS_MTG_VW$')]")

	#print sections

	for s in sections:
		col = s.xpath("descendant::td/div/span")
		for c in col:
			try:
				print c.text
			except Exception, e:
				pass			
	#print name[0].text

#print courses
#parser = ScheduleParser()
#parser.feed(r.text)