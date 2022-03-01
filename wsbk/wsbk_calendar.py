import ics
import datetime
import requests
import sys
from bs4 import BeautifulSoup

host = 'https://www.worldsbk.com'
url = host + '/en/calendar'
sess_filter = ['Superpole', 'Superpole Race', 'Race', 'Race 1', 'Race 2']
sess_filter_on = True
classes = ['WorldSSP300', 'WorldSSP', 'WorldSBK']
clas_filter = ['WorldSSP300', 'WorldSSP', 'WorldSBK']
clas_filter_on = True


def has_data_time(tag):
    return tag.has_attr('data_ini') or tag.has_attr('data_end')


def str_enc(string):
    for s in string.splitlines():
        yield s + '\n'
        # yield s.encode('utf-8').decode('cp1252') + '\n'


def main():
    cals = {}
    for c in classes:
        cals[c] = ics.Calendar()
        cals[f'{c}_filtered'] = ics.Calendar()

    r = requests.get(url)
    print(r.url)

    if r.status_code != 200:
        print('no connection')
        sys.exit()

    page = BeautifulSoup(r.text, "html.parser")

    events = page.find_all('a', class_='track-link')

    print(f'Found {len(events)} events in the calendar.')
    for link in events or []:
        loc = link.find('h2').get_text().strip()
        print(f'Loading {loc}...')
        lnk = host + link['href']
        r = requests.get(lnk)

        if r.status_code != 200:
            print(f'no connection for: {link["href"]}')
            continue

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
            clas, sess = session.get_text().strip().split('-')
            clas = clas.strip()
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

            e = ics.Event()
            e.summary = f'[{clas}] {sess}'
            e.description = f'Event: {title}\nClass: {clas}\nSession: {sess}'
            e.location = circuit
            e.url = lnk
            e.begin = tm.get('data_ini')
            e.end = tm.get('data_end')
            cals[clas].events.append(e)

            if sess in sess_filter:
                cals[f'{clas}_filtered'].events.append(e)

        # break
        print('')

    for c in cals:
        with open(f'{c}_2022_calendar.ics', 'w') as my_file:
            my_file.writelines(str_enc(cals[c].serialize()))


main()
