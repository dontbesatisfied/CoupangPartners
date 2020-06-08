from scrapy.selector import Selector


def parse_detail_content(details=list):
    contents = []
    for detail in details:
        for vendorItemContentDescription in detail['vendorItemContentDescriptions']:
            if vendorItemContentDescription['imageType']:
                contents.append(
                    'https://' + vendorItemContentDescription['content'])
            else:
                s = Selector(text=vendorItemContentDescription['content'])
                contents = s.xpath('//img/@src').extract()
    return contents
