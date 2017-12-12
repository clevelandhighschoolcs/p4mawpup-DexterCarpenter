#
# Web Scraper
# Version: 8

"""
cd C:\Users\Dexter Carpenter\Documents\GitHub\WebScraper\environment

c:\Python27\Scripts\virtualenv.exe -p C:\Python27\python.exe .lpvenv

.lpvenv\Scripts\activate

# on at home computer:

cd C:\Users\dexte\Documents\GitHub\WebScraper\environment

"""

# import libraries
import urllib2
from bs4 import BeautifulSoup
import time
from twilio.rest import Client

#variables
global tagcountnow
global tagcountold
global scrape_interval
global Twillo_null #a variable that will determine the functionality of Twillo in this program
Twillo_null = False
global account_sid 
global auth_token
global twilio_phone_number
global my_phone_number

print ''
print "Press 'Ctrl + C' to exit the Scraper"

# specify the url
print 'Enter what website you want to scrape:'
quote_page = raw_input()
try:
	webUrl = urllib2.urlopen(quote_page)
	if(webUrl.getcode() == 200):
		quote_page = '%s' %quote_page
	else:
		code = webUrl.getcode()
except Exception:
	quote_page = raw_input('Enter a valid website: ')

print ''

print 'How often do you want to scrape the webpage? (seconds)'
scrape_interval = raw_input()

print ''
#These next 20 lines have to do with Twillo and allowing that to work
print ' '
print "Would you like me to send you a text message when I find a change(y/n)? (You will need to gave a twillo number for this to work.)"
txtmessage = raw_input()
if txtmessage == "y":
	print ' '
	print 'Enter your account SID (all of the following can be obtained on your Twillo dashboard)'
	account_sid = raw_input() 
	
	print ' '
	print 'Enter your authentification token'
	auth_token = raw_input()

	print ' '
	print 'Enter your Twillo phone number'
	twilio_phone_number = raw_input()
	if (twilio_phone_number[:2] != "+1"): #this ensures a "+1" is given at the beginning of the phone number
		twilio_phone_number = "+1" + twilio_phone_number
	
	print ' '
	print "Enter your own phone number"
	my_phone_number = raw_input()
	if (my_phone_number[:2] != "+1"): #this ensures a "+1" is given at the beginning of the phone number
		my_phone_number = "+1" + my_phone_number
	
	#This makes sure that the info inputted is valid, if not, it skips this part.
	if (len(account_sid) != 34) or (len(auth_token) != 32) or (len(twilio_phone_number) != 12) or (len(my_phone_number) != 12) or (twilio_phone_number[:2] != "+1") or (my_phone_number[:2] != "+1"):
		Twillo_null = True #if this is triggered, the program will refrain from doing anything with the information given above
		
else:
	Twillo_null = True

print 'The Scraper will check the number of tags in the webpage.'
print 'The Scraper will display "Change!" if the number of tags has changed from the previous scan.'

print ''

print 'Scraping...'

#get the initial count for tags
def initial():
	global tagcountnow
	global tagcountold
	
	# query the website and return the html to the variable page
	page = urllib2.urlopen(quote_page)

	# parse the html using beautiful soup and store in variable 'soup'
	soup = BeautifulSoup(page, 'html.parser')

	#find number of tags
	tagcountold = len(soup.find_all())

if __name__ == "__main__":
        initial()

def scraper():
	global tagcountnow
	global tagcountold
	global Twillo_null
	global account_sid 
	global auth_token
	global twilio_phone_number
	global my_phone_number

    # query the website and return the html to the variable page
	page = urllib2.urlopen(quote_page)
    
    # parse the html using beautiful soup and store in variable 'soup'
	soup = BeautifulSoup(page, 'html.parser')
	
	#find number of tagss
	tagcountnow = len(soup.find_all())
	
	if tagcountnow == tagcountold:
		print 'No Change'
		body = 'No Change'
	elif tagcountnow != tagcountold:
		print 'Change!'
		body = 'Change!'
	tagcountold = tagcountnow
	
	#This sends the message to your phone
	if Twillo_null == False:
		client = Client(account_sid, auth_token)
		client.messages.create(
			body=body,
			to=my_phone_number,
			from_=twilio_phone_number
		)
	

while True:
	
    if __name__ == "__main__":
        scraper()
    
    time.sleep(float(scrape_interval))
