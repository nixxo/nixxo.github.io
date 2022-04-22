import ics
import web_pdb
import os

cals = {}
ext = '.ics'
cwd = os.path.dirname(os.path.realpath(__file__))


def str_enc(string):
    for s in string.splitlines():
        yield f'{s}\n'


def enc_str(s):
    try:
        s = s.encode('utf-8').decode('cp1252')
    except:
        s = s
    return s


def check_url(url, host):
    if url.startswith('http'):
        return url
    if host.endswith('/'):
        host = host.rstrip('/')
    if url.startswith('/'):
        url = url.lstrip('/')
    return f'{host}/{url}'


def create_calendars(output_folder, names, appendix=None):
    #web_pdb.set_trace()
    if appendix:
        appendix = '_' + appendix
    if not output_folder.endswith('/'):
        output_folder = output_folder + '/'

    for name in names:
        try:
            fn = os.path.realpath(os.path.join(cwd, output_folder, f'{name}{appendix}{ext}'))
            f = open(fn, 'r')
            cals[name] = ics.Calendar(f.read())
            f.close()
        except:
            cals[name] = ics.Calendar()


def write_calendars(output_folder, appendix=None):
    if appendix:
        appendix = '_' + appendix
    for cal in cals:
        fn = os.path.realpath(os.path.join(cwd, output_folder, f'{cal}{appendix}{ext}'))
        with open(fn, 'w') as my_file:
            my_file.writelines(str_enc(cals[cal].serialize()))


def create_event(summary, description, location, url, begin, end):
    e = ics.Event()
    e.summary = summary
    e.description = description
    e.location = location
    e.url = url
    e.begin = begin
    e.end = end
    return e


def add_if_new(clas, evt):
    found = False
    #web_pdb.set_trace()
    i = 0
    for e in cals[clas].events:
        if (e.summary == evt.summary
                and e.description == evt.description
                and e.location == e.location
                and e.begin == evt.begin
                and e.end == evt.end
                and e.url == evt.url):
            found = True
            break
        if e.summary == evt.summary and e.location == evt.location:
            #web_pdb.set_trace()
            cals[clas].events[i].description = evt.description
            cals[clas].events[i].url = evt.url
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