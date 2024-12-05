from drf_yasg import openapi


class CommentDocs:
    like = {
        'operation_summary': 'Like an entity',
        'operation_description': """
            Like an entity by its ID. This endpoint can be used to like a post, comment, or any other entity. 
            ---
            If the user has already liked or disliked the entity, the server will return a 400 error, which means that 
            the user cannot react on the entity twice. In order to change the reaction, the user should use the 
            `update_reaction` endpoint.
         """,
    }
    
    dislike = {
        'operation_summary': 'Dislike an entity',
        'operation_description': """
            Dislike an entity by its ID. This endpoint can be used to dislike a post, comment, or any other entity.
            ---
            If the user has already liked or disliked the entity, the server will return a 400 error, which means that
            the user cannot react on the entity twice. In order to change the reaction, the user should use the
            `update_reaction` endpoint. 
        """,
    }
    
    remove_reaction = {
        'operation_summary': 'Remove reaction from an entity',
        'operation_description': (
            'Remove reaction by entity id. This endpoint is needed to remove like or dislike reactions from an entity.'
            '\nReactions can be removed only by the user who added them. If the user did not add a reaction, ' 
            'the server will return a 404 error.'
        ),
    }
    
    update_reaction = {
        'operation_summary': 'Update reaction, from like to dislike and vice versa',
        'operation_description': """
            Update reaction by entity id. This endpoint is needed to change like to dislike and vice versa
            ---
            **Note**: Request body should contain `reaction_type` field with value true or false (**true** for 'like' and **false** for 'dislike')
            if reaction_type is **true**, the reaction will be changed to like, if **false** - to dislike
        """,
    }
    
    create_comment = {
        'operation_summary': 'Create comment',
        'operation_description': """
            Create comment for post by post id
            **Note**: Only authenticated users can create comments
        """,
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
        'operation_description': 'Mark correct answer by comment id, comment can be marked as correct only by post '
                                 'owner only once',
    }
    
    unmark_correct = {
        'operation_summary': 'Unmark correct answer',
        'operation_description': 'Unmark correct answer by comment id, comment can be unmarked as correct only by '
                                 'post owner',
    }
    
    delete_comment = {
        'operation_summary': 'Delete comment',
        'operation_description': 'Delete comment by comment id, comment can be deleted only by comment author and '
                                 'post owner',
    }
    