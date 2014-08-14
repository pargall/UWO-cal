import requests
import icalendar
import sys
from datetime import date
from lxml import html

reload(sys);
sys.setdefaultencoding("utf8") #Page uses UTF

class Course:
	name = ""
	sections = []

	def __init__(self, n):
		name = n

class Section:
	name =""
	location = ""
	startTime = 0
	endTime =0
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
	typeClass  = ""
	for s in sections:
		currentSection = Section()

		col = s.xpath("descendant::span[@class = 'PSEDITBOX_DISPONLY']")

		#We only want to grab the type of class because of the way the table is rendered
		if col[1].text.strip() != "":
			typeClass  = col[1].text
		print typeClass

		#Get The times
		print col[len(col)-3].text

		#get the Date
		print col[len(col)-1].text

		#get Location
		print col[len(col)-2].text
	#print name[0].text

#print courses
#parser = ScheduleParser()
#parser.feed(r.text)