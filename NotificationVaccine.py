import requests
import json
import datetime
import smtplib 

def sendMail(message):
	emails = ['******@**' , '******@gmail.com']
	
	for ids in emails:
		email = smtplib.SMTP('smtp.gmail.com', 587) 
		email.starttls()
		email.login("*******", "*******")
		email.sendmail("******", ids , message)
		email.quit() 


def processData(data,date):
	for dat in data:
		capacity = dat.get('available_capacity')	
		if capacity > 0:
			age_limit = dat.get('min_age_limit') 
			# print("Available on date " , date)
			# print("But age limit is ", age_limit)
			vaccine = dat.get('vaccine')
			
			if age_limit == 18 and str(vaccine) == 'COVAXIN':
				name = dat.get('name')
				address = dat.get('address')
				message = "\nThis mail is auto-generated. Vaccination is available at " + str(name) + ", " + str(address) + ".\nVACCINE - " + str(vaccine) + " for 18-44 , on " + str(date) + " ." + "\nAvailability : " + str(capacity) 
				sendMail(message)


baseUrl = "http://cdn-api.co-vin.in/api/"
Delhi = "v2/admin/location/districts/9"
APIdistrict = "v2/appointment/sessions/public/findByDistrict"

headers = {'User-agent': 'Mozilla/5.0'}
response = requests.get(baseUrl + Delhi, headers = headers)

if response.status_code == 200:
	district_details = json.loads(response.content)
	all_districts = district_details.get('districts')
	
	for districts in all_districts:
		dis_id = districts.get('district_id')
		if dis_id == 141 or dis_id == 145 or dis_id == 147 or dis_id == 148:
			for i in range (0,4):
				date = datetime.date.today() + datetime.timedelta(days=i)
				date = date.strftime('%d-%m-%Y')
				#print("Current date ",date)
				param = {'district_id' : str(dis_id), 'date' : date }
				resp = requests.get(baseUrl + APIdistrict, headers = headers,params = param).json()
				data = resp
				if (len(data.get('sessions')) > 0):
					processData(data.get('sessions'),date)

				











		





