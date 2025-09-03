import telebot
import requests
from bs4 import BeautifulSoup
import threading
import time

API_TOKEN = '8176515312:AAF3ba9iwCZe9oemLRmP-y4GLvAhrixd0u8'
TARGET_CHAT_ID = '470524502'
bot = telebot.TeleBot(API_TOKEN)

# מילון שמות באנגלית → עברית
HEBREW_NAMES = {
    "Teva Pharmaceutical Industries Ltd": "טבע",
    "Bank Hapoalim": "בנק הפועלים",
    "Bank Leumi": "בנק לאומי",
    "Nice Ltd": "נייס",
    "Elbit Systems": "אלביט מערכות",
    "Tower Semiconductor Ltd": "טאוור",
    "Azrieli Group": "עזריאלי",
    "Shufersal": "שופרסל",
    "Israel Corp": "החברה לישראל",
    "Mizrahi Tefahot Bank": "בנק מזרחי טפחות",
    "GIXGIX INTERNET": "גיקס",
    "FLYSFLYING SPARK": "פליינג ספארק",
    "RAYG-MRAY TLV GROUP": "ריי טי.אל.וי",
    "BARIBARAK": "ברק קפיטל",
    "TRANTRUCKNET": "טראקנט",
    "SVRTSAVOREAT": "סבוריט",
    "ZOOZZOOZ POWER": "זום פאואר",
    "UNTCUNIC-TECH": "יוניק-טק (השקעות בהייטק)",
    "BKRYBIKUREY HASADE": "ביכורי השדה",
    "AAILNAXILION": "אקיסליון",
    "BRNDBRAND": "ברנד",
    "RTMD-MRETAILMINDS": "ריטייל מיינדס",
    "BLRXBIOLINE": "ביוליין - ביומד",
    "MSVTMASSIVIT 3D": "מאסיבית",
    "SCCSPACE": "חלל תקשורת",
    "SLCLSILVER": "סילבר קסטל",
    "MRHLMERCHAVIA": "מרחביה",
    "REKAREKAH": "רקח",
    "FRSXFORESIGHT": "פורסייט - הייטק",
    "PMVMPOMVOM": "פוםוום - תוכנה",
    "SLRMSOLROM": "סולרום",
    "EEAM-ME.E.A.M.I": "אי.אי.איי.אם",
    "NURINUR INK": "נור אינק",
    "GIVOGIVOT OLAM OIL": "גבעות עולם",
    "BLRNBLADERANGER": "בלייד ריינג'ר",
    "AVRTAVROT": "אברות",
    "MSBIHAMASHBIR 365": "המשביר 365",
    "IMEDIMED": "אימד אינפיניטי",
    "PPBTPURPLE": "פרפל ביוטק",
    "TEDETEDEA": "תדאה",
    "AARANARAN": "ארן",
    "STRGSTORAGE": "סטורג דרופ",
	"NXGNNEXTGEN BIOMED": "נקסט ג'ן",
    "KRNV-MKARDAN": "קרדן אן וי",
    "IDMOIDOMOO": "אידומו",
    "LBTLLIBENTAL": "ליבנטל",
    "SHGRSHAGRIR": "שגריר",
    "CPIACIPIA VISION": "סיפיה ויז'ן",
    "BIMTBIO MEAT": "ביומיט",
    "BLWV-MBL WA WA CAP": "בלו וייב",
    "ELCREELECTRA REAL": "אלקטרה נדלן",
    "NRGNNRGENE TECHS": "אנרג'ין",
    "NSTRNORSTAR": "נורסטאר",
    "OPALOPAL": "אופל בלאנס",
    "HUMXHUMAN XTENSIONS": "יומן אקס",
    "MNIFMENIF": "מניף",
    "UPSLUPSELLON": "אפסילון",
    "ELRNELRON": "אלרון",
    "ELMRELMOR": "אלמור חשמל",
    "MPPMORE PROVIDENT":"מור גמל",
    "GOTOGOTO": "גוטו",
    "TRXTERMINAL X": "טרמינל איקס",
    "PNRGPHINERGY": "פינרגי - קלינטק",
    "UNITUNITRONICS": "יוניטרוניקס",
    "SPNTCSPUNTECH": "ספאנטק",
    "BRANBARAN": "ברן",
    "MSLAMASLAVI": "מצלאווי",
    "PMNTPAYMENT": "פיימנט",
    "CLABC-LAB": "סי-לאב",
    "SOLRSOLAER": "סולאיר",
    "EMDVEMILIA": "אמיליה פיתוח",
    "RSELRSL": "אראסל",
    "ORONORON": "אורון קבוצה",
    "AALBAALBAAD": "עלבד",
    "LUZNLUZON": "לוזון",
    "CMERMER": "ח.מר",
    "RIMORIMONI": "רימוני",
    "ACROKVUTZAT ACRO": "אקרו קבוצה",
    "RMONRIMON CONSULTING &": "רימון",
    "HGGHAGAG": "חגג - נדלן",
    "AARINARI REAL ESTATE": "ארנה גרופ",
    "SKLNSKYLINE": "סקיילייין",
    "SOLT-MSOLTERRA": "סולטרה",
    "AAMXAUTOMAX MOTORS": "אוטומקס",
    "MLD-MMIRLAND": "מירלנד - נדלן",
    "MTLFMATRICELF": "מטריסלף",
    "TNPVTCHNOPLS": "טכנופלסט",
    "EPITEPITOMEE MEDICAL": "אפיטומי מדיקל",
    "WATRWATER.IO": "ווטר אי או",
    "AUGNAUGWIND": "אוגווינד",
    "AAPLPAPOLLO": "אפולו - קלינטק",
    "VISNVISION": "ויזן סיגמא",
    "WNBZWIND BUZZ" : "ווינד באז - קלינטק",
    "ISCDISRACARD" : "ישראכארד - פיננסים",
    "PRIMPRIME ENERGY": "פריים אנרגי",
    "SHNPSCHNAPP": "שנפ",
    "TNDOTONDO SMART": "טונדו סמארט",
    "CNTCCANNABOTECH": "קנבוטק",
    "INCRINTERCURE": "אינטרקיור",
    "PAYTPAYTON": "פייטון",
    "YBRDY.B": "י.ב. התחדשות",
    "GRACGRACE BREEDING": "גרייס",
    "TPGMTOP GUM": "טופ גאם",
    "BYONBEYON 3D": "ביונ תלת מימד",
    "UNCTUNICORN TECHS": "יוניקורן טכ",
    "G107GROUP 107": "גרופ 107",
    "GLTLGILAT": "גילת",
    "PHTMPHOTOMYNE": "פוטומיין",
    "DISIDISCOUNT": "דיסקונט השקעות",
    "MPRSMEDIPRESS": "מדיפרס בריאות",
    "CNTL-MCONTINUAL":"קונטיניואל",
    "VALCVALUE CAPITAL":"וואליו קפיטל",
    "FEATFEAT FUND": "פיט השקעות",
    "ENRGENERGIX": "אנרג'יקס",
    "MGDLMIGDAL": "מגדל",
    "KAREKARDAN REAL":"קרדן נדלן",
    "INRMINROM": "אינרום",
    "MAXOMAX STOCK" :"מקס סטוק",
    "ENLTENLIGHT": "אנלייט",
    "OPCEOPC": "או.פי.סי",
    "BONSBONUS": "בונוס",
    "LUMILEUMI":"לאומי",
    "POLIPOALIM":"פועלים",
    "MSKEMESHEK ENGY": "משק אנרגיה",
    "CRSMCARASSO MOTORS": "קרסו",
    "MTRNMAYTRONICS":"מיטרוניקס",
    "AMOTAMOT": "אמות",
    "AURAAURA": "אאורה - נדלן",
    "PTNRPARTNER": "פרטנר",
    "TRATARYA ISREAL":"טריא",
    "TASETASE":"מניית הבורסה",
    "BIOVBIO":"ביוויו - ביומד",
    "PCBTP.C.B": "פיסיבי טכנולוגיה",
    "GEFRGEFFEN": "גפן מגורים",
    "AARYTARYT": "ארית - בטחוני",
    "HMGSHOMEBIOGAS": "הום ביוגז",
    "GNCLGENCELL":"ג'נסל",
    "XTLBXTL":"אקסטיאל",
    "BCURERIKA":"ביקיור",
    "AQUAAQUARIUS":"אקווריוס",
    "JEENJEEN TECH":"ג'ין טק - תוכנה",
    "POLPPOLYRAM PLASTIC":"פולירם",
    "MIAMIA DYNAMICS":"מיה דינמיקס",
    "CELCELLCOM":"סלקום - תקשורת",
    "AZRMAZORIM":"אזורים",
    "AALTFALTSHULER SHAHAM":"אלטשולר שחם",
    "ZURZUR":"צור",
    "ALARALARUM":"אלארום",
    "BULL-MBULL TRADING AND":"בול מסחר",
    "BEZQBEZEQ":"בזק",
    "ALUMAALUMA":"אלומה",
    "ELALEL":"אל על",
    "ISRGISRAIR GROUP":"ישראייר - נופש ותעופה",
    "ISCNISRAEL":"ישראל קנדה",
    "GCTG CITY":"ג'י סיטי",
    "RANIRANI":"רני צים",
    "RATIRATIO ENERGIES":"רציו",
    "ISRAISRAMCO NEGEV 2":"ישראמקו",
    "IDNTIDENTI":"איידנטי",
    "CILOCIELO-BLU":"צילו בילו - נדלן",
    "AACCLACCEL":"אקסל",
    "TEVATEVA":"טבע",
    "THESTHIRDEYE SYSTEMS":"עין שלישית",
    "BCOMB":"בי קום",
    "GNRSGENERATION":"ג'נריישן",
    "SSBENSHIKUN & BINUI":"שיכון ובינוי",
    "TKUNTIKUN OLAM":"תיקון עולם - קנאביס",
    "AABRAABRA":"אברא",
    "SONOSONOVIA":"סונוביה",
    "MYDSMYDAS":"מידאס - נדלן",
    "TECTTECTONA":"טקטונה",
    "DNAD.N.A":"די.אן.איי - נדלן וביומד",
    "WESRWESURE GLOBAL":"ווישור - ביטוח",
    "BRIHRAV BARIACH 08":"רב בריח - מוצרי בניה",
    "HARLHAREL":"הראל",
       "AYALAYALON":"איילון",
       "YBOXYBOX":"ויבוקס",
       "AACKRACKERSTEIN GROUP":"קבוצת אקרשטיין",
       "TKUNTIKUN OLAM -":"תיקון עולם - קנאביס",
       "ICLICL":"אייסיאל",
       "MVNEMIVNE":"מבנה",
       "STRSSTRAUSS":"שטראוס",
       "NWMDNEWMED ENERGY":"ניומד אנרגיה",
       "AARDMAERODROME":"אירודרום",
       "SKBNSHIKUN &":"שיכון ובינוי",
       "LBRALIBRA INSURANCE":"ליברה",
       "EMCOE&M":"אמת",
       "RTPTRATIO":"רציו פטרול",
       "RRPOLRP OPTICAL LAB":"אר טי פי אופטיקל - בטחוני",
       "DORLDORAL GP":"דוראל אנרגיה - אנרגיה מתחדשת",
       "CCPPLCITY PEOPLE OF":"אנשי העיר - נדלן",
       "MMGDOMEGIDO Y.K.":"מגידו - נדלן",
       "TMRPTAMAR":"תמר פטרוליום",
       "SHMMSHAMAYM":"שמיים",
       "TRPZTURPAZ":"תורפז",
       "HAMATHAMAT":"חמת",
       "SPENSHAPIR":"שפיר",
       "WILKWILK":"וילק",
       "RZRRAZOR LABS":"רייזור",
       "NXTGNEXTAGE":"נקסט גן",
       "PULSPULSENMORE":"פלאנסמור",
       "MTRDMEITAV TRADE":"מיטב",
       "ARYTARYT":"ארית",
       "SOFWSOFWAVE":"סופוויב",
       "ALTFALTSHULER SHAHAM":"אלטושלר שחם",
       "ARINARI REAL ESTATE":"ארי נדלן",
       "ALHEALONY":"אלוני",
       "AILNAXILION":"אקסילון",
       "MRINMOR":"מור",
       "ACKRACKERSTEIN GROUP":"אקרשטיין",
       "AMXAUTOMAX MOTORS":"אוטומקס",
       "SBENSHIKUN & BINUI":"שיכון ובינוי",
       "ISOPISRAEL":"הזדמנות ישראלית",
       "RPOLRP OPTICAL LAB":"אר פי אופטיקל",
       "YACOYACOBI":"יעקובי",
       "SAESHUFERSAL":"שופרסל",
       "NVLGNOVOLOG":"נובולוג",
       "AVGLAVGOL":"אבגול",
       "ORLBAZAN":"בזן",
       "DLEADELEK":"דלק רכב",
       "SNFLSUNFLOWER":"סאנפלוואר",
       "GOSSG 1":"ג'י וואן",
       "ARDMAERODROME":"אירודרום",
       "RRGASR.G.A SERVICES":"ר.ג.א",
       "AMRMAMRAM AVRAHAM":"עמרם"
}

