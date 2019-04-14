d=2019-02-28
while [ "$d" != 2019-04-13 ]; do
    fn=$(gdate -d $d +%y%m%d)"00.txt";
    url="https://www.fms.treas.gov/fmsweb/viewDTSFiles?dir=w&fname="$fn;
    if [ ! -f "$fn" ]; then
	curl $url -o $fn;
	sleep 3;
    fi
d=$(gdate -I -d "$d + 1 day");
done
