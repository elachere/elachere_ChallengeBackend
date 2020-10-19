# ChallengeBackend

Your goal is to create an app using the [spotify web api](https://developer.spotify.com/documentation/web-api/). You can make for example a [Flask](https://flask.palletsprojects.com/en/1.1.x/) or [Django rest framework](https://www.django-rest-framework.org/) project, it has to be able to authenticate to Spotify to fetch the new releases. Your job is to add two new features:
- A way to fetch data from spotify’s new releases API (/v1/browse/new-releases) and persist in a Postgresql DB (mandatory)
- A route : `/api/artists/` returning a JSON containing informations about artists that have released new tracks recently, from your local copy of today’s spotify’s new releases.

## Install

- Make sure you have docker (and compose) installed and running
- at the root of the repo `docker-compose up -d --build`
- should be up and running

## How it works

- First, please authenticate by calling `http://localhost:5000/auth/authorization/` (don't forget `Content-Type: application/json` header)
- Then you can call `/api/artists/`. Actually if you didn't authenticate first you'll be asked anyway.

## What it does

Every X period, a celery task is triggered to synchronize the database with the artists infos of spotify new releases.
If I did not have time to think of an elegant way to let you configure the period on which you want the app to sync, default will be 1 min (so you can see it working).
On a call to `/api/artists/`, if the database was populated before, you'll receive all artists infos. If not already populated, the app will fetch artists data synchronously.
