import urllib
import urllib2
from bs4 import BeautifulSoup
from dateutil.parser import parse
import sys

def get_redirected_url(url):
    opener = urllib2.build_opener(urllib2.HTTPRedirectHandler)
    request = opener.open(url)
    return request.url

url = "https://finalexams.rutgers.edu/"

def getFinalDate(index):
	values = {"degree_level":"U","campus":"nb","subject": "","course": "","index": index}
	data = urllib.urlencode(values)
	newUrl = get_redirected_url("%s?%s"%(url, data))
	response = urllib2.urlopen(newUrl)
	html = response.read()
	soup = BeautifulSoup(html, 'html.parser')
	dates = []
	for tr in soup.find_all('tr')[1:]:
		tds = tr('td')
		if len(tds) >= 4:
			dates.append({'index': str(tds[0].string), 'date': str(tds[-1].string)})
	indexedDates = [date for date in dates if date['index'] == index]
	if len(indexedDates) > 0:
		dateIndexSplit = indexedDates[0]['date'].index(':')
		date = indexedDates[0]['date'][:dateIndexSplit].strip()
		times = indexedDates[0]['date'][dateIndexSplit + 1:].split('-')
		return { 'date': parse(date), 'startTime': parse("%s %s"%(date, times[0].strip())), 'endTime': parse("%s %s"%(date, times[1].strip())) }
	return None

if __name__ == "__main__":
	if len(sys.argv) > 1:
	    print getFinalDate(sys.argv[1])
	else:
		prinProgFinal = getFinalDate("13150")
		print prinProgFinal

