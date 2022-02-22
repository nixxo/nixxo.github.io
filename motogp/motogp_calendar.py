import ics
import datetime
import requests
import sys
from bs4 import BeautifulSoup

url = 'https://www.motogp.com/en/calendar'
sess_filter = ['Q1', 'Q2', 'RAC']
sess_filter_on = True
classes = ['Moto3', 'Moto2', 'MotoGP']
clas_filter = ['Moto3', 'Moto2', 'MotoGP']
clas_filter_on = True


def has_data_time(tag):
    return tag.has_attr('data-ini-time') or tag.has_attr('data-end')


def str_enc(string):
    for s in string.splitlines():
        yield s.encode('utf-8').decode('cp1252') + '\n'


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

    events = page.find_all('a', class_='event_name')

    print(f'Found {len(events)} events in the calendar.')
    for link in events or []:
        # print(link['href'])
        loc = link.contents[0].strip()
        print(f'Loading {loc}...')
        r = requests.get(link['href'])

        if r.status_code != 200:
            print(f'no connection for: {link["href"]}')
            continue

        page = BeautifulSoup(r.text, "html.parser")

        # event name
        title = page.find(id='circuit_title').get_text().strip()
        print(title)

        # circuit name / location
        circuit_infos = page.find_all('div', class_='circuit_subtitle')
        circuit = ''
        for circuit_info in circuit_infos:
            circuit += f'{circuit_info.get_text().strip()} - '
        circuit = circuit.strip(' - ')
        #print(pickle.dumps(circuit))
        print(circuit)

        #sessions
        sessions = page.find_all('div', class_='c-schedule__table-row')
        print(f'Found {len(sessions)} sessions in the event.')
        #print(sessions)

        for session in sessions:
            # Category Name
            clas = session.find_all('div', class_='c-schedule__table-cell')
            clas = clas[1].get_text().strip()
            if clas not in classes:
                continue
            # Session Name
            sess_full = session.find('span', class_='hidden-xs')
            sess_full = sess_full.get_text().strip()
            sess = session.find('span', class_='visible-xs')
            sess = sess.get_text().strip()
            print(f'{clas} {sess}')
            # Session start/end
            times = session.find_all(has_data_time)
            times = list(dict.fromkeys(times))
            #print(len(times))
            tm = {}
            for tim in times:
                for k in tim.attrs:
                    # 2021-11-18T10:00:00+0100
                    try:
                        dt = datetime.datetime.strptime(tim.attrs[k], '%Y-%m-%dT%H:%M:%S%z')
                        tm[k] = dt
                    except:
                        print(tim.attrs[k])

            e = ics.Event()
            e.summary = f'[{clas}] {sess}'
            e.description = f'Event: {title}\nClass: {clas}\nSession: {sess_full}'
            e.location = circuit
            e.url = link['href']
            e.begin = tm.get('data-ini-time')
            e.end = tm.get('data-end')
            cals[clas].events.append(e)

            if sess in sess_filter:
                cals[f'{clas}_filtered'].events.append(e)

        # break
        print('')


    for c in cals:
        with open(f'{c}_2022_calendar.ics', 'w') as my_file:
            my_file.writelines(str_enc(cals[c].serialize()))


main()
