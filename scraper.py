import bs4
import requests
import re
import json
import google
import emoji

e_dict = emoji.EMOJI_UNICODE

# Degree symbol
deg = u'\N{DEGREE SIGN}'

# round & int
def r(n): return int(round(n))


def C2F(t): return int(round((t * 1.8) + 32))


def convert_temps(t_ls):
    for i in xrange(len(t_ls)):
        num = t_ls[i].replace(u'\xb0', '')
        t_ls[i] = t_ls[i].replace(num, str(C2F(int(num))))

    return t_ls


def convert_emoji(c):

    # Partly cloudy day
    c = c.replace('More Sun Than Clouds', e_dict[':sun_behind_small_cloud:'])
    c = c.replace('Sun Through High Clouds', e_dict[':sun_behind_small_cloud:'])
    c = c.replace('Periods of Clouds & Sun', e_dict[':sun_behind_small_cloud:'])
    c = c.replace('Clouds & Sun', e_dict[':sun_behind_small_cloud:'])
    c = c.replace('Sunny To Partly Cloudy', e_dict[':sun_behind_small_cloud:'])
    c = c.replace('Partly Cloudy', e_dict[':sun_behind_small_cloud:'])
    c = c.replace('Sunshine Mixing w/ Clouds', e_dict[':sun_behind_small_cloud:'])

    # Cloudy day
    c = c.replace('Considerable Cloudiness', e_dict[':sun_behind_cloud:'])
    c = c.replace('Partly Sunny', e_dict[':sun_behind_cloud:'])
    c = c.replace('Mostly Cloudy', e_dict[':cloud:'])
    c = c.replace('Cloudy', e_dict[':cloud:'])
    c = c.replace('Overcast', e_dict[':cloud:'])

    # Sunny day
    c = c.replace('Mostly Sunny', e_dict[':sun:'])
    c = c.replace('Brilliant Sunshine', e_dict[':sun:'])
    c = c.replace('Sunshine', e_dict[':sun:'])
    c = c.replace('Sunny', e_dict[':sun:'])

    # Rain
    c = c.replace('A Few Showers', e_dict[':cloud_with_rain:'])
    c = c.replace('Few Showers', e_dict[':cloud_with_rain:'])
    c = c.replace('A Shower', e_dict[':cloud_with_rain:'])
    c = c.replace('Light Rain', e_dict[':cloud_with_rain:'])
    c = c.replace('Rain', e_dict[':cloud_with_rain:'])

    # Snow
    c = c.replace('A Snow Shower', e_dict[':cloud_with_snow:'])
    c = c.replace('Snow Shower', e_dict[':cloud_with_snow:'])
    c = c.replace('Snow', e_dict[':snowflake:'])

    # Storms
    c = c.replace('T Storms', e_dict[':cloud_with_lightning_and_rain:'])
    c = c.replace('Thunderstorms', e_dict[':cloud_with_lightning_and_rain:'])
    c = c.replace('Thunderstorm', e_dict[':cloud_with_lightning_and_rain:'])
    c = c.replace('Thunder & Lightning', e_dict[':cloud_with_lightning_and_rain:'])
    c = c.replace('Lightning', e_dict[':cloud_with_lightning_and_rain:'])

    # Misc
    c = c.replace('Clouds', e_dict[':cloud:'])
    c = c.replace('Sun', e_dict[':sun:'])

    return c


def search_google(qry, dm = False):
    # Attempts to get data dictionary
    for j in google.search(qry, stop = 5):
        try:
            if 'wunderground' in qry:
                data = get_wunderground_data(j)
            elif 'accuweather' in qry:
                data = get_accuweather_data(j, dm = dm)
            return data
        except:
            continue
    return None


def get_wunderground_data(url):
    """
        Connects to wunderground site and
        parses desired weather data
        
        Returns a dictionary
    """

    site = requests.get(url)
    soup = bs4.BeautifulSoup(site.text, 'lxml')

    city = soup.head.title.text.split(' Forecast')[0]
    if '(' in city:
        city = city.split(' (')[0]

    pull = soup.findAll('script', text = lambda x: x and 'wui.asyncCityPage' in x)[0]
    txt = pull.text.replace('\t', '').replace('\n', '')

    data = json.loads('{' + re.findall('"current_observation".*}', txt)[0])['current_observation']
   # Finds weather conditions
    condition  = data['condition']
    condition += 'ing' if condition in ['Snow', 'Rain'] else ''
    temp       = str(r(data['temperature'])) + deg + 'F'
    feelslike  = str(r(data['feelslike'])) + deg + 'F'
    wind       = r(data['wind_speed'])

    ans = "Weather in " + city
    ans += ':\nCondition: ' + condition + '\nTemp: ' + temp + '\nFeels Like: ' + feelslike
    ans +=  '\nWind Speed: ' + str(wind) + ' mph'

    return ans 


def get_accuweather_data(url, dm = False):

    site = requests.get(url)

    soup = bs4.BeautifulSoup(site.text, 'lxml')

    city = soup.a.contents[0]

    data = [s for s in soup.findAll('ul') if 'Current Weather' in str(s) and '<ul>\n<li class' in str(s)][0]

    times = [d.text.replace('Current Weather', 'Currently') for d in data.findAll('a', text = lambda x: x and x != 'More' and '\n' not in x)]
    conditions = [s.text.title() for s in soup.findAll(attrs = {'class': 'cond'})]
    conditions = [c.replace('With', 'w/').replace('And', '&').replace('Of', 'of') for c in conditions]
    lbl = data.find(attrs = {'class': 'temp-label'}).text
    temps = [t.text for t in data.findAll(attrs = {'class': lambda x: x and (x == 'large-temp' or x == 'realfeel')})]
    temps[1::2] = [t[10:] for t in temps[1::2]]

    # Converts C to F for temps
    if lbl == 'C':
        temps = convert_temps(temps)

    # Adds F label to temps
    temps = [t + 'F' for t in temps]

    # Adds 'feels like' string to correct temps
    temps[1::2] = ['(feels ' + t + ')' for t in temps[1::2]]

    # Converts to emojis
    conditions = map(convert_emoji, conditions)

    # Creates tweet string
    ts = 0
    count = 0
    ans = city + '\n\n'

    spots = range(4)

    # Shorten tweet if not a DM
    if not dm:
        if 'Early AM' in times:
            spots.pop(times.index('Early AM'))
        elif 'Tonight' in times:
            spots.pop(times.index('Tonight'))
        else:
            spots = range(3)

    for j in spots:
        ans += '%s:\n%s %s\n\n' %(times[j], conditions[j], temps[ts])
        ts += 2

    ans = ans.strip('\n\n')

    return ans


def get_weather_now(inp, typ = 'accuweather', dm = False):

    # String to search
    if typ == 'wunderground':
        qry = 'wunderground ' + inp
    elif typ == 'accuweather':
        qry = 'accuweather ' + inp

    ans = search_google(qry, dm = dm)

    if ans:
        return ans
    else:
        return "I'm sorry. I couldn't find weather for that city."



