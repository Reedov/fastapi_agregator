from sqlalchemy import ForeignKey, MetaData, Table, Column, Integer, String, Boolean, sql, Text, DateTime
import sqlalchemy.types as tp

metadata = MetaData()

#  ############## таблица пользователей ##########################
users_table = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('email', String(50), unique=True, index=True),
    Column('name', String(50)),
    Column('password_hash', String()),
    Column(
        'is_active',
        Boolean(),
        server_default=sql.expression.true(),  # True по дефолту
        nullable=False
    ),
)


tokens_table = Table(
    'tokens',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('token', )
)

#  ############## таблица ресурсов ##########################
sources_table = Table(
    'sources',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50), nullable=False),
    Column('url', String(100), unique=True, nullable=False),
    Column('get_items', Integer, nullable=False),
    Column(
        'is_active',
        Boolean(),
        server_default=sql.expression.true(),  # True по дефолту
        nullable=False
    ),
)
# ############### таблица постов ############################
posts_table = Table(
    'posts',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('posted_at', DateTime()),
    Column('source_id', ForeignKey(sources_table.c.id)),
    Column('title', String(255)),
    Column('content', Text()),
    Column('url', String(100)),
    Column('img_url', String(100))
)
