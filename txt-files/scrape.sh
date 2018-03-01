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
