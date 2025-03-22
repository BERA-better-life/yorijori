import csv
import os
import django
import sys

os.chdir(".")
print("Current dir=", end=""), print(os.getcwd())

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("BASE_DIR=", end=""), print(BASE_DIR)

sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yorijori.settings")	# 1. 여기서 프로젝트명.settings입력
django.setup()
 
 # 위의 과정까지가 python manage.py shell을 키는 것과 비슷한 효과

from recipes.models import *	# 2. App이름.models
CSV_PATH = './data/recipes.csv'	# 3. csv 파일 경로
with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:	# 4. newline =''
    data_reader = csv.DictReader(csvfile)
    for row in data_reader:
        print(row)
        Recipe.objects.create(		# 5. class명.objects.create
            rcp_seq = row['RCP_SEQ'], #class 필드: csv 필드
            rcp_nm = row['RCP_NM'],
            rcp_way2 = row['RCP_WAY2'],
            rcp_pat2 = row['RCP_PAT2'],
            info_wgt = row['INFO_WGT'],
            info_eng = row['INFO_ENG'],
            info_car = row['INFO_CAR'],
            info_pro = row['INFO_PRO'],
            info_fat = row['INFO_FAT'],
            info_na =  row['INFO_NA'],
            hash_tag = row['HASH_TAG'],
            