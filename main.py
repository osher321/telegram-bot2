import telebot
import time

# -----------------------------
# הגדרות בסיסיות
# -----------------------------
TOKEN = "8201199468:AAGVSijJ3JBSyjZMhgTE220RXrjWWW0u8L4"
bot = telebot.TeleBot(TOKEN, parse_mode="HTML", threaded=True, skip_pending=True)

GROUP_CHAT_ID = -1003491475483  # Chat ID של הקבוצה שלך
WELCOME_MESSAGE = "ברוכים הבאים! כנסו ללינק: https://t.me/osherexpres"

# -----------------------------
# שולח הודעה למשתמשים חדשים
# -----------------------------
@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    for new_member in message.new_chat_members:
        try:
            # שליחת ההודעה עם הקישור לקבוצה
            sent_msg = bot.send_message(GROUP_CHAT_ID, WELCOME_MESSAGE)
            # הדבקת ההודעה למעלה
            bot.pin_chat_message(GROUP_CHAT_ID, sent_msg.message_id, disable_notification=True)
        except Exception as e:
            print("Error sending/pinning message in group:", e)
        
        # שליחת הודעה פרטית למשתמש החדש
        try:
            bot.send_message(new_member.id, WELCOME_MESSAGE)
        except Exception as e:
            print(f"Cannot send private message to {new_member.first_name}: {e}")

# -----------------------------
# שליחת הודעה אוטומטית לקבוצה (למשתמשים קיימים)
# -----------------------------
def send_to_existing_members():
    try:
        sent_msg = bot.send_message(GROUP_CHAT_ID, WELCOME_MESSAGE)
        bot.pin_chat_message(GROUP_CHAT_ID, sent_msg.message_id, disable_notification=True)
        print("Message sent and pinned in the group.")
    except Exception as e:
        print("Error sending/pinning message to the group:", e)

# -----------------------------
# הפעלת הבוט עם לולאת retry
# -----------------------------
if __name__ == "__main__":
    send_to_existing_members()  # שולח הודעה מיידית כשמתחיל
    print("Bot is running...")

    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=60)
        except Exception as e:
            print("Polling error:", e)
            print("Retrying in 5 seconds...")
            time.sleep(5)
