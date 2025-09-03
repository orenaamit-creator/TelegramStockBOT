import telebot
import requests
from bs4 import BeautifulSoup
import threading
import time
import datetime
from fuzzywuzzy import process

API_TOKEN = '8176515312:AAF3ba9iwCZe9oemLRmP-y4GLvAhrixd0u8'
TARGET_CHAT_ID = '470524502'
bot = telebot.TeleBot(API_TOKEN)

# מילון שמות באנגלית ← עברית
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

def get_best_match(raw_name, choices, min_score=75):
    """
    Finds the best fuzzy match for a given raw name from a list of choices.
    """
    best_match, score = process.extractOne(raw_name, choices)
    if score >= min_score:
        return best_match
    return None

def get_movers(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    rows = soup.select("table tr")[1:50]

    m_movers = []
    k_movers = []
    
    hebrew_names_keys = list(HEBREW_NAMES.keys())

    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 4:
            raw_name = cols[0].get_text(strip=True)
            
            best_match_key = get_best_match(raw_name, hebrew_names_keys)
            
            if best_match_key:
                display_name = HEBREW_NAMES[best_match_key]
            else:
                display_name = raw_name
                
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
                    print(f"⚠️ Could not convert change value: {change}")

    k_movers_sorted = sorted(k_movers, key=lambda x: x[3], reverse=True)
    k_movers_cleaned = [(name, volume, change) for name, volume, change, _ in k_movers_sorted]

    final_movers = m_movers + k_movers_cleaned
    return final_movers[:10]
    
def get_unusual_volume_movers(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    rows = soup.select("table tr")[1:50]

    gainers = []
    losers = []
    
    hebrew_names_keys = list(HEBREW_NAMES.keys())

    for row in rows:
        cols = row.find_all("td")
        # Ensure there are enough columns before accessing
        if len(cols) >= 5:
            raw_name = cols[0].get_text(strip=True)
            best_match_key = get_best_match(raw_name, hebrew_names_keys)
            
            display_name = HEBREW_NAMES.get(best_match_key, raw_name)
            
            volume = cols[1].get_text(strip=True)
            
            # Correcting column index from 4 to 3 based on standard TradingView tables
            # And replacing the unicode minus sign with a standard one
            change_str = cols[3].get_text(strip=True).replace('−', '-').strip()
            
            try:
                change_value = float(change_str.replace('%', '').strip())
                
                # Format change string for display
                formatted_change = f"{change_value:.2f}%"

                # Storing the original change value for sorting
                if change_value > 0:
                    gainers.append((display_name, formatted_change, volume, change_value))
                elif change_value < 0:
                    losers.append((display_name, formatted_change, volume, change_value))

            except ValueError:
                print(f"⚠️ Could not convert change value for unusual volume: {change_str}")
        else:
            print(f"⚠️ Row has fewer than 5 columns: {len(cols)}")

    # Sort gainers and losers by their change value
    gainers.sort(key=lambda x: x[3], reverse=True)
    losers.sort(key=lambda x: x[3])

    # Return top 10 from each list, and ensure the tuple has 4 values
    return gainers[:10], losers[:10]

def format_movers(title, movers, upward=True):
    arrow = "📈" if upward else "📉"
    emoji = "🟢" if upward else "🔴"
    lines = [f"{arrow} *{title}*:"]
    for idx, item in enumerate(movers, 1):
        try:
            if isinstance(item, (list, tuple)):
                if len(item) == 4:
                    # unusual volume: (name, formatted_change, volume, change_value)
                    name, change, volume, _ = item
                elif len(item) == 3:
                    # regular movers: (name, volume, change)
                    name, volume, change = item
                else:
                    # fallback for unexpected shapes
                    name = item[0] if len(item) > 0 else "—"
                    change = item[1] if len(item) > 1 else "—"
                    volume = item[2] if len(item) > 2 else "—"
            else:
                # item is a scalar or dict; try reasonable defaults
                name = getattr(item, "name", str(item))
                change = getattr(item, "change", "—")
                volume = getattr(item, "volume", "—")
        except Exception:
            name, change, volume = "—", "—", "—"
        lines.append(f"{idx}. {emoji} {name}, שינוי של {change} במחזור של ({volume})")
    return "\n".join(lines)

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

@bot.message_handler(commands=['volume'])
def unusual_volume_report(message):
    try:
        gainers, losers = get_unusual_volume_movers("https://www.tradingview.com/markets/stocks-israel/market-movers-unusual-volume/")
        
        report = ""
        if gainers:
            report += format_movers("10 המניות בעלייה חריגה", gainers, upward=True)
            report += "\n"
        if losers:
            report += format_movers("10 המניות בירידה חריגה", losers, upward=False)

        if report:
            bot.reply_to(message, report, parse_mode="Markdown")
        else:
            bot.reply_to(message, "לא נמצאו מניות עם ווליום חריג כרגע.")
            
    except Exception as e:
        bot.reply_to(message, f"שגיאה בשליפת נתוני ווליום חריג: {e}")


@bot.message_handler(commands=['start', 'help'])
def help_msg(message):
    bot.reply_to(message,
        "🤖 ברוך הבא לבוט מניות ישראל!\n"
        "פקודות זמינות:\n"
        "/top – 10 המניות שהכי עלו\n"
        "/bottom – 10 המניות שהכי ירדו\n"
        "/volume – 10 המניות עם ווליום חריג שעלו והכי ירדו\n"
        "/id – לקבלת chat ID",
        parse_mode="Markdown")

@bot.message_handler(commands=['id'])
def show_id(message):
    bot.reply_to(message, f"🔢 *Chat ID:* `{message.chat.id}`", parse_mode="Markdown")

def auto_broadcast():
    while True:
        now = datetime.datetime.now()
        day_of_week = now.weekday()

        start_hour = 10
        start_minute = 30
        
        if day_of_week == 6:
            end_hour = 23
            end_minute = 30
        elif 0 <= day_of_week <= 3:
            end_hour = 23
            end_minute = 0
        else:
            time.sleep(600)
            continue

        is_in_time_range = (
            now.hour > start_hour or (now.hour == start_hour and now.minute >= start_minute)
        ) and (
            now.hour < end_hour or (now.hour == end_hour and now.minute < end_minute)
        )

        if is_in_time_range:
            try:
                top = get_movers("https://www.tradingview.com/markets/stocks-israel/market-movers-gainers/")
                bottom = get_movers("https://www.tradingview.com/markets/stocks-israel/market-movers-losers/")
                volume_gainers, volume_losers = get_unusual_volume_movers("https://www.tradingview.com/markets/stocks-israel/market-movers-unusual-volume/")

                msg = format_movers("10 המניות שהכי עלו היום", top, True)
                msg += "\n"
                msg += format_movers("10 המניות שהכי ירדו היום", bottom, False)
                
                if volume_gainers or volume_losers:
                    msg += "\n\n"
                    msg += "📊 *ווליום חריג היום:*\n"
                    if volume_gainers:
                        msg += format_movers("עליות עם ווליום חריג", volume_gainers, True)
                    if volume_losers:
                        msg += format_movers("ירידות עם ווליום חריג", volume_losers, False)

                bot.send_message(chat_id=TARGET_CHAT_ID, text=msg, parse_mode="Markdown")
                print("Here we go, oren the King!")
            except Exception as e:
                print(f"שגיאה בשידור אוטומטי: {e}")
            time.sleep(2400)
        else:
            time.sleep(600)

threading.Thread(target=auto_broadcast, daemon=True).start()

print("Oren!You are the king!")
bot.infinity_polling()