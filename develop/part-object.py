import os
import matplotlib.pyplot as plt
import cv2
from matplotlib.widgets import RectangleSelector
from lxml import etree
import xml.etree.cElementTree as ET

			#xmin = object.find('xmin').text
			#ymin = object.find('ymin').text
			#xmax = object.find('xmax').text
			#ymax = object.find('ymax').text
			#print(xml_file)
# global constants
img = None
tl_list = []
br_list = []
object_list = []

# constants

editdir = 'Annotat'
objtokeep = 'person'

if __name__ == '__main__':
	for n, xml_file in enumerate(os.scandir(editdir)):
		doc = ET.parse(xml_file)
		root = doc.getroot()
		print(xml_file)
		for object in root.findall('object'):
			for part in object.findall('part'):
				name = part.find('name').text
				for bndbox in part.findall('bndbox'):
					xmin = bndbox.find('xmin').text
					ymin = bndbox.find('ymin').text
					xmax = bndbox.find('xmax').text
					ymax = bndbox.find('ymax').text
					#print("name: " + name)
					print("name: " + name + "  xmin:  " +xmin)
				ob = ET.SubElement(root, 'object')
				ET.SubElement(ob, 'name').text = name
				ET.SubElement(ob, 'pose').text = 'Unspecified'
				ET.SubElement(ob, 'truncated').text = '0'
				ET.SubElement(ob, 'difficult').text = '0'
				bbox = ET.SubElement(ob, 'bndbox')
				ET.SubElement(bbox, 'xmin').text = xmin
				ET.SubElement(bbox, 'ymin').text = ymin
				ET.SubElement(bbox, 'xmax').text = xmax
				ET.SubElement(bbox, 'ymax').text = ymax
				object.remove(part)
		doc.write(xml_file)
	print('end program')



		