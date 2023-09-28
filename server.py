from __init__ import *

year = datetime.now().year

# ----------------------- USER VIEWS ------------------------- #

class HomeView(View):
    '''Hone view to get all blogs from the database'''
    
    methods = ['GET', 'POST']
    
    def dispatch_request(self):
        form = SearchByAuthorForm(request.form)
        
        if request.method == 'POST' and form.validate_on_submit():
            user = session.query(User).filter_by(full_name=form.author.data).first()
            if user:
                blogs = session.query(Blog).filter_by(author_id=user.id)
                if blogs.count() > 1:
                    flash(f"{blogs.count()} blog posts found for {form.author.data}")
                else:
                    flash(f"{blogs.count()} blog post found for {form.author.data}")
                    
                return render_template('index.html', blogs=blogs, user=current_user, active_link='home', year=year, form=form)
            else:
                flash('There are no blog posts for this user.')
            
        # Get request to get all blogs
        blogs = session.query(Blog).all()
        return render_template('index.html', blogs=blogs, user=current_user, active_link='home', year=year, form=form)
    
app.add_url_rule('/', view_func=HomeView.as_view(name='home'))

    
class SignUpView(View):
    '''View to handle sign up of users'''
    
    methods = ['GET', 'POST']
    
    def dispatch_request(self):
        message = None
        form = SignUpForm(request.form)
        
        if request.method == 'POST' and form.validate_on_submit():
            full_name = form.full_name.data
            username = form.username.data
            email = form.email.data
            password = form.password.data
            password2 = form.password2.data
            profile_picture = f"{app.config['UPLOAD_FOLDER']}/default.jpeg"
            
            if password != password2:
                message = 'Your passwords do not match.'
            elif not is_valid_password(password) or not is_valid_password(password2):
                message = 'One of your passwords is invalid.'
            # No problems with password
            else:
                username_data = session.query(User).filter_by(username=username).first()
                email_data = session.query(User).filter_by(email=email).first()
                
                # check if username and email exists
                if username_data:
                    message = 'This username is taken.'
                elif email_data:
                    message = 'Thus email is in use.'
                else:
                    # hash password
                    hashed_password = generate_password_hash(password, salt_length=16)
                    
                    # Adding to database
                    user = User(
                        full_name=full_name,
                        username=username,
                        email=email,
                        password=hashed_password,
                        profile_picture=profile_picture
                    )
                    session.add(user)
                    session.commit()
                    
                    login_user(user)
                    
                    flash('You have successfully signed up')
                    return redirect(url_for('home'))

        return render_template('forms/signup.html', form=form, message=message, user=current_user, active_link='signup', year=year)
    
app.add_url_rule('/signup', view_func=SignUpView.as_view(name='signup'))


class LoginView(View):
    '''View to handle login of users'''
    
    methods = ['GET', 'POST']
    
    def dispatch_request(self):
        message = None
        
        form = LoginForm(request.form)
        
        if request.method == 'POST' and form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            
            # Perform authentication
            user = session.query(User).filter_by(username=username).first()
            
            if user is not None:
                # check for password
                if check_password_hash(pwhash=user.password, password=password):
                    login_user(user)
                    flash('Successfully logged in.')
                    return redirect(url_for('home'))
                else:
                    message = 'Password is incorrect. Try again.'
            else:
                message = 'Account does not exist.'
            
        return render_template('forms/login.html', message=message, form=form, user=current_user, active_link='login', year=year)
    
app.add_url_rule('/login', view_func=LoginView.as_view(name='login'))


class LogoutView(View):
    '''View to handle logout of users'''
    
    decorators = [login_required]
    
    def dispatch_request(self):
        logout_user()
        flash('Logout successful. See you later.')
        return redirect(url_for('home'))

app.add_url_rule('/logout', view_func=LogoutView.as_view(name='logout'))


class GetUserDetailsView(View):
    '''View to get details of current logged in user'''
    
    methods = ['GET', 'POST']
    decorators = [login_required]
    
    def dispatch_request(self):
        change_picture_form = ChangeProfilePictureForm(request.files)
        
        if change_picture_form.validate_on_submit() and 'picture' in request.files:
            flash('Profile picture updated')
            return redirect(url_for('getUserDetails'))
        
        return render_template('profile.html', user=current_user, form=change_picture_form, active_link='profile', year=year)

