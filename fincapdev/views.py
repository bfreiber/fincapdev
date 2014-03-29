from django.shortcuts import render, redirect
import oauth2 as oauth
import urlparse
import urllib2
import json
import xml.etree.ElementTree as ET
import stripe
from django.core.context_processors import csrf

########## PAGES ##########

def landing(request):
    return render(request, 'landing.html')

#def dashboard(request):
#	return render(request, 'dashboard.html')

def network_view(request):
	return render(request, 'network_view.html')

########## FUNCTIONS ##########

########## LINKEDIN ##########
CONSUMER_KEY = '***REMOVED***'
CONSUMER_SECRET = '***REMOVED***'
CONSUMER = oauth.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
CLIENT = oauth.Client(CONSUMER)
USER_TOKEN = '***REMOVED***'
USER_SECRET = '***REMOVED***'
ETURN_URL = 'http://localhost:5000'
PREDEFINED_STATE = 'DCEEFWF45453sdffef424' #NEEDS TO BE UPDATED


def linkedinauthentication(request):
	API_KEY = CONSUMER_KEY
	STATE = PREDEFINED_STATE
	REDIRECT_URI = request.build_absolute_uri('dashboard')
	redirect_url = "https://www.linkedin.com/uas/oauth2/authorization?response_type=code&client_id=%s&state=%s&redirect_uri=%s" % (API_KEY, STATE, REDIRECT_URI)
	return redirect(redirect_url)

def dashboard(request):
	current_url = request.get_full_path()
	authorization_code_position = current_url.find('code=')
	state_position = current_url.find('&state=')
	authorization_code = current_url[authorization_code_position+5:state_position]
	state = current_url[state_position+7:]
	if state == PREDEFINED_STATE:
		AUTH_CODE = authorization_code
	        REDIRECT_URI = request.build_absolute_uri('dashboard')
		API_KEY = CONSUMER_KEY
		SECRET_KEY = CONSUMER_SECRET
		post_url = "https://www.linkedin.com/uas/oauth2/accessToken?grant_type=authorization_code&code=%s&redirect_uri=%s&client_id=%s&client_secret=%s" % (AUTH_CODE, REDIRECT_URI, API_KEY, SECRET_KEY)
		data = {} #Empty dictionary so urllib2.Request performs a POST rather than GET request
		req = urllib2.Request(post_url, data)
		response = urllib2.urlopen(req)
		the_page = response.read()
		json_response_object = json.loads(the_page)
		access_token = json_response_object['access_token']
		ready_access_token = 'oauth2_access_token='+access_token

		########## CONNECTIONS ##########
		get_url = "https://api.linkedin.com/v1/people/~/connections?%s" % ready_access_token
		req = urllib2.Request(get_url)
		response = urllib2.urlopen(req)
		the_page = response.read()

		########## USABLE XML DOCUMENT ##########
		root = ET.fromstring(the_page)

		connections_list = []
		for i in range(len(root)):
			first_name = root[i][1].text
			last_name = root[i][2].text
			try:
				picture_url = root[i][4].text
			except:
				picture_url = ''
			connections_list.append([first_name, last_name, picture_url])

		########## FRIEND CONNECTION TEST ##########
		friends_using_app = []
		friend_test_list = [['Issac','Tsang'], ['Wabba', 'Dabba Dee Doo'], ['Justin', 'Warner'], ['Michelle', 'Winters'], ['Vi', 'Hoang'], ['Mark', 'Ramadan'], ['Walker', 'Williams'], ['Ali', 'Ozler'], ['Ben', 'Xiong'], ['Rachel', 'Katz'], ['Kelly', 'Knewton'], ['Amy', 'Radin'], ['Geoff', 'Judge']]

                try:
                    from test_data import friend_test_list 
                except ImportError, e:
                    print("No test_data.py data")
		for i in range(len(connections_list)):
			for friend in friend_test_list:
				if friend[0] == connections_list[i][0] and friend[1] == connections_list[i][1]:
					friends_using_app.append(connections_list[i])

		pic_1 = friends_using_app[0][2]
		pic_2 = friends_using_app[1][2]
		pic_3 = friends_using_app[2][2]
		pic_4 = friends_using_app[3][2]
		pic_5 = friends_using_app[4][2]
		pic_6 = friends_using_app[5][2]
		pic_7 = friends_using_app[6][2]
		pic_8 = friends_using_app[7][2]
		pic_9 = friends_using_app[8][2]
		pic_10 = friends_using_app[9][2]

		full_name_1 = friends_using_app[0][0]+' '+friends_using_app[0][1]
		full_name_2 = friends_using_app[1][0]+' '+friends_using_app[1][1]
		full_name_3 = friends_using_app[2][0]+' '+friends_using_app[2][1]
		full_name_4 = friends_using_app[3][0]+' '+friends_using_app[3][1]
		full_name_5 = friends_using_app[4][0]+' '+friends_using_app[4][1]
		full_name_6 = friends_using_app[5][0]+' '+friends_using_app[5][1]
		full_name_7 = friends_using_app[6][0]+' '+friends_using_app[6][1]
		full_name_8 = friends_using_app[7][0]+' '+friends_using_app[7][1]
		full_name_9 = friends_using_app[8][0]+' '+friends_using_app[8][1]
		full_name_10 = friends_using_app[9][0]+' '+friends_using_app[9][1]


		return render(request, 'dashboard.html',
			{'friends_using_app': friends_using_app,
			'pic_1': pic_1,
			'pic_2': pic_2,
			'pic_3': pic_3,
			'pic_4': pic_4,
			'pic_5': pic_5,
			'pic_6': pic_6,
			'pic_7': pic_7,
			'pic_8': pic_8,
			'pic_9': pic_9,
			'pic_10': pic_10,
			'full_name_1': full_name_1,
			'full_name_2': full_name_2,
			'full_name_3': full_name_3,
			'full_name_4': full_name_4,
			'full_name_5': full_name_5,
			'full_name_6': full_name_6,
			'full_name_7': full_name_7,
			'full_name_8': full_name_8,
			'full_name_9': full_name_9,
			'full_name_10': full_name_10})

########## STRIPE ##########
def stripepayment(request):
	if request.method == 'POST':
		stripe.api_key = 'sk_test_ZMGm2ZpPh1xYLhp2SFxdeYqD'

		#Get the credit card details submitted by the form
		token = request.POST['stripeToken']
		email_address = request.POST['stripeEmail']

		#Save customer in model

		# Create a Customer
		customer = stripe.Customer.create(
 			card=token,
 			plan="fincapdev",
  			email=email_address
		)
  		return render(request, 'dashboard.html')

#<form action="/stripepayment/" method="POST">
#			{% csrf_token %}
 # 			<script src="https://checkout.stripe.com/checkout.js" class="stripe-button" data-key="pk_test_zVrX6MQHWxIfaXvaA8Z4pNR4" data-amount="500" data-name="fincapdev" data-description="fincapdev hack subscription ($5.00/week)" data-image="tbd" data-shipping-address="true" data-label="fincapdev hack subscription" data-panel-label="Subscribe @">
  #			</script>
	#	</form>




