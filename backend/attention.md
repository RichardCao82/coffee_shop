

##
1. according to front end send back data, the post recipe data should be a list
   so modify manager /drinks POST method in file "udacity-fsnd-udaspicelatte.postman_collection.json"
{
    "title": "Water3",
    "recipe": {
        "name": "Water",
        "color": "blue",
        "parts": 1
    }
}

to

{
    "title": "Water3",
    "recipe": [{
        "name": "Water",
        "color": "blue",
        "parts": 1
    }]
}

##
# get token url
# https://rcservice.auth0.com/authorize?audience=drinks&response_type=token&client_id=DDx747OcIAWgsNPFLy1cZKiojBF5M8Px&redirect_uri=http://127.0.0.1:5000/drinks

# logout url
# https://rcservice.auth0.com/logout?client_id=DDx747OcIAWgsNPFLy1cZKiojBF5M8Px&returnTo=https://127.0.0.1:8080/logout

# user list
# manager@coffeeshop.com
# Manager123!

# barista@coffeeshop.com
# Barista123!

# user@coffeeshop.com
# User123!

##
because Auth0 is NOT accept http callback URLs, MUST change backend to https
1. add one more dependence in requirements.txt --- "pyopenssl"
2. import ssl in api.py and models.py
3. run app add one more parameter --- ssl_context='adhoc'
4. start backend server by command python3 api.py