app.add_url_rule('/profile', view_func=GetUserDetailsView.as_view(name='getUserDetails'))


class EditProfileView(View):
    '''View to edit profile'''
    
    methods = ['GET', 'POST']
    decorators = [login_required]
    
    def dispatch_request(self):
        message = None
        
        user = database.get_or_404(User, current_user.id)
        form = EditProfileForm(obj=user)
        
        if request.method == 'POST' and form.validate_on_submit():
            form.populate_obj(user)
            session.commit()
            
            flash('Profile changes saved')
            return redirect(url_for('getUserDetails'))
    
        return render_template('forms/edit-profile.html', form=form, user=current_user, message=message, active_link='profile', year=year)
    
app.add_url_rule('/profile/edit', view_func=EditProfileView.as_view(name='editProfile'))


class ChangePasswordView(View):
    '''View to change user password'''
    
    methods = ['GET', 'POST']
    decorators = [login_required]
    
    def dispatch_request(self):
        form = ChangePasswordForm(request.form)
        user = session.query(User).filter_by(username=current_user.username).first()
        
        message = None
        
        if request.method == 'POST' and form.validate_on_submit():
            old_password = form.old_password.data
            new_password = form.new_password.data
            new_password2 = form.new_password2.data
            
            if not check_password_hash(pwhash=user.password, password=old_password):
                message = 'Old password is incorrect.'
            else:
                if new_password != new_password2:
                    message = 'New passwords do not match.'
                elif not is_valid_password(new_password) or not is_valid_password(new_password2):
                    message = 'One of your new passwords is invalid.'
                else:
                    new_password_hash = generate_password_hash(new_password, salt_length=16)
                    user.password = new_password_hash
                    
                    session.commit()
                    
                    flash('Password changed successfully.')
                    return redirect(url_for('getUserDetails'))
                    
        return render_template('forms/change-password.html', form=form, user=current_user, message=message, active_link='profile', year=year)
        
    
app.add_url_rule('/profile/change-password', view_func=ChangePasswordView.as_view(name='changePassword'))


class ChangeProfilePictureView(View):
    '''View to change user profile picture'''
    
    methods = ['GET', 'POST']
    decorators = [login_required]
    
    def dispatch_request(self):
        form = ChangeProfilePictureForm(request.files)
        
        if request.method == 'POST' and form.validate_on_submit():
            
            # check if the post request has the file part
            if 'picture' not in request.files:
                flash('No file part')
            
            file = form.picture.data
            
            if not allowed_file(file.filename):
                flash('Invalid file format')
            elif file and allowed_file(file.filename):
                number = random.randint(1000, 10000000)
                filename = secure_filename(file.filename)
                save_path = f"{app.config['UPLOAD_FOLDER']}/{number}-{filename}"
                print(save_path)
                # save file
                file.save(save_path)
                
                # update database
                user = session.query(User).filter_by(id=current_user.id).first()
                user.profile_picture = save_path
                session.commit()
                
                # update database
                flash('Profile picture updated')
                return redirect(url_for('getUserDetails'))
        
        return render_template('forms/change-profile-picture.html', form=form, user=current_user, active_link='profile', year=year)
    
app.add_url_rule('/profile/change-profile-picture', view_func=ChangeProfilePictureView.as_view(name='changeProfilePicture'))


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ #

# ----------------------- BLOG VIEWS ------------------------- #

class GetUserBlogsView(View):
    '''View to get blog posts of current logged in user'''
    
    methods = ['GET', 'POST']
    decorators = [login_required]
    
    def dispatch_request(self):
        form = SearchByBlogTitleForm(request.form)
        
        if request.method == 'POST' and form.validate_on_submit():
            user_blogs = session.query(Blog).filter_by(author_id=current_user.id, title=form.blog_title.data).all()
            
            if user_blogs:
                flash(f"Blog '{form.blog_title.data}' found")
                return render_template('my-blogs.html', user_blogs=user_blogs, user=current_user, active_link='myblogs', year=year)
            else:
                flash(f"Blog '{form.blog_title.data}' does not exist")
        
        # Check database for blogs for the current logged in user
        user_blogs = session.query(Blog).filter_by(author_id=current_user.id).all()
        return render_template('my-blogs.html', user_blogs=user_blogs, user=current_user, active_link='myblogs', year=year)

