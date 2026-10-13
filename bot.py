import os
import base64
import requests
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

# ======================================
# 👇 ဒီနေရာမှာ သင့်တိုကင်အသစ်ထည့်ပါ
MY_BOT_TOKEN = "8670358434:AAFRLIRSOgTIF35TXYyrGz30PxrqCnuv-x8"
# ======================================

API_URL = "https://shadowmere.xyz/api/sub/"
bot = Bot(token=MY_BOT_TOKEN)
dp = Dispatcher()

def generate_ss_link(server):
    userinfo = f"{server['method']}:{server['password']}"
    b64 = base64.b64encode(userinfo.encode()).decode().rstrip('=')
    return f"ss://{b64}@{server['server']}:{server['server_port']}#{server['remarks']}"

def get_servers(region=None):
    try:
        r = requests.get(API_URL, timeout=30)
        r.raise_for_status()
        servers = r.json()
        if region:
            servers = [s for s in servers if region.lower() in s['remarks'].lower()]
        return servers
    except Exception as e:
        print(f"API Error: {e}")
        return []

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    text = """👋 VPN Key Bot မှ ကြိုဆိုပါတယ်!

အမှာစာများ-
/all  - နိုင်ငံအားလုံး
/sg   - Singapore 🇸🇬
/hk   - Hong Kong 🇭🇰
/jp   - Japan 🇯🇵
/kr   - South Korea 🇰🇷
/us   - United States 🇺🇸
/nl   - Netherlands 🇳🇱
/de   - Germany 🇩🇪
/uk   - United Kingdom 🇬🇧

ss:// လင့်ကို ကော်ပီကူးပြီး Shadowsocks မှာ အသုံးပြုပါ။"""
    await message.answer(text)

@dp.message(Command("all"))
async def cmd_all(message: types.Message):
    await message.answer("🔄 ဆာဗာများရယူနေသည်... ခဏစောင့်ပါ")
    servers = get_servers()
    if not servers:
        await message.answer("❌ ဒေတာရယူ၍မရပါ")
        return
    
    text = f"✅ စုစုပေါင်း ဆာဗာ {len(servers)} လုံး\n\n"
    for s in servers[:20]:
        link = generate_ss_link(s)
        text += f"{s['remarks']}\n<code>{link}</code>\n\n"
    if len(servers) > 20:
        text += f"... နောက်ထပ် {len(servers)-20} လုံး ရှိပါသေးတယ်"
    await message.answer(text, parse_mode="HTML")

async def send_by_region(message: types.Message, keyword: str):
    servers = get_servers(keyword)
    if not servers:
        await message.answer(f"❌ {keyword} ဆာဗာ မတွေ့ပါ")
        return
    
    text = f"✅ {keyword} – စုစုပေါင်း {len(servers)} ခု\n\n"
    for s in servers:
        link = generate_ss_link(s)
        text += f"{s['remarks']}\n<code>{link}</code>\n\n"
    await message.answer(text, parse_mode="HTML")

@dp.message(Command("sg"))
async def cmd_sg(message: types.Message): await send_by_region(message, "Singapore")
@dp.message(Command("hk"))
async def cmd_hk(message: types.Message): await send_by_region(message, "Hong Kong")
@dp.message(Command("jp"))
async def cmd_jp(message: types.Message): await send_by_region(message, "Japan")
@dp.message(Command("kr"))
async def cmd_kr(message: types.Message): await send_by_region(message, "South Korea")
@dp.message(Command("us"))
async def cmd_us(message: types.Message): await send_by_region(message, "United States")
@dp.message(Command("nl"))
async def cmd_nl(message: types.Message): await send_by_region(message, "Netherlands")
@dp.message(Command("de"))
async def cmd_de(message: types.Message): await send_by_region(message, "Germany")
@dp.message(Command("uk"))
async def cmd_uk(message: types.Message): await send_by_region(message, "United Kingdom")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
