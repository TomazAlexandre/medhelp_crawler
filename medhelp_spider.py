from urllib.request import urlopen as uo
from urllib.error import HTTPError as he, URLError as ue
from bs4 import BeautifulSoup as bs
from question import Question, Answer

def fetch_url(url):
	web_client = uo(url)
	try:
		web_page = web_client.read()
	except he:
		raise he('http error occurred')
	except ue:
		raise ue('http error occurred')
	else:
		return web_page
	finally:
		web_client.close()

def handle_req_tries(url, max_tries):
	for i in range(max_tries):
		web_page = fetch_url(url)
		if type(web_page) is not (he or ue):
			return web_page
		else:
			print('error trying to fetch '+url+', trying again... ('+str(i)+' of'+max_tries+')')
	raise ConnectionError('required url didn\'t respond')

#def extract_topics(url, max_tries):
#	links_list = []
#	web_page = handle_req_tries(url, max_tries)
#	if type(web_page) is ConnectionError:
#		raise ConnectionError('unable to connect to '+url)
#	souped_page = bs(web_page, 'html.parser')
#	for link in souped_page.findAll('div', {'class' : 'forums_link'}):
#		print('colecting topic '+ link.find('a')['href'])
#		links_list.append(link.find('a')['href'])
#	return links_list

def extract_links(max_pages, url_base):
	
	max_tries = 3
	page = 1
	links_list = []
	
	while page <= max_pages:
		web_page = handle_req_tries(url_base+'?page='+str(page), max_tries)
		if type(web_page) is ConnectionError:
			raise ConnectionError('unable to connect to '+url)

		souped_page = bs(web_page, 'html.parser')
		for link in souped_page.findAll('div', {'class' : 'fonts_resizable_subject subject_title hn_16b'}):
			print('colecting link '+ link.find('a')['href'])
			links_list.append(link.find('a')['href'])
		page+=1
	return links_list

def get_question_links(url_base, max_tries, file_name):
	with open(file_name) as f:
		content = f.readlines()
	content = [x.strip() for x in content]
	f.close()

	questions = []
	for link in content:
		questions.append(get_question(max_tries, url_base+link))

	for question in questions:
		print(question.title)

def get_question(max_tries, link):
	web_page = handle_req_tries(link, max_tries)
	if type(web_page) is ConnectionError:
			raise ConnectionError('unable to connect to '+url)
	souped_page = bs(web_page, 'html.parser')
	answers = []
	for answer in souped_page.find('div', {'id' : 'post_answer_body'}).findAll('div', {'class' : 'post_entry_right'}):
		post_id = answer.find('div', {'class' : 'post_message'})['data-post_id']
		ans = Answer(answer.find('a')['id']
			, answer.find('a')['href']
			, answer.find('div', {'class', 'post_message'}).contents[0].strip()
			, answer.find('div', {'class', 'subj_info os_14 '}).find('span')['data-timestamp']
			, answer.find('span', {'id' : 'user_rating_count_Post_'+post_id}).contents[0])
		answers.append(ans)

	question = Question(souped_page.find('div', {'class': 'question_title hn_16b'}).contents[0].strip()
		, souped_page.find('div', {'class', 'subj_user os_12'}).find('a')['id']
		, souped_page.find('div', {'class', 'subj_user os_12'}).find('a')['href']
		, souped_page.find('div', {'class', 'post_message'}).contents[0].strip()
		, answers
		, souped_page.find('div', {'class', 'subj_info os_14 '}).find('span')['data-timestamp'])
	return question

def save_links():
	
	#url_base = 'http://www.medhelp.org'
	#url_topics = url_base+'/forums/list'
	max_tries = 3
	file_name = 'links.txt'
	
	#print('starting topics extraction in '+url_topics)
	#topicos = extract_topics(url_topics, max_tries)
	#print('ending topics extraction in '+url_topics)
	
	#if type(topicos) is ConnectionError:
	#	return 'unable to retrieve topics'
	
	#print('opening '+file_name)
	f = open(file_name, 'w')

	topicos = [
		'http://www.medhelp.org/forums/Cord-Blood/show/1218'
		, 'http://www.medhelp.org/forums/DNA---Paternity/show/1492'
		, 'http://www.medhelp.org/forums/Fertility---Infertility---IVF/show/96'
		, 'http://www.medhelp.org/forums/Postpartum-Depression-PPD/show/309'
		, 'http://www.medhelp.org/forums/Miscarriages/show/283'
		, 'http://www.medhelp.org/forums/Pregnancy-and-Parenting-Multiples/show/343'
		, 'http://www.medhelp.org/forums/Pregnancy-Relationships/show/1854'
		, 'http://www.medhelp.org/forums/Pregnancy--Trying-to-Conceive-TTC-/show/225'
		, 'http://www.medhelp.org/forums/Pregnancy-Age-35/show/89'
		, 'http://www.medhelp.org/forums/Pregnancy-Ages-18-24-/show/152'
		, 'http://www.medhelp.org/forums/Pregnancy-Ages-25-34/show/1503'
		, 'http://www.medhelp.org/forums/Pregnancy-Am-I-Pregnant/show/1076'
		, 'http://www.medhelp.org/forums/Pregnancy-Aug-2017-Babies/show/2178'
		, 'http://www.medhelp.org/forums/Pregnancy-Birth-Plan/show/1400'
		, 'http://www.medhelp.org/forums/Pregnancy-Dec-2017-Babies/show/2186'
		, 'http://www.medhelp.org/forums/Pregnancy-July-2017-Babies/show/2176'
		, 'http://www.medhelp.org/forums/Pregnancy-June-2017-Babies-/show/2174'
		, 'http://www.medhelp.org/forums/Pregnancy-May-2017-Babies/show/2172'
		, 'http://www.medhelp.org/forums/Pregnancy-Nov-2017-Babies/show/2184'
		, 'http://www.medhelp.org/forums/Pregnancy-Oct-2017-Babies/show/2182'
		, 'http://www.medhelp.org/forums/Pregnancy-Sep-2017-Babies/show/2180'
		, 'http://www.medhelp.org/forums/Pregnancy-Social/show/1541'
		, 'http://www.medhelp.org/forums/Pregnancy-Teen/show/1855'
		, 'http://www.medhelp.org/forums/Teen-Pregnancy-Concerns/show/259'
	]
	
	for topic in topicos:
		
		print('starting topics extraction in '+topic)
		links_list = extract_links(10, topic)
		print('ending topics extraction in '+topic)
		
		print('saving links in '+file_name)
		for link in links_list:
			f.write(link+'\n')
	
	print('closing '+file_name)
	f.close()

#save_links()
get_question_links('http://www.medhelp.org', 3, 'links.txt')