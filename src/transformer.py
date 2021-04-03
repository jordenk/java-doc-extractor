"""
The transformer reads the index.js file in a java doc folder and transform it into json representing Scala functions.
Minimal keys are renamed, and no json values are altered. The transformer goal is to standardize the output without
mutating values.
"""

import sys
import json
from typing import Dict, List
from dataclasses import dataclass, asdict

FUNCTION_BLOCK_KEYS = {'members_object', 'members_trait', 'members_class', 'members_case class'}


@dataclass
class FunctionBlock:
    """
    Represents a Scala function located in a JSON value list. The known JSON keys containing functions are:
    'members_object', 'members_trait', 'members_class', 'members_case class'
    """
    label: str
    tail: str
    member: str
    link: str
    kind: str


@dataclass
class EnrichedFunctionBlock:
    """
    Represents a function with the associated Scala Type (Class, Case Class, Object, Trait) that contains the function.
    This is a denormalized view of the data to make downstream indexing easier. This dataclass will be sparse with
    regard to the the _link fields.
    """
    # TODO use this to join
    package_name: str
    # TODO Need to use this to join
    file_name: str
    short_description: str
    kind: str
    case_class_link: str
    class_link: str
    object_link: str
    trait_link: str
    function_block: FunctionBlock


def trim_index_js(raw_index_js: str) -> str:
    """
    Helper function to convert an index.js string into parsable JSON.
    """
    stripped = raw_index_js.strip()
    arr = stripped.split("Index.PACKAGES = ")
    if len(arr) > 2:
        # TODO log
        # Kill the process if more than one index packages string is found. This is unexpected
        # and can be handled if needed in the future.
        print("Found 'Index.PACKAGES = ' string in index.js body.")
        sys.exit(1)
    prefix_removed = "".join(arr)
    return prefix_removed.rstrip(";")


def index_js_to_enriched_function_blocks(index_js: str) -> List[EnrichedFunctionBlock]:
    """
    Main function of the file. Converts raw index.js file into the output dataclass.
    """
    trimmed_index_js = trim_index_js(index_js)
    index_json = json.loads(trimmed_index_js)

    rtn_blocks = []
    for package_name, list_of_scala_types in index_json.items():
        for scala_type in list_of_scala_types:
            enriched_blocks = extract_enriched_function_blocks(package_name, scala_type)
            rtn_blocks.extend(enriched_blocks)
    return rtn_blocks


def extract_enriched_function_blocks(package_name: str, scala_type: Dict) -> List[EnrichedFunctionBlock]:
    """
    Iterates through nested function blocks. Produces function blocks enriched with data from the parent block.
    """
    rtn_blocks = []
    for k, v in scala_type.items():
        if type(v) is list:
            if k in FUNCTION_BLOCK_KEYS:
                fbst = _enrich_function_blocks(package_name, scala_type, v)
                rtn_blocks.extend(fbst)
            else:
                # TODO log, maybe error
                print(f"error may be missing functions in block {k}")
    return rtn_blocks


def _enrich_function_blocks(package_name: str, meta_data: Dict, fn_blocks: List[Dict]) -> List[EnrichedFunctionBlock]:
    """
    Helper function. Build an enriched function block.
    """
    kind = meta_data.get('kind')

    if kind not in {"case class", "class", "object", "trait"}:
        # TODO log, maybe error
        print(f"Unexpected Scala Type found. Kind: {kind}")

    for fb in fn_blocks:
        _function_block = build_function_block(fb)
        if _function_block:
            yield EnrichedFunctionBlock(
                package_name=package_name,
                file_name=meta_data.get('name'),
                short_description=meta_data.get('shortDescription'),
                kind=kind,
                case_class_link=meta_data.get('case class'),
                class_link=meta_data.get('class'),
                object_link=meta_data.get('object'),
                trait_link=meta_data.get('trait'),
                function_block=_function_block
            )


def build_function_block(block: Dict) -> FunctionBlock:
    """
    Helper function. Build a function block.
    """
    if set(block.keys()) == set(FunctionBlock.__annotations__.keys()):
        return FunctionBlock(
            label=block.get('label'),
            tail=block.get('tail'),
            member=block.get('member'),
            link=block.get('link'),
            kind=block.get('kind')
        )
    else:
        # ErrorBlocks unhandled- not needed right now. These contain keys ('member', 'error'). There
        # may be other blocks to handle in the future, but the bulk of the blocks are function blocks.
        pass


def encode_enriched_function_block(efb: EnrichedFunctionBlock) -> str:
    """
    Encodes an EnrichedFunctionBlock as a JSON string.
    """
    return json.dumps(asdict(efb), separators=(',', ':'))
