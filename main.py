import platform
import subprocess
import speech_recognition as sr #importa a biblioteca
import sys
import pyttsx3
import datetime
import os
import imageio_ffmpeg

# --- Configuração do FFMPEG (DEVE SER FEITA ANTES DE IMPORTAR PYDUB) ---
# Adiciona o diretório do FFMPEG ao PATH do sistema para que pydub o encontre.
ffmpeg_dir = os.path.dirname(imageio_ffmpeg.get_ffmpeg_exe())
os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")

from pydub import AudioSegment
from pydub.playback import play

listener = sr.Recognizer() #configurar reconhecimento
engine = pyttsx3.init()
voices = engine.getProperty('voices') #define a voz jarvis
engine.setProperty('voice', voices[0].id) #altera a voz do jarvis

# --- Configuração de Caminhos ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(SCRIPT_DIR, 'audios')

def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]

    return subprocess.call(command) == 0

def talk(text):
    engine.say(text)
    engine.runAndWait()

def play_response(basename):
    """
    Encontra e toca um arquivo de áudio (m4a, mp3, etc.) da pasta 'audios'.
    """
    supported_extensions = ['.m4a', '.mp3', '.wav']
    audio_path = None
    for ext in supported_extensions:
        path = os.path.join(AUDIO_DIR, basename + ext)
        if os.path.exists(path):
            audio_path = path
            break

    if audio_path:
        try:
            sound = AudioSegment.from_file(audio_path)
            play(sound)
        except Exception as e:
            print(f"Erro ao tocar o áudio {audio_path}: {e}")
    else:
        print(f"Nenhum arquivo de áudio encontrado para: {basename}")
        talk("Desculpe, não encontrei o arquivo de áudio para essa resposta.")

def transcribe_audio_file(basename):
    """
    Encontra um arquivo de áudio na pasta 'audios', converte para WAV (se necessário)
    e transcreve seu conteúdo.
    """
    supported_extensions = ['.m4a', '.mp3', '.wav']
    audio_path = None
    for ext in supported_extensions:
        path = os.path.join(AUDIO_DIR, basename + ext)
        if os.path.exists(path):
            audio_path = path
            break

    if not audio_path:
        print(f"Arquivo de áudio '{basename}' não encontrado na pasta 'audios'.")
        talk(f"Arquivo {basename} não encontrado.")
        return

    # speech_recognition funciona melhor com WAV. Vamos converter se não for WAV.
    wav_path = os.path.join(SCRIPT_DIR, "temp_transcribe.wav")
    try:
        print(f"Processando {os.path.basename(audio_path)}...")
        sound = AudioSegment.from_file(audio_path)
        sound.export(wav_path, format="wav")
    except Exception as e:
        print(f"Erro ao converter o áudio para WAV: {e}")
        talk("Desculpe, tive um problema ao processar o arquivo de áudio.")
        if os.path.exists(wav_path):
            os.remove(wav_path)
        return

    # Agora, transcrever o arquivo WAV
    r = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio_data = r.record(source)
        try:
            text = r.recognize_google(audio_data, language='pt-BR')
            print(f"\n--- Texto Transcrito de '{basename}' ---\n{text}\n----------------------------------")
            talk("O texto do áudio é: " + text)
        except sr.UnknownValueError:
            print("Não consegui entender o conteúdo do áudio.")
            talk("Não consegui entender o conteúdo do áudio.")
        except sr.RequestError as e:
            print(f"Não foi possível conectar ao serviço de reconhecimento; {e}")
            talk("Estou com problemas para me conectar ao serviço de reconhecimento de voz.")
        finally:
            os.remove(wav_path) # Limpa o arquivo temporário

def take_command():
    command = ""
    try:
        with sr.Microphone() as source: #inicia o microfone
            print('listen....') #imprime que esta escutando
            voice = listener.listen(source) #salva o que foi dito
            command = listener.recognize_google(voice, language='pt-BR') #fala o que foi dito
            command = command.lower() #deixa tudo em caixa alta

    except sr.UnknownValueError:
        print("Não entendi o que foi dito.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    return command

def run_jarvis():
    command = take_command()

    if not command:
        # take_command já imprimiu o erro (ex: "Não entendi..."), então apenas retornamos.
        return

    if 'jarvis' in command:
        # Divide o comando na palavra "jarvis" e pega o que vem depois, limpando espaços
        b = command.split("jarvis", 1)
        command = b[1].strip() if len(b) > 1 else ""

        if not command:
            play_response("sim_mestre") # Toca um áudio de confirmação
        elif 'que horas são' in command or 'que horas é' in command:
            talk("Parça agora é  " + str(datetime.datetime.now().strftime('%I:%M ')))
        elif 'está bem' in command:
            play_response("bem")
        elif 'ajusta os comandos' in command:
            play_response("ajustado")
        elif 'testar conexão'  in command:
            play_response("ping_para_onde")
            msg = take_command() # Reutilizando a função principal de escuta
            print(msg)
            resposta = ping(msg)

            if resposta == True:
                play_response("servidor_online")
            else:
                play_response("servidor_offline")
        elif 'transcrever áudio' in command or 'transcreva o áudio' in command:
            talk("Qual o nome do arquivo de áudio que você quer transcrever?")
            audio_basename = take_command()
            if audio_basename:
                # Substitui espaços por _ para corresponder a nomes de arquivo como "sim_mestre"
                clean_basename = audio_basename.replace(" ", "_")
                transcribe_audio_file(clean_basename)
        elif 'quem te fez' in command:
            play_response("criador")
        elif 'sextou' in command:
            play_response("sextou")
        elif 'o tiago é' in command:
            play_response("tiago")
        elif 'eu sou o homem de ferro' in command:
            play_response("homem_de_ferro")
        elif 'a juliana é' in command:
            play_response("juliana")
        elif 'quem é você' in command:
            play_response("quem_e_voce")
        else:
            print(command)
            talk("não econtrei nada com " + str(command))
    else:
        # Se algo foi dito, mas não foi "jarvis"
        print(f"Comando ignorado: '{command}'. Diga 'Jarvis' para me ativar.")

if __name__ == "__main__":
    # Verifica se um nome de arquivo foi passado como argumento na linha de comando
    if len(sys.argv) > 1:
        # O primeiro argumento (sys.argv[0]) é o nome do script.
        # O segundo (sys.argv[1]) é o que queremos.
        audio_basename = sys.argv[1]
        print(f"Modo de transcrição: processando o arquivo '{audio_basename}'...")
        # Remove a extensão do arquivo, se houver, para a função que busca por várias
        if '.' in audio_basename:
            audio_basename = os.path.splitext(audio_basename)[0]
        transcribe_audio_file(audio_basename)
    else:
        # Se nenhum arquivo for fornecido, inicia o modo assistente interativo
        print("Nenhum arquivo de áudio fornecido. Iniciando o assistente Jarvis...")
        print("Diga 'Jarvis' seguido de um comando para interagir.")
        while True:
            run_jarvis()
            print("-" * 20) # Adiciona um separador visual para cada ciclo de escuta