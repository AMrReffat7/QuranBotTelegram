from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,MessageHandler,filters
)
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import os
import logging
import requests
import quranpy

logging.basicConfig(
    format='%(asctime)s // %(name)s // %(levelname)s // %(message)s',
    level=logging.INFO)
audio = "alafasy"
selected_audio = "ar.alafasy"
TOKEN = ""
PATH = ""


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a help message."""
    message = "Hello there! I'm a Quran bot. To begin, please use the /start command.\nTo download a Surah, follow these steps:\n1. Use the /audio command to choose the reader.\n2. Then, use the /download command to download the audio file.\nTo know the number of your wanted surah use /list."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a start message."""
    message = "To download a specific Surah, please use the command /download followed by the Surah number.\n For example, to download Surah Al-Nas (Surah number 114), type /download 114\nTo select the reader, use the command /audio."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


async def audio_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton("Mishary Rashid Alafasy", callback_data="ar.alafasy"),
            InlineKeyboardButton("Sa'ud al-Shuraym", callback_data="ar.saudalshuraim"),
        ],
        [InlineKeyboardButton("AbdulBaset AbdulSamad", callback_data="ar.abdulbasitmujawwad")],
        [InlineKeyboardButton("Mahmud Ali Al Banna", callback_data="ar.mahmoudalialbanna")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Please choose:", reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=f"Great! Your request has been processed. Now, please select the Surah number you'd like.")
    global selected_audio
    selected_audio = query.data
    global audio
    audio = query.data.split('.')[1]


async def download_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages."""
    surah_number = context.args[0]
    global selected_audio
    audio_edition = selected_audio
    url = f'https://cdn.islamic.network/quran/audio-surah/128/{audio_edition}/{surah_number}.mp3'
    surah = quranpy.Surah(chapter=surah_number)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Surat {surah.name} ({surah.arabic_name}) is currently being processed. Please wait a moment.",
    )
    global audio
    response = requests.get(url)
    file_name = f"{audio} - Surat{surah.name}.mp3"
    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(response.content)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Downloaded content successfully")
    else:
        print(
            f"Failed to download content from {url}. Status code: {response.status_code}"
        )
    output_path = os.path.join(PATH, file_name)
    await context.bot.send_audio(chat_id=update.effective_chat.id, audio=output_path)
    os.remove(output_path)


async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="1. Al-Fatiha (The Opening)\n2. Al-Baqarah (The Cow)\n3. Aal-E-Imran (The Family of Imran)\n4. An-Nisa' (The Women)\n5. Al-Ma'idah (The Table Spread)\n6. Al-An'am (The Cattle)\n7. Al-A'raf (The Heights)\n8. Al-Anfal (The Spoils of War)\n9. At-Tawbah (The Repentance)\n10. Yunus (Jonah)\n11. Hud (Hud)\n12. Yusuf (Joseph)\n13. Ar-Ra'd (The Thunder)\n14. Ibrahim (Abraham)\n15. Al-Hijr (The Rocky Tract)\n16. An-Nahl (The Bee)\n17. Al-Isra' (The Night Journey)\n18. Al-Kahf (The Cave)\n19. Maryam (Mary)\n20. Ta-Ha (Ta-Ha)\n21. Al-Anbiya' (The Prophets)\n22. Al-Hajj (The Pilgrimage)\n23. Al-Mu'minun (The Believers)\n24. An-Nur (The Light)\n25. Al-Furqan (The Criterion)\n26. Ash-Shu'ara' (The Poets)\n27. An-Naml (The Ant)\n28. Al-Qasas (The Stories)\n29. Al-Ankabut (The Spider)\n30. Ar-Rum (The Romans)\n31. Luqman (Luqman)\n32. As-Sajda (The Prostration)\n33. Al-Ahzab (The Combined Forces)\n34. Saba' (Sheba)\n35. Fatir (The Originator)\n36. Ya-Sin (Ya-Sin)\n37. As-Saffat (Those Ranged in Ranks)\n38. Sad (Sad)\n39. Az-Zumar (The Companies)\n40. Ghafir (The Forgiver)\n41. Fussilat (Explained in Detail)\n42. Ash-Shura (Consultation)\n43. Az-Zukhruf (The Gold Adornments)\n44. Ad-Dukhan (The Smoke)\n45. Al-Jathiyah (The Crouching)\n46. Al-Ahqaf (The Wind-Curved Sandhills)\n47. Muhammad (Muhammad)\n48. Al-Fath (The Victory)\n49. Al-Hujurat (The Rooms)\n50. Qaf (Qaf)\n51. Adh-Dhariyat (The Winnowing Winds)\n52. At-Tur (The Mount)\n53. An-Najm (The Star)\n54. Al-Qamar (The Moon)\n55. Ar-Rahman (The Beneficent)\n56. Al-Waqi'ah (The Inevitable)\n57. Al-Hadid (The Iron)\n58. Al-Mujadila (The Pleading Woman)\n59. Al-Hashr (The Exile)\n60. Al-Mumtahina (The Examined One)\n61. As-Saff (The Ranks)\n62. Al-Jumu'ah (The Congregation)\n63. Al-Munafiqun (The Hypocrites)\n64. At-Taghabun (The Manifestation of Losses)\n65. At-Talaq (The Divorce)\n66. At-Tahrim (The Prohibition)\n67. Al-Mulk (The Dominion)\n68. Al-Qalam (The Pen)\n69. Al-Haqqah (The Reality)\n70. Al-Ma'arij (The Ascending Stairways)\n71. Nuh (Noah)\n72. Al-Jinn (The Jinn)\n73. Al-Muzzammil (The Enshrouded One)\n74. Al-Muddathir (The Cloaked One)\n75. Al-Qiyamah (The Resurrection)\n76. Al-Insan (Man)\n77. Al-Mursalat (The Emissaries)\n78. An-Naba' (The Tidings)\n79. An-Nazi'at (Those Who Drag Forth)\n80. 'Abasa (He Frowned)\n81. At-Takwir (The Overthrowing)\n82. Al-Infitar (The Cleaving)\n83. Al-Mutaffifin (The Defrauding)\n84. Al-Inshiqaq (The Splitting Open)\n85. Al-Buruj (The Mansions of the Stars)\n86. At-Tariq (The Morning Star)\n87. Al-A'la (The Most High)\n88. Al-Ghashiyah (The Overwhelming)\n89. Al-Fajr (The Dawn)\n90. Al-Balad (The City)\n91. Ash-Shams (The Sun)\n92. Al-Lail (The Night)\n93. Ad-Duha (The Morning Hours)\n94. Ash-Sharh (The Relief)\n95. At-Tin (The Fig)\n96. Al-'Alaq (The Clot)\n97. Al-Qadr (The Power)\n98. Al-Bayyinah (The Clear Proof)\n99. Az-Zalzalah (The Earthquake)\n100. Al-'Adiyat (The Courser)\n101. Al-Qari'ah (The Calamity)\n102. At-Takathur (The Rivalry in World Increase)\n103. Al-'Asr (The Declining Day)\n104. Al-Humazah (The Traducer)\n105. Al-Fil (The Elephant)\n106. Quraysh (Quraysh)\n107. Al-Ma'un (The Small Kindnesses)\n108. Al-Kawthar (The Abundance)\n109. Al-Kafirun (The Disbelievers)\n110. An-Nasr (The Divine Support)\n111. Al-Masad (The Palm Fiber)\n112. Al-Ikhlas (The Sincerity)\n113. Al-Falaq (The Daybreak)\n114. An-Nas (The Mankind)\n")

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

async def wrong(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Try use /help for info.")

if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()

    help_handler = CommandHandler("help", help_command)
    start_handler = CommandHandler("start", start_command)
    message_handler = CommandHandler("download", download_command)
    audio_handler = CommandHandler("audio", audio_command)
    button_handler = CallbackQueryHandler(button)
    list_handler = CommandHandler("list", list_command)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    wrong_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), wrong)

    application.add_handler(button_handler)
    application.add_handler(help_handler)
    application.add_handler(start_handler)
    application.add_handler(message_handler)
    application.add_handler(audio_handler)
    application.add_handler(list_handler)
    application.add_handler(unknown_handler)
    application.add_handler(wrong_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)
