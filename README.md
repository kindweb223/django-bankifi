# Bankifi

## Website and Demo apps to showcase banking and other 3rd part API integration.

Provides demos for the following:  

- Accounts - Uses the Open Banking Project APIs to display and aggregate a customers accounts and balances
- Bankifi - Bankifi Website and main Bankifi projects
- Bankinfo - Uses the Open Banking Project APIs and Sandbox to showcase use of their banking project APIs.
- Branch - Uses the HSBC branch finder APIs and Google Map APIs to showcase how combining(mashup) APIs can provide added value and innovation.
- Bankxero - Uses the Xero Accounting package APIs to allow is to access a dummy user account. Show a scenario where a 3rd party TPP could provide enhanced services (Invoice Finance Loans) to the package user. Uses
- Cashflow - Liquidity management app for small businesses. Integrates with Xero.
- OAUTH to provide consent management.
- Obp_oauth - Demonstration of the Open Banking Project OAUTH authentication APIs.
- Xero - Clone of 3rd party package (pyxero) that is used to access the Xero API via Python.

## Documentation
Uses pycco for documentation. For example, `pycco cashflow/*.py`

## Third-party integrations

### APIs
- Xero - you can setup a free account [here](https://developer.xero.com/documentation/getting-started/getting-started-guide)
- Nordea -
- RBS -

### Hosting
- AWS S3 and Cloudfront - for `collectstatic` i.e. speed up serving of static files and condense the several apps within this project to a single place
    - N.B. this can be configured to work without S3/Cloudfront it seems
- Heroku - the app can be deployed straightforwardly here. Needs the following add-ons:
    - Postgres
    - Redis

## Running for development

Follow next 3 sections to get the app up and running locally:

#### A) [Dev Setup] Checkout code and add config 

1. Install Python3 `brew install python3` (pythong 3.6.* is required)
    ```
    brew unlink python # ONLY if you have installed (with brew) another version of python 3

    brew install --ignore-dependencies https://raw.githubusercontent.com/Homebrew/homebrew-core/f2a764ef944b1080be64bd88dca9a1d80130c558/Formula/python.rb
    ```
    https://stackoverflow.com/questions/51125013/how-can-i-install-a-previous-version-of-python-3-in-macos-using-homebrew/51125014#51125014


    
1. Install virtual env `pip3 install virtualenv`
1. Create virtualenv `cd /path/to/bankifi && virtualenv $(pwd)`
    1. Activate virtualenv `source bin/activate`
1. Install Django `pip3 install Django`
1. Install dependencies `pip3 install -r requirements.txt`
1. Create file /bankifi/settings/local.py with following content:
    ```
    DEBUG = True
    SECRET_KEY='local-dev'
    DATABASES = {
            'default': {
                'ENGINE':'django.db.backends.postgresql_psycopg2',
                'NAME': 'bankifi',
                'USER': 'dev',
                'PASSWORD': 'password',
                'HOST': '127.0.0.1',
                'PORT': '5432',
            }
        }

    AWS_ACCESS_KEY_ID = ''
    AWS_SECRET_ACCESS_KEY = ''
    AWS_STORAGE_BUCKET_NAME = ''
    AWS_S3_HOST = ''
    COMPRESS_ENABLED = False
    STATIC_URL = "/static/"
    COMPRESS_STORAGE = ''
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
    ACCOUNT_EMAIL_VERIFICATION="optional"
    XERO_CLIENT_KEY = "SET_YOUR_OWN"
    XERO_CLIENT_SECRET = "SET_YOUR_OWN"
    XERO_CALLBACK_URI = 'http://localhost:8000/cashflow/authorize'
    ```
#### B) [Dev Setup] Install dependencies and start server 

1. Ensure you have docker installed: https://docs.docker.com/install/

1. Start postgres: `docker run --rm  --name postgres-docker -e POSTGRES_PASSWORD=docker -d -p 5432:5432 -v $HOME/docker/volumes/postgres:/var/lib/postgresql/data  postgres`
1. Setup postgress database and account:

    `docker exec -it postgres-docker psql -U postgres -c "create database bankifi;"`

    `docker exec -it postgres-docker psql -U postgres -c "create user dev  with encrypted password 'password';"`

    `docker exec -it postgres-docker psql -U postgres -c "grant all privileges on database bankifi to dev;"`

1. Start redis: `docker run -d -p 6379:6379 redis`
1. RUN `python manage.py migrate`
1. RUN `python manage.py createsuperuser`
1. Run `python manage.py collectstatic --noinput `
    1. error happens here - see `bankifi/bankifi/settings/storage.py`
1. Run server `ON_HEROKU=True DEBUG=True python manage.py runserver`

#### B) [Dev Setup] Setup reference data and access app 

1. Create Receivable account on admin screen: http://localhost:8000/admin/ (make sure to use xero account id 51387801-7668-48b0-a276-e8cadc2d33de)
1. Create Payable account on admin screen: http://localhost:8000/admin/ (make sure to use xero account id 45674523)
1. Ensure you have Xero developer account login (and client key and secret in the local.py)
1. Login to the app http://localhost:8000/cashflow/forecast
1. Reset demo (Setup -> Reset Demo)
1. Generate demo data (http://localhost:8000/cashflow/invoice/generate)
1. Dashboard page should have data displayed


#### Additional Notes from Unifi Software Development
```
Nice to meet you too! I did manage to spin up BankiFI as a local test server after minor code modifications.

Disabled the ‘branch’ and ‘branchfinder’ apps + urls
Set COMPRESS_ENABLES = False
Disabled the AWS setup
Set STATIC_ROOT = ‘static’
Set STATIC_URL = ‘/static/’

BankiFI local development setup guide

Copy the source code to ~/code/bankiFI

Copy the attached files to the correct location
·         base.py – ~/code/bankiFI/bankifi/settings/base.py
·         urls.py - ~/code/bankiFI/bankifi/urls.py
·         breakdown.py – ~/code/bankiFI/nordea/breakdown.py

brew install postgresql
brew install redis

mkdir -p ~/vens/bankiFI && cd $_
virtualenv -p /usr/local/bin/python3 .
source bin/activate
pip install -r ~/code/bankiFI/requirements.txt

brew info postgres
pg_ctl -D /usr/local/var/postgres start
createdb bankifi

psql bankifi
CREATE USER test_user;
GRANT ALL PRIVILEGES ON DATABASE bankifi to test_user;
\du
\q

cd ~/code/bankiFI/
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic

In a separate terminal window
brew info redis
redis-server /usr/local/etc/redis.conf

python manage.py runserver
```

## Deploying to environments

1. Host it in Github
1. Create Heroku app
1. Setup ancillliary accounts
    1. AWS account, S3 bucket and access keys [guide1](https://devcenter.heroku.com/articles/s3) OR [guide2](https://www.caktusgroup.com/blog/2014/11/10/Using-Amazon-S3-to-store-your-Django-sites-static-and-media-files/), ensure the bucket is publicly READ_ONLY
        1. `arn:aws:s3:::bankifi-production-eu-west-1`
    1. Sendgrid
        1. Create an API key
        1. Inject the generated username/password as `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` config variables in Heroku
1. Set config vars - see `bankifi/bankifi/settings/production.py`
    1. set config var `SECRET_KEY=xyz`
    1. set `ON_HEROKU=true`
    1. `AWS_ACCESS_KEY_ID=xxx`
    1. `AWS_SECRET_ACCESS_KEY=yyy`
    1. `AWS_S3_HOST=s3-eu-west-1.amazonaws.com` **!IMPORTANT!**
1. it will try to `python manage.py collectstatic --noinput`
    1. see errors encountered below for the fix
    1. you should be able to deploy once done - Aaron suggested disabling S3 usage
1. Error in nordea transactions breakdown.py
    1. handled 0 transactions error in commit `2cc6522`
1. It will complain about Redis missing
    1. Install Heroku Redis add-on and the `REDIS_URL` will auto-pickup by the app

At this point the landing page now works, but the apps do not.

1. Migrate the `SITE_ID` stuff (see [this](https://stackoverflow.com/questions/23925726/django-relation-django-site-does-not-exist) Stackoverflow question)
    1. Only need to run this on Heroku: `heroku run bash`
    1. Then `python manage.py migrate`
    1. Suggest some more expertise knowledge from Unifi/Aaron around Django to verify this cleanly

## Errors encountered

### 1. collectstatic runs will fail

1. manually
    1. `aws s3 cp ~/asset_storage/ s3://bankifi-production-eu-west-1/ --recursive`
    1. `aws s3 cp ~/.heroku/python/lib/python3.6/site-packages/django/contrib/admin/static/admin/ s3://bankifi-production-eu-west-1/admin/ --recursive`
    1. rerun collectstatic for app to be happy, may need a few runs

### 2. loading any page
After completing `collectstatic` we get the following error:

```
2017-11-08T16:52:28.897781+00:00 app[web.1]:   File "/app/nordea/api/urls.py", line 15, in <module>
2017-11-08T16:52:28.897781+00:00 app[web.1]:     from .views import (
2017-11-08T16:52:28.897782+00:00 app[web.1]:   File "/app/nordea/api/views.py", line 56, in <module>
2017-11-08T16:52:28.897782+00:00 app[web.1]:     from nordea.currency import total_networth, total_credits, total_debits
2017-11-08T16:52:28.897782+00:00 app[web.1]:   File "/app/nordea/currency.py", line 11, in <module>
2017-11-08T16:52:28.897783+00:00 app[web.1]:     breakdown = get_breakdown()
2017-11-08T16:52:28.897783+00:00 app[web.1]:   File "/app/nordea/breakdown.py", line 43, in get_breakdown
2017-11-08T16:52:28.897784+00:00 app[web.1]:     for t in get_transactions(pk)['transactions']:
2017-11-08T16:52:28.897784+00:00 app[web.1]: KeyError: 'transactions'
```

Looks like we may need data injected somewhere, as it's looking for the value under the key `'transactions'` but nothing exists in the array/list of `get_transactions(pk)`.

Further leads to this error:

```
KeyError: 'en-gb'` in `../django/urls/resolvers.py
```

See `bankifi/settings/base.py` line `281` - no results from `NORDEA_API_ROOT = 'https://api.nordeaopenbanking.com/v1'`

Maybe we need to setup the callback URLs?

```
# grep -ri bankifi.com .

./bankifi/settings/base.py:    OAUTH_CALLBACK_URI = 'http://demo.bankifi.com/oauth/authorize'
./bankifi/settings/base.py:    XERO_CALLBACK_URI = 'http://demo.bankifi.com/cashflow/pobo/create'
Binary file ./bankifi/settings/base.pyc matches
Binary file ./cashflow/__pycache__/admin.cpython-36.pyc matches
./cashflow/admin.py:Access to the admin is via [admin url](demo.bankifi.com/admin).
Binary file ./cashflow/views/__pycache__/pobo.cpython-36.pyc matches
./cashflow/views/pobo.py:                    'Url': 'http://www.bankifi.com/cashflow/pobo/pay?number={0}'.format(self.object.number),
./docs/admin.html:Access to the admin is via <a href="demo.bankifi.com/admin">admin url</a>.</p>
./docs/pobo.html:                    <span class="s1">&#39;Url&#39;</span><span class="p">:</span> <span class="s1">&#39;http://demo.bankifi.com/cashflow/pobo/pay?number={0}&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">object</span><span class="o">.</span><span class="n">number</span><span class="p">),</span>
```

## Accounts and Environment notes

1. AWS - organisation `thestartupfactory`
    1. new user `bankifi-prod` with keys injected to Heroku app
1. Xero developer account - use this for local development
    1. Create your own account [here](https://developer.xero.com/documentation/getting-started/getting-started-guide) for free
