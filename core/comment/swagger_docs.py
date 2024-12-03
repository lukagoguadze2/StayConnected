from drf_yasg import openapi

class CommentDocs:
    
    like_comment = {
        'operation_summary': 'Like comment',
        'operation_description': 'Like comment by comment id',
    }
    
    dislike_comment = {
        'operation_summary': 'Dislike comment',
        'operation_description': 'Dislike comment by comment id',
    }
    
    remove_reaction = {
        'operation_summary': 'Remove reaction from comment',
        'operation_description': 'Remove reaction by comment id. This endpoint is needed to remove like or dislike reactions from a comment',
    }
    
    update_reaction = {
        'operation_summary': 'Update reaction, from like to dislike and vice versa',
        'operation_description': 'Update reaction by comment id. This endpoint is needed to change like to dislike and vice versa',
    }
    
    create_comment = {
        'operation_summary': 'Create comment',
        'operation_description': 'Create comment for post by post id',
        'request_body': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'content': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Comment text',
                    example='This is a comment'
                ),
                'post': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='Post id',
                    example=1
                )
            }
        )
    }    
    
    post_comments = {
        'operation_summary': 'Get comments for post',
        'operation_description': 'Get comments for post by post id',
    }
    
    mark_correct = {
        'operation_summary': 'Mark correct answer',
        'operation_description': 'Mark correct answer by comment id, comment can be marked as correct only by post owner only once',
    }
    
    unmark_correct = {
        'operation_summary': 'Unmark correct answer',
        'operation_description': 'Unmark correct answer by comment id, comment can be unmarked as correct only by post owner',
    }
    
    delete_comment = {
        'operation_summary': 'Delete comment',
        'operation_description': 'Delete comment by comment id, comment can be deleted only by comment author and post owner',
    }
    