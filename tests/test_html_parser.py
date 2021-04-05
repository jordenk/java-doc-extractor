import bs4

from src.html_parser import *

test_dir_path = os.path.join(os.path.dirname(__file__))


def test_collect_html_file_paths():
    test_data_path = os.path.join(test_dir_path, "resources", "html_parser_test_data", "nested_file_structure_data")

    actual = collect_html_file_paths(test_data_path, [])
    expected = {
        os.path.join(test_data_path, "test_top_b.html"),
        os.path.join(test_data_path, "test_top_c.html"),
        os.path.join(test_data_path, "nested_2a", "nested_3b", "test_2a_3b_a.html"),
        os.path.join(test_data_path, "nested_2a", "test_2a_a.html"),
        os.path.join(test_data_path, "nested_2a", "nested_3a", "test_2a_3a_a.html"),
        os.path.join(test_data_path, "nested_2b", "test_2b_a.html"),
        os.path.join(test_data_path, "test_top_a.html")
    }
    assert set(actual) == expected


def test_select_link():
    s = """
        <li class="indented0 " name="scala.AnyRef#ne" group="Ungrouped" fullComment="yes" data-isabs="false" visbl="pub"><a
                id="ne(x$1:AnyRef):Boolean" class="anchorToMember"></a><a id="ne(AnyRef):Boolean" class="anchorToMember"></a>
            <span class="permalink"><a href="../cats/Bifunctor.html#ne(x$1:AnyRef):Boolean" title="Permalink"><i
                        class="material-icons"></i></a></span> <span class="modifier_kind"><span class="modifier">final </span>
                <span class="kind">def</span></span> <span class="symbol"><span class="name">ne</span><span
                    class="params">(<span name="arg0">arg0: <a
                            href="https://www.scala-lang.org/api/2.13.4/scala/AnyRef.html#scala.AnyRef" name="scala.AnyRef"
                            id="scala.AnyRef" class="extype">AnyRef</a></span>)</span><span class="result">: <a
                        href="https://www.scala-lang.org/api/2.13.4/scala/Boolean.html#scala.Boolean" name="scala.Boolean"
                        id="scala.Boolean" class="extype">Boolean</a></span></span>
            <div class="fullcomment">
                <dl class="attributes block">
                    <dt>Definition Classes</dt>
                    <dd>AnyRef</dd>
                </dl>
            </div>
        </li>
    """
    li_tag = bs4.BeautifulSoup(markup=s, features='html.parser').find(name='li')
    assert select_link(li_tag) == "cats/Bifunctor.html#ne(x$1:AnyRef):Boolean"


def test_node_to_flattened_function_comment_block_with_comments():
    s = """
        <li class="indented0 " name="cats.Bifunctor#leftWiden" group="Ungrouped" fullComment="yes" data-isabs="false"
            visbl="pub"><a id="leftWiden[A,B,AA&gt;:A](fab:F[A,B]):F[AA,B]" class="anchorToMember"></a><a
                id="leftWiden[A,B,AA&gt;:A](F[A,B]):F[AA,B]" class="anchorToMember"></a> <span class="permalink"><a
                    href="../cats/Bifunctor.html#leftWiden[A,B,AA&gt;:A](fab:F[A,B]):F[AA,B]" title="Permalink"><i
                        class="material-icons"></i></a></span> <span class="modifier_kind"><span class="modifier"></span> <span
                    class="kind">def</span></span> <span class="symbol"><span class="name">leftWiden</span><span
                    class="tparams">[<span name="A">A</span>, <span name="B">B</span>, <span name="AA">AA &gt;: <span
                            name="cats.Bifunctor.leftWiden.A" class="extype">A</span></span>]</span><span class="params">(<span
                        name="fab">fab: <span name="cats.Bifunctor.F" class="extype">F</span>[<span
                            name="cats.Bifunctor.leftWiden.A" class="extype">A</span>, <span name="cats.Bifunctor.leftWiden.B"
                            class="extype">B</span>]</span>)</span><span class="result">: <span name="cats.Bifunctor.F"
                        class="extype">F</span>[<span name="cats.Bifunctor.leftWiden.AA" class="extype">AA</span>,
                    <span name="cats.Bifunctor.leftWiden.B" class="extype">B</span>]</span></span>
            <p class="shortcomment cmt">Widens A into a supertype AA.</p>
            <div class="fullcomment">
                <div class="comment cmt">
                    <p>Widens A into a supertype AA.
                        Example:</p>
                    <pre>scala&gt; <span class="kw">import</span> cats.implicits._
        scala&gt; <span class="kw">sealed</span> <span class="kw">trait</span> Foo
        scala&gt; <span class="kw">case</span> <span class="kw">object</span> Bar <span class="kw">extends</span> Foo
        scala&gt; <span class="kw">val</span> x1: Either[Bar.<span class="kw">type</span>, <span class="std">Int</span>] = Either.left(Bar)
        scala&gt; <span class="kw">val</span> x2: Either[Foo, <span class="std">Int</span>] = x1.leftWiden</pre>
                </div>
            </div>
        </li>
    """
    li_tag = bs4.BeautifulSoup(markup=s, features='html.parser').find(name='li')
    actual = node_to_flattened_function_comment_block(li_tag)
    expected = HtmlCommentBlock(link='cats/Bifunctor.html#leftWiden[A,B,AA>:A](fab:F[A,B]):F[AA,B]',
                                short_comment='Widens A into a supertype AA.',
                                full_comment='Widens A into a supertype AA.', is_deprecated=False,
                                deprecated_comment=None)
    assert actual == expected


