import glob
import re
from datetime import date
import pandas as pd

number = re.compile('-?[0-9,]+(?!/)') ## can include negatives, the trailing / is used in footnotes

def main():
    rows = []
    for fn in glob.glob('txt-files/*.txt'):
        ds = filename_to_date(fn)
        with open(fn, encoding='latin-1') as f:
            lines = f.read().splitlines()
            if len(lines) == 1:
                continue
            rows.extend(parse_lines(lines, ds))
    return pd.DataFrame(rows)

fields = {
    'Withheld Income and Employment Taxes': 'income.withheld',
    'Individual Income Taxes': 'income',
    'Railroad Retirement Taxes': 'railroad',
    'Excise Taxes': 'excise',
    'Corporation Income Taxes': 'corporate',
    'Federal Unemployment Taxes': 'unemployment',
    'Estate and Gift Taxes': 'estate',
}

def filename_to_date(fn):
    st = number.search(fn).group(0)
    y = 2000 + int(st[:2])
    m = int(st[2:4])
    d = int(st[4:6])
    return date(y, m, d)

def parse_lines(lines, ds):
    result = []
    for line in lines:
        for key in fields:
            if line.lstrip().startswith(key):
                nums = parse_numbers(line)
                if len(nums) != 3:
                    print('Did not parse {} on {}'.format(ds, line))
                    continue
                result.append({
                    'ds': ds,
                    'type': fields[key],
                    'rev': nums[0],
                    'mtd': nums[1],
                    'ytd': nums[2],
                })
    return result

def parse_numbers(line):
    nums = number.findall(line)
    return [int(num.replace(',', '')) for num in nums]


if __name__ == '__main__':
    all_data = main()
    all_data.to_csv('data/treasury_income.csv', index=False)
