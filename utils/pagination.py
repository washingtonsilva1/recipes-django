from math import ceil


def make_pagination_range(range, pages, current):
    middle_page = ceil(pages/2)
    start_page = current - middle_page
    last_page = current + middle_page
    total = ceil(len(range)/pages)

    if current > middle_page:
        if last_page > total:
            return range[start_page:total + 1]
        return range[start_page:last_page]
    return range[:4]
