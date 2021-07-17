from Google import Create_Service


def getMessageList(tipo):
    list_id = []
    CLIENT_SECRET_FILE = 'client_secret.json'
    API_NAME = 'gmail'
    API_VERSION = 'v1'
    SCOPES = ['https://mail.google.com/']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    messages = service.users().messages().list(userId='me', includeSpamTrash=False,
                                               maxResults=25, pageToken='1', q=tipo).execute()

    for index, valor1 in enumerate(messages["messages"]):
        for llave, valor2 in valor1.items():
            if llave == "id":
                list_id.append(valor2)

    return(messages["resultSizeEstimate"], list_id)


def getContentMessages(tipo):
    lista_completa = getMessageList(tipo)
    lista_iterable = lista_completa[1]

    # print(lista_iterable[0])

    CLIENT_SECRET_FILE = 'client_secret.json'
    API_NAME = 'gmail'
    API_VERSION = 'v1'
    SCOPES = ['https://mail.google.com/']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    lista_email = []

    if tipo == 'is:inbox':
        for x in lista_iterable:
            contenido_mensajes = service.users().messages().get(
                userId='me', id=x, format='full').execute()

            de = contenido_mensajes["payload"]["headers"][0]['value']
            hora = contenido_mensajes["payload"]["headers"][1]['value']
            body = contenido_mensajes["payload"]["parts"][1]['body']['data']
            subject = contenido_mensajes["payload"]["headers"][19]['value']
            resumen = contenido_mensajes["snippet"]

            email = [de, hora, subject, body, resumen]
            lista_email.append(email)
    elif tipo == 'in:sent':
        for x in lista_iterable:
            contenido_mensajes = service.users().messages().get(
                userId='me', id=x, format='full').execute()

            subject = contenido_mensajes["payload"]["headers"][3]['value']
            hora = contenido_mensajes["payload"]["headers"][1]['value']
            body = contenido_mensajes["payload"]["parts"][0]['body']['data']
            para = contenido_mensajes["payload"]["headers"][5]['value']
            resumen = contenido_mensajes["snippet"]

            email = [para, hora, subject, body, resumen]
            lista_email.append(email)
    elif tipo == 'is:unread':
        for x in lista_iterable:
            contenido_mensajes = service.users().messages().get(
                userId='me', id=x, format='full').execute()

            de = contenido_mensajes["payload"]["headers"][16]['value']
            hora = contenido_mensajes["payload"]["headers"][17]['value']
            subject = contenido_mensajes["payload"]["headers"][19]['value']
            resumen = contenido_mensajes["payload"]["headers"][3]['value']
            body = contenido_mensajes["payload"]["parts"][0]['body']['data']

            email = [de, hora, subject, body, resumen]
            lista_email.append(email)
    else:
        pass

    return(lista_email)
