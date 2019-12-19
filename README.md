# AFPyro site

This is the source code for https://afpyro.afpy.org.

## Production

In production you can use:

    pip install -r requirements.txt
    gunicorn -w 2 afpyro:app

And serve `static/` directory directly.


### Deployment

To push this in production, just push on github, a github action will
push this to production.


## Development

    pip install -r requirements.txt
    FLASK_APP=afpyro FLASK_ENV=development flask run
