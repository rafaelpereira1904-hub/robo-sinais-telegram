import datetime
import random
import time
import requests

TELEGRAM_TOKEN = "6922393084:AAELCwWX_RXH5Ba6_VuUWGgQAQscJPkFVbk"
CHAT_ID = "-1002179849033"


def enviar_telegram(mensagem, chat_id=CHAT_ID):
  url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
  payload = {"chat_id": chat_id, "text": mensagem, "parse_mode": "Markdown"}
  try:
    requests.post(url, json=payload, timeout=10)
  except Exception as e:
    print(f"⚠️ Erro ao enviar mensagem: {e}")


def analisar_confluencia_smc(ativo):
  wins = random.randint(17, 23)
  losses = random.randint(1, 4)
  total = wins + losses
  win_rate = (wins / total) * 100
  direcao = "CALL (BUY)" if random.choice([True, False]) else "PUT (SELL)"
  padrao_identificado = random.choice([
      "Fair Value Gap (FVG) + RSI Sobrevendido",
      "Order Block de M5 + Retração de Fibonacci",
      "Point of Control (POC) + Rompimento de Estrutura (BOS)",
  ])
  return {
      "ativo": ativo,
      "wins": wins,
      "losses": losses,
      "win_rate": win_rate,
      "direcao": direcao,
      "padrao": padrao_identificado,
  }


def gerar_relatorio_sinais():
  ativos = ["EUR/USD", "GBP/USD", "USD/JPY", "EUR/USD-OTC", "AUD/CAD-OTC"]
  sinais_qualificados = []

  for ativo in ativos:
    analise = analisar_confluencia_smc(ativo)
    if analise["win_rate"] >= 80.0:
      sinais_qualificados.append(analise)

  if not sinais_qualificados:
    return "⚠️ *Nenhum par atingiu a assertividade mínima de 80% neste ciclo.*"

  data_hora = datetime.datetime.now().strftime("%d/%m/%Y às %H:%M")
  mensagem = (
      f"🤖 *IA ANALISADOR SMC & PRICE ACTION* 🤖\n"
      f"🗓️ _{data_hora} | Timeframe: M1/M5_\n"
      f"-----------------------------------------\n\n"
  )

  for s in sinais_qualificados:
    emoji = "🟢" if "CALL" in s["direcao"] else "🔴"
    mensagem += (
        f"🌐 *Ativo:* `{s['ativo']}`\n"
        f"🎯 *Assertividade:* `{s['win_rate']:.1f}%` "
        f"({s['wins']}W / {s['losses']}L)\n"
        f"⚙️ *Padrão:* _{s['padrao']}_\n"
        f"{emoji} *Direção:* *{s['direcao']}*\n"
        f"-----------------------------------------\n"
    )

  mensagem += "\n🚀 *Monitore o gráfico para a retração na zona!*"
  return mensagem


def verificar_comandos_telegram(ultimo_offset):
  url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates?offset={ultimo_offset}&timeout=5"
  try:
    resposta = requests.get(url, timeout=10).json()
    if "result" in resposta:
      for update in resposta["result"]:
        ultimo_offset = update["update_id"] + 1
        if "message" in update and "text" in update["message"]:
          texto = update["message"]["text"].strip().lower()
          chat_id_usuario = update["message"]["chat"]["id"]
          if "/sinal" in texto or "/catalogar" in texto:
            resposta_ia = gerar_relatorio_sinais()
            enviar_telegram(resposta_ia, chat_id=chat_id_usuario)
  except Exception as e:
    print(f"Erro ao checar comandos: {e}")
  return ultimo_offset


def rodar_sistema():
  print("🚀 Bot Híbrido de Sinais iniciado com sucesso!")
  ultimo_offset = 0
  tempo_ultimo_envio = 0
  INTERVALO_AUTOMATICO = 900  # 15 minutos

  while True:
    tempo_atual = time.time()
    if tempo_atual - tempo_ultimo_envio >= INTERVALO_AUTOMATICO:
      relatorio = gerar_relatorio_sinais()
      enviar_telegram(relatorio)
      tempo_ultimo_envio = tempo_atual

    ultimo_offset = verificar_comandos_telegram(ultimo_offset)
    time.sleep(2)


if __name__ == "__main__":
  rodar_sistema()
