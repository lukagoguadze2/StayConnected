from http.client import responses

from drf_yasg import openapi
from authentication.swagger_docs import ProfilePostsDocs


class PostDocs:
    create_post = {
        'operation_description': 'Create a new post.',
        'operation_summary': 'Create Post. Requires authentication.\nUse this endpoint to create a new post.',
        'request_body': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING),
                'description': openapi.Schema(type=openapi.TYPE_STRING),
                'tags': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_INTEGER),
                    description='List of tag ids. (Array can be empty)',
                    example=[1, 2, 3]
                ),
            },
            required=['title', 'description', 'tags'],
        ),
    }

    filter_post = {
        'operation_summary': 'Filter posts',
        'operation_description': (
            'Filter posts by tag or query. Use this endpoint to filter posts by tag or query.\n'
            '**Example**: {baseurl}/api/posts/filter/?query=python&tag=1'
        )
    }

    single_post = {
        'operation_summary': 'Get post details',
        'operation_description': 'Get post details by id. Use this endpoint to get post details by id.',
        'responses': {200: ProfilePostsDocs.post_schema}
    }

    update_post = {
        'operation_summary': 'Update post',
        'operation_description': 'Update post by id. Use this endpoint to update post by id.',
        'responses': responses
    }

    delete_post = {
        'operation_summary': 'Delete post',
        'operation_description': (
            'Delete post by id. Use this endpoint to delete post by id.\n'
            '**Note**: Only post owner and staff member can delete the post.'
        ),
    }

    responses = ProfilePostsDocs.responses

    operation_description = """
    Returns a list of posts. Use this endpoint to get the list of posts.
    """
    operation_summary = "Get list of posts"
