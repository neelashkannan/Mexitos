from firebase_admin import db

def fetch_chicken_dry_items(ref):
    chicken_dry_items = ref.child('chicken fry').get()
    return chicken_dry_items

def fetch_bread_items(ref):
    bread_items = ref.child('bread_items').get()
    return bread_items
