class Extraccion: 
    
    def __init__(self, lat, lon, pais):
        self.lat = lat
        self.lon = lon
        self.pais = pais
        self.producto = producto
        
    def llamada_API(self, producto):
        
        self.producto = producto
    
        # hacemos la llamada  a la API
        url = f'http://www.7timer.info/bin/api.pl?lon=-{self.lon}&lat={self.lat}&product={producto}&output=json'

        response = requests.get(url=url)
        codigo_estado = response.status_code
        razon_estado = response.reason
        if codigo_estado == 200:
            print('La peticion se ha realizado correctamente, se ha devuelto el código de estado:',codigo_estado,' y como razón del código de estado: ',razon_estado)
        elif codigo_estado == 402:
            print('No se ha podido autorizar usario, se ha devuelto el código de estado:', codigo_estado,' y como razón del código de estado: ',razon_estado)
        elif codigo_estado == 404:
            print('Algo ha salido mal, el recurso no se ha encontrado,se ha devuelto el código de estado:', codigo_estado,' y como razón del código de estado: ',razon_estado)
        else:
            print('Algo inesperado ha ocurrido, se ha devuelto el código de estado:', codigo_estado,' y como razón del código de estado: ',razon_estado)

        # convertimos los resultados en un dataframe: 
        df_clima = pd.DataFrame.from_dict(pd.json_normalize(response.json()['dataseries']))
        return df_clima

    def juntar_dfs(self, df_completo, df_clima): 

        df["pais"]=self.pais
        df["latitud"]=self.lat
        df["longitud"]=self.lon

        df_completo = pd.concat([df_completo,df_clima], axis = 0)
    
        return df_completo

    def chequear_datos(self, df): 
    
        print("Las columnas son:", "\n")
        print(list(df.columns))
        print("-----------------------------------------")

        print("Los tipos de datos que tenemos son:", "\n")
        print(df.dtypes)
        print("-----------------------------------------")

        print("El porcentaje de nulos:", "\n")
        print((df.isnull().sum() / df.shape[0]) *  100)

    def insertar_fecha(self, df_completo): 

        hoy = datetime.now()
        hoy = datetime.strftime(hoy, '%Y-%m-%d') 

        df_completo["fecha"] = hoy #Creamos una columna dentro del DF

    def limpiar_dataframe(self, df, lista_columnas): 

        #convertimos la fecha a datetime
        df_completo["fecha"] = pd.to_datetime(df_completo["fecha"])

        # reemplazamos los nulos de las columnas por la media
        # lista de columnas en las que queremos reemplazar los nulos
        df_completo[lista_columnas]=df_completo[lista_columnas].fillna(df.mean())

        # quitar columnas repetidas:
        
        df_completo.drop(["ciudad_y"], axis = 1, inplace = True)
        
        # renombrar columnas
        
        df_completo.rename(columns = {"ciudad_x": "ciudad"}, inplace = True)

        # quitar % 
        df_completo["rh2m"] = df_completo["rh2m"].replace(r"%", "", regex = True)

        # guardamos los datos una vez limpios
        df_completo.to_pickle('datos_Madrid.pkl')
        df_completo.to_csv('datos_Madrid.csv')

        return df_completo