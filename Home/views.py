from django.shortcuts import render, redirect,HttpResponse
from django.contrib import messages
from .models import *
from .utils import *
from .forms import *
import requests, json


genere = {28:"Action",12:"Adventure",16:"Animation",35:"Comedy",80:"Crime",99:"Documentary",18:"Drama",10751:"Family",14:"Fantasy",36:"History",27:"Horror",10402:"Music",9648:"Mystery",10749:"Romance",878:"Science Fiction",10770:"TV Movie",53:"Thriller",10752:"War",37:"Western"}

# for hoge page preprocess start

ptitle = []
pid = []
prelease_date = []
prate = []
pposter = []
pbackdrop = []
pgenere = []
gid = []
def home_preprocess():

   alldata = requests.get('https://api.themoviedb.org/3/movie/popular?api_key=f38512c9e3eca768a4175a1560292553&language=en-US&page=1')
   alldata = alldata.json()
   for temp in alldata['results']:
    #   print(temp)
      ptitle.append(temp['title'])
      pid.append(temp['id'])
      prelease_date.append(temp['release_date'][0:4])
      prate.append(temp['vote_average'])
      pposter.append('https://image.tmdb.org/t/p/original'+temp['poster_path'])
      pbackdrop.append('https://image.tmdb.org/t/p/original'+temp['backdrop_path'])
      g = []
      gi = []
      for x in temp['genre_ids']:
         g.append(genere[x])
         gi.append(x)
      pgenere.append(g)
      gid.append(gi)

   
#    for (a, b,c,d,e) in zip(ptitle,pid,prelease_date,prate,pposter):
#       print(a,b,c,d,e)
#    for x in pgenere:
#       print(x)

# for hoge page preprocess END



# Create your views here.
def HomePage(request):
    home_preprocess()
    # Filter movies by search query
    Movies, search_query, serials = searchMovies_Serials(request)
   
    # Manage pagination bar
    custom_range, Movies = paginateMovies(request, Movies,9) # 9 post per page
    print(Movies)
    # get all genres for navbar
    Navbar_genre = Genre.objects.all()
    # get the most popular movies
    Most_views_movies = HomePageModel.objects.all().order_by('-page_view') 
    # get all serials
    Serials_new = Serial.objects.all()

    # send data
    # data = zip(pgenere,gid)
    fulldata = zip(ptitle,pid,pposter,prate,pgenere,gid,prelease_date)
    context ={
    'movies' : Movies, 'serials' : serials, 'popular' : Most_views_movies,
    'genres' : Navbar_genre, 'search_query' : search_query,
     'custom_range' : custom_range, 'new_serials' : Serials_new,'fulldata':fulldata
    }
    return render(request, 'Home/home.html', context)



# Single Serial Page
def SingleSerialPage(request, pk):
    # get serial object by id
    serial = Serial.objects.get(id=pk)
    # comments
    forms = CommentsFormSerial()
    if request.method == 'POST':
        form = CommentsFormSerial(request.POST)
        review = form.save(commit=False)
        review.serial_page = serial
        review.save()
        
        return redirect('single-serial', pk=serial.id)


    # count page view
    serial.page_view = serial.page_view + 1
    # get all movies for "New Movies"
    Movies = HomePageModel.objects.all()
    # get similar serials for "Similar Serials" section in front-end
    Similar_Serials = Serial.objects.all().distinct().filter(genre__in=serial.genre.all())
    # get all genres for navbar
    Navbar_genre = Genre.objects.all()
    # get all comments
    comments_all = serial.comments_serial.all()

    context = {
        'serial' : serial, 'similar' : Similar_Serials,
        'view' : serial.page_view, 'genres' : Navbar_genre,
        'movies' : Movies, 'comments_all' : comments_all, 'forms' : forms
    }
    return render(request, 'Home/single-serial.html', context)



