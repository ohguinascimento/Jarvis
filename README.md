# Jarvis

Seja muito bem-vindo ao Jarvis, o assistente pessoal inspirado no Homem de Ferro.

Este projeto é um assistente de voz em Python capaz de entender comandos, responder a perguntas e executar tarefas, como também uma ferramenta de linha de comando para transcrever arquivos de áudio.

## ✨ Recursos

*   **Assistente de Voz Interativo**: Ativado pela palavra-chave "Jarvis".
*   **Comandos Dinâmicos**: Consulte as horas, teste a conectividade com servidores (ping) e muito mais.
*   **Respostas com Áudio Personalizado**: Utiliza arquivos de áudio pré-gravados da pasta `audios/` para dar mais personalidade ao assistente.
*   **Transcrição de Áudio**: Transcreve o conteúdo de arquivos de áudio para texto diretamente pela linha de comando.

## 📋 Requisitos

*   **Python 3.8+**
*   **Microfone** (para o modo de assistente de voz)
*   **Conexão com a Internet** (para o reconhecimento de voz do Google)
*   **Bibliotecas Python**: As dependências estão listadas no arquivo `requirements.txt`.

## 🚀 Instalação

Siga os passos abaixo para configurar o ambiente e executar o projeto.

1.  **Clone o repositório:**
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd Jarvis
    ```

2.  **(Recomendado) Crie e ative um ambiente virtual:**

    *   No Windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    *   No macOS/Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Instale as dependências:**
    Execute o comando abaixo para instalar todas as bibliotecas necessárias.
    ```bash
    pip install -r requirements.txt
    ```
    > **Nota**: A instalação da biblioteca `PyAudio` pode falhar em alguns sistemas. Se isso ocorrer, consulte guias de instalação específicos para seu sistema operacional (pode ser necessário instalar o "PortAudio" no Linux ou "Visual C++ Build Tools" no Windows).

## ⚙️ Como Usar

O script pode ser executado de duas maneiras:

### 1. Modo Assistente de Voz

Para iniciar o Jarvis e interagir por voz, execute o script sem argumentos:
```bash
python main.py
```
Aguarde a mensagem `listen....` e diga "Jarvis" seguido de um comando (ex: "Jarvis, que horas são?").

### 2. Modo de Transcrição de Áudio

Para transcrever um arquivo de áudio da pasta `audios/`, execute o script passando o nome do arquivo como argumento.
```bash
python main.py nome_do_arquivo
```
**Exemplo:**
```bash
python main.py sim_mestre.m4a
```
O programa irá processar o arquivo, imprimir o texto contido nele e finalizar a execução.