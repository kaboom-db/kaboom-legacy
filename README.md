![Header](/brand%20assets/KABOOM.png)
<h1><b>Kaboom</b></h1>

## What is Kaboom?
The best way to explain what Kaboom is meant to be is the 'Trakt of comics and cartoons' - a comic tracker/database. Currently its just a skeleton, the only way to interface with the database is through the Django API - there is a limited frontend. Hopefully in the future there will be multiple different clients built off of the API, abit like Trakt. The database includes metadata for comics and cartoons, as well as some user accounts functionality.

## Note
Kaboom has always just been a hobby project for me. I don't have a lot of experience with web technologies and I'm still learning Django (a lot of the code in this project will need refactoring later down the line). I've never deployed a project this big, so I've decided to gain experience first with other cloud platforms before I bother deploying Kaboom. If the project gains more attention maybe then I will look at deploying.

Kaboom is in a deployable state, if you want to use it you can [host it yourself](#self-hosting-kaboom) - when it comes to actually making Kaboom go live I'll probably write a script to import user data to the live server.

## Self hosting Kaboom
Instructions on how to self host Kaboom will be coming soon.

## Developer Notes

If you want to make a client for Kaboom but don't want to go through the hassle of self hosting it, you can use the demo/staging server located here: https://staging-kaboom.herokuapp.com/v1. This is just a slimmed down version of Kaboom with limited functionality.

You can also download the Postman collection here, which is pre-configured with the staging url and a demo user access token: https://github.com/crxssed7/kaboom-api/blob/master/KABOOM.postman_collection.json

Any data uploaded to the staging database does not persist and will be refreshed frequently.

Documentation coming soon.