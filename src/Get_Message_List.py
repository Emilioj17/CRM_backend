from Google import Create_Service


def getMessageList():
    list_id = []
    CLIENT_SECRET_FILE = 'client_secret.json'
    API_NAME = 'gmail'
    API_VERSION = 'v1'
    SCOPES = ['https://mail.google.com/']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    messages = service.users().messages().list(userId='me', includeSpamTrash=False,
                                               maxResults=25, pageToken='1', q='is:inbox').execute()

    for index, valor1 in enumerate(messages["messages"]):
        for llave, valor2 in valor1.items():
            if llave == "id":
                list_id.append(valor2)

    return(messages["resultSizeEstimate"], list_id)


def getContentMessages():
    lista_completa = getMessageList()
    lista_iterable = lista_completa[1]

    print(lista_iterable[0])

    CLIENT_SECRET_FILE = 'client_secret.json'
    API_NAME = 'gmail'
    API_VERSION = 'v1'
    SCOPES = ['https://mail.google.com/']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    contenido_mensajes = service.users().messages().get(
        userId='me', id=lista_iterable[0], format='full').execute()

    de = contenido_mensajes["payload"]["headers"][0]['value']
    hora = contenido_mensajes["payload"]["headers"][1]['value']
    body = contenido_mensajes["payload"]["parts"][1]['body']['data']
    resumen = contenido_mensajes["snippet"]

    email = [de, hora, body, resumen]

    return(email)
