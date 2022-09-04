from csv import reader
with open('sites.csv', 'r') as reader:
    csv_reader = reader(read_obj)
    list_of_rows = list(csv_reader)
    for list in list_of_rows:
        region = list[5]
        if region in ['Greater London','East Midlands','Eastern','Highland','North East','North West & Merseyside','South East','South West','West Midlands','Yorkshire & Humberside','Central Scotland','North East Scotland','Scottish Borders','South Wales','North Wales','Northern Ireland']:
            print('good')
        else:
            print('bad')
