from firebase_admin import db

def fetch_chicken_dry_items(ref):
    chicken_dry_items = ref.child('chicken fry').get()
    return chicken_dry_items

def fetch_bread_items(ref):
    bread_items = ref.child('bread_items').get()
    return bread_items

def fetch_shawarma_items(ref):
    shawarma_items = ref.child('shawarma').get()
    return shawarma_items

def fetch_rice_items(ref):
    rice_items = ref.child('rice and noodles items').get()
    return rice_items

def fetch_starter_items(ref):
    starter_items = ref.child('starters').get()
    return starter_items