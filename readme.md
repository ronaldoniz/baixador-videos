# Video Downloader

Interface gráfica desktop desenvolvida em Python para download automatizado de vídeos a partir de links de diversas plataformas de redes sociais, incluindo YouTube, Facebook e TikTok.

## Funcionalidades

- **Download Multiplataforma:** Integração com o motor `yt-dlp` para extração de mídias do YouTube e Facebook, e fallback automatizado para API externa (TikWM) para contornar restrições de rede do TikTok.
- **Interface Gráfica Nativa:** Interface intuitiva construída com a biblioteca `tkinter`, projetada para operação simplificada sem necessidade de interação com o terminal.
- **Feedback de Progresso:** Monitoramento em tempo real da porcentagem de conclusão do download e estimativa de tempo restante (ETA) para plataformas compatíveis.
- **Conversão Automática:** Junção nativa de faixas de vídeo e áudio em alta definição em um arquivo consolidado no formato MP4.

## Arquitetura e Dependências

O projeto utiliza o interpretador Python 3 e baseia-se nas seguintes dependências principais:

- **yt-dlp:** Mecanismo de extração de vídeo e metadados.
- **Tkinter:** Interface gráfica de usuário (GUI).
- **FFmpeg (Estático):** Requisitado para a multiplexação (merge) de fluxos de vídeo e áudio separados de alta resolução em containers MP4.

## Configuração do Ambiente de Desenvolvimento

1. Certifique-se de que o Python está instalado e configurado corretamente nas variáveis de ambiente do sistema (`PATH`).
2. Instale as dependências necessárias via gerenciador de pacotes:
    ```bash
    pip install yt-dlp
    ```
3. Faça o download dos binários estáticos do **FFmpeg** (arquivos `ffmpeg.exe` e `ffprobe.exe`) e posicione-os na raiz do diretório do projeto.

Para executar a aplicação em modo de desenvolvimento, utilize o comando:

```bash
python downloader.py
```

## Distribuição e Empacotamento

Para gerar o executável autônomo para o usuário final, utiliza-se o `pyinstaller`.

1. Instale o empacotador:

```bash
pip install pyinstaller
```

2. Execute o comando de compilação:

```bash
pyinstaller --onefile --noconsole --name="Baixador_de_Videos" downloader.py
```

3. Após a compilação, mova o arquivo `Baixador_de_Videos.exe` gerado na pasta `dist` para o diretório final de distribuição.
4. Inclua obrigatoriamente os arquivos `ffmpeg.exe` e `ffprobe.exe` no mesmo diretório do executável final para garantir o funcionamento correto dos downloads multiplataforma.

## Estrutura de Diretórios para Distribuição

```text
📁 Diretorio_Final/
├── 📄 Baixador_de_Videos.exe
├── 📄 ffmpeg.exe
└── 📄 ffprobe.exe
```

Os arquivos baixados pelo aplicativo são direcionados automaticamente para a pasta padrão de Downloads do usuário do sistema operacional (`%USERPROFILE%\Downloads`).
