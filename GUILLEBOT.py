import discord
import random
import string
import asyncio
from discord import FFmpegPCMAudio
import subprocess

intents = discord.Intents.all()
intents.voice_states = True
client = discord.Client(intents=intents)

polls = {}

output_path = "."

# Configura el prefijo de los comandos
PREFIX = '$'

# Diccionario para almacenar las conexiones de voz por servidor
voice_clients = {}

help_message = (
    "**¡Saludos! Aquí tienes una lista de comandos que puedo ejecutar para ayudarte:**\n\n"
    "```markdown\n"
    "**$buscar <palabra>**\n"
    "   - Pon a prueba a GUILLE para encontrar una palabra específica.\n\n"
    "**$frase**\n"
    "   - Proporciono sabias palabras para reflexionar.\n\n"
    "**$join**\n"
    "   - Me uno al canal de voz en el que te encuentras.\n\n"
    "**$leave**\n"
    "   - Abandono el canal de voz en el que me encuentro.\n\n"
    "**$play <URL>**\n"
    "   - Reproduzco audio desde el enlace de YouTube proporcionado.\n\n"
    "**$create_poll <pregunta> <opción1> <opción2> ... <opciónN>**\n"
    "   - Creo una encuesta con la pregunta y las opciones proporcionadas.\n"
    "```"
)

frases = [
    "No mas novias hasta 2027",
    "Si pesa mas que un pollo no hay excusa",
    "El que no rape no fuma del vape",
    "Si juega al Valorant no es la buena",
    "Merienda de señores un buen pan con mayo",
    "Si es peliroja es la buena pero esta loca",
    "Si es argentina siempre sera mejor",
    "Siempre apuntando a la meca",
    "Coño con pelito no hay delito",
    "Me cago en toda tu puta madre puto hijo de puta, hasta un bot sabe que estarías mejor muerto que estorbando",
]

# Función para verificar si el usuario que ejecutó el comando está en un canal de voz
def check_author(ctx):
    return ctx.author.voice and ctx.author.voice.channel

# Comando para unir al bot al canal de voz del usuario que lo invocó
async def join(voice_channel):
    if not voice_channel:
        await ctx.send("Debes estar en un canal de voz para usar este comando.")
        return

    guild = voice_channel.guild
    if guild.id not in voice_clients:
        voice_clients[guild.id] = await voice_channel.connect()
    else:
        await voice_clients[guild.id].move_to(voice_channel)
        
# Comando para salir del canal de voz
async def leave(ctx):
    if ctx.guild.id in voice_clients:
        await voice_clients[ctx.guild.id].disconnect()
        del voice_clients[ctx.guild.id]

# Comando para reproducir un archivo de audio local
async def play(ctx, file_path):
    if ctx.guild.id in voice_clients:
        if not voice_clients[ctx.guild.id].is_playing():
            voice_clients[ctx.guild.id].play(FFmpegPCMAudio(file_path, executable=r'C:\Users\daniel\Downloads\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe'))
        else:
            await ctx.send("Ya se está reproduciendo un audio.")
    else:
        await ctx.send("El bot no está en un canal de voz.")

def obtener_frase_aleatorio():
    return random.choice(frases)

def generar_frase_aleatoria(tamaño):
    letras = string.ascii_lowercase + " "
    return ''.join(random.choice(letras) for _ in range(tamaño))

async def animacion_puntos(message):
    while True:
        for _ in range(4):
            await message.edit(content="Buscando" + "." * _)
            await asyncio.sleep(0.3)
        await message.edit(content="Buscando")
        await asyncio.sleep(0.3)

async def intentar_frase_deseada(message, frase_deseada):
    intentos = 0
    while True:
        intentos += 1
        frase_generada = generar_frase_aleatoria(len(frase_deseada))
        if frase_generada == frase_deseada:
            await message.edit(content=f"¡Frase encontrada!\nSe necesitaron {intentos} intentos.")
            break

# Define un evento para cuando el bot esté listo
@client.event
async def on_ready():
    print(f'{client.user.name} está listo para funcionar!')

# Define un evento para manejar los mensajes
@client.event
async def on_message(message):
    # Verifica si el mensaje es el comando $hola y si proviene de un servidor
    if message.content == PREFIX + 'help' and message.guild:
        await message.channel.send(help_message)

    frase = obtener_frase_aleatorio()

    if message.content == PREFIX + 'frase' and message.guild:
        await message.channel.send(frase)

    #busca una frase aleatoria que escriba el usuario
    if message.content.startswith(PREFIX + 'buscar'):
        frase_deseada = message.content[8:].lower().strip()
        if not frase_deseada:
            await message.channel.send("Por favor, ingrese una frase.")
            return
        palabras = frase_deseada.split()
        for palabra in palabras:
            if len(palabra) > 5:
                await message.channel.send(f"La palabra '{palabra}' excede la longitud máxima permitida de 5 caracteres.")
                return
        mensaje_busqueda = await message.channel.send("Buscando")
        await intentar_frase_deseada(mensaje_busqueda, frase_deseada)

    if message.content == PREFIX + 'join' and message.guild:
        await join(message.author.voice.channel)
    if message.content == PREFIX + 'leave' and message.guild:
        await leave(message)
    if message.content == PREFIX + 'play' and message.guild: 
        await join(message.author.voice.channel)
        subprocess.run(["python", "GUILLEBORRADOR.py"])
        # Divide el mensaje en palabras
        words = message.content.split()
        # Encuentra la posición de "$help" en la lista de palabras
        index = words.index('$play')
        # Verifica si hay al menos una palabra después de "$play"
        if index + 1 < len(words):
            # Guarda la siguiente palabra después de "$play" en una variable
            YTurl = words[index + 1]

        # Ejecutar el script.py con los argumentos
        subprocess.run(["python", "GUILLEMUSICAL.py", YTurl, output_path])
        await play(message, r'C:\Users\daniel\Desktop\GUILLE\GUILLEBOT\audio.mp4')

    if message.content.startswith(PREFIX + 'create_poll'):
        content = message.content.split(' ')
        question = ' '.join(content[1:])
        options = content[2:]
        formatted_options = "\n".join([f"{index + 1}. {option}" for index, option in enumerate(options)])
        poll_message = f"{question}\n\n{formatted_options}"
        poll = await message.channel.send(poll_message)
        for index in range(len(options)):
            await poll.add_reaction(chr(127462 + index))  # Añade una reacción de emoji para cada opción
        polls[poll.id] = {'question': question, 'options': options, 'votes': [0]*len(options)}

@client.event
async def on_raw_reaction_add(payload):
    if payload.message_id in polls:
        index = chr(payload.emoji.codepoint) - 127462
        polls[payload.message_id]['votes'][index] += 1

@client.event
async def on_raw_reaction_remove(payload):
    if payload.message_id in polls:
        index = chr(payload.emoji.codepoint) - 127462
        polls[payload.message_id]['votes'][index] -= 1

# Ejecuta el bot con el token
client.run('')
