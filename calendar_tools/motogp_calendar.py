import datetime
import requests
import sys
from bs4 import BeautifulSoup

import calendar_common as cc
#import web_pdb

url = 'https://www.motogp.com/en/calendar'
sess_filter = ['Q1', 'Q2', 'RAC']
sess_exclude = ['VIDEO', 'SHOW', 'PRESS']
classes = ['Moto3', 'Moto2', 'MotoGP', 'MotoE']
output_folder = '../motogp/'


def has_data_time(tag):
    return tag.has_attr('data-ini-time') or tag.has_attr('data-end')


def main():
    #web_pdb.set_trace()
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

    page = BeautifulSoup(r.text, "html.parser")

    events = page.find_all('a', class_='event_name')

    print(f'Found {len(events)} events in the calendar.')
    for link in events or []:
        # print(link['href'])
        loc = link.contents[0].strip()
        if 'Test' in loc:
            print(f'Skipping {loc}...')
            continue
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
            if sess in sess_exclude:
                print(f'{clas} {sess} {sess_full} skipped.')
                continue
            print(f'{clas} {sess} {sess_full}')
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

            e = cc.create_event(
                cc.enc_str(f'[{clas}] {sess}'),
                cc.enc_str(f'Event: {title}\nClass: {clas}\nSession: {sess_full}'),
                cc.enc_str(circuit),
                link['href'],
                tm.get('data-ini-time'),
                tm.get('data-end'),
            )
            cc.add_if_new(clas, e)

            if sess in sess_filter:
                cc.add_if_new(f'{clas}_filtered', e)

        #break
        print('')

    cc.write_calendars(output_folder, '2022_calendar')


main()
