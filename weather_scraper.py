import bs4
import requests
import datetime as dt
import codecs


def last_day_of_month(first):
    next_month = first.replace(day=28) + dt.timedelta(days=4)
    return next_month - dt.timedelta(days=next_month.day)


def weather_scraper(save_to_file: [bool] = False, fp: [str] = None):
    for this_year in range(2015, 2022):
        for this_month in range(1,13):
            last_day_dt = str(last_day_of_month(dt.date(this_year,this_month,1))).split("-")
            last_day = f"{last_day_dt[2]}.{last_day_dt[1]}.{last_day_dt[0]}"
            # CHANGE THE ID in the URL according to yout choice of weather station
            # id=23 - Berlin Tempelhof
            # id=19 - Berlin Alexanderplatz
            # id=G005 - Berlin Marzahn
            # id=20 - Berlin Dahlem                             ... here ...   ---⤵
            url = f"https://wetterkontor.de/de/wetter/deutschland/rueckblick.asp?id=23&" \
                  f"datum0=01.{this_month}.{this_year}&datum1={last_day}&jr=2022&mo=3&datum=04.03.2022&t=4&part=0"
            response = requests.get(url=url)
            response.raise_for_status()
            website = response.text  # read out the html code as text
            soup = bs4.BeautifulSoup(website, "html.parser")  # make soup
            td_s = soup.find_all(class_="uk-text-left")
            this_month = []
            for _ in range(0, len(td_s), 8):
                this_line = ""
                for i in range(8):
                    this_line += f"{td_s[_+i].text};"
                this_line = this_line[:-1]
                this_month.append(this_line)
            this_month.reverse()
            for _ in this_month:
                print(_)
            if save_to_file and fp:
                with codecs.open(fp, "a+", encoding="utf-8") as f:
                    for line in this_month:
                        f.write(f"{line}\n")


if __name__ == "__main__":
    weather_scraper(save_to_file=True, fp="./data/weather_data_tempelhof.csv")

