<p align="center">
<a href="https://iconscout.com/icon/tiktok-4069944"><img src="images/tiktok.png" align="center" height=365 alt="Tok Mate Bot" />
</p>

<p align="center">
<a href="https://t.me/tokmatebot">
<img src='https://img.shields.io/badge/Tok Mate-Active-blue?style=for-the-badge&logo=telegram'>
</a>
<a href="https://t.me/h9youtube">
<img src='https://img.shields.io/badge/Channel-Join-blue?style=for-the-badge&logo=telegram'>
</a>

</P>
<h1 align='center'>⬇️ Tokmate - Telegram Bot to download TikTok videos</h1>


# ⛲ Features

- Superfast and supports all type of TikTok links
- Download any TikTok videos without matermark
- Cache the videos so that future requests for that video can be served faster
- Inline and group support

# 🌐 Chrome Extension

The chrome extension for the TokMate Bot is under construction in [this](https://github.com/hemantapkh/TokMateextension) repo.

# 🔥 API

- Get your Token by sending `/token` to the bot or by clicking [here](https://t.me/tokmatebot?start=getToken).
- Send a post request to ``https://hemantapokharel.com.np/tokmateApi/`` with the following  JSON data: ```{"token": "<your_token>", "url": "<tiktok_url>"}```
- On a successful request, you will get the TikTok video without watermark in your Telegram app.

---

## 🔒 Privacy

For any TikTok videos the bot uploads, the `TikTok URL` of that video and the `video_file_id` **(File Id of the video in the Telegram server)**  are stored in the database so that any future requests for that video can be served faster. 

**These data will not be associated with any users and the video is already public in the TikTok. So, the bot does not affect your privacy.**

*The `TikTok Url` and the `video_file_id` of the video requested from the inline query is not stored in the database.*


---

## ⚒️ Deployment

This bot can be deployed similarly as the [Torrent Hunt bot](https://github.com/hemantapkh/torrenthunt).

---

## 💚 Contributing

Any contributions you make are **greatly appreciated**.

---
❇️ Made for fun in Python💙 by [Hemanta Pokharel](https://github.com/hemantapkh/) [[✉️](mailto:hemantapkh@yahoo.com) [💬](https://t.me/hemantapkh) [📺](https://youtube.com/h9youtube)]

❣ Logo by [Iconscout](https://iconscout.com/icon/tiktok-4069944)