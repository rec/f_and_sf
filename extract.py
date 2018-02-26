#!/usr/bin/env python3

import calendar, csv

MONTHS = list(calendar.month_name)
FILENAME = '/Users/tom/Downloads/F&SF - Sheet1.csv'


def extract(filename=FILENAME):
    for d in csv.DictReader(open(filename)):
        yield {k.strip(): v.strip() for k, v in d.items()}


def runs(data, matches):
    runs, run = [], []

    for d in data:
        if matches(d):
            run.append(d)
        else:
            run and runs.append(run)
            run = []

    run and runs.append(run)

    for d in runs:
        yield d[0]['Date'], d[-1]['Date']


def run_ranges(matches, filename=FILENAME):
    data = extract(filename)
    # data = list(data)[8:15]
    for begin, end in runs(data, matches):
        if begin == end:
            print(begin)
        else:
            print(begin, '-', end)


def print_runs():
    print('    RUNS')
    print()
    run_ranges(lambda d: d['Present'])
    print()
    print()

    print('    GAPS')
    print()
    run_ranges(lambda d: not d['Present'])


def tables():
    result = {}
    for d in extract():
        present = not d['Present']
        month, year = d['Date'].split()
        month = MONTHS.index(month)
        result.setdefault(year, [[], []])[present].append(month)

    for year, (present, missing) in sorted(result.items()):
        if not present:
            print(year + ':', 'none')
        elif not missing:
            print(year + ':', 'ALL')
        else:
            print(year + ':', present, ' -- ', missing)


if __name__ == '__main__':
    tables()
