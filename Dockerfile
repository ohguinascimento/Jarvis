# Use uma imagem base oficial do Python
FROM python:3.9-slim-buster

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Instala dependências do sistema necessárias para PyAudio e Pydub/FFmpeg
# - portaudio19-dev: necessário para a compilação do PyAudio
# - ffmpeg: necessário para o Pydub processar arquivos de áudio como .m4a
RUN apt-get update && apt-get install -y --no-install-recommends \
    portaudio19-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de requisitos primeiro para aproveitar o cache de camadas do Docker
COPY requirements.txt .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação para o diretório de trabalho
COPY . .

# Define o comando padrão para executar quando o contêiner iniciar
CMD ["python", "main.py"]