def test_node_to_flattened_function_comment_block_with_deprecated_function():
    s = """
        <li class="indented0 " name="cats.Bifunctor#catsBifunctorForTuple2" group="Ungrouped" fullComment="yes"
            data-isabs="false" visbl="pub"><a id="catsBifunctorForTuple2:cats.Bifunctor[Tuple2]" class="anchorToMember"></a><a
                id="catsBifunctorForTuple2:Bifunctor[Tuple2]" class="anchorToMember"></a> <span class="permalink"><a
                    href="../cats/Bifunctor$.html#catsBifunctorForTuple2:cats.Bifunctor[Tuple2]" title="Permalink"><i
                        class="material-icons"></i></a></span> <span class="modifier_kind"><span class="modifier"></span> <span
                    class="kind">def</span></span> <span class="symbol"><span class="name deprecated"
                    title="Deprecated: (Since version 2.4.0) Use catsStdBitraverseForTuple2 in cats.instances.NTupleBitraverseInstances">catsBifunctorForTuple2</span><span
                    class="result">: <a href="Bifunctor.html" name="cats.Bifunctor" id="cats.Bifunctor"
                        class="extype">Bifunctor</a>[<a
                        href="https://www.scala-lang.org/api/2.13.4/scala/Tuple2.html#scala.Tuple2" name="scala.Tuple2"
                        id="scala.Tuple2" class="extype">Tuple2</a>]</span></span>
            <div class="fullcomment">
                <dl class="attributes block">
                    <dt>Annotations</dt>
                    <dd><span class="name">@deprecated</span> </dd>
                    <dt>Deprecated</dt>
                    <dd class="cmt">
                        <p><i>(Since version 2.4.0)</i> Use catsStdBitraverseForTuple2 in
                            cats.instances.NTupleBitraverseInstances</p>
                    </dd>
                </dl>
            </div>
        </li>
    """
    li_tag = bs4.BeautifulSoup(markup=s, features='html.parser').find(name='li')
    actual = node_to_flattened_function_comment_block(li_tag)
    expected = HtmlCommentBlock(link='cats/Bifunctor$.html#catsBifunctorForTuple2:cats.Bifunctor[Tuple2]',
                                short_comment=None, full_comment=None, is_deprecated=True,
                                deprecated_comment='Deprecated: (Since version 2.4.0) Use catsStdBitraverseForTuple2 in cats.instances.NTupleBitraverseInstances')
    assert actual == expected


