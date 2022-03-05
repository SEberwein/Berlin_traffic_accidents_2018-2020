import bs4
import requests
import datetime as dt
import codecs


def vac_scraper(save_to_file: [bool] = False, fp: [str] = None):
    """visit website, scrape the hot 100 songs and artists and return it as df"""
    this_year = 2016
    vac_lst = []
    bank_hol = []
    for this_year in range(2016, 2022):
        url = f"https://www.ferienkalender.com/ferien_deutschland/Berlin/{this_year}-ferien-berlin.htm"
        response = requests.get(url=url)
        response.raise_for_status()
        website = response.text  # read out the html code as text
        soup = bs4.BeautifulSoup(website, "html.parser")  # make soup
        td_s = soup.find_all("td")
        for _ in range(4, len(td_s) - 2):
            if _ % 2 != 0:
                if td_s[_].text[0].isdigit():
                    if "-" in td_s[_].text:
                        st = td_s[_].text.split(" - ")[0].split(".")
                        en = td_s[_].text.split(" - ")[1].split(".")
                        vac_lst.append((f"{this_year}_{st[1]}_{st[0]}", f"{this_year}_{en[1]}_{en[0]}"))
                    else:
                        for s in td_s[_].text.split("/"):
                            vac_lst.append((f"{this_year}_{s.split('.')[1]}_{s.split('.')[0]}",))
                else:
                    bank_hol.append(
                        dt.datetime.strftime(dt.datetime.strptime(td_s[_].text.split(" ")[1], "%d.%m.%Y"), "%Y_%m_%d"))
    print(vac_lst)
    print(bank_hol)

    if save_to_file:
        with codecs.open(fp, "a+", encoding="utf-8") as f:
            f.write(f"{this_year}\n")


def daterange(date1, date2):
    for n in range(int((date2 - date1).days) + 1):
        yield date1 + dt.timedelta(n)


if __name__ == "__main__":
    # vac_scraper(False, "./data/berlin.csv")
    vac_lst1 = [('2016_02_01', '2016_02_06'), ('2016_03_21', '2016_04_02'), ('2016_05_06',), ('2016_05_17',),
                ('2016_05_18',),
                ('2016_07_21', '2016_09_02'), ('2016_10_17', '2016_10_28'), ('2016_12_23', '2016_01_03'),
                ('2017_01_30', '2017_02_03'), ('2017_04_10', '2017_04_18'), ('2017_05_24', '2017_06_09'),
                ('2017_07_20', '2017_09_01'), ('2017_10_02', '2017_11_04'), ('2017_12_21', '2017_01_02'),
                ('2018_02_05', '2018_02_10'), ('2018_03_26', '2018_04_06'), ('2018_04_30',), ('2018_05_11',),
                ('2018_05_22',),
                ('2018_07_05', '2018_08_17'), ('2018_10_22', '2018_11_02'), ('2018_12_22', '2018_01_05'),
                ('2019_02_04', '2019_02_09'), ('2019_04_15', '2019_04_26'), ('2019_05_31',), ('2019_06_11',),
                ('2019_06_20', '2019_08_02'), ('2019_10_04', '2019_10_19'), ('2019_12_23', '2019_01_04'),
                ('2020_02_03', '2020_02_08'), ('2020_04_06', '2020_04_17'), ('2020_05_08',), ('2020_05_22',),
                ('2020_06_25', '2020_08_07'), ('2020_10_12', '2020_10_24'), ('2020_12_21', '2020_01_02'),
                ('2021_02_01', '2021_02_06'), ('2021_03_29', '2021_04_10'), ('2021_05_14',),
                ('2021_06_24', '2021_08_06'),
                ('2021_10_11', '2021_10_23'), ('2021_12_23', '2021_12_31')]
    bank_hol = ['2016_01_01', '2016_03_25', '2016_03_28', '2016_05_01', '2016_05_05', '2016_05_16', '2016_10_03',
                '2016_12_25',
                '2016_12_26', '2017_01_01', '2017_04_14', '2017_04_17', '2017_05_01', '2017_05_25', '2017_06_05',
                '2017_10_03',
                '2017_10_31', '2017_12_25', '2017_12_26', '2018_01_01', '2018_03_30', '2018_04_02', '2018_05_01',
                '2018_05_10',
                '2018_05_21', '2018_10_03', '2018_12_25', '2018_12_26', '2019_01_01', '2019_03_08', '2019_04_19',
                '2019_04_22',
                '2019_05_01', '2019_05_30', '2019_06_10', '2019_10_03', '2019_12_25', '2019_12_26', '2020_01_01',
                '2020_03_08',
                '2020_04_10', '2020_04_13', '2020_05_01', '2020_05_08', '2020_05_21', '2020_06_01', '2020_10_03',
                '2020_12_25',
                '2020_12_26', '2021_01_01', '2021_03_08', '2021_04_02', '2021_04_05', '2021_05_01', '2021_05_13',
                '2021_05_24',
                '2021_10_03', '2021_12_25', '2021_12_26']

    # for v in vac_lst:
    # from datetime import timedelta, date
    vac_lst = []
    for _ in range(len(vac_lst1)):
        if len(vac_lst1[_]) == 2:
            start_dt = dt.datetime.strptime(vac_lst1[_][0], "%Y_%m_%d")
            end_dt = dt.datetime.strptime(vac_lst1[_][1], "%Y_%m_%d")
            delta = end_dt - start_dt  # returns timedelta
            for d in range(delta.days + 1):
                day = start_dt + dt.timedelta(days=d)
                vac_lst.append(dt.datetime.strftime(day, "%Y_%m_%d"))
        else:
            vac_lst.append(vac_lst1[_][0])
    with open("./data/school_vacation_days_berlin.txt", "w") as f:
        for _ in vac_lst:
            f.write(f"{_}\n")
    with open("./data/bank_holidays_berlin.txt", "w") as f:
        for _ in bank_hol:
            f.write(f"{_}\n")

