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
    match_found: bool = False
    match_content: str = ''
    match_depths: list[int] = []
    match_cntn_idx: list[int] = []
    tag_depth: int = 0

    def handle_starttag(self, tag: str, attrs: Attr_t):
        for search in self.searches:
            if not cmp(tag, search['tag']):
                continue
            if not cmp_attrs(attrs, search['attr']):
                continue
            self.match_depths.append(self.tag_depth)
            self.match_cntn_idx.append(len(self.match_content))
        if self.match_depths:
            attr_simple = ' '.join([f'{i}="{j}"' for i, j in attrs])
            self.match_content += f'<{tag} {attr_simple}>'
        self.tag_depth += 1

    def handle_endtag(self, tag: str):
        if self.match_depths:
            self.match_content += f'</{tag}>'

        if self.tag_depth < 0:
            return
        else:
            self.tag_depth -= 1

        if (
            self.tag_depth > -1
            and self.match_depths
            and self.tag_depth == self.match_depths[-1]
        ):
            self.match_depths.pop()
            frm = self.match_cntn_idx.pop()
            self.matches.append(self.match_content[frm:])

    def handle_data(self, data: str | None):
        if self.match_depths and data:
            self.match_content += data


if __name__ == '__main__':
    parser = TagParser()
    parser.searches = [{'tag': 'div', 'attr': [('class', 'card v4 tight')]}]
    # parser.searches = [{'tag': 'a', 'attr': [('data-media-type', 'person')]}]
    with open('test.html', 'r', encoding='utf-8') as fp:
        parser.feed(fp.read())
    print(len(parser.matches))
    # for match in parser.matches[:1]:
    #     print('-' * 10)
    #     print(match.replace('\n', '').replace('\t', ''))
    #     print('==' * 10, '\n\n')
