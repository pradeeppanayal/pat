
__version__ = 'develop'
__author__ = 'Pradeep CH'


class HTML(object):
	def printHeader(self,title,contenttype='Content-type:text/html'):
		print "%s\r\n\r\n" %contenttype
		print "<html>"
		print "<head>"
		print "<title>%s</title>" %title
		print "</head>"

	def printBodyContent(self,content):
		print "<body>"
		print "<body>"
		print content
		print "</body>"
		print "</html>"

	def getBackButton(self,href):
		return "<a href='%s' style='color:blue'>Go back</a></br></br>" %href
