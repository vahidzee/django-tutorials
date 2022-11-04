# # Uncomment all of the lines below once you have created your tweet model in dwitter/apps/tweets/models.py
# # to start working on the admin configuration for the tweet model
# from django.contrib import admin

# # Register the Tweet model with the admin site
# # This will allow us to view and edit the tweets in the admin site
# # https://docs.djangoproject.com/en/4.1/ref/contrib/admin/
# from .models import Tweet
# from django.contrib import admin



# # create inline model admin for the reply_to field
# # https://docs.djangoproject.com/en/4.1/ref/contrib/admin/#django.contrib.admin.TabularInline
# class RepliesInline(admin.StackedInline):
#     # We specify the model that we want to create a admin inline form from
#     model = Tweet
#     # we want inline editing of the replies (i.e. we want to be able to edit the replies from the tweet detail page)
#     # see https://docs.djangoproject.com/en/4.1/ref/contrib/admin/#django.contrib.admin.StackedInline
#     # therefore, we set the foreign key field (fk_name) to "reply_to"
#     # ADDITION: set fk_name to "reply_to"


#     # "Reply" and "Replies" should be the verbose name
#     verbose_name = "Reply"
#     verbose_name_plural = "Replies"

#     # By default, we only show 1 inline form, we can change this by setting the extra attribute
#     # ADDITION: set extra attribute to 1

   


# # configurate the tweet list view in the admin site to show the tweet text and the username of the user who posted the tweet
# # https://docs.djangoproject.com/en/4.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display
# class TweetAdmin(admin.ModelAdmin):
#     # We specify the model that we want to create a admin page from
#     model = Tweet

#     # We specify the fields that we want to show in the list view of the admin page by setting the list_display attribute
#     # see https://docs.djangoproject.com/en/4.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display
#     # ADDITION: set list_display to "text" and "user", "uploaded_at" and "reply_to"

    
#     # We can set the fields that are clickable to link to the detail view of the tweet by setting the list_display_links attribute
#     # see https://docs.djangoproject.com/en/4.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display_links
#     # ADDITION: set list_display_links to "text"


#     # We can set the fields that we can search for by setting the search_fields attribute
#     # see https://docs.djangoproject.com/en/4.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.search_fields
#     # ADDITION: set search_fields to "text" and "user__username" (i.e. the username of the user who posted the tweet)

#     # We can add inline forms to the tweet detail view by setting the inlines attribute
#     # ADDITION: set inlines to "RepliesInline" (it should be a list of the class objects of the inline models) 


# # register the TweetAdmin class with the admin site
# admin.site.register(Tweet, TweetAdmin)