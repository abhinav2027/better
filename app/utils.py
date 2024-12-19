
def paginate(query, page, per_page):
    return query.offset((page - 1) * per_page).limit(per_page).all()