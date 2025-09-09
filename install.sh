#!/bin/bash

echo "=== Dark Web Monitor - Script de Instalação ==="

# Instalar dependências Python
echo "Instalando dependências Python..."
pip install -r requirements.txt

# Verificar se o TOR está instalado
if ! command -v tor &> /dev/null; then
    echo "TOR não encontrado. Instalando..."

    # Ubuntu/Debian
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y tor

    # CentOS/RHEL
    elif command -v yum &> /dev/null; then
        sudo yum install -y tor

    # macOS
    elif command -v brew &> /dev/null; then
        brew install tor

    else
        echo "Sistema não suportado. Instale o TOR manualmente."
        exit 1
    fi
fi

# Configurar TOR
echo "Configurando TOR..."
sudo tee /etc/tor/torrc > /dev/null <<EOF
SocksPort 9050
ControlPort 9051
CookieAuthentication 1
EOF

# Iniciar TOR
echo "Iniciando TOR..."
sudo systemctl start tor
sudo systemctl enable tor

echo "Instalação concluída!"
echo "Execute: python app.py para iniciar a aplicação"