# Single Movie Page
def SingleMoviePage(request, pk): #when we click on ant movie this function redirect to that perticular movie..
    # get movie object by id
    print("got id: ",pk)
    
    MovieDetails = requests.get(('https://api.themoviedb.org/3/movie/')+pk+('?api_key=f38512c9e3eca768a4175a1560292553&language=en-US'))
    MovieDetails = MovieDetails.json()

    print(MovieDetails)
    title = MovieDetails['title']
    print(title)
    return HttpResponse("This is Single Movie page")

    Movie = HomePageModel.objects.get(id=pk)
    # comments
    forms = CommentsForm()
    if request.method == 'POST':
        form = CommentsForm(request.POST)
        review = form.save(commit=False)
        review.movie_page = Movie
        review.save()

        return redirect('single-movie', pk=Movie.id)

    # count page view
    Movie.page_view = Movie.page_view + 1
    # get all movies for "New items" section in front-end 
    Movies = HomePageModel.objects.all()
    print(type(Movie.genre.all))
    # get similar movies for "Similar Movies" section in front-end
    Similar_Movies = HomePageModel.objects.all().filter(genre__in=Movie.genre.all()).distinct()
    # get all genres for navbar
    Navbar_genre = Genre.objects.all()
    # get all serials
    Serials = Serial.objects.all()
    # get all comments
    comments_all = Movie.comments.all()

    print("Hello trailer link: ")
    print(Movie.trailer)
    alldata = requests.get('https://api.themoviedb.org/3/movie/436270/videos?api_key=f38512c9e3eca768a4175a1560292553&language=en-US')
    alldata = alldata.json()
    key = ""

    #loop over the json data
    for temp in alldata['results']:
        # print(temp['key'])
        if(temp['type']=='Trailer' and temp['official']==True):
            print(temp['key'])
            key = temp['key']
            break

    print(alldata['results'][0]['key']) #hLTQxSyT3mc
    mval = 'youtube.com/watch?v='+key
    print(mval)
    # send all data
    context = {'movie' : Movie, 'movies' : Movies, 'similar' : Similar_Movies,
    'view' : Movie.page_view, 'genres' : Navbar_genre, 'serials' : Serials,
     'forms' : forms, 'comments_all' : comments_all,'tri':mval}
    return render(request, 'Home/single-movie.html', context)



# Single Genre Page
def SingleGenrePage(request, pk):
    # get genre object by id
    genre = Genre.objects.get(id=pk)
    # get movies by genre
    Movies_filtered = HomePageModel.objects.all().filter(genre=genre).distinct()
    # get serial by genre
    Serials_filtered = Serial.objects.all().filter(genre=genre).distinct()
    # Serial_Movies_filtered = HomePageModel.objects.all().filter(genre=genre).distinct(), Serial.objects.all().filter(genre=genre).distinct()
    # get all movies
    Movies = HomePageModel.objects.all()
    # get all genres for navbar
    Navbar_genre = Genre.objects.all()
    # get all serials
    Serials = Serial.objects.all()

    context = {'genre' : genre, 'movies_filtered' : Movies_filtered,
     'serials_filtered' : Serials_filtered, 'movies' : Movies, 
     'genres' : Navbar_genre, 'serials' : Serials}
    return render(request, 'Home/single-genre.html', context)
    


# Director
def SingleDirectorPage(request, pk):
    # director by id
    director = Director.objects.get(id=pk)
    # filter movies by director id
    Movies_filtered = HomePageModel.objects.all().filter(director=director).distinct()
    # get serial by genre
    Serials_filtered = Serial.objects.all().filter(director=director).distinct()
    # get all movies
    Movies = HomePageModel.objects.all()
    # get all genres for navbar
    Navbar_genre = Genre.objects.all()
    # get all serials
    Serials = Serial.objects.all()

    context = {'director' : director, 'movies_filtered' : Movies_filtered,
    'serials_filtered' : Serials_filtered, 'movies' : Movies, 
    'genres' : Navbar_genre, 'serials' : Serials}
    return render(request, 'Home/single-director.html', context)