def test_extract_list_nodes():
    test_data_path = os.path.join(test_dir_path, "resources", "html_parser_test_data", "test_bifunctor.html")
    actual = extract_list_nodes(test_data_path)
    expected = [
        HtmlCommentBlock(link='cats/Bifunctor.html#bimap[A,B,C,D](fab:F[A,B])(f:A=>C,g:B=>D):F[C,D]',
                         short_comment='The quintessential method of the Bifunctor trait, it applies a\nfunction to each "side" of the bifunctor.',
                         full_comment='The quintessential method of the Bifunctor trait, it applies a\nfunction to each "side" of the bifunctor.',
                         is_deprecated=False, deprecated_comment=None),
        HtmlCommentBlock(link='cats/Bifunctor.html#!=(x$1:Any):Boolean', short_comment=None, full_comment=None,
                         is_deprecated=False, deprecated_comment=None),
        HtmlCommentBlock(link='cats/Bifunctor.html###:Int', short_comment=None, full_comment=None, is_deprecated=False,
                         deprecated_comment=None),
        HtmlCommentBlock(link='cats/Bifunctor.html#==(x$1:Any):Boolean', short_comment=None, full_comment=None,
                         is_deprecated=False, deprecated_comment=None),
        HtmlCommentBlock(link='cats/Bifunctor.html#asInstanceOf[T0]:T0', short_comment=None, full_comment=None,
                         is_deprecated=False, deprecated_comment=None),
        HtmlCommentBlock(link='cats/Bifunctor.html#clone():Object', short_comment=None, full_comment=None,
                         is_deprecated=False, deprecated_comment=None),
        HtmlCommentBlock(
            link='cats/Bifunctor.html#compose[G[_,_]](implicitG0:cats.Bifunctor[G]):cats.Bifunctor[[α,β]F[G[α,β],G[α,β]]]',
            short_comment='The composition of two Bifunctors is itself a Bifunctor\n', full_comment=None,
            is_deprecated=False, deprecated_comment=None),
        HtmlCommentBlock(link='cats/Bifunctor.html#eq(x$1:AnyRef):Boolean', short_comment=None, full_comment=None,
                         is_deprecated=False, deprecated_comment=None),
        HtmlCommentBlock(link='cats/Bifunctor.html#equals(x$1:Object):Boolean', short_comment=None, full_comment=None,
                         is_deprecated=False, deprecated_comment=None),
        HtmlCommentBlock(link='cats/Bifunctor.html#finalize():Unit', short_comment=None, full_comment=None,
                         is_deprecated=False, deprecated_comment=None),
        HtmlCommentBlock(link='cats/Bifunctor.html#getClass():Class[_]', short_comment=None, full_comment=None,
                         is_deprecated=False, deprecated_comment=None),
        HtmlCommentBlock(link='cats/Bifunctor.html#hashCode():Int', short_comment=None, full_comment=None,
                         is_deprecated=False, deprecated_comment=None),
        HtmlCommentBlock(link='cats/Bifunctor.html#isInstanceOf[T0]:Boolean', short_comment=None, full_comment=None,
                         is_deprecated=False, deprecated_comment=None),
        HtmlCommentBlock(link='cats/Bifunctor.html#leftFunctor[X]:cats.Functor[[α$1$]F[α$1$,X]]', short_comment=None,
                         full_comment=None, is_deprecated=False, deprecated_comment=None),
        HtmlCommentBlock(link='cats/Bifunctor.html#leftMap[A,B,C](fab:F[A,B])(f:A=>C):F[C,B]',
                         short_comment='apply a function to the "left" functor\n', full_comment=None,
                         is_deprecated=False,
                         deprecated_comment=None),
        HtmlCommentBlock(link='cats/Bifunctor.html#leftWiden[A,B,AA>:A](fab:F[A,B]):F[AA,B]',
                         short_comment='Widens A into a supertype AA.', full_comment='Widens A into a supertype AA.',
                         is_deprecated=False, deprecated_comment=None),
        HtmlCommentBlock(link='cats/Bifunctor.html#ne(x$1:AnyRef):Boolean', short_comment=None, full_comment=None,
                         is_deprecated=False, deprecated_comment=None),
        HtmlCommentBlock(link='cats/Bifunctor.html#notify():Unit', short_comment=None, full_comment=None,
                         is_deprecated=False, deprecated_comment=None),
        HtmlCommentBlock(link='cats/Bifunctor.html#notifyAll():Unit', short_comment=None, full_comment=None,
                         is_deprecated=False, deprecated_comment=None),
        HtmlCommentBlock(link='cats/Bifunctor.html#rightFunctor[X]:cats.Functor[[β$0$]F[X,β$0$]]', short_comment=None,
                         full_comment=None, is_deprecated=False, deprecated_comment=None),
        HtmlCommentBlock(link='cats/Bifunctor.html#synchronized[T0](x$1:=>T0):T0', short_comment=None,
                         full_comment=None,
                         is_deprecated=False, deprecated_comment=None),
        HtmlCommentBlock(link='cats/Bifunctor.html#toString():String', short_comment=None, full_comment=None,
                         is_deprecated=False, deprecated_comment=None),
        HtmlCommentBlock(link='cats/Bifunctor.html#wait():Unit', short_comment=None, full_comment=None,
                         is_deprecated=False,
                         deprecated_comment=None),
        HtmlCommentBlock(link='cats/Bifunctor.html#wait(x$1:Long,x$2:Int):Unit', short_comment=None, full_comment=None,
                         is_deprecated=False, deprecated_comment=None),
        HtmlCommentBlock(link='cats/Bifunctor.html#wait(x$1:Long):Unit', short_comment=None, full_comment=None,
                         is_deprecated=False, deprecated_comment=None)]
    assert actual == expected
