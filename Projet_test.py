import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

# --- 1. CRÉATION DU PDF ---
def create_pdf(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "Récapitulatif F1 - Test Automatique")
    
    c.setFont("Helvetica", 12)
    c.drawString(100, 720, "Ceci est un exemple de document généré par ton futur système.")
    c.drawString(100, 700, "Résultats du week-end :")
    
    # Simulation de données
    c.drawString(120, 680, "- Vainqueur : Max Verstappen")
    c.drawString(120, 660, "- Meilleur tour : Lando Norris")
    c.drawString(120, 640, "- Incident : Safety Car au tour 12")
    
    c.save()

# --- 2. ENVOI DU MAIL ---
def send_email(receiver_email, file_to_attach):
    # Paramètres de connexion (Exemple pour Gmail)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "robin.nagel2001@gmail.com"
    password = "vtgawtwbluxpzbtl" # Ne pas utiliser le mot de passe principal

    # Création du message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "🏎️ Ton Récap F1 est arrivé !"

    body = "Salut ! Voici le compte-rendu du dernier Grand Prix en pièce jointe."
    msg.attach(MIMEText(body, 'plain'))

    # Pièce jointe
    with open(file_to_attach, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {file_to_attach}")
        msg.attach(part)

    # Envoi réel
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)
        server.quit()
        print("Mail envoyé avec succès !")
    except Exception as e:
        print(f"Erreur lors de l'envoi : {e}")

# --- EXÉCUTION ---
pdf_name = "Recap_F1_Test.pdf"
create_pdf(pdf_name)
send_email("robin.nagel2001@gmail.com", pdf_name)