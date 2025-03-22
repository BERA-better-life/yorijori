import csv
import os
from django.core.management.base import BaseCommand
from recipes.models import Recipe
from django.conf import settings

class Command(BaseCommand):
    help = 'CSV 파일을 MySQL RDS 데이터베이스에 로드합니다.'

    def handle(self, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, 'data', 'recipes.csv')

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Recipe.objects.create(
                    rcp_seq=row['RCP_SEQ'],
                    rcp_nm=row['RCP_NM'],
                    rcp_way2=row['RCP_WAY2'],
                    rcp_pat2=row['RCP_PAT2'],
                    info_wgt=row.get('INFO_WGT', None),
                    info_eng=row.get('INFO_ENG', None),
                    info_car=row.get('INFO_CAR', None),
                    info_pro=row.get('INFO_PRO', None),
                    info_fat=row.get('INFO_FAT', None),
                    info_na=row.get('INFO_NA', None),
                    hash_tag=row.get('HASH_TAG', None),
                    att_file_no_main=row.get('ATT_FILE_NO_MAIN', None),
                    att_file_no_mk=row.get('ATT_FILE_NO_MK', None),
                    rcp_parts_dtls=row.get('RCP_PARTS_DTLS', None),
                )
        self.stdout.write(self.style.SUCCESS('✅ CSV 데이터 로드 완료!'))
