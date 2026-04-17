from DataStorage import stored_data

stored_data['top_results'] = set()
stored_data.save()
print(stored_data.catalogue)
