from wtforms import Form, fields, validators
from flask_wtf import FlaskForm

class SignUpForm(FlaskForm):
    '''Form to handle sign up of users'''
    
    full_name = fields.StringField(
        label='Full Name *',
        validators=[validators.Length(min=4, max=50, message=f'This field allows minimum of 4 characters and maximum of 50 characters')],
        render_kw={'placeholder': 'John Doe', 'required': True}
    )
    
    username = fields.StringField(
        label='Username *',
        validators=[validators.Length(min=6, max=30, message=f'This field allows minimum of 6 characters and maximum of 30 characters')],
        render_kw={'placeholder': 'johndoe123', 'required': True}
    )
    
    email = fields.EmailField(
        label='Email *', 
        render_kw={'placeholder': 'johndoe123@gmail.com', 'required': True}
    )
    
    password = fields.PasswordField(
        label='Password *',
        render_kw={'placeholder': 'Johndoe@123', 'required': True}
    )
    
    password2 = fields.PasswordField(
        label='Confirm Password *',
        render_kw={'placeholder': 'Johndoe@123', 'required': True}
    )
    
    submit = fields.SubmitField(
        render_kw={'value':'Sign Up'}
    )
    
    
class LoginForm(FlaskForm):
    '''Form to handle login  of users'''
    
    username = fields.StringField(
        label='Username *',
        validators=[validators.Length(min=6, max=30, message=f'This field allows minimum of 6 characters and maximum of 30 characters')],
        render_kw={'placeholder': 'johndoe123', 'required': True}
    )
    
    password = fields.PasswordField(
        label='Password *',
        render_kw={'placeholder': 'Johndoe@123', 'required': True}
    )
    
    submit = fields.SubmitField(
        render_kw={'value':'Login'}
    )
    
        
class EditProfileForm(FlaskForm):
    '''Form to handle editing of user profile'''  
    
    full_name = fields.StringField(
        label='Full Name *',
        validators=[validators.Length(min=4, max=50, message=f'This field allows minimum of 4 characters and maximum of 50 characters')],
        render_kw={'placeholder': 'John Doe', 'required': True}
    )
    
    username = fields.StringField(
        label='Username *',
        validators=[validators.Length(min=6, max=30, message=f'This field allows minimum of 6 characters and maximum of 30 characters')],
        render_kw={'placeholder': 'johndoe123', 'required': True}
    )
    
    email = fields.EmailField(
        label='Email *', 
        render_kw={'placeholder': 'johndoe123@gmail.com', 'required': True}
    )
    
    submit = fields.SubmitField(
        render_kw={'value':'Make Changes'}
    )


class ChangePasswordForm(FlaskForm):
    '''Form to handle changing of user password'''
    
    username = fields.StringField(
        label='Username *',
        validators=[validators.Length(min=6, max=30, message=f'This field allows minimum of 6 characters and maximum of 30 characters')],
        render_kw={'placeholder': 'johndoe123', 'required': True}
    )
    
    old_password = fields.PasswordField(
        label='Old Password *',
        render_kw={'placeholder': 'Johndoe@123', 'required': True}
    )
    
    new_password = fields.PasswordField(
        label='New Password *',
        render_kw={'placeholder': 'Johndoe@123', 'required': True}
    )
    
    new_password2 = fields.PasswordField(
        label='Confirm New Password *',
        render_kw={'placeholder': 'Johndoe@123', 'required': True}
    )
    
    submit = fields.SubmitField(
        render_kw={'value':'Make Changes'}
    )
    

class ChangeProfilePictureForm(FlaskForm):
    '''Form to handle changing of profile picture'''
    
    picture = fields.FileField(
        label='Profile Picture *',
        validators=[validators.InputRequired(message='Select a file.')]
    )
    
    submit = fields.SubmitField(
        render_kw={'value':'Make Changes'}
    )
