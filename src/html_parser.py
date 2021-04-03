from bs4 import BeautifulSoup
from typing import List, Iterator
import os


def parse(path: str):
    with open(path) as f:
        soup = BeautifulSoup(f, 'html.parser')
        return soup


def collect_html_file_paths(path: str, acc: List[str]) -> List[str]:
    iter_items: Iterator[os.DirEntry] = os.scandir(path)
    for item in iter_items:
        if item.is_dir():
            collect_html_file_paths(item.path, acc)
        else:
            if item.name.endswith(".html"):
                acc.append(item.path)
    return acc

# id div template
## div id allMembers
## inheritedMembers
## groupedMembers
### soup.prettify())
# print(out.prettify())

# html_file_paths = collect_html_files("/Users/jorden/Downloads/cats-core_2.13-2.4.2-javadoc/cats/arrow", [])
#
# for file in html_file_paths:
#     out = parse(file)
#     template_nodes = out.findAll(id='template')
#     if len(template_nodes) != 1:
#         # throw exception and log
#         pass
#     else:
#         a = template_nodes[0]
#         print(type(a))
#         print(a.attrs)
#         print(a.get_text())
#         break
