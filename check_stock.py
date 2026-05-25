import requests, os

SKU_ID = os.environ["SKU_ID"]
TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

def check_stock():
    url = f"https://www.falabella.com/s/browse/v1/listing/cl?skuId={SKU_ID}"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers).json()
    
    results = r.get("data", {}).get("results", [])
    if not results:
        print("No se encontró el producto")
        return
    
    product = results[0]
    name = product.get("displayName", "Producto")
    prices = product.get("prices", [])
    available = product.get("quantityAvailable", 0)

    if available > 0:
        price = prices[0].get("originalPrice", "?") if prices else "?"
        notify(f"✅ {name} está disponible!\n💰 Precio: ${price:,}\nfalabella.com")
    else:
        print(f"Sin stock: {name}")

def notify(msg):
    requests.get(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        params={"chat_id": CHAT_ID, "text": msg}
    )

check_stock()
