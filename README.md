# VoiceMod Linux 🎙️

Uma aplicação de modificação de voz em tempo real para Linux, com interface gráfica intuitiva.

## Funcionalidades

- ✨ Modificação de voz em tempo real
- 🎵 Múltiplos efeitos de áudio (grave, agudo, robô, alien, eco, etc.)
- 🎚️ Controle de volume e pitch em tempo real
- 🔊 Seleção de dispositivos de entrada/saída
- 🎯 Interface gráfica moderna (PyQt6)
- 🐧 Compatível com Linux (Debian, Ubuntu, Fedora, CentOS)

## Instalação

### Ubuntu/Debian
```bash
sudo apt update
sudo apt install ./voicemod-linux_1.0.0_amd64.deb
```

### Fedora/CentOS/RHEL
```bash
sudo dnf install voicemod-linux-1.0.0-1.x86_64.rpm
```

## Uso

Após instalar, execute:
```bash
voicemod
```

Ou pelo menu de aplicações.

## Requisitos de Compilação

- Python 3.8+
- PyQt6
- numpy
- scipy
- sounddevice
- librosa

## Desenvolvimento

### Instalação das dependências
```bash
git clone https://github.com/darkLab-error618/voicemod-linux.git
cd voicemod-linux
pip install -r requirements.txt
```

### Executar a aplicação
```bash
python3 -m voicemod.main
```

### Compilar pacotes

#### Debian/Ubuntu (.deb)
```bash
cd packaging
./build_deb.sh
```

#### Fedora/CentOS (.rpm)
```bash
cd packaging
./build_rpm.sh
```

## Licença

MIT License

## Contribuições

Contributions são bem-vindas! Abra uma issue ou pull request.

## Autor

darkLab-error618