def clean_stock_name(raw_name):
    parts = raw_name.split()
    if len(parts) > 1:
        last = parts[-1]
        if last.isupper() or '.' in last:
            parts = parts[:-1]
    return ' '.join(parts)

def get_movers(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    rows = soup.select("table tr")[1:50]  # דילוג על כותרת + לקיחה של עד 50 שורות

    m_movers = []
    k_movers = []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 4:
            raw_name = cols[0].get_text(strip=True)
            name_clean = clean_stock_name(raw_name)
            display_name = HEBREW_NAMES.get(name_clean, name_clean)
            volume = cols[1].get_text(strip=True)
            change = cols[3].get_text(strip=True).strip()

            if "M" in change:
                m_movers.append((display_name, volume, change))
            elif "K" in change:
                try:
                    change_value = float(change.replace("K", "").strip())
                    if change_value > 100:
                        k_movers.append((display_name, volume, change, change_value))
                except ValueError:
                    print(f"⚠️ לא ניתן להמיר: {change}")

    # מיון לפי ערך מספרי יורד רק לרשומות עם K
    k_movers_sorted = sorted(k_movers, key=lambda x: x[3], reverse=True)
    # מחיקת עמודת הערך המספרי אחרי המיון
    k_movers_cleaned = [(name, volume, change) for name, volume, change, _ in k_movers_sorted]

    # שילוב M ואחריהם K ממוינים
    final_movers = m_movers + k_movers_cleaned
    return final_movers[:10]

def format_movers(title, movers, upward=True):
    arrow = "📈" if upward else "📉"
    emoji = "🟢" if upward else "🔴"
    response = f"{arrow} *{title}*:\n"
    for idx, (name, volume, change) in enumerate(movers, 1):
        response += f"{idx}. {emoji}  {name}, שינוי של {volume} במחזור של ({change})\n"
    return response

@bot.message_handler(commands=['top'])
def top_gainers(message):
    try:
        data = get_movers("https://www.tradingview.com/markets/stocks-israel/market-movers-gainers/")
        response = format_movers("10 המניות שהכי עלו היום", data, upward=True)
        bot.reply_to(message, response, parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"שגיאה בשליפת עליות: {e}")

@bot.message_handler(commands=['bottom'])
def top_losers(message):
    try:
        data = get_movers("https://www.tradingview.com/markets/stocks-israel/market-movers-losers/")
        response = format_movers("10 המניות שהכי ירדו היום", data, upward=False)
        bot.reply_to(message, response, parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"שגיאה בשליפת ירידות: {e}")

@bot.message_handler(commands=['start', 'help'])
def help_msg(message):
    bot.reply_to(message,
        "🤖 ברוך הבא לבוט מניות ישראל!\n"
        "פקודות זמינות:\n"
        "/top – 10 המניות שהכי עלו\n"
        "/bottom – 10 המניות שהכי ירדו\n"
        "/id – לקבלת chat ID",
        parse_mode="Markdown")

@bot.message_handler(commands=['id'])
def show_id(message):
    bot.reply_to(message, f"🔢 *Chat ID:* `{message.chat.id}`", parse_mode="Markdown")

def auto_broadcast():
    while True:
        try:
            top = get_movers("https://www.tradingview.com/markets/stocks-israel/market-movers-gainers/")
            bottom = get_movers("https://www.tradingview.com/markets/stocks-israel/market-movers-losers/")
            msg = format_movers("10 המניות שהכי עלו היום", top, True)
            msg += "\n"
            msg += format_movers("10 המניות שהכי ירדו היום", bottom, False)
            bot.send_message(chat_id=TARGET_CHAT_ID, text=msg, parse_mode="Markdown")
            print("Here we go, oren the King!")
        except Exception as e:
            print(f"שגיאה בשידור אוטומטי: {e}")
        time.sleep(2400)

threading.Thread(target=auto_broadcast, daemon=True).start()

print("Oren!You are the king!")
bot.infinity_polling()
