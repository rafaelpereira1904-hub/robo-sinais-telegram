import os
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests

# Configurações do Telegram
TOKEN = "6922393084:AAELCwWX_RXH5Ba6_VuUWGgQAQscJPkFVbk"
CHAT_ID = "-1002179849033"
URL = f"https://api.telegram.org/bot{TOKEN}"

# 1. Servidor web falso para o Railway manter o serviço ativo
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running 24/7!")

def run_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

# Iniciar o servidor web numa thread separada
threading.Thread(target=run_server, daemon=True).start()

# 2. Funções do Robô de Sinais
def enviar_mensagem(texto):
    url = f"{URL}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": texto,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")

def verificar_comandos():
    offset = 0
    while True:
        try:
            url = f"{URL}/getUpdates?offset={offset}&timeout=30"
            response = requests.get(url).json()
            
            if "result" in response:
                for update in response["result"]:
                    offset = update["update_id"] + 1
                    if "message" in update and "text" in update["message"]:
                        texto_msg = update["message"]["text"]
                        chat_id_origem = update["message"]["chat"]["id"]
                        
                        # Resposta ao comando /sinal
                        if texto_msg.startswith("/sinal"):
                            sinal_exemplo = (
                                "🚨 *SINAL MANUAL SOLICITADO* 🚨\n\n"
                                "📊 **Ativo:** EUR/USD (OTC)\n"
                                "⏰ **Horário:** Próxima Vela\n"
                                "📉 **Direção:** PUT (Venda)\n"
                                "⏳ **Expiração:** 1 Minuto"
                            )
                            requests.post(f"{URL}/sendMessage", json={
                                "chat_id": chat_id_origem,
                                "text": sinal_exemplo,
                                "parse_mode": "Markdown"
                            })
        except Exception as e:
            print(f"Erro no listener de comandos: {e}")
        
        time.sleep(2)

# Iniciar o ouvinte de comandos numa thread separada
threading.Thread(target=verificar_comandos, daemon=True).start()

print("Robô iniciado com sucesso na nuvem!")

# 3. Loop principal para envio automático de sinais programados
while True:
    # Exemplo de envio automático a cada X horas ou minutos
    sinal_automatico = (
        "💎 *SINAL AUTOMÁTICO - VIP* 💎\n\n"
        "📊 **Par:** GBP/USD\n"
        "⏰ **Horário:** 18:15\n"
        "📈 **Direção:** CALL (Compra)\n"
        "⏳ **Expiração:** 5 Minutos"
    )
    enviar_mensagem(sinal_automatico)
    
    # Aguarda 1 hora (3600 segundos) até ao próximo sinal automático
    time.sleep(3600)
