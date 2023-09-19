from math import ceil


def make_pagination_range(page_range, pages, current):
    middle_page = ceil(pages / 2)
    start_page = current - middle_page
    last_page = current + middle_page
    total = len(page_range)
    if current >= total - middle_page:
        last_page = total
        start_page = total - pages
    if current < middle_page:
        start_page = 0
        last_page = pages
    return {
        'pagination': page_range[start_page:last_page],
        'page_range': page_range,
        'start_page': start_page,
        'qty_pages': pages,
        'last_page': total,
        'current': current,
        'first_page_out_of_page_range': current > middle_page,
        'last_page_out_of_page_range': current < total - middle_page,
    }
