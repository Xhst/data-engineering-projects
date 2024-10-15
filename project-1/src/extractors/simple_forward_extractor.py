from lxml import html
from json_schema import TableData


def get_table_from_figure(figure):

    table_tags: list[html.HtmlElement] = figure.xpath('.//table[contains(@id, ".T")]')

    if table_tags == []:
        return

    table = ""

    for table_tag in table_tags:
        table = table + html.tostring(table_tag).decode("utf-8")

    return table


# captions from only markup that contain "ltx_caption"
def get_caption_from_figure(figure):

    caption_fragments = figure.xpath('.//*[contains(@class, "ltx_caption")]//text()')
    caption = ""

    for caption_fragment in caption_fragments:
        caption = caption + caption_fragment

    return caption


def get_footnotes_from_figure(figure):

    # return footnotes
    return []


#!!! Nested figures might repeat or miss some references !!!
def get_references_from_figure(paper, table_number):

    references: list[str] = []
    p_ref_list = paper.xpath(f'.//a[contains(@title, "Table {table_number}")]/..')

    for p_ref in p_ref_list:
        ref = ""
        ref_fragments = p_ref.xpath(f".//text()")
        for ref_fragment in ref_fragments:
            ref = ref + ref_fragment
        references.append(ref)

    # return references
    return references


# simple extraction from figures
def extract_paper_data(paper):

    paperData = {}

    table_data_list: list[TableData] = []
    figure_list: list[html.HtmlElement] = paper.xpath('.//figure[contains(@id, ".T")]')

    for figure in figure_list:

        table_data = TableData()

        # check nested figure
        if len(figure.xpath('.//figure[contains(@id, ".T")]')) > 1:
            continue
        figure_id: str = figure.get("id")
        table_number = (figure_id.split(".")[1]).split("T")[1]

        table_id = figure_id
        table_data.table = get_table_from_figure(figure)
        table_data.caption = get_caption_from_figure(figure)
        table_data.references = get_references_from_figure(paper, table_number)
        table_data.footnotes = get_footnotes_from_figure(figure)

        paperData[table_id] = table_data

    return paperData
