# views.py

import json
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponseNotAllowed, HttpResponseNotFound
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from .forms import RegistrationForm, AddToRankingForm
from django.contrib.auth import logout
from django.core.mail import send_mail
import requests
from django.core.paginator import Paginator
from .models import Movie, UserRanking, RankedMovie
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import F

def home(request):
    api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZTZkMDVjNGRlOTE4NzNiY2Y3Y2JjMGExYjM3MDVmOCIsInN1YiI6IjY0NmY5Nzk1NTQzN2Y1MDEwNTVjZDQyOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.GU8f9Wsj9uwCiVcRjZQT9eGvzfSbsz4zG_dfPUQqPyY'
    url_trending = "https://api.themoviedb.org/3/trending/all/day?language=en-US"
    url_search = "https://api.themoviedb.org/3/search/movie?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    page = request.GET.get('page', 1)  # Get the page number from the request parameters (default: 1)
    search_query = request.GET.get('search', '')
    results_per_page = 6  # Number of movies to fetch per page
    
    if search_query:
        payload = {'query': search_query}
        response = requests.get(url_search, headers=headers, params=payload)
    else:
        response = requests.get(url_trending, headers=headers)
        #search_query = None  # Reset search query to None
    
    data = response.json()
    movies = data.get('results', [])

    paginator = Paginator(movies, results_per_page)
    page_obj = paginator.get_page(page)
    return render(request, 'home.html', {'movies': page_obj, 'search_query': search_query})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            
            # Send registration confirmation email
            subject = 'Registration Confirmation'
            message = 'Thank you for registering to our website! \n You can now log in to your account.'
            from_email = 'movie.ranking@yahoo.com'
            to_email = form.save().email
            send_mail(subject, message, from_email, [to_email])
            
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})

def my_account(request):
    return render(request, 'my_account.html')

def logout_user(request):
    logout(request)
    return redirect('home')

@login_required
def my_account(request):
    # Pobierz lub utwórz ranking użytkownika
    user_ranking, created = UserRanking.objects.get_or_create(user=request.user)

    ranked_movies = RankedMovie.objects.filter(ranking=user_ranking).order_by('position')
    
    # Fetch movie details from the TMDB API
    api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZTZkMDVjNGRlOTE4NzNiY2Y3Y2JjMGExYjM3MDVmOCIsInN1YiI6IjY0NmY5Nzk1NTQzN2Y1MDEwNTVjZDQyOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.GU8f9Wsj9uwCiVcRjZQT9eGvzfSbsz4zG_dfPUQqPyY'
    movies_with_details = []
    headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZTZkMDVjNGRlOTE4NzNiY2Y3Y2JjMGExYjM3MDVmOCIsInN1YiI6IjY0NmY5Nzk1NTQzN2Y1MDEwNTVjZDQyOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.GU8f9Wsj9uwCiVcRjZQT9eGvzfSbsz4zG_dfPUQqPyY"
    }

    for ranked_movie in ranked_movies:
        movie_id = ranked_movie.movie_id
        url = f'https://api.themoviedb.org/3/movie/{movie_id}'
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            movie_details = json.loads(response.content)
            # Add the movie details to the list
            movies_with_details.append({
                'title': movie_details['title'],
                'overview': movie_details['overview'],
                'poster_path': movie_details['poster_path'],
                'position': ranked_movie.position
            })
    
    context = {
        'movies': movies_with_details
    }

    return render(request, 'my_account.html', context)

@login_required
def user_ranking(request):
    user_ranking = UserRanking.objects.get_or_create(user=request.user)[0]
    ranked_movies = RankedMovie.objects.filter(ranking=user_ranking)
    context = {
        'user_ranking': user_ranking,
        'ranked_movies': ranked_movies
    }
    return render(request, 'my_account.html', context)

@login_required
def add_movie_to_ranking(request, movie_id):
    if request.method == 'POST':
        position = int(request.POST.get('position'))
        user_ranking = UserRanking.objects.get_or_create(user=request.user)[0]
        
    try:
        ranked_movie = RankedMovie.objects.get(ranking=user_ranking, movie_id=movie_id)
        
        if ranked_movie.position != position:
            # Case 3: Movie is already in the ranking at a specific position and changing position
            if RankedMovie.objects.filter(ranking=user_ranking, position=position).exists():
                # Move movies between the old and new positions up or down depending on the direction
                if ranked_movie.position < position:
                    RankedMovie.objects.filter(ranking=user_ranking, position__gt=ranked_movie.position, position__lte=position).update(position=F('position') - 1)
                else:
                    RankedMovie.objects.filter(ranking=user_ranking, position__lt=ranked_movie.position, position__gte=position).update(position=F('position') + 1)

            ranked_movie.position = position
            ranked_movie.save()
    except RankedMovie.DoesNotExist:
        # Case 1: Movie is not in the ranking and the position is available
        if not RankedMovie.objects.filter(ranking=user_ranking, position=position).exists():
            RankedMovie.objects.create(ranking=user_ranking, movie_id=movie_id, position=position)
        else:
            # Case 2: Movie is not in the ranking, but another movie is at the specified position
            existing_movie = RankedMovie.objects.get(ranking=user_ranking, position=position)
            RankedMovie.objects.filter(ranking=user_ranking, position__gte=position).update(position=F('position') + 1)
            RankedMovie.objects.create(ranking=user_ranking, movie_id=movie_id, position=position)

    return redirect('my_account')

def edit_profile(request):
    return render(request, 'edit_profile.html')

@login_required
def delete_account(request):
    if request.method == 'POST':
        # Delete the user account
        request.user.delete()
        messages.success(request, 'Your account has been deleted.')
        # Send a confirmation email before deleting the account
        subject = 'Confirmation for Account Deletion'
        message = 'Your account deletion request has been received. Your account has been deleted'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [request.user.email]
        send_mail(subject, message, from_email, to_email)
        return redirect('home')  # Redirect to the home page or another page
    return render(request, 'delete_account.html')  # Display a confirmation page

@login_required
def remove_movie(request, position):
   if request.method == 'POST':
        user_ranking = get_object_or_404(UserRanking, user=request.user)

        try:
            ranked_movie = RankedMovie.objects.get(ranking=user_ranking, position=position)

            # Delete the ranked movie
            ranked_movie.delete()

            # Update positions of movies below the deleted movie
            RankedMovie.objects.filter(ranking=user_ranking, position__gt=position).update(position=F('position') - 1)

        except RankedMovie.DoesNotExist:
            # Handle the case where the movie is not in the ranking
            pass

        return redirect('my_account')