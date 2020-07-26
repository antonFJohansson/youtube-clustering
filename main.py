
from youtube_class_file import youtube_class
from LDAmodel_file import LDAmodel
from retrieve_csv_info_file import retrieve_csv_info


## Mike Thurston https://www.youtube.com/channel/UCzGLDaTu81nJDtWK10MniGg



save_folder = 'downloaded_info'
video_channel_id = 'UC4ijq8Cg-8zQKx8OH12dUSw'
num_playlists = 5


## Code starts here
channel_info = youtube_class(save_folder, video_channel_id)
channel_info.retrieve_channel_info()

sub_store, title_store, video_id_store = retrieve_csv_info('Subs', save_folder)

lda = LDAmodel(sub_store, title_store, video_id_store,
               num_playlists, num_passes = 100, no_below=10,
               no_above=0.5)
lda.fit_LDAmodel()
lda.print_clusters()
lda.save_video_clusters(save_folder)
lda.print_cluster_help()

