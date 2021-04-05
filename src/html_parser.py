import bs4
import logging
import os
from dataclasses import dataclass
from typing import List, Iterator, Optional, Dict


@dataclass
class HtmlCommentBlock:
    link: str
    short_comment: Optional[str] = None
    full_comment: Optional[str] = None
    is_deprecated: bool = False
    deprecated_comment: Optional[str] = None


def collect_html_file_paths(path: str, acc: List[str]) -> List[str]:
    iter_items: Iterator[os.DirEntry] = os.scandir(path)
    for item in iter_items:
        if item.is_dir():
            collect_html_file_paths(item.path, acc)
        else:
            if item.name.endswith(".html"):
                acc.append(item.path)
    return acc


def extract_list_nodes(path: str) -> List[HtmlCommentBlock]:
    # 'cats/instances/package$$all$.html#catsStdNonEmptyParallelForSeqZipSeq:cats.NonEmptyParallel.Aux[Seq,cats.data.ZipSeq]
    with open(path) as f:
        soup = bs4.BeautifulSoup(markup=f, features='html.parser')
        template_nodes = soup.findAll(id='template')
        if len(template_nodes) != 1:
            # throw exception and log
            pass
        else:
            head: bs4.element.Tag = template_nodes[0]
            list_elements = head.find_all(name="li")
            return list(map(lambda li: node_to_flattened_function_comment_block(li), list_elements))


def node_to_flattened_function_comment_block(tag: bs4.element.Tag) -> HtmlCommentBlock:
    maybe_short_comment_tag = tag.find(attrs={'class': "shortcomment cmt"})
    maybe_short_comment = maybe_short_comment_tag.text if maybe_short_comment_tag else None

    maybe_full_comment_tag = tag.find(attrs={'class': "comment cmt"})
    maybe_full_comment = maybe_short_comment_tag.text if maybe_full_comment_tag else None

    maybe_deprecated_tag = tag.find(attrs={'class': "name deprecated"})
    deprecated_comment = maybe_deprecated_tag.attrs.get('title') if maybe_deprecated_tag else None
    if not deprecated_comment and "@deprecated" in tag.text:
        logging.warning(
            f"""Found @deprecated text in html, but record was not marked as deprecated. Inspect and update parser.
            Raw html: {tag}""")
    return HtmlCommentBlock(link=select_link(tag), short_comment=maybe_short_comment, full_comment=maybe_full_comment,
                            is_deprecated=bool(maybe_deprecated_tag), deprecated_comment=deprecated_comment)


def select_link(tag: bs4.element.Tag) -> str:
    function_id = tag.find(name="a", attrs={'class': "anchorToMember"})
    links = tag.find_all(name="a", href=True)
    for link in links:
        current = link.attrs.get('href')
        if function_id.text in current:
            return current.lstrip("../")
    # TODO throw exception or log
    return ""
