import time
import requests

# --- НАСТРОЙКИ БОТА ---
TOKEN = "8649834813:AAFydQFK4JuRuel9hqcvp41bahXrEUQR20c"  # Твой токен
CHAT_ID = "908565496"  # Твой Chat ID

# Имя файла для локального лога
LOG_FILE = "net_log.txt"


def write_log(message):
  """Функция записи событий в локальный текстовый файл"""
  timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
  log_line = f"[{timestamp}] {message}\n"
  try:
    with open(LOG_FILE, "a", encoding="utf-8") as f:
      f.write(log_line)
  except Exception as e:
    print(f"⚠️ Не удалось записать лог в файл: {e}")


def send_telegram_alert(message):
  """Функция отправки сообщения в Telegram"""
  url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
  payload = {"chat_id": CHAT_ID, "text": message}
  try:
    response = requests.post(url, json=payload, timeout=5)
    return response.status_code == 200
  except Exception as e:
    print(f"⚠️ Не удалось отправить сообщение в Telegram: {e}")
    return False


def check_internet():
  """Проверка доступности интернета через Cloudflare"""
  try:
    response = requests.get("https://www.cloudflare.com/cdn-cgi/trace", timeout=3)
    return response.status_code == 200
  except:
    return False


def main():
  print("🛡️ DevOps-сторож запущен и ведет локальный лог...")
  write_log("Система мониторинга запущена.")
  is_offline_notified = False

  while True:
    status = check_internet()
    current_time = time.strftime("%H:%M:%S")

    if status:
      print(f"[{current_time}] ✅ Интернет в норме.")
      if is_offline_notified:
        log_msg = "Интернет на рабочем месте восстановлен."
        write_log(log_msg)
        send_telegram_alert(f"🟢 Внимание: {log_msg}")
        is_offline_notified = False
    else:
      print(f"[{current_time}] ❌ СЕТЬ УПАЛА!")
      if not is_offline_notified:
        log_msg = "ТРЕВОГА! Пропал интернет или упала сеть на рабочем месте!"
        write_log(log_msg)
        # Пробуем отправить в Telegram (если сеть «упала» локально, но до интернета ТГ еще может достучаться)
        send_telegram_alert(f"🚨 {log_msg}")
        is_offline_notified = True

    # Пауза перед следующей проверкой (30 секунд)
    time.sleep(10)


if __name__ == "__main__":
  main()