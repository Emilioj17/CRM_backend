from Google import Create_Service


def getContentMessages(tipo):
    lista_iterable = []
    lista_email = []
    CLIENT_SECRET_FILE = 'client_secret.json'
    API_NAME = 'gmail'
    API_VERSION = 'v1'
    SCOPES = ['https://mail.google.com/']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    messages = service.users().messages().list(userId='me', includeSpamTrash=False,
                                               maxResults=10, pageToken='1', q=tipo).execute()

    for index, valor1 in enumerate(messages["messages"]):
        for llave, valor2 in valor1.items():
            if llave == "id":
                lista_iterable.append(valor2)

    if tipo == 'is:inbox':
        for x in lista_iterable:
            contenido_mensajes = service.users().messages().get(
                userId='me', id=x, format='full').execute()

            for x in contenido_mensajes["payload"]["headers"]:
                # Reply-To  Delivered-To
                if x["name"] == "Reply-To":
                    de = x["value"]
                if x["name"] == "Date":
                    hora = x["value"]
                if x["name"] == "Subject":
                    subject = x["value"]

            body = contenido_mensajes["payload"]["parts"][1]['body']['data']
            resumen = contenido_mensajes["snippet"]

            email = [de, hora, subject, body, resumen]
            lista_email.append(email)

    elif tipo == 'in:sent':
        for x in lista_iterable:
            contenido_mensajes = service.users().messages().get(
                userId='me', id=x, format='full').execute()

            for x in contenido_mensajes["payload"]["headers"]:
                # Reply-To  Delivered-To to
                if x["name"] == "to":
                    para = x["value"]
                if x["name"] == "Date":
                    hora = x["value"]
                if x["name"] == "subject":
                    subject = x["value"]

            body = contenido_mensajes["payload"]["parts"][0]['body']['data']
            resumen = contenido_mensajes["snippet"]

            email = [para, hora, subject, body, resumen]
            lista_email.append(email)

    return(lista_email)
