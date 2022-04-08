import ics
import datetime
import requests
import sys
from bs4 import BeautifulSoup
import web_pdb

url = 'https://www.motogp.com/en/calendar'
sess_filter = ['Q1', 'Q2', 'RAC']
sess_exclude = ['VIDEO', 'SHOW', 'PRESS']
classes = ['Moto3', 'Moto2', 'MotoGP', 'MotoE']
cals = {}
#clas_filter = ['Moto3', 'Moto2', 'MotoGP']
#clas_filter_on = True


def has_data_time(tag):
    return tag.has_attr('data-ini-time') or tag.has_attr('data-end')


def enc_str(s):
    return s.encode('utf-8').decode('cp1252')


def str_enc(string):
    for s in string.splitlines():
        #yield enc_str(s) + '\n'
        yield f'{s}\n'


#def load_ics(cals):
#    for c in cals:
#        f = open(f'{c}_2022_calendar.ics', 'r')
#        my_file.writelines(str_enc(cals[c].serialize()))

def add_if_new(clas, evt):
    found = False
    #web_pdb.set_trace()
    i = 0
    for e in cals[clas].events:
        if (e.summary == evt.summary
                and e.description == evt.description
                and e.location == e.location
                and e.begin == evt.begin
                and e.end == evt.end):
            found = True
            break
        if e.summary == evt.summary and e.location == evt.location:
            #web_pdb.set_trace()
            cals[clas].events[i].description = evt.description
            # clear end time to avoid errors
            cals[clas].events[i].end = None
            cals[clas].events[i].begin = evt.begin
            if evt.begin != evt.end:
                cals[clas].events[i].end = evt.end
            found = True
            print('UPDATED')
            break
        i = i + 1
    if not found:
        #web_pdb.set_trace()
        print('NEW EVENT')
        cals[clas].events.append(evt)


def main():
    #web_pdb.set_trace()
    for c in classes:
        try:
            f = open(f'{c}_2022_calendar.ics', 'r')
            cals[c] = ics.Calendar(f.read())
        except:
            cals[c] = ics.Calendar()
        finally:
            f.close()
        try:
            f = open(f'{c}_filtered_2022_calendar.ics', 'r')
            cals[f'{c}_filtered'] = ics.Calendar(f.read())
        except:
            cals[f'{c}_filtered'] = ics.Calendar()
        finally:
            f.close()

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
        # r = requests.get('https://www.motogp.com/en/event/Qatar')

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

            e = ics.Event()
            e.summary = enc_str(f'[{clas}] {sess}')
            e.description = enc_str(f'Event: {title}\nClass: {clas}\nSession: {sess_full}')
            e.location = enc_str(circuit)
            e.url = link['href']
            e.begin = tm.get('data-ini-time')
            e.end = tm.get('data-end')
            add_if_new(clas, e)
            #cals[clas].events.append(e)

            if sess in sess_filter:
                add_if_new(f'{clas}_filtered', e)
                #cals[f'{clas}_filtered'].events.append(e)

        #break
        print('')

    for c in cals:
        with open(f'{c}_2022_calendar.ics', 'w') as my_file:
            my_file.writelines(str_enc(cals[c].serialize()))


main()
