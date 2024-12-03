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


class ResetPasswordRequestDocs:
    request_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(
                title='email',
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_EMAIL,
                description="User's email address",
                example='user@example.com'
            )
        },
        required=['email']
    )
    
    responses = {
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'detail': openapi.Schema(
                    title='detail',
                    type=openapi.TYPE_STRING,
                    description="Response message",
                    example='Password can be reset for this email.'
                ),
                'email': openapi.Schema(
                    title='email',
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_EMAIL,
                    description="User's email address",
                    example='user@example.com'
                )
            }
        )
    }
    
    operation_description = """
    Takes a user's email address and checks if the email exists in the database. Use this endpoint to request a password reset.
    If the email exists, a response message will be returned. And you can use this email to reset the password with the next endpoint.
    Pass the retrieved email to the next endpoint to reset the password.
    """
    
    operation_summary = "Request a password reset for the given email address"
    
    
class ResetPasswordDocs:
    request_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(
                title='email',
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_EMAIL,
                description="Need to pass email from the previous endpoint",
                example='user@example.com'
            ),
            'password': openapi.Schema(
                title='password',
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_PASSWORD,
                description="New password",
                example='SecureP@ssw0rd!'
            ),
            'password_2': openapi.Schema(
                title='password_2',
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_PASSWORD,
                description="Confirm the new password",
                example='SecureP@ssw0rd!'
            )
        },
        required=['email', 'password', 'password_2']
    )
    
    responses = {
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'detail': openapi.Schema(
                    title='detail',
                    type=openapi.TYPE_STRING,
                    description="Response message",
                    example='Password reset successfully'
                )
            }
        ),
        400: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'detail': openapi.Schema(
                    title='detail',
                    type=openapi.TYPE_STRING,
                    description="Password reset only works if user is not logged in",
                    example='You are already logged in'
                )
            }
        ),
    }
    
    operation_description = """
    Takes a set of user credentials and resets the user's password. Use this endpoint to reset the password for the given email address.
    """
    
    operation_summary = "Reset the password for the given email address"
    
    
class SignupDocs:
    request_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(
                title='username',
                type=openapi.TYPE_STRING,
                description="User's username",
                example='user123'
            ),
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
            ),
            'password_2': openapi.Schema(
                title='password_2',
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_PASSWORD,
                description="Confirm the password",
                example='SecureP@ssw0rd!'
            )
        },
        required=['username', 'email', 'password', 'password_2']
    )

    responses = {
        201: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'detail': openapi.Schema(
                    title='detail',
                    type=openapi.TYPE_STRING,
                    description="Response message",
                    example='User registered successfully'
                )
            }
        ),
    }
                
    operation_description = """
    Takes a set of user credentials and creates a new user account. Use this endpoint to register a new user.
    
    **Full address - https:/(baseURL)/api/auth/signup/**
    
    Password requirements:
    - At least 8 characters long
    - Contains a digit
    - Contains a letter
    - Contains an uppercase letter
    """
    
    operation_summary = "Register a new user account"
    

                
class ProfileDocs:
    responses = {
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(
                    title='id',
                    type=openapi.TYPE_NUMBER,
                    description="User's ID",
                    example=1
                ),
                'username': openapi.Schema(
                    title='username',
                    type=openapi.TYPE_STRING,
                    description="User's username",
                    example='user123'
                ),
                'email': openapi.Schema(
                    title='email',
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_EMAIL,
                    description="User's email address",
                    example='user@example.com'
                ),
                'rating': openapi.Schema(
                    title='rating',
                    type=openapi.TYPE_NUMBER,
                    description="User's rating",
                    example=68
                ),
                'answered_questions': openapi.Schema(
                    title='answered_questions',
                    type=openapi.TYPE_NUMBER,
                    description="Number of answered questions (correct answers)",
                    example=1
                )
            }
        )
    }
    
    operation_description = """
    Takes a user's ID and returns the user's profile information. Use this endpoint to get the user's profile.
    """
    
    operation_summary = "Get the user's profile information"
    
    
