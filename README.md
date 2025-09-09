# Dark Web Monitor

Uma aplicação web em Python para monitorar a dark web em busca de palavras-chave específicas usando TOR.

## ⚠️ AVISO IMPORTANTE

Esta ferramenta é destinada APENAS para:
- Fins educacionais
- Monitoramento de segurança legítima
- Proteção de dados próprios

**NÃO use para atividades ilegais. Sempre respeite as leis locais.**

## Funcionalidades

- 🔍 Crawler simples para sites .onion
- 🔑 Gerenciamento de palavras-chave
- 🌐 Monitoramento de URLs específicas
- 📊 Dashboard com resultados
- 🔒 Integração com TOR
- 💾 Banco de dados SQLite

## Instalação

### 1. Pré-requisitos
- Python 3.7+
- TOR Browser ou TOR daemon

### 2. Instalação Automática (Linux/macOS)
```bash
chmod +x install.sh
./install.sh
```

### 3. Instalação Manual

#### Instalar dependências Python:
```bash
pip install -r requirements.txt
```

#### Instalar TOR:

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install tor
```

**CentOS/RHEL:**
```bash
sudo yum install tor
```

**macOS:**
```bash
brew install tor
```

#### Configurar TOR:
```bash
sudo cp torrc /etc/tor/torrc
sudo systemctl start tor
sudo systemctl enable tor
```

## Uso

### 1. Iniciar a aplicação:
```bash
python app.py
```

### 2. Acessar o dashboard:
Abra o navegador em: `http://localhost:5000`

### 3. Configurar monitoramento:
1. Adicione palavras-chave (ex: nome da empresa, domínios, emails)
2. Adicione URLs .onion para monitorar
3. Clique em "Iniciar Monitoramento"

## Estrutura do Projeto

```
dark-web-monitor/
├── app.py                 # Aplicação principal Flask
├── requirements.txt       # Dependências Python
├── install.sh            # Script de instalação
├── torrc                 # Configuração do TOR
├── templates/            # Templates HTML
│   ├── base.html
│   ├── index.html
│   ├── keywords.html
│   ├── urls.html
│   └── results.html
└── darkweb_monitor.db    # Banco de dados (criado automaticamente)
```

## Configuração Avançada

### Proxy TOR
Por padrão, a aplicação usa:
- SOCKS5 proxy: `127.0.0.1:9050`
- Control port: `9051`

### Parâmetros do Crawler
- Profundidade máxima: 2 níveis
- Links por página: 5
- Timeout: 30 segundos

## Segurança

- Use apenas para monitoramento legítimo
- Não armazene dados sensíveis
- Configure firewall adequadamente
- Use VPN adicional se necessário

## Troubleshooting

### TOR não conecta:
```bash
# Verificar status do TOR
sudo systemctl status tor

# Reiniciar TOR
sudo systemctl restart tor

# Verificar logs
sudo tail -f /var/log/tor/notices.log
```

### Erro de dependências:
```bash
# Atualizar pip
pip install --upgrade pip

# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
```

## Limitações

- Funciona apenas com sites .onion
- Crawler simples (não JavaScript)
- Sem autenticação avançada
- Limitado a texto simples

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## Licença

Este projeto é apenas para fins educacionais. Use por sua própria conta e risco.

## Disclaimer

Os desenvolvedores não se responsabilizam pelo uso indevido desta ferramenta. 
Sempre respeite as leis locais e use apenas para fins legítimos.
