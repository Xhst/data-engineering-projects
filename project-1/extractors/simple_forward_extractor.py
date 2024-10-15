import json
import paths
import os
import time

from dataclasses import dataclass, field
from lxml import html


@dataclass
class TableData:
    table_id: str = ""
    caption: str = ""
    table: str = ""
    references: list[str] = field(default_factory=list)
    footnotes: list[str] = field(default_factory=list)

    def to_custom_dict(self):
        return {
            self.table_id: {
                "caption": self.caption,
                "table": self.table,
                "references": self.references,
                "footnotes": self.footnotes,
            }
        }


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
if __name__ == "__main__":
    filenames = os.listdir(paths.HTML_FOLDER)

    # make sure the JSON folder exists
    if not os.path.exists(paths.JSON_FOLDER):
        os.makedirs(paths.JSON_FOLDER)

    for filename in filenames:

        with open(f"{paths.HTML_FOLDER}/{filename}", "r", encoding="utf-8") as file:

            file_content = file.read().encode("utf-8")
            paper = html.fromstring(file_content, parser=html.HTMLParser())
            filename = filename.replace(".html", "")

            table_data_list: list[TableData] = []
            figure_list: list[html.HtmlElement] = paper.xpath(
                './/figure[contains(@id, ".T")]'
            )

            for figure in figure_list:

                table_data = TableData()

                # check nested figure
                if len(figure.xpath('.//figure[contains(@id, ".T")]')) > 1:
                    continue
                figure_id: str = figure.get("id")
                table_number = (figure_id.split(".")[1]).split("T")[1]

                table_data.table_id = figure_id
                table_data.table = get_table_from_figure(figure)
                table_data.caption = get_caption_from_figure(figure)
                table_data.references = get_references_from_figure(paper, table_number)
                table_data.footnotes = get_footnotes_from_figure(figure)

                table_data_list.append(table_data)

        custom_table_data_list = [
            table_data.to_custom_dict() for table_data in table_data_list
        ]

        with open(
            f"{paths.JSON_FOLDER}/{filename}.json", "w", encoding="utf-8"
        ) as jsonFile:
            json.dump(
                custom_table_data_list, jsonFile, default=lambda o: o.__dict__, indent=4
            )
