from wtforms import Form, fields, validators
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm

class AddBlogForm(FlaskForm):
    '''Form to handle adding new blog post'''
    
    title = fields.StringField(
        label='Blog Post Title *',
        validators=[validators.Length(min=3, max=50, message=f'This field allows minimum of 3 characters and maximum of 50 characters')],
        render_kw={'placeholder': 'Title', 'required': True}
    )
    
    subtitle = fields.StringField(
        label='Blog Post Subtitle *',
        validators=[validators.Length(min=3, max=200, message=f'This field allows minimum of 3 characters and maximum of 200 characters')],
        render_kw={'placeholder': 'A short description (not more than 200 chracters)', 'required': True}
    )
    
    image_url = fields.URLField(
        label='Blog Image URL',
        render_kw={'placeholder': 'Image URL (serves as your blog\'s cover image)'}
    )
    
    blog_content = CKEditorField(
        label='Blog Content *',
        render_kw={'required': True}
    )
    
    submit = fields.SubmitField(
        render_kw={'value':'Submit Post'}
    )
    
    
class EditBlogFrom(FlaskForm):
    '''Form to handle editing blog posts'''
    
    title = fields.StringField(
        label='Blog Post Title *',
        validators=[validators.Length(min=3, max=50, message=f'This field allows minimum of 3 characters and maximum of 50 characters')],
        render_kw={'placeholder': 'Title', 'required': True}
    )
    
    subtitle = fields.StringField(
        label='Blog Post Subtitle *',
        validators=[validators.Length(min=3, max=200, message=f'This field allows minimum of 3 characters and maximum of 200 characters')],
        render_kw={'placeholder': 'A short description (not more than 200 chracters)', 'required': True}
    )
    
    image_url = fields.URLField(
        label='Blog Image URL',
        render_kw={'placeholder': 'Image URL (serves as your blog\'s cover image)'}
    )
    
    blog_content = CKEditorField(
        label='Blog Content *',
        render_kw={'required': True}
    )
    
    submit = fields.SubmitField(
        render_kw={'value':'Edit Post'}
    )
    

class AddCommentForm(FlaskForm):
    '''Form to handle editing blog posts'''
    
    comment = fields.StringField(
        validators=[validators.Length(min=3, max=500, message=f'This field allows minimum of 3 characters and maximum of 500 characters')],
        render_kw={'placeholder': 'Enter comment', 'required': True}
    )
    
    submit = fields.SubmitField(
        render_kw={'value':'Add Comment'}
    )
    
    