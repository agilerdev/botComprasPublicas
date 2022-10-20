const TelegramBot = require('node-telegram-bot-api');
require('dotenv').config()

const token = process.env.BOT_TOKEN;
const chatId = process.env.TELEGRAM_CHAT_ID;
const bot = new TelegramBot(token, { polling: true });

async function enviar(message) {
    return await bot.sendMessage(chatId, message);
}

exports.enviar = enviar;
