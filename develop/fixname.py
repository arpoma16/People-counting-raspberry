import os
import cv2
from lxml import etree
import xml.etree.cElementTree as ET

direct = 'Anotation'
directnew = 'anotFix'

if __name__ == '__main__':

	if not os.path.isdir(directnew):
		os.makedirs(directnew)

	for n, xml_file in enumerate(os.scandir(direct)):
		doc = ET.parse(xml_file)
		root = doc.getroot()
		file= root.find('filename')
		name = str(int(file.text) - 1)
		file.text = name
		print('name: ' ,name )
		#save_path = os.path.join(directnew, name +".xml")
		#with open(save_path, 'wb') as temp_xml:
		#	temp_xml.write(xml_file)
		xml_str = ET.tostring(root)
		root = etree.fromstring(xml_str)
		xml_str = etree.tostring(root, pretty_print=True)
		save_path = os.path.join(directnew, name +".xml")
		with open(save_path, 'wb') as temp_xml:
			temp_xml.write(xml_str)

