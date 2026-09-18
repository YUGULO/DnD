import tkinter as tk
from tkinter import ttk
from datetime import datetime
import pandas as pd
import os
from PIL import Image, ImageDraw, ImageFont, ImageGrab
import io
import win32clipboard
from io import BytesIO

#Calendario Harptos
class CalendarioHarptos:
    def __init__(self, root):
        self.root = root
        self.root.title("Calendario de Harptos - Costa de la Espada")
        
        # Definir colores para los grupos
        self.colores = {
            'principal': '#4CAF50',  # Verde
            'grupo1': '#ffd700',     # Amarillo
            'grupo2': '#ff4444',     # Rojo
            'grupo3': '#4444ff'      # Azul
        }
        
        # Configuración de meses y festividades
        self.meses_harptos = [
            "Hammer", "Alturiak", "Ches", "Tarsakh", "Mirtul", "Kythorn",
            "Flamerule", "Eleasis", "Eleint", "Marpenoth", "Uktar", "Nightal"
        ]
        
        self.festividades = {
            "Midwinter": (0, 30),
            "Greengrass": (3, 30),
            "Midsummer": (6, 30),
            "Highharvestide": (8, 30),
            "Feast of the Moon": (10, 30)
        }

        # Frame principal
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(expand=True, fill='both', padx=10, pady=10)

        # Frame izquierdo para los calendarios de grupo
        self.grupos_frame = ttk.Frame(self.main_frame)
        self.grupos_frame.pack(side='left', fill='both', expand=True)

        # Frame derecho para el calendario principal
        self.principal_frame = ttk.Frame(self.main_frame)
        self.principal_frame.pack(side='right', fill='both', expand=True)

        # Frame para botones
        self.botones_frame = ttk.Frame(self.principal_frame)
        self.botones_frame.pack(pady=5)

        # Crear calendarios
        self.crear_calendario_principal()
        self.crear_calendarios_grupo()

        # Botón de sincronización
        self.btn_sincronizar = ttk.Button(
            self.botones_frame, 
            text="Sincronizar", 
            command=self.sincronizar_calendarios
        )
        self.btn_sincronizar.pack(side='left', padx=5)

        # Botón de Discord
        self.btn_discord = ttk.Button(
            self.botones_frame,
            text="Discord",
            command=self.copiar_para_discord
        )
        self.btn_discord.pack(side='left', padx=5)

        # Botón de Imagen
        self.btn_imagen = ttk.Button(
            self.botones_frame,
            text="IMG",
            command=self.copiar_imagen
        )
        self.btn_imagen.pack(side='left', padx=5)

        # Cargar datos iniciales
        self.cargar_datos()

    def crear_calendario_principal(self):
        """Crear el calendario principal con tres meses"""
        frame = ttk.LabelFrame(self.principal_frame, text="Calendario Principal")
        frame.pack(fill='both', expand=True, padx=5, pady=5)

        # Selectores de fecha
        self.principal_selectors = self.crear_selectores_fecha(frame)
        
        # Frame para los tres calendarios
        calendarios_frame = ttk.Frame(frame)
        calendarios_frame.pack(fill='both', expand=True)
        
        # Crear los tres meses
        self.mes_anterior_frame = ttk.LabelFrame(calendarios_frame, text="Mes Anterior")
        self.mes_anterior_frame.pack(fill='both', expand=True, padx=5, pady=2)
        self.mes_anterior_dias = self.crear_grid_dias(self.mes_anterior_frame)
        
        self.mes_actual_frame = ttk.LabelFrame(calendarios_frame, text="Mes Actual")
        self.mes_actual_frame.pack(fill='both', expand=True, padx=5, pady=2)
        self.principal_dias = self.crear_grid_dias(self.mes_actual_frame)  # Este es el grid principal
        
        self.mes_siguiente_frame = ttk.LabelFrame(calendarios_frame, text="Mes Siguiente")
        self.mes_siguiente_frame.pack(fill='both', expand=True, padx=5, pady=2)
        self.mes_siguiente_dias = self.crear_grid_dias(self.mes_siguiente_frame)

    def crear_calendarios_grupo(self):
        """Crear los tres calendarios de grupo"""
        self.grupos_calendarios = []
        for i in range(3):
            frame = ttk.LabelFrame(self.grupos_frame, text=f"Grupo {i+1}")
            frame.pack(fill='both', expand=True, padx=5, pady=5)
            
            # Selectores de fecha
            selectors = self.crear_selectores_fecha(frame)
            
            # Grid de días
            dias = self.crear_grid_dias(frame)
            
            self.grupos_calendarios.append({
                'frame': frame,
                'selectors': selectors,
                'dias': dias
            })

    def crear_selectores_fecha(self, parent):
        """Crear los selectores de día, mes y año"""
        frame = ttk.Frame(parent)
        frame.pack(fill='x', padx=5, pady=5)

        # Día
        ttk.Label(frame, text="Día:").pack(side='left')
        btn_dia_menos = ttk.Button(frame, text="-", width=2, 
                                 command=lambda: self.ajustar_dia(-1, frame))
        btn_dia_menos.pack(side='left')
        dia = ttk.Combobox(frame, values=list(range(1, 31)), width=5)
        dia.set(1)
        dia.pack(side='left')
        btn_dia_mas = ttk.Button(frame, text="+", width=2,
                               command=lambda: self.ajustar_dia(1, frame))
        btn_dia_mas.pack(side='left', padx=(0,5))

        # Mes
        ttk.Label(frame, text="Mes:").pack(side='left')
        btn_mes_menos = ttk.Button(frame, text="-", width=2,
                                 command=lambda: self.ajustar_mes(-1, frame))
        btn_mes_menos.pack(side='left')
        mes = ttk.Combobox(frame, values=self.meses_harptos, width=10)
        mes.set(self.meses_harptos[0])
        mes.pack(side='left')
        btn_mes_mas = ttk.Button(frame, text="+", width=2,
                               command=lambda: self.ajustar_mes(1, frame))
        btn_mes_mas.pack(side='left', padx=(0,5))

        # Año
        ttk.Label(frame, text="Año:").pack(side='left')
        btn_año_menos = ttk.Button(frame, text="-", width=2,
                                command=lambda: self.ajustar_año(-1, frame))
        btn_año_menos.pack(side='left')
        año = ttk.Combobox(frame, values=list(range(1400, 2000)), width=7)
        año.set(1495)
        año.pack(side='left')
        btn_año_mas = ttk.Button(frame, text="+", width=2,
                              command=lambda: self.ajustar_año(1, frame))
        btn_año_mas.pack(side='left')

        # Agregar eventos para actualizar marcadores
        dia.bind('<<ComboboxSelected>>', lambda e: self.actualizar_al_cambiar())
        mes.bind('<<ComboboxSelected>>', lambda e: self.actualizar_al_cambiar())
        año.bind('<<ComboboxSelected>>', lambda e: self.actualizar_al_cambiar())

        return {'dia': dia, 'mes': mes, 'año': año}

    def obtener_selectores(self, frame):
        """Obtener los selectores correspondientes al frame"""
        # Obtener el LabelFrame que contiene los selectores
        parent_frame = frame.master
        
        # Verificar si es el calendario principal (incluyendo todos sus subframes)
        principal_label_frame = self.principal_frame.winfo_children()[1]  # El LabelFrame principal
        if (parent_frame == principal_label_frame or 
            parent_frame in principal_label_frame.winfo_children() or
            parent_frame in [self.mes_anterior_frame, self.mes_actual_frame, self.mes_siguiente_frame]):
            return self.principal_selectors
        
        # Verificar si es alguno de los grupos
        for grupo in self.grupos_calendarios:
            if parent_frame == grupo['frame']:
                return grupo['selectors']
        
        # Si no se encontró, imprimir información de depuración
        print(f"No se encontraron selectores para el frame: {frame}")
        print(f"Parent frame: {parent_frame}")
        print(f"Principal label frame: {principal_label_frame}")
        print(f"Principal label frame children: {principal_label_frame.winfo_children()}")
        print(f"Grupo frames: {[grupo['frame'] for grupo in self.grupos_calendarios]}")
        return None

    def ajustar_dia(self, incremento, frame):
        """Ajustar el día con los botones + y -"""
        selectors = self.obtener_selectores(frame)
        if selectors:
            try:
                dia_actual = int(selectors['dia'].get())
                nuevo_dia = dia_actual + incremento
                if 1 <= nuevo_dia <= 30:
                    selectors['dia'].set(str(nuevo_dia))  # Convertir a string
                    self.actualizar_al_cambiar()
            except Exception as e:
                print(f"Error al ajustar día: {e}")

    def ajustar_mes(self, incremento, frame):
        """Ajustar el mes con los botones + y -"""
        selectors = self.obtener_selectores(frame)
        if selectors:
            try:
                mes_actual_idx = self.meses_harptos.index(selectors['mes'].get())
                nuevo_idx = (mes_actual_idx + incremento) % 12
                selectors['mes'].set(self.meses_harptos[nuevo_idx])
                self.actualizar_al_cambiar()
            except Exception as e:
                print(f"Error al ajustar mes: {e}")

    def ajustar_año(self, incremento, frame):
        """Ajustar el año con los botones + y -"""
        selectors = self.obtener_selectores(frame)
        if selectors:
            try:
                año_actual = int(selectors['año'].get())
                nuevo_año = año_actual + incremento
                if 1400 <= nuevo_año <= 1999:
                    selectors['año'].set(str(nuevo_año))  # Convertir a string
                    self.actualizar_al_cambiar()
            except Exception as e:
                print(f"Error al ajustar año: {e}")

    def actualizar_al_cambiar(self):
        """Actualizar marcadores y guardar cuando cambian los selectores"""
        self.actualizar_marcadores()
        self.actualizar_meses_adyacentes()
        self.guardar_datos()

    def crear_grid_dias(self, parent):
        """Crear el grid de días del calendario"""
        frame = ttk.Frame(parent)
        frame.pack(fill='both', expand=True, padx=5, pady=5)

        # Cabecera de días
        for i in range(10):
            ttk.Label(frame, text=f"{i+1}º").grid(row=0, column=i, padx=2, pady=2)

        # Grid de días
        dias = []
        for i in range(3):
            fila = []
            for j in range(10):
                dia_num = i*10 + j + 1
                dia = tk.Label(frame, text=f"{dia_num}", relief="solid", width=4,
                             bg='white', bd=1)  # Cambiado a tk.Label para poder cambiar colores
                dia.grid(row=i+1, column=j, padx=2, pady=2)
                dia.bind('<Button-1>', lambda e, d=dia_num, f=frame: self.dia_clickado(d, f))
                fila.append(dia)
            dias.append(fila)

        return dias

    def dia_clickado(self, dia, frame):
        """Manejar el clic en un día del calendario"""
        # Inicializar selectors como None
        selectors = None
        
        # Obtener el LabelFrame (calendario) que contiene el frame de días
        calendario_frame = frame.master

        # Identificar a qué calendario pertenece el día clickado
        if calendario_frame in [self.mes_anterior_frame, self.mes_actual_frame, self.mes_siguiente_frame]:
            selectors = self.principal_selectors
            
            # Si es mes anterior o siguiente, ajustar el mes antes de establecer el día
            if calendario_frame == self.mes_anterior_frame:
                mes_actual_idx = self.meses_harptos.index(self.principal_selectors['mes'].get())
                año_actual = int(self.principal_selectors['año'].get())
                
                if mes_actual_idx == 0:  # Si es Hammer
                    nuevo_mes = self.meses_harptos[11]  # Nightal
                    selectors['año'].set(año_actual - 1)
                else:
                    nuevo_mes = self.meses_harptos[mes_actual_idx - 1]
                
                selectors['mes'].set(nuevo_mes)
                
            elif calendario_frame == self.mes_siguiente_frame:
                mes_actual_idx = self.meses_harptos.index(self.principal_selectors['mes'].get())
                año_actual = int(self.principal_selectors['año'].get())
                
                if mes_actual_idx == 11:  # Si es Nightal
                    nuevo_mes = self.meses_harptos[0]  # Hammer
                    selectors['año'].set(año_actual + 1)
                else:
                    nuevo_mes = self.meses_harptos[mes_actual_idx + 1]
                
                selectors['mes'].set(nuevo_mes)
            
            print("Click en calendario principal")
        else:
            # Buscar en los calendarios de grupo
            for i, grupo in enumerate(self.grupos_calendarios):
                if calendario_frame == grupo['frame']:
                    selectors = grupo['selectors']
                    print(f"Click en calendario grupo {i+1}")
                    break

        # Verificar que se encontró un selector válido
        if selectors is not None:
            selectors['dia'].set(dia)
            self.actualizar_marcadores()
            self.actualizar_meses_adyacentes()
            self.guardar_datos()
        else:
            print(f"Error: No se pudo identificar el calendario clickado.")
            print(f"Frame clickado: {calendario_frame}")
            print(f"Frames principales: {[self.mes_anterior_frame, self.mes_actual_frame, self.mes_siguiente_frame]}")
            print(f"Frames grupos: {[grupo['frame'] for grupo in self.grupos_calendarios]}")

    def actualizar_marcadores(self):
        """Actualizar los marcadores visuales en todos los calendarios"""
        try:
            # Resetear todos los días a blanco/gris según corresponda
            self.resetear_colores()

            # Obtener información del calendario principal
            dia_principal = int(self.principal_selectors['dia'].get())
            mes_principal = self.principal_selectors['mes'].get()
            año_principal = int(self.principal_selectors['año'].get())
            
            # Obtener índices y años de los tres meses
            mes_actual_idx = self.meses_harptos.index(mes_principal)
            mes_anterior_idx = (mes_actual_idx - 1) % 12
            mes_siguiente_idx = (mes_actual_idx + 1) % 12
            
            año_anterior = año_principal - 1 if mes_actual_idx == 0 else año_principal
            año_siguiente = año_principal + 1 if mes_actual_idx == 11 else año_principal

            # Marcar día principal siempre en el mes actual
            self.colorear_dia(self.principal_dias, dia_principal, self.colores['principal'])

            # Marcar días de los grupos en los tres meses
            for i, grupo in enumerate(self.grupos_calendarios):
                dia_grupo = int(grupo['selectors']['dia'].get())
                mes_grupo = grupo['selectors']['mes'].get()
                año_grupo = int(grupo['selectors']['año'].get())
                mes_grupo_idx = self.meses_harptos.index(mes_grupo)
                
                # Colorear el día en el calendario del grupo
                self.colorear_dia(grupo['dias'], dia_grupo, self.colores[f'grupo{i+1}'])
                
                # Marcar en el mes que corresponda
                if mes_grupo_idx == mes_anterior_idx and año_grupo == año_anterior:
                    self.colorear_dia(self.mes_anterior_dias, dia_grupo, self.colores[f'grupo{i+1}'])
                elif mes_grupo_idx == mes_actual_idx and año_grupo == año_principal:
                    self.colorear_dia(self.principal_dias, dia_grupo, self.colores[f'grupo{i+1}'])
                elif mes_grupo_idx == mes_siguiente_idx and año_grupo == año_siguiente:
                    self.colorear_dia(self.mes_siguiente_dias, dia_grupo, self.colores[f'grupo{i+1}'])

        except Exception as e:
            print(f"Error al actualizar marcadores: {e}")

    def resetear_colores(self):
        """Resetear todos los días a sus colores base"""
        # Resetear mes anterior a gris
        for fila in self.mes_anterior_dias:
            for dia in fila:
                dia.configure(bg='lightgray')

        # Resetear mes actual a blanco
        for fila in self.principal_dias:
            for dia in fila:
                dia.configure(bg='white')

        # Resetear mes siguiente a gris
        for fila in self.mes_siguiente_dias:
            for dia in fila:
                dia.configure(bg='lightgray')

        # Resetear calendarios de grupo a blanco
        for grupo in self.grupos_calendarios:
            for fila in grupo['dias']:
                for dia in fila:
                    dia.configure(bg='white')

    def colorear_dia(self, grid_dias, numero_dia, color):
        """Colorear un día específico en un grid de días"""
        fila = (numero_dia - 1) // 10
        columna = (numero_dia - 1) % 10
        if 0 <= fila < len(grid_dias) and 0 <= columna < len(grid_dias[0]):
            grid_dias[fila][columna].configure(bg=color)

    def sincronizar_calendarios(self):
        """Sincronizar todos los calendarios con el principal"""
        dia = self.principal_selectors['dia'].get()
        mes = self.principal_selectors['mes'].get()
        año = self.principal_selectors['año'].get()

        for grupo in self.grupos_calendarios:
            grupo['selectors']['dia'].set(dia)
            grupo['selectors']['mes'].set(mes)
            grupo['selectors']['año'].set(año)

        # Actualizar marcadores visuales después de sincronizar
        self.actualizar_marcadores()
        self.guardar_datos()

    def cargar_datos(self):
        """Cargar datos del CSV y actualizar según días transcurridos"""
        csv_path = 'data/DnD5_Calendario_Control.csv'
        if os.path.exists(csv_path):
            try:
                df = pd.read_csv(csv_path)
                ultima_fila = df.iloc[-1]
                
                # Obtener y comparar fechas
                fecha_guardada = datetime.strptime(ultima_fila['fecha_real'], '%Y-%m-%d %H:%M:%S')
                fecha_actual = datetime.now()
                dias_transcurridos = (fecha_actual - fecha_guardada).days
                
                print(f"Fecha guardada: {fecha_guardada}")
                print(f"Fecha actual: {fecha_actual}")
                print(f"Días transcurridos: {dias_transcurridos}")

                # Cargar fecha del calendario principal
                fecha_principal = ultima_fila['fecha_harptos_principal'].split('-')
                año = int(fecha_principal[0])
                mes = int(fecha_principal[1])
                dia = int(fecha_principal[2])

                # Si han pasado días, actualizar la fecha del calendario principal
                if dias_transcurridos > 0:
                    # Avanzar los días
                    dia += dias_transcurridos
                    
                    # Ajustar si el día supera 30
                    while dia > 30:
                        dia -= 30
                        mes += 1
                        if mes > 12:
                            mes = 1
                            año += 1
                    
                    print(f"Nueva fecha Harptos: {año}-{mes}-{dia}")
                    
                    # Guardar la nueva fecha
                    self.guardar_datos()

                # Actualizar calendario principal
                self.principal_selectors['año'].set(año)
                self.principal_selectors['mes'].set(self.meses_harptos[mes-1])
                self.principal_selectors['dia'].set(dia)

                # Actualizar calendarios de grupo
                for i, grupo in enumerate(self.grupos_calendarios):
                    fecha_grupo = ultima_fila[f'fecha_harptos_grupo{i+1}'].split('-')
                    grupo['selectors']['año'].set(fecha_grupo[0])
                    grupo['selectors']['mes'].set(self.meses_harptos[int(fecha_grupo[1])-1])
                    grupo['selectors']['dia'].set(int(fecha_grupo[2]))

                # Actualizar marcadores visuales
                self.actualizar_marcadores()
                self.actualizar_meses_adyacentes()

            except Exception as e:
                print(f"Error al cargar datos: {e}")

    def guardar_datos(self):
        """Guardar datos en el CSV"""
        fecha_real = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Obtener fecha del calendario principal
        mes_principal = str(self.meses_harptos.index(self.principal_selectors['mes'].get()) + 1).zfill(2)
        fecha_principal = f"{self.principal_selectors['año'].get()}-{mes_principal}-{self.principal_selectors['dia'].get().zfill(2)}"
        
        # Obtener fechas de los grupos
        fechas_grupos = []
        for grupo in self.grupos_calendarios:
            mes = str(self.meses_harptos.index(grupo['selectors']['mes'].get()) + 1).zfill(2)
            fecha = f"{grupo['selectors']['año'].get()}-{mes}-{grupo['selectors']['dia'].get().zfill(2)}"
            fechas_grupos.append(fecha)

        # Crear DataFrame y guardar
        df = pd.DataFrame({
            'fecha_real': [fecha_real],
            'fecha_harptos_principal': [fecha_principal],
            'fecha_harptos_grupo1': [fechas_grupos[0]],
            'fecha_harptos_grupo2': [fechas_grupos[1]],
            'fecha_harptos_grupo3': [fechas_grupos[2]]
        })

        # Asegurar que existe el directorio data
        os.makedirs('data', exist_ok=True)
        
        # Guardar en CSV
        df.to_csv('data/DnD5_Calendario_Control.csv', index=False)

    def copiar_para_discord(self):
        """Copiar imagen y fechas formateadas para Discord"""
        try:
            # Crear y copiar imagen
            self.copiar_imagen()
            
            # Preparar el texto
            texto = "\n\n"  # Espacio después de la imagen
            texto += "```\n"
            texto += "CALENDARIO DE HARPTOS - COSTA DE LA ESPADA\n"
            texto += "=" * 45 + "\n\n"
            
            # Fecha real
            fecha_real = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            texto += f"Fecha Real: {fecha_real}\n"
            texto += "-" * 45 + "\n\n"
            
            # Calendario Principal (Verde)
            texto += "CALENDARIO PRINCIPAL (VERDE)\n"
            texto += f"Día: {self.principal_selectors['dia'].get()}\n"
            texto += f"Mes: {self.principal_selectors['mes'].get()}\n"
            texto += f"Año: {self.principal_selectors['año'].get()}\n"
            texto += "-" * 30 + "\n\n"
            
            # Colores de los grupos
            colores = ['AMARILLO', 'ROJO', 'AZUL']
            
            # Calendarios de Grupo
            for i, grupo in enumerate(self.grupos_calendarios, 1):
                texto += f"GRUPO {i} ({colores[i-1]})\n"
                texto += f"Día: {grupo['selectors']['dia'].get()}\n"
                texto += f"Mes: {grupo['selectors']['mes'].get()}\n"
                texto += f"Año: {grupo['selectors']['año'].get()}\n"
                if i < len(self.grupos_calendarios):
                    texto += "-" * 20 + "\n\n"
            
            texto += "```"
            
            # Copiar texto al portapapeles
            self.root.clipboard_append(texto)
            
            # Feedback visual
            self.mostrar_mensaje_copiado()
            
        except Exception as e:
            print(f"Error al copiar al portapapeles: {e}")
            ventana = tk.Toplevel(self.root)
            ventana.title("Error")
            ttk.Label(ventana, text=f"Error al copiar: {str(e)}").pack(pady=10)
            ventana.after(3000, ventana.destroy)

    def crear_imagen_calendario(self):
        """Crear una imagen del calendario capturando la pantalla"""
        try:
            # Asegurar que la ventana está al frente
            self.root.lift()
            self.root.update()
            
            # Pequeña pausa para asegurar que la ventana está actualizada
            self.root.after(100)
            
            # Obtener las coordenadas del frame de calendarios
            calendarios_frame = self.principal_frame.winfo_children()[1]  # LabelFrame del calendario principal
            x = calendarios_frame.winfo_rootx()
            y = calendarios_frame.winfo_rooty()
            width = calendarios_frame.winfo_width()
            height = calendarios_frame.winfo_height()
            
            # Capturar la pantalla
            screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
            
            return screenshot
            
        except Exception as e:
            print(f"Error al crear imagen: {e}")
            return None

    def mostrar_mensaje_copiado(self):
        """Mostrar una pequeña ventana de confirmación"""
        ventana = tk.Toplevel(self.root)
        ventana.title("")
        
        # Centrar en la pantalla
        x = self.root.winfo_x() + self.root.winfo_width()//2 - 100
        y = self.root.winfo_y() + self.root.winfo_height()//2 - 25
        ventana.geometry(f"200x50+{x}+{y}")
        
        # Mensaje
        ttk.Label(ventana, text="¡Copiado al portapapeles!").pack(pady=10)
        
        # Cerrar automáticamente después de 1 segundo
        ventana.after(1000, ventana.destroy)

    def actualizar_meses_adyacentes(self):
        """Actualizar los meses anterior y siguiente"""
        # Obtener mes y año actuales
        mes_actual_idx = self.meses_harptos.index(self.principal_selectors['mes'].get())
        año_actual = int(self.principal_selectors['año'].get())

        # Calcular mes anterior
        if mes_actual_idx == 0:  # Si es Hammer
            mes_anterior_idx = 11  # Nightal
            año_anterior = año_actual - 1
        else:
            mes_anterior_idx = mes_actual_idx - 1
            año_anterior = año_actual

        # Calcular mes siguiente
        if mes_actual_idx == 11:  # Si es Nightal
            mes_siguiente_idx = 0  # Hammer
            año_siguiente = año_actual + 1
        else:
            mes_siguiente_idx = mes_actual_idx + 1
            año_siguiente = año_actual

        # Actualizar títulos de los frames
        self.mes_anterior_frame.configure(text=f"{self.meses_harptos[mes_anterior_idx]} {año_anterior}")
        self.mes_actual_frame.configure(text=f"{self.meses_harptos[mes_actual_idx]} {año_actual}")
        self.mes_siguiente_frame.configure(text=f"{self.meses_harptos[mes_siguiente_idx]} {año_siguiente}")

        # Establecer color de fondo gris pero mantener los marcadores
        self.colorear_fondo_mes(self.mes_anterior_dias, 'lightgray')
        self.colorear_fondo_mes(self.mes_siguiente_dias, 'lightgray')

    def colorear_fondo_mes(self, grid_dias, color):
        """Colorear el fondo de un mes sin afectar los marcadores"""
        for fila in grid_dias:
            for dia in fila:
                if dia.cget('bg') == 'white':  # Solo cambiar si no está marcado
                    dia.configure(bg=color)

    def copiar_imagen(self):
        """Copiar solo la imagen al portapapeles"""
        try:
            # Crear imagen del calendario
            img = self.crear_imagen_calendario()
            
            # Convertir imagen a bytes en formato PNG
            output = BytesIO()
            img.save(output, 'BMP')  # Cambiar a BMP para mejor compatibilidad
            data = output.getvalue()[14:]  # Eliminar cabecera BMP
            output.close()

            # Copiar imagen al portapapeles
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
            win32clipboard.CloseClipboard()
            
            # Feedback visual
            self.mostrar_mensaje_copiado()
            
        except Exception as e:
            print(f"Error al copiar imagen: {e}")
            # Mostrar mensaje de error
            ventana = tk.Toplevel(self.root)
            ventana.title("Error")
            ttk.Label(ventana, text=f"Error al copiar imagen: {str(e)}").pack(pady=10)
            ventana.after(3000, ventana.destroy)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarioHarptos(root)
    root.mainloop()
