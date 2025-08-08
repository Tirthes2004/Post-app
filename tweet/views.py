from django.views.decorators.http import require_POST
import json
from django.shortcuts import render, get_object_or_404, redirect
from .forms import TweetForm, CommentForm  # ✅ Importing forms correctly
from .models import Tweet, Like, Comment # ✅ Capitalized model name
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
import os




# posts/tweet/views.py

from django.shortcuts import render
from .models import Tweet

# def tweet_list(request):
#     # grab the raw search term (or empty string)
    # q = request.GET.get('q', '').strip()

    # if q:
    #     # filter tweets whose author’s username contains q (case-insensitive)
    #     tweets = (
    #         Tweet.objects
    #              .filter(user__username__icontains=q)
    #              .order_by('-created_at')
    #     )
    # else:
    #     # no search → show all
    #     tweets = Tweet.objects.all().order_by('-created_at')

    # return render(request, 'tweet_list.html', {
    #     'tweets': tweets,
    #     'q': q,    # so we can prefill the search box
    # })


@login_required
def tweet_list(request):
    q = request.GET.get('q', '').strip()

    if q:
        tweets = Tweet.objects.filter(user__username__icontains=q).order_by('-created_at')
    else:
        tweets = Tweet.objects.all().order_by('-created_at')

    liked_ids = set(
        Like.objects.filter(user=request.user, tweet__in=tweets)
                    .values_list('tweet_id', flat=True)
    )

    return render(request, 'tweet_list.html', {
        'tweets': tweets,
        'liked_ids': liked_ids,
        'q': q,
    })



@login_required
def tweet_create(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            new_tweet = form.save(commit=False)
            new_tweet.user = request.user  # Make sure user is authenticated
            new_tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()
    
    return render(request, 'tweet_form.html', {'form': form})


@login_required
def tweet_edit(request, tweet_id):
    tweet_instance = get_object_or_404(Tweet, id=tweet_id, user=request.user)  # ✅ Capitalized model
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet_instance)
        if form.is_valid():
            updated_tweet = form.save(commit=False)
            updated_tweet.user = request.user
            updated_tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet_instance)
    
    return render(request, 'tweet_form.html', {'form': form, 'tweet': tweet_instance})


@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    if tweet.user != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')  # or wherever you want to go after deletion


@login_required
def user_profile(request):
    user_posts = Tweet.objects.filter(user=request.user).order_by('-id')  # or .created_at if you have
    return render(request, 'profile.html', {'tweets': user_posts})




@login_required
def like_toggle(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    liked = Like.objects.filter(tweet=tweet, user=request.user)
    if liked.exists():
        liked.delete()
        status = 'unliked'
    else:
        Like.objects.create(tweet=tweet, user=request.user)
        status = 'liked'
    return JsonResponse({'status': status, 'likes_count': tweet.likes.count()})

@login_required
def add_comment(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)

    # Django will populate request.POST from FormData
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.tweet = tweet
        comment.user  = request.user
        comment.save()
        return JsonResponse({
            'id': comment.id,
            'user': comment.user.username,
            'content': comment.content,
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M'),
        })
    return JsonResponse({'errors': form.errors}, status=400)


def view_comments(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)

    # all commenter usernames (may include users who also liked)
    commenters = (
        tweet.comments
             .values_list('user__username', flat=True)
             .distinct()
    )

    # all liker usernames (may include users who also commented)
    likers = tweet.likes.values_list('user__username', flat=True)


    return render(request, 'comment.html', {
        'tweet': tweet,
        'comments': tweet.comments.order_by('created_at'),
        'commenters': sorted(commenters),
        'likers':    sorted(likers),
    })

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        # ← Add this block
        if request.content_type == 'application/json':
            import json
            data = json.loads(request.body)
        else:
            data = request.POST

        form = CommentForm(data, instance=comment)
        if form.is_valid():
            form.save()
            return JsonResponse({'content': comment.content})
        return JsonResponse({'errors': form.errors}, status=400)

    return JsonResponse({'error': 'Invalid method'}, status=405)



@login_required
@require_POST
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user != request.user:
        return HttpResponseForbidden()
    comment.delete()
    return JsonResponse({'deleted': True})
