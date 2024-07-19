### Telegram Phone Lookup Bot - Telegram bot search phone number identity

| 🇺🇸 [English](README.md) | 🇮🇷 [Persian](README-FA.md) |
|--------------------------|----------------------------|
<br>

## Description (English)

### Project Introduction

The Telegram Phone Lookup Bot is a Telegram bot that allows you to query phone numbers through various services such as TrueCaller, Numberbook, Numverify, OpenCNAM, and a local database. The bot also provides administrative capabilities for viewing and managing user activities and searches.

### Features

- **Phone Number Lookup**: Check phone numbers using TrueCaller, Numberbook, Numverify, OpenCNAM, and a local database.
- **User Management**: Restrict and unrestrict users.
- **Admin Management**: Add and view a list of admins.
- **Authorized Users**: Add and view a list of authorized users.
- **Statistics and Reports**: View reports and statistics of user searches.

### Installation and Setup

1. **Clone the Repository**

   ```sh
   git clone https://github.com/yourusername/PhoneLookupBot.git
   cd PhoneLookupBot
   ```

2. **Create and Activate a Virtual Environment**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```sh
   pip install -r requirements.txt
   ```

4. **Set Environment Variables**

   Create a `.env` file in the project's root directory and configure the following variables:

   ```env
   TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
   TRUECALLER_API_KEY=YOUR_TRUECALLER_API_KEY
   NUMBERBOOK_API_KEY=YOUR_NUMBERBOOK_API_KEY
   NUMVERIFY_API_KEY=YOUR_NUMVERIFY_API_KEY
   OPENCNAM_API_KEY=YOUR_OPENCNAM_API_KEY
   REDIS_HOST=localhost
   REDIS_PORT=6379
   REDIS_DB=0
   ADMIN_USER_ID=YOUR_TELEGRAM_USER_ID
   ```

5. **Initialize the Database**

   ```sh
   python -c "from database import init_db; init_db()"
   ```

6. **Run the Bot**

   ```sh
   python bot.py
   ```

### Future Improvements

- **Add New Services**: Integrate new services for phone number lookup.
- **Multi-language Support**: Add support for multiple languages.
- **UI Enhancements**: Add new features to the user interface and improve its appearance.
- **Rating System**: Implement a rating system to limit the number of searches per user.

---

By following these instructions, you can set up and run the Phone Lookup Bot efficiently. The project can be extended and improved with additional features in future versions.