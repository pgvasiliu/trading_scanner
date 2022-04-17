##################################
######  UPGRADES/DOWNGRADES  #####
##################################
def get_analysts_upgrades_downgrades_marketwatch():

    from bs4 import BeautifulSoup
    import requests

    def add_data_to_dict(n_check, n_val, key, val, storage_dict):

        if n_val == n_check:
            storage_dict[key] = val.string

    url = "https://www.marketwatch.com/tools/upgrades-downgrades"
    raw_page = requests.get(url)
    soup = BeautifulSoup(raw_page.content, 'lxml')

    table = soup.find('table')
    raw_data_rows = table.find_all('tr')

    row_text_data = list()

    for tr in raw_data_rows[1:]:

        data = dict()
        for n, td in enumerate(tr):
            add_data_to_dict(1, n, "date", td.string, data)
            add_data_to_dict(3, n, "ticker", td.string, data)
            add_data_to_dict(5, n, "company", td.string, data)
            add_data_to_dict(7, n, "rating", td.string, data)
            add_data_to_dict(9, n, "analyst", td.string, data)

        row_text_data.append(data)

    return row_text_data

