import psycopg2
from dotenv import load_dotenv
import os
from pathlib import Path

caminho_env = Path(__file__).resolve().parent.parent / 'config' / '.env'

load_dotenv(dotenv_path=caminho_env)

DATABASE_URL = os.getenv("DATABASE_URL")

connection = psycopg2.connect(DATABASE_URL)
