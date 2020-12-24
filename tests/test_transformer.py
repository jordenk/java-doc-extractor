from src.transformer import *
import pytest
import os


def test_trim_index_js_removes_left_and_right_characters():
    """The string 'Index.PACKAGES = ' should be removed from the left side of the index.js string."""
    actual = trim_index_js("""Index.PACKAGES = {"cats.data": {}};""")
    expected = """{"cats.data": {}}"""
    assert actual == expected


def test_trim_index_js_does_not_remove_inner_semicolons():
    """The trailing semicolon should be removed from the right side of the index.js string."""
    actual = trim_index_js("""Index.PACKAGES = {"cats.data": "here;"};""")
    expected = """{"cats.data": "here;"}"""
    assert actual == expected


def test_raises_a_critical_system_exit_when_multiple_index_packages_strings_are_present():
    """If the text 'Index.PACKAGES = ' appears anywhere beside the left side of the string, raise an error.
    This is extremely unlikely as the text would need to be part of a function description."""
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        trim_index_js("""Index.PACKAGES = {"cats.data": "Index.PACKAGES = valid"};""")
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_extract_enriched_function_blocks_builds_a_list_of_valid_output():
    test_scala_type = {
        'name': 'test_file_name',
        'shortDescription': 'description here',
        'kind': 'case class',
        'case class': 'link',
        'members_object': [
            {
                'label': 'test_label',
                'tail': 'test_tail',
                'member': 'test_member',
                'link': 'test_link',
                'kind': 'test_kind'
            },
            {
                'label': 'test_label2',
                'tail': 'test_tail2',
                'member': 'test_member2',
                'link': 'test_link2',
                'kind': 'test_kind2'
            }
        ]
    }
    actual = extract_enriched_function_blocks("test_package_name", test_scala_type)
    expected = [
        EnrichedFunctionBlock(package_name='test_package_name', file_name='test_file_name',
                              short_description='description here', kind='case class',
                              case_class_link='link', class_link=None, object_link=None, trait_link=None,
                              function_block=FunctionBlock(label='test_label', tail='test_tail', member='test_member',
                                                           link='test_link', kind='test_kind')),
        EnrichedFunctionBlock(package_name='test_package_name', file_name='test_file_name',
                              short_description='description here', kind='case class',
                              case_class_link='link', class_link=None, object_link=None, trait_link=None,
                              function_block=FunctionBlock(label='test_label2', tail='test_tail2',
                                                           member='test_member2',
                                                           link='test_link2', kind='test_kind2'))
    ]
    assert actual == expected


def test_extract_enriched_function_blocks_does_not_extract_functions_from_unrecognized_keys():
    test_scala_type = {
        'name': 'test_file_name',
        'shortDescription': 'description here',
        'kind': 'case class',
        'case class': 'link',
        'unrecognized_key': [
            {
                'label': 'test_label',
                'tail': 'test_tail',
                'member': 'test_member',
                'link': 'test_link',
                'kind': 'test_kind'
            }
        ]
    }
    actual = extract_enriched_function_blocks("test_package_name", test_scala_type)
    assert actual == []


def test_build_function_block_should_return_a_vaild_function_block_when_passed_valid_data():
    test_function_block = {
        'label': 'test_label',
        'tail': 'test_tail',
        'member': 'test_member',
        'link': 'test_link',
        'kind': 'test_kind'
    }
    actual = build_function_block(test_function_block)
    expected = FunctionBlock(label='test_label', tail='test_tail', member='test_member', link='test_link',
                             kind='test_kind')
    assert actual == expected


def test_build_function_block_should_return_none_when_required_keys_are_not_present():
    actual = build_function_block({})
    assert actual is None


