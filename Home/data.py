import requests, json

# class PopularMovie:
#    title = ""
#    director = ""
#    release_date = ""
#    short_intro = ""
#    IMDb_RATING = ""
#    genre = ""
#    poster = ""
#    movie_page_poster = ""
#    summary = ""
#    trailer = ""
#    download_link_1080 = ""
#    download_link_720 = ""
#    download_link_480 = ""
#    page_view = ""
#    created = ""
#    id = ""
#    def __init__(self):
#       # function to initialize the data variable
#       alldata = requests.get('https://api.themoviedb.org/3/movie/popular?api_key=f38512c9e3eca768a4175a1560292553&language=en-US&page=1')
#       alldata = alldata.json()
#       for temp in alldata['results']:
#          print("hello")

genere = {28:"Action",12:"Adventure",16:"Animation",35:"Comedy",80:"Crime",99:"Documentary",18:"Drama",10751:"Family",14:"Fantasy",36:"History",27:"Horror",10402:"Music",9648:"Mystery",10749:"Romance",878:"Science Fiction",10770:"TV Movie",53:"Thriller",10752:"War",37:"Western"}

ptitle = []
pid = []
prelease_date = []
prate = []
pposter = []
pbackdrop = []
pgenere = []
def home_preprocess():

   alldata = requests.get('https://api.themoviedb.org/3/movie/popular?api_key=f38512c9e3eca768a4175a1560292553&language=en-US&page=1')
   alldata = alldata.json()
   for temp in alldata['results']:
      print(temp)
      ptitle.append(temp['original_title'])
      pid.append(temp['id'])
      prelease_date.append(temp['release_date'][0:4])
      prate.append(temp['vote_average'])
      pposter.append('https://image.tmdb.org/t/p/original'+temp['poster_path'])
      pbackdrop.append('https://image.tmdb.org/t/p/original'+temp['backdrop_path'])
      g = []
      for x in temp['genre_ids']:
         g.append(genere[x])
      pgenere.append(g)

   
   for (a, b,c,d,e) in zip(ptitle,pid,prelease_date,prate,pposter):
      print(a,b,c,d,e)
   for x in pgenere:
      print(x)

home_preprocess()
print(pposter[0])
for i in range(len(ptitle)):
   print(ptitle[i])