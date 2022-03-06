import bs4
import requests
import datetime as dt
import codecs


def vac_scraper(save_to_file: [bool] = False, fp: [str] = None):
    """visit website, scrape the hot 100 songs and artists and return it as df"""
    this_year = 2016
    vac_lst = []
    bank_hol = []
    for this_year in range(2015, 2022):
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
    if save_to_file and fp:
        with codecs.open(fp, "a+", encoding="utf-8") as f:
            f.write(f"{this_year}\n")
    return (vac_lst, bank_hol)


def save_dates(fp_hol: [str] = None, fp_ban: [str] = None):
    vac_lst1, bank_hol = vac_scraper()
    if fp_hol and fp_ban:
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
        with open(fp_hol, "w") as f:
            for _ in vac_lst:
                f.write(f"{_}\n")
        with open(fp_ban, "w") as f:
            for _ in bank_hol:
                f.write(f"{_}\n")


if __name__ == "__main__":
    vac_scraper(False, "./data/berlin.csv")
    save_dates("./data/school_vacation_days_berlin.txt", "./data/bank_holidays_berlin.txt")
    with open("./data/school_vacation_days_berlin.txt") as f:
        school_vac_lst = f.read().splitlines()
    with open("./data/bank_holidays_berlin.txt") as f:
        bank_holid_lst = f.read().splitlines()
    print(school_vac_lst)
    print(bank_holid_lst)
