#!/usr/bin/env python3
from ..exceptions import ValidationError, InternalServerError



# importamos la libreria smtplib (no es necesario instalarlo)
import smtplib 
import getpass, poplib
# importamos librerias  para construir el mensaje
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.parser import Parser
from email.message import Message


class email:

	def send_email(addr_to,addr_from,smtp_user,smtp_pass,msg):
		#print("Hola enviando correo",addr_to,addr_from)
		# inicializamos el stmp para hacer el envio
		server = smtplib.SMTP("smtp.gmail.com", 587)
		server.starttls()
		#logeamos con los datos ya seteamos en la parte superior
		server.login(smtp_user,smtp_pass)
		#el envio
		server.sendmail(addr_from, addr_to, msg.as_string())
		#apagamos conexion stmp
		server.quit()

	def read_email(addr_to,addr_from,smtp_user,smtp_pass,msg):
		# Se establece conexion con el servidor pop de gmail
		m = poplib.POP3_SSL('pop.gmail.com',995)
		m.user(smtp_user)
		m.pass_(smtp_pass)
		numero = len(m.list()[1])
		print(numero)
		#print(m.noop())
		#print(m.retr(1))
		mensaje = ""
		# Se mete todo el mensaje en un unico string
		for i in range(1):
			response, headerLines, bytes = m.retr(i+1)
			for j in range(len(headerLines)):
				mgs = '\n'+str(headerLines[j])
				#print(mgs)
				mensaje += mgs
			#mensaje= headerLines.join("\n")
			print(headerLines)
			#mensaje= '\n'.join(headerLines)
			print("pro")
			print(mensaje)
			p = Parser()
			email = p.parsestr(mensaje)
			#print(email)
			# Se sacan por pantalla los campos from, to y subject
			#print ("From: "+email["From:"])
			#print ("To: "+email["To"])
			#print ("Subject: "+email["Subject"])

	@staticmethod
	def get_email(addr_to,name,phone,message):
		# definimos los correo de remitente y receptor
		##se envia un mail a
		#addr_to   = 'angelica.accexasociadossas@gmail.com'#'davidzuluaga1991@gmail.com'
		##el mail sale desde el correo
		addr_from = 'davidzuluaga1991@gmail.com'#'angelica.accexasociadossas@gmail.com'
		# Define SMTP email server details
		# smtp_server = 'mail.gmail.com'
		smtp_user   = "davidzuluaga1991@gmail.com"
		smtp_pass   = '19910808Dz'
		#message = 'Hola Buenas Tardes' 
		# Construimos el mail
		msg = MIMEMultipart() 
		msg['To'] = addr_to
		msg['From'] = addr_from
		msg['Subject'] = 'Ingresaron a un Formulario'
		#cuerpo del mensaje en HTML y si fuera solo text puede colocar en el 2da parametro 'plain'
		msg.attach(MIMEText('<div style="display: block; position:absolute; top:100px; left:150px; width:300px; background-color:#92a8d1; border-radius: 10px; border-style:solid; border-width:10px; border-color: #92a8d1;"><div> Para:  '+ addr_to +'</div> <div><br></div><div><br></div> <div>Asunto: '+message+'<div></div> <br></div> </div>','html'))
		
		email.send_email(addr_to = addr_to,addr_from = addr_from,smtp_user = smtp_user,smtp_pass = smtp_pass,msg = msg)
		#addr_to = "produccion1@softpymes.com.co"
		#email(addr_to = addr_to,addr_from = addr_from,smtp_user = smtp_user,smtp_pass = smtp_pass)
		return "Envio los Datos al Correo"
	#return get_email