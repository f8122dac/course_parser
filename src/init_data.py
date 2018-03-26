from bs4 import BeautifulSoup
import requests
import pickle
import re
import sys

DEPT = sys.argv[-1]

BASE_URL = "https://www.washington.edu/students/crscat/{}.html"
def fetch(dept):
    res = requests.get(BASE_URL.format(dept))
    if res.status_code is not 200:
        print('faild to fetch the {}'.format(url))
        exit(1) 

    soup = BeautifulSoup(res.content, "html5lib")
    data = soup.find_all("p")[2:]
    head = lambda x: x.find_all("b")[0].text
    desc = lambda x: x.find_all("a")[0].br.next
    return tuple( (str(head(d)).strip(), str(desc(d)).strip()) for d in data )

_title = re.compile('^[A-Z][A-Z ]{2,5} [0-9]{3}(.*)\(.*\).*')
get_title = lambda x: _title.search(x).groups()[0].strip()

_credit= re.compile('^[A-Z][A-Z ]{2,5} [0-9]{3}.*\((.*)\).*')
get_credit= lambda x: _credit.search(x).groups()[0].strip().replace('*','0')

_id    = re.compile('^[A-Z][A-Z ]{2,5} [0-9]{3}')
__id   = lambda x: x[:-4] + x[-3:]
get_id = lambda x: __id(_id.findall(x)[0].strip())

is_ugrad = lambda x: int(get_id(x[0])[-3]) < 5    # only undergrad courses

if __name__ == "__main__":
    data = fetch(DEPT)
    data = [{ 'id':get_id(d[0]), 
              'title': get_title(d[0]), 
              'credit': get_credit(d[0]), 
              'description': '' if len(d) is 1 else d[1]
            } for d in data if is_ugrad(d) ]
    pickle.dump(data, open('out/p/{}.p'.format(DEPT), 'wb'))


