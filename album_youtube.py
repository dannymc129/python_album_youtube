import json
import urllib2
import httplib2
import sys

#to convert unicode api results to string
def convert(input):
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

h = httplib2.Http()

userAgent = "dev"

url = "http://api.discogs.com/"

resp, content = h.request(url + "database/search?q=coheed&type=artist", 
    headers={'Content-Type':'application/json', 'User-Agent' : userAgent} )


artists = convert(json.loads(content))['results']

for position, artist in enumerate(artists):
	print str(position) + ") " + artist['title'] 

artist_pos = raw_input("Selection from above artists: ")

artistUrl = convert(json.loads(content))['results'][int(artist_pos)]['resource_url']

resp, content = h.request(artistUrl, 
    headers={'Content-Type':'application/json', 'User-Agent' : userAgent} )


releasesUrl = convert(json.loads(content))['releases_url']

resp, content = h.request(releasesUrl, 
    headers={'Content-Type':'application/json', 'User-Agent' : userAgent} )

releases = convert(json.loads(content))['releases']

for position,release in enumerate(releases):
	if "type" in release and release['type'] == 'master':
		if "role" in release and release['role'] == "Main":
			print str(position) + ") " + release['title']

release_pos = raw_input("Select release")

releaseUrl = releases[int(release_pos)]['resource_url']

resp, content = h.request(releaseUrl, 
    headers={'Content-Type':'application/json', 'User-Agent' : userAgent} )

print "Track Listing: "

tracks = convert(json.loads(content))['tracklist']

for track in tracks:
    print track['position'] + ") " + track['title'] + ' - ' + track['duration']
