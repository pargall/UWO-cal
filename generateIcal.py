import requests
import icalendar
import sys
import datetime
from lxml import html

reload(sys);
sys.setdefaultencoding("utf8") #Page uses UTF

class Course:
	name = ""
	sections = []

	def __init__(self, n):
		self.name = n
		sections = []

class Section:
	name =""
	location = ""
	startDateTime = 0
	endDateTime =0
	lastClass = 0

	def __init__(self, _name, _location, _startDateTime, _endDateTime, _lastClass):
		self.name = _name
		self.location = _location
		self.startDateTime = _startDateTime
		self.endDateTime = _endDateTime
		self.lastClass = _lastClass

	def __repr__(self):
		return self.name + ", Location: " + self.location + " start Time: " + str(self.startDateTime) + " End Time: " + str(self.endDateTime)


def uwoDaytoWeekDay(day):
	if day == "Mo":
		return 1
	elif day == "Tu":
		return 2
	elif day == "We":
		return 3
	elif day == "Th":
		return 4
	elif day == "Fr":
		return 5

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
	#print name[0].text
	c = Course(name[0].text) 

	#Find the sections we're signed uo for
	sections =  course.xpath("descendant::tr[starts-with(@id,'trCLASS_MTG_VW$')]")

	typeClass  = ""
	for s in sections:
		col = s.xpath("descendant::span[@class = 'PSEDITBOX_DISPONLY']")

		#We only want to grab the type of class because of the way the table is rendered
		if col[1].text.strip() != "":
			typeClass  = col[1].text

		#get the Date
		#Note this is the start and end date of the term, not the course 
		startDate = datetime.datetime.strptime(col[len(col)-1].text[0:10], "%Y/%m/%d")
		
		recurEndDate = datetime.datetime.strptime(col[len(col)-1].text[13:23], "%Y/%m/%d")

		#Get The times
		times = col[len(col)-3].text;

		#Get the day of the week
		day = uwoDaytoWeekDay(times[0:2])
		
		#Check to see if the start times hour is 1 digit and pad it
		if(times[4] == ':'):
			startTime = '0' + times[3:9];
			if(times[13] == ':'):
				endTime = '0' + times[12:18]
			else:
				endTime = times[12:19]
		else:
			startTime = times[3:10];
			if(times[14] == ':'):
				endTime = '0' + times[13:19]
			else:
				endTime = times[13:20]
		startTime = datetime.datetime.strptime(startTime, "%I:%M%p")
		endTime = datetime.datetime.strptime(endTime, "%I:%M%p");
		
		#adjust the start day to line up with the day the course starts(rather the when the term starts)
		while (startDate.isoweekday() != day):
			startDate = startDate + datetime.timedelta(days=1)

		#Figure out the DateTime of the course
		startDateTime = startDate + (startTime - datetime.datetime(1900, 1, 1))
		endDateTime = startDateTime + (endTime-startTime)

		#get Location
		location = col[len(col)-2].text


		c.sections.append(Section(typeClass, location, startDateTime, endDateTime, recurEndDate))

	courseList.append(c)
	#print name[0].text