#!/usr/bin/env python

from decouple import config
from unipath import Path

BASE_DIR = Path(__file__).parent

ELASTIC_CLOUD_ID = config("ELASTIC_CLOUD_ID", cast=str)
ELASTIC_USERNAME = config("ELASTIC_USERNAME", cast=str)
ELASTIC_PASSWORD = config("ELASTIC_PASSWORD", cast=str)

ES_INDEX = config("ES_INDEX", cast=str)

BASE_URL = config("BASE_URL", cast=str)

LLM_SERVICE = config("LLM_SERVICE", cast=str, default="supercoolLLM")

SOME_NUMBER = config("SOME_NUMBER", cast=str, default=10)
ANOTHER_NUMBER = config("ANOTHER_NUMBER", cast=int, default=10)
