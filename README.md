# Prenses Music Bot (YouTube + Voice Chat Assistant)

Telegram müzik botu — YouTube araması (YouTube API v3) + sesli sohbette çalma (PyTgCalls).
Bot hesabı komutları alır; **asistan (user) hesabı** sesli sohbete bağlanıp müziği çalar.

## Özellikler
- `/play <şarkı adı | YouTube linki>`: Sıraya ekler ve çalar
- `/skip`: Geç
- `/pause` / `/resume`: Duraklat / Devam et
- `/stop`: Sırayı temizle ve ayrıl
- `/queue`: Mevcut sıra
- `/join`: Asistanı sesliye çağırır (gerekmeyebilir, /play otomatik bağlar)

## Gerekli Ortam Değerleri (.env)
Aşağıdaki örneği `.env` olarak kopyalayın ve düzenleyin:

```env
API_ID=123456
API_HASH=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11

# Asistan (USER) hesabı — zorunlu (bot hesapları sesli sohbete tek başına giremez)
SESSION_STRING=
# veya telefon ile giriş yapmak isterseniz (opsiyonel, SESSION_STRING yerine):
ASSISTANT_PHONE=+90xxxxxxx

# Günlük/loglarınız için bir grup/kanal ID'si (opsiyonel)
LOG_GROUP_ID=0

# YouTube Data API v3 anahtarı (kullanıcı sağladı)
YOUTUBE_API_KEY=AIzaSyBWEUJjXpdrWP9lNdkhuiynVjyqnIzd-So
```

> **Not:** `SESSION_STRING` oluşturmak için herhangi bir string-gen botu veya yerelde kısa bir script kullanabilirsiniz. (Pyrogram `StringSession`)

## Heroku (Buildpacks) Deploy
1) `.env` içeriğini Heroku `Config Vars` olarak ekleyin (satır satır).  
2) Deploy edin. (Bu repo buildpack tabanlıdır)
3) **Dyno**: `worker` tipini açın.

## Docker
İsterseniz `Dockerfile` ile çalıştırabilirsiniz.

## Termux / Lokal Çalıştırma
```bash
pip install -r requirements.txt
python main.py
```

— Derdo için özel: Hata olursa `LOG_GROUP_ID` ekleyip çıktıları oraya alabilirsiniz.


### 🚀 Heroku Üzerinden Kurulum
Aşağıdaki butona basarak botu Heroku'ya kolayca kurabilirsiniz:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Kralderdo/Promucisbot/tree/main)
