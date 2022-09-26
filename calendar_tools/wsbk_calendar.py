import datetime
import requests
import sys
from bs4 import BeautifulSoup
#import web_pdb

import calendar_common as cc

host = 'https://www.worldsbk.com'
url = cc.check_url('/en/calendar', host)
sess_filter = ['Superpole', 'Superpole Race', 'Race', 'Race 1', 'Race 2']
sess_filter_on = True
classes = ['R3 bLU cRU Cup', 'WorldSSP300', 'WorldSSP', 'WorldSBK']
output_folder = '../wsbk/'


def has_data_time(tag):
    return tag.has_attr('data_ini') or tag.has_attr('data_end')


def main():

    # generate calendar names
    names = []
    for c in classes:
        names.append(c)
        names.append(c + '_filtered')

    cc.create_calendars(output_folder, names, '2022_calendar')

    r = requests.get(url)
    print(r.url)

    if r.status_code != 200:
        print('no connection')
        sys.exit()

    # parse calendar webpage
    page = BeautifulSoup(r.text, "html.parser")

    # extract events
    events = page.find_all('a', class_='track-link')

    print(f'Found {len(events)} events in the calendar.')
    for link in events or []:
        loc = link.find('h2').get_text().strip()
        print(f'Loading {loc}...')

        # get single event webpage
        lnk = cc.check_url(link['href'], host)
        r = requests.get(lnk)

        if r.status_code != 200:
            print(f'no connection for: {link["href"]}')
            continue

        # parse event webpage
        page = BeautifulSoup(r.text, "html.parser")

        # event name
        title = page.find('h2', class_='country-flag').get_text().strip()
        print(title)

        # circuit name / location
        circuit_info_page = page.find(id='destination-iframe')['src']
        # print(circuit_info_page)
        r = requests.get(circuit_info_page)
        if r.status_code != 200:
            print(f'no connection for: {link["href"]}')
            continue
        info_page = BeautifulSoup(r.text, "html.parser")

        circuit = info_page.find('h2', class_='c-widget__title--primary') or info_page.find('h2', class_='c-widget__title--secondary')

        if circuit:
            circuit = circuit.get_text().strip()
        else:
            circuit = ''

        # sessions
        sessions = page.find_all('div', class_='timeIso')
        print(f'Found {len(sessions)} sessions in the event.')
        # print(sessions)

        for session in sessions:
            # class / session
            cat = session.find('div', class_='cat-session')

            clas, sess = cat.get_text().strip().split('-')
            clas = clas.strip()
            sess = sess.replace('Video', '')
            sess = sess.replace('Live', '')
            sess = sess.replace('Timing', '')
            sess = sess.strip()
            if clas not in classes:
                continue
            print(f'{clas} {sess}')

            # Session start/end
            times = session.find_all(has_data_time)
            times = list(dict.fromkeys(times))
            # print(len(times))
            tm = {}
            for tim in times:
                for k in tim.attrs:
                    # 2021-11-18T10:00:00+0100
                    try:
                        dt = datetime.datetime.strptime(tim.attrs[k], '%Y-%m-%dT%H:%M:%S%z')
                        tm[k] = dt
                    except:
                        pass
                        # print(tim.attrs[k])
            e = cc.create_event(
                cc.enc_str(f'[{clas}] {sess}'),
                cc.enc_str(f'Event: {title}\nClass: {clas}\nSession: {sess}'),
                cc.enc_str(circuit),
                cc.check_url(link['href'], host),
                tm.get('data_ini'),
                tm.get('data_end'),
            )
            cc.add_if_new(clas, e)

            if sess in sess_filter:
                cc.add_if_new(f'{clas}_filtered', e)

        print('')

    cc.write_calendars(output_folder, '2022_calendar')


main()