class ProfilePostsDocs:    
    responses = {
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'count': openapi.Schema(
                    title='count',
                    type=openapi.TYPE_NUMBER,
                    description="Number of posts",
                    example=4
                ),
                'next': openapi.Schema(
                    title='next',
                    type=openapi.TYPE_STRING,
                    description="URL for the next page of pagination",
                    example=None
                ),
                'previous': openapi.Schema(
                    title='previous',
                    type=openapi.TYPE_STRING,
                    description="URL for the previous page of pagination",
                    example=None
                ),
                'results': openapi.Schema(
                    title='results',
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(
                                title='id',
                                type=openapi.TYPE_NUMBER,
                                description="Post's ID",
                                example=5
                            ),
                            'author': openapi.Schema(
                                title='author',
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(
                                        title='id',
                                        type=openapi.TYPE_NUMBER,
                                        description="User's ID",
                                        example=1
                                    ),
                                    'username': openapi.Schema(
                                        title='username',
                                        type=openapi.TYPE_STRING,
                                        description="User's username",
                                        example='gela'
                                    ),
                                    'email': openapi.Schema(
                                        title='email',
                                        type=openapi.TYPE_STRING,
                                        format=openapi.FORMAT_EMAIL,
                                        description="User's email address",
                                        example='user@example.com'
                                    ),
                                    'rating': openapi.Schema(
                                        title='rating',
                                        type=openapi.TYPE_NUMBER,
                                        description="User's rating",
                                        example=68
                                    ),
                                    'answered_questions': openapi.Schema(
                                        title='answered_questions',
                                        type=openapi.TYPE_NUMBER,
                                        description="Number of answered questions (correct answers)",
                                        example=0
                                    )
                                }
                            ),
                            'title': openapi.Schema(
                                title='title',
                                type=openapi.TYPE_STRING,
                                description="Post's title",
                                example='C#'
                            ),
                            'description': openapi.Schema(
                                title='description',
                                type=openapi.TYPE_STRING,
                                description="Post's description",
                                example='How can we declare variables in C#?'
                            ),
                            'created_at': openapi.Schema(
                                title='created_at',
                                type=openapi.TYPE_NUMBER,
                                description="Timestamp of post creation",
                                example=1733229510
                            ),
                            'tags': openapi.Schema(
                                title='tags',
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'id': openapi.Schema(
                                            title='id',
                                            type=openapi.TYPE_NUMBER,
                                            description="Tag's ID",
                                            example=2
                                        ),
                                        'title': openapi.Schema(
                                            title='title',
                                            type=openapi.TYPE_STRING,
                                            description="Tag's title",
                                            example='C#'
                                        )
                                    }
                                )
                            ),
                            'engagement': openapi.Schema(
                                title='engagement',
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'likes': openapi.Schema(
                                        title='likes',
                                        type=openapi.TYPE_NUMBER,
                                        description="Number of likes",
                                        example=0
                                    ),
                                    'dislikes': openapi.Schema(
                                        title='dislikes',
                                        type=openapi.TYPE_NUMBER,
                                        description="Number of dislikes",
                                        example=0
                                    ),
                                    'comments': openapi.Schema(
                                        title='comments',
                                        type=openapi.TYPE_NUMBER,
                                        description="Number of comments",
                                        example=0
                                    )
                                }
                            ),
                            'is_owner': openapi.Schema(
                                title='is_owner',
                                type=openapi.TYPE_BOOLEAN,
                                description="Is the user the author of the post",
                                example=True
                            ),
                            'has_correct_answer': openapi.Schema(
                                title='has_correct_answer',
                                type=openapi.TYPE_BOOLEAN,
                                description="Does the post have a correct answer",
                                example=False
                            ),
                            'seen_by_user': openapi.Schema(
                                title='seen_by_user',
                                type=openapi.TYPE_BOOLEAN,
                                description="Is the post seen by the user",
                                example=False
                            )
                        }
                    )
                )
            }
        )
    }

    operation_description = """
    Takes a user's ID and returns the user's posts. Use this endpoint to get the user's posts.
    """
    
    operation_summary = "Get the user's posts"                     
    