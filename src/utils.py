

def transformar(modelo : object, schema : object):
    print('holaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaas')
    lista_schema = []
    for esto in dir(schema): 
        if '__' not in esto: 
            lista_schema.append(esto)
    lista_modelo = []
    for esto in dir(modelo): 
        if '__' not in esto:
            lista_modelo.append(esto)
 
    for esto in lista_schema: 
        if esto in lista_modelo: 
            print(esto)
            schema[esto] = modelo[esto]

    return schema