def test_index_js_to_enriched_function_blocks():
    with open(os.path.join(os.path.dirname(__file__), "resources", "test_index.js")) as f:
        raw_index_js_string = f.read()
        actual = index_js_to_enriched_function_blocks(raw_index_js_string)

        expected = [
            EnrichedFunctionBlock(package_name='cats.instances', file_name='cats.instances.all', short_description='',
                                  kind='object', case_class_link=None, class_link=None,
                                  object_link='cats/instances/package$$all$.html', trait_link=None,
                                  function_block=FunctionBlock(label='catsStdNonEmptyParallelForSeqZipSeq',
                                                               tail='(): Aux[Seq, ZipSeq]',
                                                               member='cats.instances.SeqInstances.catsStdNonEmptyParallelForSeqZipSeq',
                                                               link='cats/instances/package$$all$.html#catsStdNonEmptyParallelForSeqZipSeq:cats.NonEmptyParallel.Aux[Seq,cats.data.ZipSeq]',
                                                               kind='implicit def')),
            EnrichedFunctionBlock(package_name='cats.instances', file_name='cats.instances.all', short_description='',
                                  kind='object', case_class_link=None, class_link=None,
                                  object_link='cats/instances/package$$all$.html', trait_link=None,
                                  function_block=FunctionBlock(label='catsStdShowForSeq',
                                                               tail='(arg0: Show[A]): Show[Seq[A]]',
                                                               member='cats.instances.SeqInstances.catsStdShowForSeq',
                                                               link='cats/instances/package$$all$.html#catsStdShowForSeq[A](implicitevidence$1:cats.Show[A]):cats.Show[Seq[A]]',
                                                               kind='implicit def')),
            EnrichedFunctionBlock(package_name='cats.data', file_name='cats.data.Binested',
                                  short_description='Compose a two-slot type constructor F[_, _] with two single-slot type constructors G[_] and H[_], resulting in a two-slot type constructor with respect to the inner types.',
                                  kind='case class', case_class_link='cats/data/Binested.html', class_link=None,
                                  object_link='cats/data/Binested$.html', trait_link=None,
                                  function_block=FunctionBlock(label='catsDataBitraverseForBinested',
                                                               tail='(F0: Bitraverse[F], H0: Traverse[H], G0: Traverse[G]): Bitraverse[[δ$4$, ε$5$]Binested[F, G, H, δ$4$, ε$5$]]',
                                                               member='cats.data.BinestedInstances.catsDataBitraverseForBinested',
                                                               link='cats/data/Binested$.html#catsDataBitraverseForBinested[F[_,_],G[_],H[_]](implicitF0:cats.Bitraverse[F],implicitH0:cats.Traverse[H],implicitG0:cats.Traverse[G]):cats.Bitraverse[[δ$4$,ε$5$]cats.data.Binested[F,G,H,δ$4$,ε$5$]]',
                                                               kind='implicit def')),
            EnrichedFunctionBlock(package_name='cats.data', file_name='cats.data.Binested',
                                  short_description='Compose a two-slot type constructor F[_, _] with two single-slot type constructors G[_] and H[_], resulting in a two-slot type constructor with respect to the inner types.',
                                  kind='case class', case_class_link='cats/data/Binested.html', class_link=None,
                                  object_link='cats/data/Binested$.html', trait_link=None,
                                  function_block=FunctionBlock(label='catsDataProfunctorForBinested',
                                                               tail='(F: Profunctor[F], G: Functor[G], H: Functor[H]): Profunctor[[δ$0$, ε$1$]Binested[F, G, H, δ$0$, ε$1$]]',
                                                               member='cats.data.BinestedInstances.catsDataProfunctorForBinested',
                                                               link='cats/data/Binested$.html#catsDataProfunctorForBinested[F[_,_],G[_],H[_]](implicitF:cats.arrow.Profunctor[F],implicitG:cats.Functor[G],implicitH:cats.Functor[H]):cats.arrow.Profunctor[[δ$0$,ε$1$]cats.data.Binested[F,G,H,δ$0$,ε$1$]]',
                                                               kind='implicit def')),
            EnrichedFunctionBlock(package_name='cats.data', file_name='cats.data.Binested',
                                  short_description='Compose a two-slot type constructor F[_, _] with two single-slot type constructors G[_] and H[_], resulting in a two-slot type constructor with respect to the inner types.',
                                  kind='case class', case_class_link='cats/data/Binested.html', class_link=None,
                                  object_link='cats/data/Binested$.html', trait_link=None,
                                  function_block=FunctionBlock(label='value', tail=': F[G[A], H[B]]',
                                                               member='cats.data.Binested.value',
                                                               link='cats/data/Binested.html#value:F[G[A],H[B]]',
                                                               kind='val')),
            EnrichedFunctionBlock(package_name='cats.data', file_name='cats.data.Binested',
                                  short_description='Compose a two-slot type constructor F[_, _] with two single-slot type constructors G[_] and H[_], resulting in a two-slot type constructor with respect to the inner types.',
                                  kind='case class', case_class_link='cats/data/Binested.html', class_link=None,
                                  object_link='cats/data/Binested$.html', trait_link=None,
                                  function_block=FunctionBlock(label='productElementNames', tail='(): Iterator[String]',
                                                               member='scala.Product.productElementNames',
                                                               link='cats/data/Binested.html#productElementNames:Iterator[String]',
                                                               kind='def'))]
        assert actual == expected


def test_encode_enriched_function_block_converts_to_string_json():
    test_efb = EnrichedFunctionBlock(package_name='cats.data', file_name='cats.data.Binested',
                                     short_description='Compose a two-slot type constructor F[_, _] with two single-slot type constructors G[_] and H[_], resulting in a two-slot type constructor with respect to the inner types.',
                                     kind='case class', case_class_link='cats/data/Binested.html', class_link=None,
                                     object_link='cats/data/Binested$.html', trait_link=None,
                                     function_block=FunctionBlock(label='productElementNames',
                                                                  tail='(): Iterator[String]',
                                                                  member='scala.Product.productElementNames',
                                                                  link='cats/data/Binested.html#productElementNames:Iterator[String]',
                                                                  kind='def'))
    actual = encode_enriched_function_block(test_efb)
    expected = """{"package_name":"cats.data","file_name":"cats.data.Binested","short_description":"Compose a two-slot type constructor F[_, _] with two single-slot type constructors G[_] and H[_], resulting in a two-slot type constructor with respect to the inner types.","kind":"case class","case_class_link":"cats/data/Binested.html","class_link":null,"object_link":"cats/data/Binested$.html","trait_link":null,"function_block":{"label":"productElementNames","tail":"(): Iterator[String]","member":"scala.Product.productElementNames","link":"cats/data/Binested.html#productElementNames:Iterator[String]","kind":"def"}}"""
    assert actual == expected
