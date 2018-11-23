from lxml import etree
import re, time

class parser():
	def search(self, string):
		reg = r"<\/GANGLIA_XML>"
		m = re.search(reg, string)

		if m is None:
			return 0

		return 1

	def recvAll(self, socket, size):
		chunks = []
		c = self.search('')
		while c < 1:
		    chunk = socket.recv(size)
		    chunks.append(chunk)
		    str = ''.join(chunks)
		    c = self.search(str)
		
		return ''.join(chunks)

	def parse(self, xml):
		d = {}

		root = etree.fromstring(xml)
		ms = etree.XPath("//METRIC")
		cs = etree.XPath("//CLUSTER")

		cluster = cs(root)

		for i in ms(root):
			tn = cluster[0].attrib['NAME'].replace('-', '_') + '_' + i.attrib['NAME'].replace('-', '_').replace('.', '_')
			d.setdefault(tn, [])
			n = [
				i.getparent().attrib['REPORTED'],
	    		i.attrib['VAL'],
	    		i.getparent().attrib['NAME'],
	    		i.getparent().attrib['IP'],
	    		i.attrib['TN'],
	    		i.attrib['TMAX'],
				i.attrib['DMAX']
			]

			d[tn].append(n)

		return d