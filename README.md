![Header](/brand%20assets/KABOOM.png)
<h1><b>Kaboom</b></h1>

## What is Kaboom?
The best way to explain what Kaboom is meant to be is the 'Trakt of comics and cartoons' - a comic tracker/database. Currently its just a skeleton, the only way to interface with the database is through the Django API - there is no frontend. Hopefully in the future there will be multiple different clients built off of the API, abit like Trakt. The database includes metadata for comics and cartoons, as well as some user accounts functionality.

## Note
There is currently nothing in the database, the documentation is still a WIP (https://kaboom.readthedocs.io/en/latest/), and the production server is not yet live.

## Developer Notes

While testing your client, please make sure to only use the staging server, located here: https://staging-kaboom.herokuapp.com/v1

You can also download the Postman collection here, which is pre-configured with the staging url and a demo user access token: https://github.com/crxssed7/kaboom-api/blob/master/KABOOM.postman_collection.json

Any data uploaded to the staging database does not persist and will be refreshed frequently.
