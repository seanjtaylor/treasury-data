# Daily Treasury Statements

Every business day the US Treasury Department publishes a report on the cash and debt operations of the United States Treasury.  What's neat (to me) about this is that it tells you how much revenue the government is taking in from income tax withholding.  There's likely a lot more cool stuff in this data so I wanted to make the scraper/parser public.

Special thanks to [Joel Wertheimer](https://twitter.com/wertwhile) for telling me about this data set.

[Here's an example statement](https://www.fms.treas.gov/fmsweb/viewDTSFiles?dir=a&fname=18010200.txt).

The section I'm interested in is Table IV, which looks like this:

```
___________________________________________________________________________________________
      TABLE IV  Federal Tax Deposits
 ___________________________________________________________________________________________
                                                                     This         Fiscal
                  Classification                       Today         month         year
                                                                    to date      to date
____________________________________________________________________________________________
 
 Withheld Income and Employment Taxes              $     46,295  $     46,295 $      662,789
 Individual Income Taxes                                    760           760         13,799
 Railroad Retirement Taxes                                   30            30          1,378
 Excise Taxes                                                51            51         21,222
 Corporation Income Taxes                                   195           195         79,410
 Federal Unemployment Taxes                                  11            11            781
 Estate and Gift Taxes & Misc IRS Rcpts.                      4             4            196
    Total                                          $     47,347  $     47,347 $      779,574
 Cash Federal Tax Deposits:
   Direct                                          $         25  $         25 $        7,383
   Through Depositaries                                  45,546        45,546        745,106
    Total Cash FTD's                               $     45,571  $     45,571 $      752,489
 Inter-agency Transfers                                   1,776         1,776         27,086
    Total                                          $     47,347  $     47,347 $      779,574
 ___________________________________________________________________________________________
```

## Scraping

See `txt-files/scrape.sh`.  It uses curl and just downloads every date it can.  The "archive" (which are before a certain date) DTSs are scraped separately because the URL is slightly different.  I have included by scraped files in this checkout.

```
d=2010-01-01
while [ "$d" != 2017-09-30 ]; do
    fn=$(gdate -d $d +%y%m%d)"00.txt";
    url="https://www.fms.treas.gov/fmsweb/viewDTSFiles?dir=a&fname="$fn;
    if [ ! -f "$fn" ]; then
	curl $url -o $fn;
	sleep 3;
    fi
d=$(gdate -I -d "$d + 1 day");
done
```

## Parsing

See `parse.py`.  It's a really simple line-based parser but works becuase the format is pretty consistent.

## Data

See `data/treasury_income.csv'.  The data are (mostly) tidy:

- ds: date of the statement
- mtd: month to date tally of the revenue
- rev: revenue on that day
- type: type of revenue (I map the descriptions to rough categories)
- ytd: (fiscal) year-to-date tally of the revenue

## EDA

See `EDA.ipynb`.  Not much there yet! Feel free to fork and have fun.
