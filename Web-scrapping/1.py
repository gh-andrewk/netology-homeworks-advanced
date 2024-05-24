# определяем список хабов, которые нам интересны

import json
import requests
from fake_headers import Headers
from bs4 import BeautifulSoup



MARKS = ["django", "flask"]


def check_title(title):
    for i in MARKS:
        if i in title.lower():
            return True
    return False


ret = requests.get(
    url="https://hh.ru/search/vacancy?text=python&area=1&area=2",
    headers=Headers(browser="firefox", os="win").generate(),
)

soup = BeautifulSoup(ret.text, "html.parser")
vacancyes = soup.find_all("div", class_="vacancy-card--H8LvOiOGPll0jZvYpxIF font-inter")
RESULT_LIST = []
for vac in vacancyes:
    _name = None
    _href = None
    _money = None
    _comp = None
    _city = None

    title_span = vac.find("span", class_="serp-item__title-link-wrapper")
    if title_span is None:
        continue

    name = title_span.find(
        "span",
        class_="vacancy-name--SYbxrgpHgHedVTkgI_cA serp-item__title-link serp-item__title-link_redesign",
    )
    if name is None:
        continue
    name = name.text
    if not check_title(name):
        continue
    _name = name

    href = title_span.find("a", class_="bloko-link", href=True)
    href = href["href"] if href is not None else None
    _href = href

    money = vac.find("div", class_="compensation-labels--xC4zhiLojEYQtDuE4Qcf")
    if money is not None:
        m_text = money.find(
            "span",
            class_="compensation-text--cCPBXayRjn5GuLFWhGTJ fake-magritte-primary-text--qmdoVdtVX3UWtBb3Q7Qj separate-line-on-xs--pwAEUI79GJbGDu97czVC",
        )
        if m_text is not None:
            _money = m_text.text

    info = vac.find("div", class_="info-section--u_omJryeVsCvqQyS23m_")
    if info is not None:
        comp_span = info.find(
            "span", class_="separate-line-on-xs--pwAEUI79GJbGDu97czVC"
        )
        if comp_span is not None:
            c_name_span = comp_span.find(
                "span", class_="company-info-text--O32pGCRW0YDmp3BHuNOP"
            )
            _comp = c_name_span.text if c_name_span is not None else None

        addr_span = info.find(
            "div", class_="serp-item-control-gt-xs--AkKykYTSX24KOQAbGpkV"
        )
        if addr_span is not None:
            city = addr_span.find(
                "span", class_="fake-magritte-primary-text--qmdoVdtVX3UWtBb3Q7Qj"
            )
            _city = city.text if city is not None else None

    RESULT_LIST.append(
        {
            "Имя": _name,
            "Ссылка": _href,
            "Зарплата": _money,
            "Компания": _comp,
            "Город": _city,
        }
    )

print(json.dumps(RESULT_LIST, indent=4, ensure_ascii=False))
