from math import ceil

class DistribucionObjetosMagicos:
    def __init__(self):
        # Definir la tabla de distribución base por nivel
        self.tabla_distribucion = {
            "1-4": {"comun": 6, "poco_comun": 4, "raro": 1, "muy_raro": 0, "legendario": 0},
            "5-10": {"comun": 10, "poco_comun": 17, "raro": 6, "muy_raro": 1, "legendario": 0},
            "11-16": {"comun": 3, "poco_comun": 7, "raro": 11, "muy_raro": 7, "legendario": 2},
            "17-20": {"comun": 0, "poco_comun": 0, "raro": 5, "muy_raro": 11, "legendario": 9}
        }

    def calcular_objetos_acumulados(self, nivel):
        """
        Calcula el total de objetos mágicos acumulados hasta el nivel especificado
        """
        objetos_totales = {
            "comun": 0,
            "poco_comun": 0,
            "raro": 0,
            "muy_raro": 0,
            "legendario": 0
        }
        
        rangos_nivel = ["1-4", "5-10", "11-16", "17-20"]
        nivel = int(nivel)
        
        for rango in rangos_nivel:
            inicio, fin = map(int, rango.split('-'))
            if nivel >= inicio:
                for tipo, cantidad in self.tabla_distribucion[rango].items():
                    objetos_totales[tipo] += cantidad
            if nivel <= fin:
                break
                
        return objetos_totales

    def obtener_total_por_tipo(self, nivel):
        """
        Muestra el total de objetos de cada tipo para un nivel dado en formato de tabla ASCII
        """
        totales = self.calcular_objetos_acumulados(nivel)
        
        # Caracteres para la tabla
        esquina_sup_izq = '┌'
        esquina_sup_der = '┐'
        esquina_inf_izq = '└'
        esquina_inf_der = '┘'
        linea_horizontal = '─'
        linea_vertical = '│'
        union_izq = '├'
        union_der = '┤'
        union_sup = '┬'
        union_inf = '┴'
        cruz = '┼'
        
        # Formato de las columnas
        ancho_col1 = 15
        ancho_col2 = 8
        
        # Crear líneas de la tabla
        linea_superior = f"{esquina_sup_izq}{linea_horizontal * ancho_col1}{union_sup}{linea_horizontal * ancho_col2}{esquina_sup_der}"
        linea_media = f"{union_izq}{linea_horizontal * ancho_col1}{cruz}{linea_horizontal * ancho_col2}{union_der}"
        linea_inferior = f"{esquina_inf_izq}{linea_horizontal * ancho_col1}{union_inf}{linea_horizontal * ancho_col2}{esquina_inf_der}"
        
        # Formato para las filas
        formato_fila = f"{linea_vertical}{{:<{ancho_col1}}}{linea_vertical}{{:>{ancho_col2}}}{linea_vertical}"
        
        # Construir la tabla
        tabla = [
            f"\nNivel {nivel}:",
            linea_superior,
            formato_fila.format("Tipo", "Cantidad"),
            linea_media,
            formato_fila.format("Comunes", totales['comun']),
            formato_fila.format("Poco comunes", totales['poco_comun']),
            formato_fila.format("Raros", totales['raro']),
            formato_fila.format("Muy raros", totales['muy_raro']),
            formato_fila.format("Legendarios", totales['legendario']),
            linea_media,
            formato_fila.format("Total", sum(totales.values())),
            linea_inferior
        ]
        
        return "\n".join(tabla)

    def obtener_tabla_por_personaje(self):
        """
        Muestra una tabla formateada con la distribución de objetos mágicos por nivel
        """
        # Caracteres para la tabla
        esquina_sup_izq = '┌'
        esquina_sup_der = '┐'
        esquina_inf_izq = '└'
        esquina_inf_der = '┘'
        linea_horizontal = '─'
        linea_vertical = '│'
        union_izq = '├'
        union_der = '┤'
        union_sup = '┬'
        union_inf = '┴'
        cruz = '┼'
        
        # Anchos de columnas
        anchos = {
            'nivel': 10,
            'comun': 8,
            'poco_comun': 12,
            'raro': 8,
            'muy_raro': 10,
            'legendario': 10,
            'total': 8
        }
        
        # Crear líneas de la tabla
        linea_superior = esquina_sup_izq
        linea_media = union_izq
        linea_inferior = esquina_inf_izq
        
        for i, ancho in enumerate(anchos.values()):
            linea_superior += linea_horizontal * ancho + (esquina_sup_der if i == len(anchos)-1 else union_sup)
            linea_media += linea_horizontal * ancho + (union_der if i == len(anchos)-1 else cruz)
            linea_inferior += linea_horizontal * ancho + (esquina_inf_der if i == len(anchos)-1 else union_inf)
        
        # Formato para las filas
        formato_fila = linea_vertical
        for ancho in anchos.values():
            formato_fila += f"{{:^{ancho}}}{linea_vertical}"
        
        # Headers
        headers = ["Nivel", "Común", "Poco Común", "Raro", "Muy Raro", "Legendario", "Total"]
        niveles = [
            ("1-4", 6, 4, 1, 0, 0),
            ("5-10", 10, 17, 6, 1, 0),
            ("11-16", 3, 7, 11, 7, 2),
            ("17-20", 0, 0, 5, 11, 9)
        ]
        
        # Construir la tabla
        tabla = [
            "\nDistribución de objetos mágicos por nivel:",
            linea_superior,
            formato_fila.format(*headers),
            linea_media
        ]
        
        for nivel_info in niveles:
            nivel, comun, poco_comun, raro, muy_raro, legendario = nivel_info
            total = comun + poco_comun + raro + muy_raro + legendario
            fila = [nivel, str(comun), str(poco_comun), str(raro), str(muy_raro), str(legendario), str(total)]
            tabla.append(formato_fila.format(*fila))
            if nivel_info != niveles[-1]:
                tabla.append(linea_media)
        
        tabla.append(linea_inferior)
        return "\n".join(tabla)

    def obtener_tabla_totales_acumulados(self):
        """
        Muestra una tabla con los totales acumulados de objetos mágicos por nivel
        """
        # Caracteres para la tabla
        esquina_sup_izq = '┌'
        esquina_sup_der = '┐'
        esquina_inf_izq = '└'
        esquina_inf_der = '┘'
        linea_horizontal = '─'
        linea_vertical = '│'
        union_izq = '├'
        union_der = '┤'
        union_sup = '┬'
        union_inf = '┴'
        cruz = '┼'
        
        # Anchos de columnas
        anchos = {
            'nivel': 10,
            'comun': 8,
            'poco_comun': 12,
            'raro': 8,
            'muy_raro': 10,
            'legendario': 10,
            'total': 8
        }
        
        # Crear líneas de la tabla
        linea_superior = esquina_sup_izq
        linea_media = union_izq
        linea_inferior = esquina_inf_izq
        
        for i, ancho in enumerate(anchos.values()):
            linea_superior += linea_horizontal * ancho + (esquina_sup_der if i == len(anchos)-1 else union_sup)
            linea_media += linea_horizontal * ancho + (union_der if i == len(anchos)-1 else cruz)
            linea_inferior += linea_horizontal * ancho + (esquina_inf_der if i == len(anchos)-1 else union_inf)
        
        # Formato para las filas
        formato_fila = linea_vertical
        for ancho in anchos.values():
            formato_fila += f"{{:^{ancho}}}{linea_vertical}"
        
        # Headers
        headers = ["Nivel", "Común", "Poco Común", "Raro", "Muy Raro", "Legendario", "Total"]
        niveles_muestra = ["1-4", "5-10", "11-16", "17-20"]
        
        # Construir la tabla
        tabla = [
            "\nTotales acumulados de objetos mágicos por nivel:",
            linea_superior,
            formato_fila.format(*headers),
            linea_media
        ]
        
        objetos_acumulados = {
            "comun": 0,
            "poco_comun": 0,
            "raro": 0,
            "muy_raro": 0,
            "legendario": 0
        }
        
        for nivel in niveles_muestra:
            # Sumar los objetos del nivel actual
            for tipo, cantidad in self.tabla_distribucion[nivel].items():
                objetos_acumulados[tipo] += cantidad
            
            # Preparar la fila con los totales acumulados
            total = sum(objetos_acumulados.values())
            fila = [
                nivel,
                str(objetos_acumulados["comun"]),
                str(objetos_acumulados["poco_comun"]),
                str(objetos_acumulados["raro"]),
                str(objetos_acumulados["muy_raro"]),
                str(objetos_acumulados["legendario"]),
                str(total)
            ]
            tabla.append(formato_fila.format(*fila))
            if nivel != niveles_muestra[-1]:
                tabla.append(linea_media)
        
        tabla.append(linea_inferior)
        return "\n".join(tabla)

    def obtener_tabla_por_jugador(self):
        """
        Muestra una tabla con la distribución de objetos mágicos por jugador (grupo de 4)
        """
        # Caracteres para la tabla (igual que las otras funciones)
        esquina_sup_izq = '┌'
        esquina_sup_der = '┐'
        esquina_inf_izq = '└'
        esquina_inf_der = '┘'
        linea_horizontal = '─'
        linea_vertical = '│'
        union_izq = '├'
        union_der = '┤'
        union_sup = '┬'
        union_inf = '┴'
        cruz = '┼'
        
        # Anchos de columnas
        anchos = {
            'nivel': 10,
            'comun': 8,
            'poco_comun': 12,
            'raro': 8,
            'muy_raro': 10,
            'legendario': 10,
            'total': 8
        }
        
        # Crear líneas de la tabla
        linea_superior = esquina_sup_izq
        linea_media = union_izq
        linea_inferior = esquina_inf_izq
        
        for i, ancho in enumerate(anchos.values()):
            linea_superior += linea_horizontal * ancho + (esquina_sup_der if i == len(anchos)-1 else union_sup)
            linea_media += linea_horizontal * ancho + (union_der if i == len(anchos)-1 else cruz)
            linea_inferior += linea_horizontal * ancho + (esquina_inf_der if i == len(anchos)-1 else union_inf)
        
        # Formato para las filas
        formato_fila = linea_vertical
        for ancho in anchos.values():
            formato_fila += f"{{:^{ancho}}}{linea_vertical}"
        
        # Headers
        headers = ["Nivel", "Común", "Poco Común", "Raro", "Muy Raro", "Legendario", "Total"]
        niveles_muestra = ["1-4", "5-10", "11-16", "17-20"]
        
        # Construir la tabla
        tabla = [
            "\nDistribución de objetos mágicos por jugador (grupo de 4):",
            linea_superior,
            formato_fila.format(*headers),
            linea_media
        ]
        
        objetos_acumulados = {
            "comun": 0,
            "poco_comun": 0,
            "raro": 0,
            "muy_raro": 0,
            "legendario": 0
        }
        
        for nivel in niveles_muestra:
            # Sumar los objetos del nivel actual
            for tipo, cantidad in self.tabla_distribucion[nivel].items():
                objetos_acumulados[tipo] += cantidad
            
            # Dividir entre 4 y ajustar para mantener coherencia
            objetos_por_jugador = {
                "comun": ceil(objetos_acumulados["comun"] / 4),
                "poco_comun": ceil(objetos_acumulados["poco_comun"] / 4),
                "raro": ceil(objetos_acumulados["raro"] / 4),
                "muy_raro": ceil(objetos_acumulados["muy_raro"] / 4),
                "legendario": ceil(objetos_acumulados["legendario"] / 4)
            }
            
            # Preparar la fila con los totales por jugador
            total_jugador = sum(objetos_por_jugador.values())
            fila = [
                nivel,
                str(objetos_por_jugador["comun"]),
                str(objetos_por_jugador["poco_comun"]),
                str(objetos_por_jugador["raro"]),
                str(objetos_por_jugador["muy_raro"]),
                str(objetos_por_jugador["legendario"]),
                str(total_jugador)
            ]
            tabla.append(formato_fila.format(*fila))
            if nivel != niveles_muestra[-1]:
                tabla.append(linea_media)
        
        tabla.append(linea_inferior)
        return "\n".join(tabla)

    def obtener_tabla_por_jugador_cinco(self):
        """
        Muestra una tabla con la distribución de objetos mágicos por jugador (grupo de 5)
        """
        # Caracteres para la tabla (igual que las otras funciones)
        esquina_sup_izq = '┌'
        esquina_sup_der = '┐'
        esquina_inf_izq = '└'
        esquina_inf_der = '┘'
        linea_horizontal = '─'
        linea_vertical = '│'
        union_izq = '├'
        union_der = '┤'
        union_sup = '┬'
        union_inf = '┴'
        cruz = '┼'
        
        # Anchos de columnas
        anchos = {
            'nivel': 10,
            'comun': 8,
            'poco_comun': 12,
            'raro': 8,
            'muy_raro': 10,
            'legendario': 10,
            'total': 8
        }
        
        # Crear líneas de la tabla
        linea_superior = esquina_sup_izq
        linea_media = union_izq
        linea_inferior = esquina_inf_izq
        
        for i, ancho in enumerate(anchos.values()):
            linea_superior += linea_horizontal * ancho + (esquina_sup_der if i == len(anchos)-1 else union_sup)
            linea_media += linea_horizontal * ancho + (union_der if i == len(anchos)-1 else cruz)
            linea_inferior += linea_horizontal * ancho + (esquina_inf_der if i == len(anchos)-1 else union_inf)
        
        # Formato para las filas
        formato_fila = linea_vertical
        for ancho in anchos.values():
            formato_fila += f"{{:^{ancho}}}{linea_vertical}"
        
        # Headers
        headers = ["Nivel", "Común", "Poco Común", "Raro", "Muy Raro", "Legendario", "Total"]
        niveles_muestra = ["1-4", "5-10", "11-16", "17-20"]
        
        # Construir la tabla
        tabla = [
            "\nDistribución de objetos mágicos por jugador (grupo de 5):",
            linea_superior,
            formato_fila.format(*headers),
            linea_media
        ]
        
        objetos_acumulados = {
            "comun": 0,
            "poco_comun": 0,
            "raro": 0,
            "muy_raro": 0,
            "legendario": 0
        }
        
        for nivel in niveles_muestra:
            # Sumar los objetos del nivel actual
            for tipo, cantidad in self.tabla_distribucion[nivel].items():
                objetos_acumulados[tipo] += cantidad
            
            # Dividir entre 5 y ajustar para mantener coherencia
            objetos_por_jugador = {
                "comun": ceil(objetos_acumulados["comun"] / 5),
                "poco_comun": ceil(objetos_acumulados["poco_comun"] / 5),
                "raro": ceil(objetos_acumulados["raro"] / 5),
                "muy_raro": ceil(objetos_acumulados["muy_raro"] / 5),
                "legendario": ceil(objetos_acumulados["legendario"] / 5)
            }
            
            # Preparar la fila con los totales por jugador
            total_jugador = sum(objetos_por_jugador.values())
            fila = [
                nivel,
                str(objetos_por_jugador["comun"]),
                str(objetos_por_jugador["poco_comun"]),
                str(objetos_por_jugador["raro"]),
                str(objetos_por_jugador["muy_raro"]),
                str(objetos_por_jugador["legendario"]),
                str(total_jugador)
            ]
            tabla.append(formato_fila.format(*fila))
            if nivel != niveles_muestra[-1]:
                tabla.append(linea_media)
        
        tabla.append(linea_inferior)
        return "\n".join(tabla)

    def mostrar_distribucion_grupos(self):
        """
        Muestra las tablas de distribución para grupos de 4 y 5 jugadores una debajo de la otra
        """
        tabla_4 = self.obtener_tabla_por_jugador()
        tabla_5 = self.obtener_tabla_por_jugador_cinco()
        
        # Combinar las tablas con una línea en blanco entre ellas
        return tabla_4 + "\n\n" + tabla_5

# Ejemplo de uso
if __name__ == "__main__":
    distribucion = DistribucionObjetosMagicos()
    print(distribucion.obtener_tabla_por_personaje())
    print("\n")
    print(distribucion.obtener_tabla_totales_acumulados())
    print("\n")
    print(distribucion.mostrar_distribucion_grupos())
