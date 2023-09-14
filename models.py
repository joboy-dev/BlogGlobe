from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    '''Users table/model'''
    
    __table_name__ = 'user'
    
    id = sa.Column(sa.Integer, primary_key=True)
    full_name = sa.Column(sa.Text, nullable=False)
    username = sa.Column(sa.String, unique=True, nullable=False)
    email = sa.Column(sa.String, unique=True, nullable=False)
    password = sa.Column(sa.String, nullable=False)
    profile_picture = sa.Column(sa.String, nullable=False)
    
    posts = relationship('Blog', back_populates='post_author')
    comments = relationship('Comment', back_populates='comment_author')
    
    def __str__(self):
        return f'{self.id} | {self.username} | {self.email}'


class Blog(db.Model):
    '''Posts table/model'''
    
    __table_name__ = 'blog'
    
    id =  sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String, nullable=False)
    subtitle = sa.Column(sa.String, nullable=False)
    image_url = sa.Column(sa.String, nullable=False)
    blog_content = sa.Column(sa.Text, nullable=False)
    created = sa.Column(sa.String)
    updated = sa.Column(sa.String)
    
    author_id = sa.Column(sa.Integer, sa.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    post_author = relationship('User', back_populates='posts')
    comments = relationship('Comment', back_populates='parent_post')
    
    def __str__(self):
        return f'{self.title}'
    

class Comment(db.Model):
    '''Comnents table/model'''
    
    __table_name__ = 'comment'
    
    id =  sa.Column(sa.Integer, primary_key=True)
    comment = sa.Column(sa.String, nullable=True)
    created = sa.Column(sa.String)
    
    blog_id = sa.Column(sa.Integer, sa.ForeignKey('blog.id', ondelete='CASCADE'), nullable=False)
    parent_post = relationship('Blog', back_populates='comments')
    
    author_id = sa.Column(sa.Integer, sa.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    comment_author = relationship('User', back_populates='comments')
    
