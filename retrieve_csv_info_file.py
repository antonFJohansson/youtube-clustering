

import os, csv
import io
def retrieve_csv_info(retrieve_col, save_folder, file = 'stored_information.csv'):

    """
    Retrieves the csv info from the given file
    retrieve_col: Which column in the csv file to retrieve
    save_folder: Which folder to look for the results in
    file: The csv file
    """
    
    retrieve_col_dict = {'Title': 0, 'Description': 1, 'Video_id': 2, 'Subs': 3}
    col_id = retrieve_col_dict[retrieve_col]
    
    file_path = os.path.join(save_folder, file)
    
    store_info = []
    title_store = []
    video_id_store = []
    with io.open(file_path, encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for idx, row in enumerate(csv_reader):
            if idx != 0 and len(row)>0:
                title_info = row[0]
                csv_info = row[col_id]
                video_id_info = row[2]
                store_info.append(csv_info)
                title_store.append(title_info)
                video_id_store.append(video_id_info)
    return store_info, title_store, video_id_store




       
