from .base_settings import *
DEBUG = False
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',     # 引擎
        'LOCATION':"redis://192.168.42.128:6379/10",
        'TIMEOUT': 300,            # 缓存超时时间（默认300，None表示永不过期，0表示立即过期）
        'OPTIONS':{
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            'PASSWORD':'root123',
            'MAX_ENTRIES': 300,       # 最大缓存个数（默认300）
            'CULL_FREQUENCY': 3,    # 缓存到达最大个数之后，剔除缓存个数的比例，（默认3）
        },
        'KEY_PREFIX': '',          # 缓存key的前缀（默认空）
        'VERSION': 1,              # 缓存key的版本（默认1）
        # 'KEY_FUNCTION'： 函数名     # 生成key的函数（默认函数会生成为：【前缀:版本:key】）
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'drf_web_two',
        'USER': 'root',
        'PASSWORD': 'Root123!',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}