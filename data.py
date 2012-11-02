import os
import csv

import dateutil.parser

import swiss as D
import swiss.tabular

cache = 'cache'
URL = 'http://www.w3schools.com/browsers/browsers_stats.asp'
retriever = D.Cache(cache)

class Parser:
    def __init__(self):
        self.browsers = []
        self.dates = []
        self.results = {}

    def execute(self):
        html = open(retriever.retrieve(URL, force=False))
        reader = swiss.tabular.HtmlReader()
        tdata = reader.read(html, table_index=4)
        # print [ t.data[0] for t in reader.tables ]
        self.parse(tdata)
        self.dump()

    def dump(self):
        tdata = swiss.tabular.TabularData()
        tdata.header = ['Date (Year-Month)'] + self.browsers
        self.dates.sort()
        for dd in self.dates:
            row = [dd] + [ self.results[b].get(dd, '') for b in self.browsers ]
            tdata.data.append(row)
        fileobj = file('data.csv', 'w')
        writer = swiss.tabular.CsvWriter()
        writer.write(tdata, fileobj)
        fileobj.close()

    def parse(self, tdata):
        self.browsers = set()
        values = {}
        for idx, row in enumerate(tdata.data):
            if idx == 0 or tdata.data[idx-1][0] == '':
                self.browsers.update(set(row[1:]))
        self.browsers = list(self.browsers)
        self.browsers.append('MS (All)')
        self.browsers.append('Opera (All)')
        self.browsers.append('Moz (All)')
        self.browsers.sort()
        for k in self.browsers:
            self.results[k] = {}
        section = []
        for row in tdata.data:
            if row[0] == '':
                self.parse_section(section)
                section = []
            else:
                section.append(row)
        self.parse_section(section)
        # add in extra
        for browser,date_dict in self.results.items():
            for dd,v in date_dict.items():
                if browser.startswith('IE'):
                    self.results['MS (All)'][dd] = \
                            self.results['MS (All)'].get(dd, 0) \
                            + v
                if browser.startswith('N') or browser in ['Fx', 'Firefox',
                        'Moz', 'Mozilla']:
                    self.results['Moz (All)'][dd] = \
                            self.results['Moz (All)'].get(dd, 0) \
                            + v
                if browser.startswith('O'):
                    self.results['Opera (All)'][dd] = \
                            self.results['Opera (All)'].get(dd, 0) \
                            + v


    def parse_section(self, section):
        year = int(section[0][0])
        for row in section[1:]:
            month = dateutil.parser.parse(row[0]).month
            date = '%d-%02d' % (year, month)
            self.dates.append(date)
            for idx, value in enumerate(row[1:]):
                browser = section[0][idx+1]
                v = value.replace('%', '')
                if v: v = float(v)
                else: v = 0.0
                self.results[browser][date] = v

def test_1():
    p = Parser()
    p.execute()
    assert len(p.browsers) == 20, len(p.browsers)
    ie7 = p.results['IE7']
    assert len(ie7) == 27, len(ie7)
    assert ie7['2008-01'] == 21.2, ie7['2008-01']
    aol = p.results['AOL']
    assert len(aol) == 6, len(aol)
    assert os.path.exists('data.csv')

import datetime
def plot():
    import pylab
    reader = swiss.tabular.CsvReader()
    tdata = reader.read(open('data.csv'))
    transposed = zip(*tdata.data)
    dates = transposed[0]
    transposed = D.floatify_matrix(transposed)
    dates = [ dateutil.parser.parse(d) for d in dates ]
    ms = transposed[tdata.header.index('MS (All)')]
    moz = transposed[tdata.header.index('Moz (All)')]
    fx = transposed[tdata.header.index('Fx')]
    pylab.plot_date(dates, ms, fmt='k-.', label='IE (All)')
    pylab.plot_date(dates, moz, fmt='b-', label='Moz (All)')
    pylab.plot_date(dates, fx, fmt='r--', label='Fx')
    ayear = datetime.timedelta(days=365)
    xmax = dates[-1] + ayear
    xmin = dates[0] - ayear
    pylab.xlim(xmax=xmax, xmin=xmin)
    pylab.ylim(ymax=100)
    pylab.ylabel('Market Share')
    pylab.xlabel('Date')
    pylab.legend()
    pylab.savefig('browser_stats_ms_moz.png')

import optparse
import sys
if __name__ == '__main__':
    usage = '''%prog {action}

    extract: extract the data into data.csv
    plot: plot local browser stats picture using matplotlib
        (requires extraction first)

You can run tests using nosetests.
'''
    parser = optparse.OptionParser(usage)
    options, args = parser.parse_args()
    if not args:
        parser.print_help()
        sys.exit(1)
    if args[0] == 'extract':
        p = Parser()
        p.execute()
    if args[0] == 'plot':
        plot()

