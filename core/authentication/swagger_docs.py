from drf_yasg import openapi

JWT_FORMAT = "JWT"

class LoginDocs:
    request_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(
                title='email',
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_EMAIL,
                description="User's email address",
                example='user@example.com'
            ),
            'password': openapi.Schema(
                title='password',
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_PASSWORD,
                description="User's password",
                example='SecureP@ssw0rd!'
            )
        },
        required=['email', 'password']
    )

    __refresh_token_description = """
    Use 'refresh token' to get a new access token and refresh tokens when the current one expires. 
    """
    
    __access_token_description = """
    Use 'access token' to authenticate subsequent requests. Pass it in the `Authorization` header of requests that require authentication. 
    Format of the token for request header is `Bearer <access_token>`.
    """
    
    responses = {
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh': openapi.Schema(
                    title='refresh token',
                    type=openapi.TYPE_STRING,
                    format=JWT_FORMAT,
                    description=__refresh_token_description,
                    example='eyJ0eXAiOiJKV1Qi...'
                ),
                'access': openapi.Schema(
                    title='access token',
                    type=openapi.TYPE_STRING,
                    format=JWT_FORMAT,
                    description=__access_token_description,
                    example='eyJ0eXAiOiJKV1Qi...'
                )
            }
        )
    }
    
    operation_description = """
    Takes a set of user credentials and returns an access and refresh JSON web token pair to prove the authentication of those credentials.
    
    **Save** the tokens and include the access token in the `Authorization` header for all requests that require authentication.
    **Use** refresh token to get a new access token and refresh tokens when the current one expires.
    
    View more about request body and response examples below.

    **Full address - https:/(baseURL)/api/auth/login/**
    """
    
    operation_summary = "Log in with an existing account"
    

class LogOutDocs:
    request_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'refresh': openapi.Schema(
                title='refresh',
                type=openapi.TYPE_STRING,
                format=JWT_FORMAT,
                description="Refresh token",
                example='eyJ0eXAiOiJKV1Qi...'
            )
        },
        required=['refresh']
    )
    
    responses = {
        201: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'detail': openapi.Schema(
                    title='detail',
                    type=openapi.TYPE_STRING,
                    description="Response message",
                    example='User logged out successfully, refresh token blacklisted'
                )
            }
        ),
    }
    
    operation_description = """
    Use 'refresh token' to log out and invalidate the access token and blacklist the 'refresh token'.
    
    **Full address - https:/(baseURL)/api/auth/logout/**
    """
    
    operation_summary = "Log out and invalidate the access token and blacklist refresh token"
