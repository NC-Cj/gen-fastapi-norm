from environs import Env

env = Env()

DATABASE_URL = env.str('DATABASE_URL')
REDIS_DATABASE_URL = env.str('REDIS_DATABASE_URL')
