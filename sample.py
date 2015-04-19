import os
import shutil
import glob

from lxml import etree

ctr = 0
TOTAL = 5000
INPUT_FOLDER = "data"
SAMPLE_FOLDER = "sample"
SAMPLE_CATEGORY = "cricket"




for xml_file in glob.glob(os.path.join(INPUT_FOLDER,"*")):

	if(ctr == TOTAL):
		break

	tree = etree.parse(xml_file)
	root = tree.getroot()

	for cat in root.find('CATEGORIES'):
		if(SAMPLE_CATEGORY in cat.text):
			#print xml_file
			#print cat.text
			#print xml_file.lstrip(INPUT_FOLDER).lstrip('/')
			print os.path.join(SAMPLE_FOLDER, xml_file.lstrip(INPUT_FOLDER).lstrip('/'))
			shutil.copy(xml_file, os.path.join(SAMPLE_FOLDER, xml_file.lstrip(INPUT_FOLDER).lstrip('/')))
			print ctr
			ctr += 1
			break


