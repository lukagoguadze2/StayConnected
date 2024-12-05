from drf_yasg import openapi

class TagDocs:
    create_tag = {
        'operation_summary': 'Create tag',
        'operation_description': 'Create tag with name',
        'request_body': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Tag name',
                    example='Python'
                )
            },
            required=['title']
        ),
        'responses': {
             201 : openapi.Response(
                description='Tag created',
                examples={
                    'application/json': {
                        'id': 1,
                        'name': 'Python'
                    }
                }
            )
        }
    }
    
    get_tags = {
        'operation_summary': 'Get tags',
        'operation_description': 'Get all tags',
    }
    
    
class LeaderBoardDocs:
    operation_summary = 'Leaderboard'
    operation_description = 'Get leaderboard of users ordered by rating'
    
    responses = {
        200: openapi.Response(
            description='Leaderboard',
            examples={
                'application/json': {
                    'count': 21,
                    'next': None,
                    'previous': None,
                    'results': [
                        {
                            'username': 'Name',
                            'email': 'user@example.com',
                            'rating': 24,
                            'answered_questions': 0,
                            'rank': 1
                        }
                    ]
                }
            }
        )
    }
                        