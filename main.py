from models import IRSFinder

# to beatify the dict output
import json

# search criteria
FORM_NAME = 'Form 706'

taxes_json = IRSFinder().get_taxes_json([FORM_NAME])
# display json result
print(json.dumps(taxes_json, indent=4))


year_range = [2014, 2019]
IRSFinder().download_taxes(FORM_NAME, *year_range)
