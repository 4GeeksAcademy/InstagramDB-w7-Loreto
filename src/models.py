from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, ForeignKey, Float, Table
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

follower = Table(
    'follower',
    Base.metadata,
    Column('user_from_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('user_to_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('created_at', DateTime, nullable=False)
)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    user_name = Column(String(120), nullable=False, unique=True)
    email = Column(String(120), nullable=False, unique=True)
    password = Column(String(120), nullable=False)
    active = Column(Boolean, default=True)
    last_login = Column(DateTime)

    # uselist= False uno a uno, 1:1
    profile = relationship('Profile', uselist=False)

    # un usuario muchos posts, comments, 1:N
    post = relationship('Post', back_populates="user")
    comment = relationship('Comment', back_populates="user")

    # autoreferencia follower following- *:*
    following = relationship(
        "User",
        secondary=follower,
        # how the current User (the "left" side) connects to the association table
        primaryjoin=id == follower.columns.user_from_id,
        # how the association table connects to the other User (the "right" side, the related object).
        secondaryjoin=id == follower.columns.user_to_id,
        # reverse relationship on the class followers
        backref="followers"
    )


class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True)
    name = Column(String(120))
    biography = Text(String)
    facebook = Column(String(120))
    avatar = Column(String)

    used_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='profiles')


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    caption = Column(String(120))
    location = Column(String)
    content_text = Text(String(200))
    published_at = Column(String(120))

    used_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates="posts")

    # relacion hace regferencia al nombre del modelo no de la table
    # un post muchos media, comments 1:N

    media = relationship('Media', back_populates='posts')
    comments = relationship('Comment', back_populates='posts')


class Media(Base):
    __tablename__ = "medias"
    id = Column(Integer, primary_key=True)
    type = Column(String(20))
    url = Column(String)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    post = relationship('Post', back_populates="medias")

    post = relationship('Post', back_populates='medias')


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    comment_text = Text(String(300))
    created_at = Column(DateTime)
    used_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)

    user = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')
