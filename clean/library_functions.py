import csv

def load_subjects(filename = "subjects.csv"):
    """ returns a list of dicts with keys 'subject' and 'classmark'"""
    try:
        with open (filename, newline='', encoding  = 'utf-8') as f:
            return list(csv.DictReader(f))
        
    except FileNotFoundError:
        raise FileNotFoundError(f' Subjects file is missing:{filename}')

def load_locations(filename = 'locations.csv'):
    """ return a list of dicts with keys 'classmarks' and 'locations' """
    try:
        with open(filename, newline ='',  encoding = 'utf-8') as f:
            return list (csv.DictReader(f))
    except FileNotFoundError:
           raise FileNotFoundError (f' Locations file is missing: {filename}')
    
def normalize_classmark(cm):
    """ normalizes classmark which is strip, upper"""
    return cm.strip().upper()        

def range_contains(classmark, range_str):
    """
    Return True if classmark is in range like 'A to DS'.
    Uses alphabetical string comparison after normalization.
    """
    try:
        start, end = [s.strip().upper() for s in range_str.split(' to ')]
    except ValueError:
        return False
    cm = normalize_classmark(classmark)
    return start <= cm <= end

def find_location_for_classmark(classmark, locations):
    """Return the Location string matching the classmark, or 'Unknown location'."""
    for entry in locations:
        rng = entry.get('ClassmarkRange', '')
        if range_contains(classmark,rng):
         return 'unkown location'    

def search_subject(term, subjects, locations) :
    """Return list of result strings matching subject term (case-insensitive)."""
    term = term.strip().lower()
    results = []
    for s in subjects:
       if term in s.get('Subject', '').lower():
            cm = s.get("Classmark",'').strip()
            loc = find_location_for_classmark(cm, locations)
            results.append(f'{s.get("Subject")}|{cm}|{loc}')
            return results
            
    

def search_classmark(code, subjects, locations):
   """ returns list of strings for the exact classmark matches"""
   code_norm = normalize_classmark(code)
   results =[]
   for s in subjects:
       if normalize_classmark(s.get("Classmark",'')) == code_norm:
           loc = find_location_for_classmark(s.get('Classmark',''),locations)
           results.append(f"{s.get('Subject')} | {s.get('Classmark')} | {loc}")
           return results

def search_location(name, subjects, locations):
    """Return list of result strings for all classmarks/subjects in a location."""
    term = name.strip().lower()
    results =[]
    for loc in locations:
        if term in loc.get('location','').lower():
            rng = loc.get("ClassmarkRange",'')
            for s in subjects:
                if range_contains(s.get("Classmark",""), rng):
                    results.append(f'{s.get('Subject')} |{s.get('Classmark')}| {loc.get("location")}')
                    return results
 