from fastapi.datastructures import URL


def paginate(
    url: URL, count: int, limit: int, offset: int
) -> tuple[str | None, str | None]:
    return (
        _paginate_next(url, count, limit, offset),
        _paginate_previous(url, limit, offset),
    )


def _paginate_next(url: URL, count: int, limit: int, offset: int) -> str | None:
    calculated = offset + limit
    if calculated > count:
        return None

    return str(url.include_query_params(offset=calculated))


def _paginate_previous(url: URL, limit: int, offset: int) -> str | None:
    if offset <= 0:
        return None

    calculated = offset - limit if offset > limit else 0

    return str(url.include_query_params(offset=calculated))
