#!/usr/bin/env python
import csv
import os
import sys

sys.path.append("..")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_states.settings")

from main.models import State, City

csv_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "zip_codes_states.csv")

print csv_file_path

csv_file = open(csv_file_path, 'r')

reader = csv.DictReader(csv_file)

for row in reader:
	
	try:
		state_obj, created = State.objects.get_or_create(abbreviation=row['state'])
	except Exception, e:
		print e
		print row['state']


	city_obj, created = City.objects.get_or_create(zip_code=row['zip_code'])

	city_obj.name = row['city']
	city_obj.county = row['county']
	city_obj.latitude = row['latitude']
	city_obj.longitude = row['longitude']
	city_obj.state = state_obj

	try:
		city_obj.save()
	except Exception, e:
		print e
		print row['city']
		print row['state']


	print city_obj.name
	print created

#"zip_code","latitude","longitude","city","state","county"

#name = models.CharField(max_length=30, null=True)
	#county = models.CharField(max_length=30, null=True)
	#zip_code = models.IntegerField(null=True)
	#latitude = models.FloatField(null=True)
	#longitude = models.FloatField(null=True)
	#state = models.ForeignKey('main.State', null=True)