app.add_url_rule('/myblogs', view_func=GetUserBlogsView.as_view(name='getUserBlogs'))


class AddBlogView(View):
    '''View to handle adding of blogs'''
    
    methods = ['GET', 'POST']
    decorators = [login_required]
    
    def dispatch_request(self):
        
        form = AddBlogForm(request.form)
        messages = None
        
        if request.method == 'POST' and form.validate_on_submit():
            
            date = get_date()
            
            blog = Blog(
                title=form.title.data,
                subtitle=form.subtitle.data,
                image_url='https://img.freepik.com/free-photo/toy-bricks-table-with-word-blog_144627-47465.jpg?size=626&ext=jpg&uid=R65046554&ga=GA1.2.163047648.1692182630&semt=sph' if len(form.image_url.data) == 0 else form.image_url.data,
                blog_content=form.blog_content.data,
                created=date,
                updated=date,
                author_id=current_user.id
            )
            
            session.add(blog)
            session.commit()
            
            flash('Blog post added.')
            return redirect(url_for('getUserBlogs'))
        
        messages = form.form_errors
        print(messages)
        return render_template('forms/add-blog.html', form=form, user=current_user, active_link='addblog', year=year)
    
app.add_url_rule('/addBlog', view_func=AddBlogView.as_view(name='addBlog'))


class EditBlogView(View):
    '''View to handle editing of blogs'''
    
    methods = ['GET', 'POST']
    decorators = [login_required]
    
    def dispatch_request(self, id):
        message = None
        blog = database.get_or_404(Blog, id)
        
        form = EditBlogFrom(obj=blog)
        
        if request.method == 'POST' and form.validate_on_submit():
            date = get_date()
            form.populate_obj(blog)
            
            if blog.author_id == current_user.id:
                blog.updated = date
                session.commit()
                
                flash('Blog post updated.')
                return redirect(url_for('getBlog', id=blog.id))
            else:
                message = 'You cannot edit another user\'s post'
                return abort(code=401)
            
        return render_template('forms/edit-blog.html', form=form, blog=blog, user=current_user, message=message, active_link='myblogs', year=year)
    
app.add_url_rule('/blog/<int:id>/edit', view_func=EditBlogView.as_view(name='editBlog'))


class GetBlogView(View):
    '''View to get individual blogs'''
    
    # decorators = [login_required]
    
    def dispatch_request(self, id):
        form = AddCommentForm(request.form)
        
        # Filter database for blogs based on id
        blog =  database.get_or_404(Blog, id)
        
        return render_template('blog-detail.html', blog=blog, form=form, user=current_user, year=year)

app.add_url_rule('/blog/<int:id>', view_func=GetBlogView.as_view(name='getBlog'))


class DeleteBlogView(View):
    '''View to get individual blogs'''
    
    decorators = [login_required]
    
    def dispatch_request(self, id):
        message = None
        # Filter database for blogs based on id
        blog =  database.get_or_404(Blog, id)
        
        if blog.author_id == current_user.id: 
            session.delete(blog)
            session.commit()
            
            flash('Blog post deleted')
            return redirect(url_for('getUserBlogs'))
        else:
            message = 'You cannot delete another user\'s blog.'
            return abort(code=401)
            

app.add_url_rule('/blog/<int:id>/delete', view_func=DeleteBlogView.as_view(name='deleteBlog'))


class AddBlogCommentView(View):
    '''View to add comments to blogs'''
    
    methods = ['POST']
    
    def dispatch_request(self, id):
        form = AddCommentForm(request.form)
        blog = database.get_or_404(Blog, id)
        
        if request.method == 'POST' and form.validate_on_submit():
            date = get_date()
            
            # create comment object to add to database
            comment = Comment(
                comment=form.comment.data,
                created=date,
                blog_id=blog.id,
                author_id=current_user.id
            )
            
            session.add(comment)
            session.commit()
            
            flash('Comment added')
            
        return redirect(url_for('getBlog', id=blog.id))
        
        
app.add_url_rule('/blog/<int:id>/addComment', view_func=AddBlogCommentView.as_view(name='addComment'))



# Run app
if __name__ == '__main__':
    app.run(debug=True)
