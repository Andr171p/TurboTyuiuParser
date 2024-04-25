from Avito.AvitoParser.parser import HTMLLoader, AvitoParser


def start_parse():
    REGION = "tyumen"
    HTMLLoader(region=REGION).html_loader()
    parser = AvitoParser()
    data = parser.get_parse()

    return data