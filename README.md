# PAT
PAT is an application developed with HTML, JS as frontend and Python as backend. It uses CGI to communicate. 

# Features
PAT is multi utility application.PAT allows
* To Generate/SIGN SSL certificate 
* To manage DHCP with VMware/Proxmos
* Reset/Authentication check ARISTA EOS nodes
* Image push and config push to EOS devices using eAPI/SSH
* Easy remote SSH
* Open VMWare node console in your machine from PAT server

# Usage
Install java
Install python
Set JAVA_HOME or JRE_HOME
Change context to enable CGI and set python path
Copy "v2" folder to '/webapps/pat/' folder
Copy "cgi" to the configured cgi poth. Example /webapps/pat/WEB_INF/cgi
Start tomcat 
PAT URL : http://127.0.0.1:8080/pat/v2





