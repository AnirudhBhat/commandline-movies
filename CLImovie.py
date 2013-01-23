#! /usr/bin/env python

from __future__ import print_function
import urllib2
import json
import sys
import os
import time
import argparse
import cgi
import gdata.service
import gdata.youtube
import gdata.youtube.service


API_KEY = "c5b633xj3ats73tmf9cez333"

boxoffice_url = "http://api.rottentomatoes.com/api/public/v1.0"
movie_url = "http://api.rottentomatoes.com/api/public/v1.0/movies.json?apikey="
base_url = "http://api.rottentomatoes.com/api/public/v1.0/movies.json?apikey="

type = "/lists/movies/box_office.lson?apikey="

def youtube_trailer(title):
    client = gdata.youtube.service.YouTubeService()
    query = gdata.youtube.service.YouTubeVideoQuery()
    #cgi.escape(self.request.get('content')).encode('UTF-8')
    search_term = cgi.escape(title + "trailer").encode('UTF-8')


    query.vq = search_term
    query.max_results = '5'
    feed = client.YouTubeQuery(query)
    url = {}
    for entry in feed.entry:
        if entry.GetSwfUrl():
            url = cgi.escape(entry.GetSwfUrl()).encode('UTF-8')
            break
    return url



parser = argparse.ArgumentParser()
#parser.add_argument("-b","--boxoffice",help="displays current top boxoffice movies")
parser.add_argument("-m","--movie",help="displays information about entered movie")
parser.add_argument("-r","--ratings",help="displays rotten tomatoe's rating for movies present in your specified directory")
args = parser.parse_args()

#if args.boxoffice:
   
if args.movie:
    k = 0
    Title = args.movie.replace(' ','+')
    url = movie_url + API_KEY + '&q=' + Title
    #print (url)
    try:
        RT = json.loads(urllib2.urlopen(url).read())
        print ("title: ",RT['movies'][0]['title'])
        print ("year: ",RT['movies'][0]['year'])
        print ("mpaa-ratings: ",RT['movies'][0]['mpaa_rating'])
        print ("runtime: ",RT['movies'][0]['runtime'])
        print ("critics-consensus: ",RT['movies'][0]['critics_consensus'])
        print ("release date: ",RT['movies'][0]['release_dates']['theater'])
        print ("critics-rating: ",RT['movies'][0]['ratings']['critics_rating'])
        print ("critics-score: ",RT['movies'][0]['ratings']['critics_score'])
        print ("audience-rating: ",RT['movies'][0]['ratings']['audience_rating'])
        print ("audience-score: ",RT['movies'][0]['ratings']['audience_score'])
        print ("cast:")
        for j in RT["movies"][k]["abridged_cast"]:
            print(j["name"])
   	    print(j["characters"],end="\n\n\n")
        print (youtube_trailer(Title))
    except:
        pass


elif args.ratings:
    try:
        os.system('cd')
        mvname = os.listdir(sys.argv[2])
        #x = 0
        #y = (100/len(mvname))
        print ("downloading ratings,please wait.It may take couple of minutes")
    except:
        print (sys.argv[2])
        print ('make sure your directory name is correct')
        exit(0)


    def movie_ratings():
        try:
            movie_name = mvname[i].replace(' ','+')
            url = base_url + API_KEY + '&q=' + movie_name
        #print url
            RT = json.loads(urllib2.urlopen(url).read())
            criticsscore =  RT['movies'][0]['ratings']['critics_score']
            audiencescore = RT['movies'][0]['ratings']['audience_score']
            runtime = RT['movies'][0]['runtime']
            moviename = RT['movies'][0]['title']
            year = RT['movies'][0]['year']
            #global x 
            #global y
            #x = x + y
            #print ("%s" %(x),end=" ")
            return (criticsscore,audiencescore,runtime,moviename,year)
        except:
            #x = x + y
            #print ("%s"%(x),end=" ")
            pass          


    #start_time = time.time()
    
    a = [movie_ratings() for i in range(len(mvname))]

    print ('critics-rating'.ljust(30),end=" ")
    print ('audience-rating'.ljust(30),end=" ")
    print ('runtime'.ljust(30),end=" ")
    print ('moviename'.ljust(30),end=" ")
    print ('year')
    for i in range(len(a)):
        print()
        for j in range(5):
            try:
                print(str(a[i][j]).ljust(30),end=" ")
            except:
                pass
    #print (time.time() - start_time,"seconds")


else:
    url = boxoffice_url + type + API_KEY
    result = json.load(urllib2.urlopen(url))
    k=0
    z=0
    for i in result["movies"]:
        print(i["title"])
        print("SYNOPSIS",end="\n")
        print(i["synopsis"],end="\n")
        print("TRAILER",end="\n")
    #print(i["links"]["clips"],end="\n")
        print(youtube_trailer(title=i["title"]))
        print("CASTS",end="\n")
        for j in result["movies"][k]["abridged_cast"]:
            print(j["name"])
   	    print(j["characters"],end="\n\n\n")
    #for a in result["movies"]:
        print("CRITICS_RATING:",end="     ")
        print(result["movies"][z]["ratings"]["critics_rating"])
        print("CRITICS_SCORE:",end="      ")
        print(result["movies"][z]["ratings"]["critics_score"])
        print("AUDIENCE_RATING:",end="    ")
        print(result["movies"][z]["ratings"]["audience_rating"])
        print("AUDIENCE_SCORE:",end="     ")
        print(result["movies"][z]["ratings"]["audience_score"],end="\n\n\n")
        print("\t-----------------------------------------------------------")
    #print(i["abridged_cast"][j]["name"])
    #print(i["abridged_cast"][j]["characters"],end="\n\n\n") 
        z=z+1
        k=k+1
     

    
