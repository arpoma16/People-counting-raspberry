import os
direct = 'database1'
depimg = 'database'
depxml = 'anotFix'

if __name__ == '__main__':
	for img_file, xmldep in zip(enumerate(os.scandir(depimg)), enumerate(os.scandir(depxml))):
		nam = os.path.basename(img_file[1] .name).split(".")
		namxml = os.path.basename(xmldep[1] .name).split(".")
		print(nam[0] , namxml[0])
		state = True
		for n, img_dep in enumerate(os.scandir(direct)):
			namdep = os.path.basename(img_dep .name).split(".")
			if namdep[0] == nam[0]:
				state = False
		if state:
			os.remove(img_file[1])
			os.remove(xmldep[1])

			namdep =[]
		nam =[]
		namxml = []
		"""for n, xml_file in enumerate(os.scandir(depxml)):
			namxml = os.path.basename(xml_file .name).split(".")
			print(namxml[0])
			namxml =[]"""