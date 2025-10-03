from html.parser import HTMLParser
from typing import TypedDict

Attr_t = list[tuple[str, str | None]]


class Query_T(TypedDict):
    tag: str
    attr: Attr_t


def cmp(a: str, b: str):
    return a.lower() == b.lower()


def cmp_find(_in: str | None, _x: str | None):
    if not _x:
        return True
    if not _in:
        return False
    in_lis = [a.lower().strip() for a in _in.split(' ')]
    x_lis = [a.lower().strip() for a in _x.split(' ')]
    if x_lis == ['']:
        return True
    return all([a in in_lis for a in x_lis])


def cmp_attrs(_in: Attr_t, _x: Attr_t):
    if _in == _x:
        return True
    for name, value in _x:
        found = False
        for n2, v2 in _in:
            if cmp(name, n2):
                if not cmp_find(v2, value):
                    return False
                found = True
        if not found:
            return False
    return True


class TagParser(HTMLParser):
    searches: list[Query_T] = []
    matches: list[str] = []

    def handle_starttag(self, tag: str, attrs: Attr_t):
        for search in self.searches:
            if not cmp(tag, search['tag']):
                continue
            if not cmp_attrs(attrs, search['attr']):
                continue
            print('Match Found', tag, attrs)

    def handle_endtag(self, tag: str): ...

    def handle_data(self, data: str | None): ...


if __name__ == '__main__':
    parser = TagParser()
    parser.searches = [{'tag': 'div', 'attr': [('class', 'card v4 tight')]}]
    with open('test.html', 'r', encoding='utf-8') as fp:
        parser.feed(fp.read())
    print(parser.matches)
