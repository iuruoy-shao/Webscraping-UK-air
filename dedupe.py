from csv import reader

city_list = []
duplicated_city_list = []
with open('sites.csv', 'r') as read_obj2:
  csv_reader2 = reader(read_obj2)
  list_of_rows2 = csv_reader2
  for list in list_of_rows2:
    if list[4] in city_list:
        if list[4] not in duplicated_city_list:
          duplicated_city_list.append(list[4])
    else:
      city_list.append(list[4])
print(duplicated_city_list)
