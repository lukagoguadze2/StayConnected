from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

description = """
# StayConnected API Documentation

Welcome to the StayConnected API documentation. This API allows users to interact with the StayConnected platform, providing access to various features designed for seamless communication and data management. Below you'll find details about the available endpoints, request/response structures, and usage guidelines.

## Overview
Nothing yet.

---

## Authentication
App uses token-based authentication. To authenticate, include an `Authorization` header in your requests with the value `Bearer <access_token>`.
To obtain an access token, you need to register a new user and log in with an existing account. for that you can use the following endpoints:
 **https:/(baseURL)/api/auth/signup/** - to register a new user
 **https:/(baseURL)/api/auth/login/** - to log in with an existing account

- **Signup request example**
request type: POST
request body:
```json 
{
    "username": "user1",
    "email": "example@gmail.com",
    "password": "password123",
    "password_2": "password123"
}
```

- **Login request example**
request type: POST
request body:
```json 
{
  "email": "string",
  "password": "string"
}
```

Successful login will return a response with an access and refresh tokens that you can use to authenticate subsequent requests and refresh the access token.

- **response example**
response body:
```json
{
  "refresh": "refresh_token",
  "access": "access_token"
}
```

**Save** the tokens and include the access token in the `Authorization` header for all requests that require authentication.
**Use** refresh token to get a new access token and refresh tokens when the current one expires.


- **Logout**
To log out and invalidate the access token, you can use the following endpoint:
**https:/(baseURL)/api/auth/logout/**
request type: POST
request body: 
```json
{
  "refresh": "refresh_token"
}
```
response body if refresh token was not provided: 
```json
{
  "detail": "Token is invalid or expired",
  "code": "token_not_valid"
}
```
response body if refresh token was provided:
```json
{ }
```
**Note:** Not returning any response body for now, would be better if it does.

---
## Tokens 
Access tokens are valid for 1 hour, and refresh tokens are valid for 1 day. When an access token expires, you can use the refresh token to obtain a new access token and refresh token.

- **Access token**
    - Valid for 1 hour
    - Used to authenticate requests
    - Include in the `Authorization` header as `Bearer <access_token>` for all requests that require authentication

- **Refresh token**
    - Valid for 1 day
    - Used to obtain a new access token and refresh token
    - Include in the request body when refreshing the access token
    
To refresh the access token, you can use the following endpoint:
**https:/(baseURL)/api/token/refresh/**

- **Refresh token request example**
request type: POST
request body:
```json 
{
   "refresh": "refresh_token"
}
```

- **Refresh token response example**
response body:
```json
{
    "access": "new_access_token",
    "refresh": "new_refresh_token",
}
```

---
## Profiles
User profiles contain information about registered users. 
For user profiles, you can use the following endpoint:
**https:/(baseURL)/api/profile/**

- **Profile request example**
request type: GET
request body: None
For this request, you need to include the access token in the `Authorization` header. Obtainin the access token is described in the Authentication section.
Updating the token is described in the Tokens section. 
If the request is successful, you will receive a response with the user's profile information.

- **Profile response example**
response body:
```json
{
  "username": "username",
  "email": "user@example.com",
  "is_active": boolean,
  "is_staff": boolean
}
```

**Note:** This response body is not final and needs to be changed, Still needs some DB implementations.

**If access token was not provided in request header**
response body:
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

## Endpoints
Here’s a brief overview of key endpoints available in this API:

- **Authentication**
    - `POST https:/(baseURL)/api/auth/signup/` - Register a new user
    - `POST https:/(baseURL)/api/auth/login/` - Log in with an existing account
    - `POST https:/(baseURL)/api/auth/logout/` - Log out and blacklist (invalidate) the access token

- **Tokens**
    - `POST https:/(baseURL)/api/token/refresh/` - Refresh the access token

- **Profiles**
    - `GET https:/(baseURL)/api/profile/` - Retrieve user profile information


- For more details on each endpoint, including request/response structures and usage guidelines, refer to the API documentation above.
- You can also test the endpoints directly from the documentation by clicking on the "Try it out" button and providing the required parameters.
- Also, you can view the response body by clicking on the "Execute" button in 'try it out' section, to do this you need to provide the required parameters in the request body.
- For endpoints requiring the access token, make sure to include it in the `Authorization` header as `Bearer <access_token>`. You can do this by clicking on the "Authorize" button and providing the access token in the input field.
---
"""


schema_view = get_schema_view(
    openapi.Info(
        title="StayConnected API Documentation",
        default_version='v1',
        description=description,
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
