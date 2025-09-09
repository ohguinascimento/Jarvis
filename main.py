import platform
import subprocess
import speech_recognition as sr #importa a biblioteca
import pyttsx3
import datetime

listener = sr.Recognizer() #configurar reconhecimento
engine = pyttsx3.init()
voices = engine.getProperty('voices') #define a voz jarvis
engine.setProperty('voice', voices[0].id) #altera a voz do jarvis

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

def Repet_command():
    command = ""
    try:
        with sr.Microphone() as source: #inicia o microfone
            print('listen....') #imprime que esta escutando
            voice = listener.listen(source) #salva o que foi dito
            command = listener.recognize_google(voice, language='pt-BR') #fala o que foi dito
            command = command.lower() #deixa tudo em caixa alta
    except Exception as e:
        print(f"Ocorreu um erro ao repetir comando: {e}")
    return command

def run_jarvis():
    command = take_command()
    if 'jarvis' in command:  # ativa o jarvis
        #command = command.replace('jarvis', '')
        b = command.split("jarvis")
        command = (b[1])

        if 'que horas é' in command:
            talk("Parça agora é  " + str(datetime.datetime.now().strftime('%I:%M ')))
        elif 'está bem' in command:
            talk("Hoje esta suave na nave")
        elif 'ajusta os comandos' in command:
            talk("Esta ajustado vamo com tudo")
        elif 'testar conexão'  in command:
            talk("pra onde vamos pingar ?")
            msg = Repet_command()
            print(msg)
            resposta = ping(msg)

            if resposta == True:
                talk("Servidor online chefe")
            else:
                talk("Fudeou mano Caiu tudo")
        elif 'quem te fez' in command:
            talk("O homem de ferro")
        elif 'sextou' in command:
            talk("Dia de derrubar o servidor")
        elif 'o tiago é' in command:
            talk("Viadinho")
        elif 'eu sou o homem de ferro' in command:
            talk("não, o tony stark que é")
        elif 'a juliana é' in command:
            talk("minhaaaa vidaaaa")
        elif 'quem é você' in command:
            talk("Sou Jarvis o assistente do homem de ferro")
        else:
            print(command)
            talk("não econtrei nada com " + str(command))
    else:
        print(command)
        take_command()
while True:
    run_jarvis()