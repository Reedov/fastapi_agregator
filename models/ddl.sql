-- таблица пользователей --
CREATE TABLE users (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   username   TEXT  NOT NULL UNIQUE,
   email TEXT NOT NULL UNIQUE,
   second_name  TEXT,
   first_name   TEXT,
   birthdate  TIMESTAMP
   password_hash TEXT NOT NULL,
   created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- таблица подписок --
CREATE TABLE subscribes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id),
    source_id INTEGER REFERENCES sources(id),
    UNIQUE(user_id, source_id)
);

-- таблица типов ресурсов --
CREATE TABLE source_type (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
);

-- таблица ресурсов --
CREATE TABLE sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    url TEXT,
    get_items INTEGER,
    is_active INTEGER, -- boolean
    type_id INTEGER REFERENCES source_type(id),
    get_period_sec INTEGER,
    icon TEXT  DEFAULT 'default.ico',
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

-- таблица посещения ресурсов --
CREATE TABLE sources_get (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id INTEGER REFERENCES sources(id) UNIQUE,
    get_at  TIMESTAMP
    );

-- таблица постов --
CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    posted_at TIMESTAMP,
    source_id INTEGER REFERENCES sources(id),
    title TEXT,
    content TEXT,
    url TEXT,
    img_url TEXT,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(source_id, title)
);

-- таблица логгирования запросов --
CREATE TABLE requests_log(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    requested_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    client_host TEXT,
    url TEXT
);
