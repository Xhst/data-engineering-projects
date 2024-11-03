from lxml import html
from json_schema import TableData


def get_name():
    return "forward_extractor"


def extract_references(
    table_num: str, table_id: str, paper: html.HtmlElement
) -> list[str]:
    """
    Extracts paragraphs text where references to the table are found.

    It searches for all the references linked to a specific table ID, then finds the paragraph containing the reference.

    Parameters:
        table_id (str): The table ID we are searching the references for.
        table_num (str): The table number written like this: "Table 1"
        paper (html.HtmlElement): The paper HTML element from which to extract the references and section titles.

    Returns:
        list[str]: A list of paragraphs' text associated with the references to the table.
    """
    refs_text: list[str] = []

    paragraphs_ref = paper.xpath(f'//a[contains(@href, "{table_id}")]/..')

    # If there are no link references, we try to find the ref by table number text (es. "Table 1")
    if paragraphs_ref == []:
        paragraphs_ref = paper.xpath(
            f'//p[contains(normalize-space(text()), "{table_num} ") or '
            f'contains(normalize-space(text()), "{table_num}.") or '
            f'contains(normalize-space(text()), "{table_num};") or '
            f'contains(normalize-space(text()), "{table_num},")]'
        )

    for par in paragraphs_ref:
        par_text = ""
        segments = par.xpath(".//text()")
        for seg in segments:
            par_text = par_text + seg
        refs_text.append(par_text)

    return refs_text


def extract_caption(table_container: html.HtmlElement, table_id: str) -> str:
    """
    Extracts captions.

    It searches for captions inside the table container. It tries strictier rules where necessary.

    Parameters:
        table_id: The table ID we are searching the caption for.
        table_container (html.HtmlElement): The table container HTML element from which to extract the caption.

    Returns:
        list[str]: A list of section titles associated with the references to the table.
    """
    # Extracting captions ("Table X: " + "caption")
    caption_fragments = table_container.xpath(
        './/*[contains(@class, "ltx_caption")]//text()'
    )
    # If we did not found any caption, we try a stricter rules
    if caption_fragments == []:
        caption_fragments = table_container.xpath(
            f'./p[contains(@id, "{table_id}.")]//text()'
        )
    if caption_fragments == []:
        caption_fragments = table_container.xpath(
            f'./span[contains(@id, "{table_id}.")]//text()'
        )

    caption = "".join(caption_fragments)

    return caption


def extract_footnotes(table: html.HtmlElement) -> list[str]:
    """
    Extracts the footnotes from the table by combining the non-numeric text segments
    of each footnote, ignoring specific nested elements.

    The structure of every footnote seems to be:
        footnote id = "footnote1" (the most outer part)\n
        |__> footnote id = "footnote1.1" (an hidden html element that appears
                when mouse hovering -> which we are not interested in)\n
            |__> several text fragments componing the footnote (we take these directly from the first element)

    Of these fragments, the first ones are usually the footnote number repeated, so we can ignore them
    Then, we combine the rest

    Parameters:
        table (html.HtmlElement): The table element from which to extract the footnotes.

    Returns:
        list[str]: A list of strings where each string is a table footnote's full text.
    """
    footnotes_xpath = table.xpath(
        './/*[contains(@id, "footnote") and not(contains(@id, "."))]'
    )
    footnotes: list[str] = []

    for footnote in footnotes_xpath:
        footnote_segments = footnote.xpath(".//text()")

        if footnote_segments:
            foot_text = ""
            for segment in footnote_segments:
                if segment == "" or segment.isnumeric() or segment == "footnotetext: ":
                    continue
                foot_text += segment

            footnotes.append(foot_text)

    return footnotes


def extract_paper_data(paper: html.HtmlElement) -> dict[str, TableData]:
    article_json: dict[str, TableData] = {}

    # Extracting tables, here "tables" are intended as tags containing table tags

    # Most tables are contained within a figure element with a class of "ltx_table" and id containing ".T",
    # while in rare cases they are contained within a div element with a class of "ltx_minipage".
    # In that case, we select only those divs that contain a table element.
    # TODO: confront with others
    table_containers = paper.xpath(
        '//figure[contains(@id, ".T")] | '
        + '//table/ancestor::div[contains(@id, ".") and contains(@class, "ltx_minipage") and not(ancestor::figure)] | '
        + '//table/ancestor::div[contains(@id, "example") and not(ancestor::figure)]'
    )

    for table_container in table_containers:
        if (
            table_container == None
            or table_container == []
            or not (table_container.getchildren())
        ):
            continue

        # we exclude equations and figures (id = ".E" or ".F")
        table_tags = table_container.xpath(
            './/table[contains(@id, ".T") or contains(@id, "example")]'
        )

        if table_tags == []:
            continue

        table_id = table_container.get("id")

        # Extracting caption
        caption = extract_caption(table_container, table_id)

        # Extracting footnotes
        footnotes = extract_footnotes(table_container)

        # Extracting references
        # We need this to search for some references, we take the first part of the caption ("Table X:")
        paragraphs_refs = []
        if caption:
            table_num = caption.split(":")[0]
            paragraphs_refs = extract_references(table_num, table_id, paper)

        # We then insert it into the json
        table_tag_str = ""
        for table_tag in table_tags:
            table_tag_str = table_tag_str + html.tostring(table_tag).decode("utf-8")

        # populate TableData
        table_json = TableData()
        table_json.caption = caption
        table_json.table = table_tag_str
        table_json.footnotes = footnotes
        table_json.references = paragraphs_refs

        # Store the table JSON with its id
        article_json[table_id] = table_json

    return article_json
