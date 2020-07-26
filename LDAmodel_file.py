

from gensim.models import LdaModel

import pandas as pd
import gensim
import nltk
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
stemmer = SnowballStemmer('english')
nltk.download('wordnet')
from numpy import argmax, array, argsort
import os



class LDAmodel():
    
    """
    Class to work with the LDA model and to store the resulting clusters.
    document_store: A list with the subtitles for the videos
    title_store: A list with the corresponding titles for each video
    video_id_store: A list with the corresponding video ids
    num_topics: The number of clusters for the model
    num_passes: The number of iterations in the model fitting
    no_below: Remove all words that appear in less than 10 documents
    no_above: Remove all words that appear in more that 50% of the documents
    """
    
    def __init__(self, document_store, title_store, video_id_store, num_topics = 2,
                 num_passes = 100, no_below=10, no_above=0.5):
        self.document_store = document_store
        self.num_topics = num_topics
        self.title_store = title_store
        self.video_id_store = video_id_store
        
        self.stemmer = SnowballStemmer('english')
        self.num_passes = num_passes
        self.no_below = no_below
        self.no_above = no_above
        
        nltk.download('wordnet')
        
    def fit_LDAmodel(self):
        
        """
        Fits the LDA model to the given data
        """
        def lem_stem(text):
            return self.stemmer.stem(WordNetLemmatizer().lemmatize(text,pos='v'))
        
        def preprocess(text):
            result = []
            for token in gensim.utils.simple_preprocess(text):
                if token not in STOPWORDS and len(token) >= 3:
                    result.append(lem_stem(token))
            return result
        

        pd_doc = pd.Series(self.document_store)
        self.processed_docs = pd_doc.map(preprocess)
        
        self.dictionary = gensim.corpora.Dictionary(self.processed_docs)
        self.dictionary.filter_extremes(no_below=self.no_below, no_above=self.no_above) 
        self.common_corpus = [self.dictionary.doc2bow(doc) for doc in self.processed_docs]

        print('Fitting model...')
        self.lda = LdaModel(self.common_corpus,
                            num_topics=self.num_topics,
                            alpha = 'auto',
                            passes = self.num_passes)
    
    
    def print_clusters(self, num_to_print = 5):
        """
        Print the clusters obtained from the lda model
        """
        
        self.top_videos_title, self.top_video_id = self.get_top_video()
        
        for id_clu in range(self.num_topics):
            print('Topic {}'.format(id_clu))
            word_list = [self.dictionary[int(idx)] for idx,_ in self.lda.show_topic(id_clu)]
            str_word_list = 'Defining words for this cluster are: ' + ', '.join(word_list)
            print(str_word_list)
            print('The top videos associated with this cluster are:')
            for video in self.top_videos_title[id_clu][0:num_to_print]:
                print(video)
            print(10*'--')
            
    def save_video_clusters(self, save_folder):
        
        """
        Saves the clusters as text files.
        """
        
        if not os.path.isdir(save_folder):
            os.mkdir(save_folder)
        for id_clu, (vid_title_list, vid_id_list) in enumerate(zip(self.top_videos_title, self.top_video_id)):
            word_list = [self.dictionary[int(idx)] for idx,_ in self.lda.show_topic(id_clu)]
            save_path = 'Cluster {} '.format(id_clu) + '(' +  '_'.join(word_list[0:3]) + ')' + '.txt'
            save_path = os.path.join(save_folder, save_path)
            
            import io
            with io.open(save_path, "w", encoding="utf-8") as file:
            #with open(save_path, 'w') as file:
                    
                    str0 = 'Defining words for this cluster are: ' + ', '.join(word_list)
                    file.write(str0 + '\n')
                    file.write('Title | Video Url \n')
                    for vid_title, vid_id in zip(vid_title_list, vid_id_list):
                        str1 = vid_title
                        str2 = ' | '
                        str3 = 'https://www.youtube.com/watch?v={}'.format(vid_id)
                        file.write(str1 + str2 + str3 + '\n')
            file.close()
                
        


    def get_top_video(self):
        
        """
        Gets the top videos for each cluster
        """
        
        topics = self.lda.get_document_topics(self.common_corpus, minimum_probability = 0)
        doc_topics = [doc_topics for doc_topics in topics]
        
        store_doc_info = [[] for kkk in range(self.num_topics)]
        
        for idx, doc_dist in enumerate(doc_topics):
            probs = [prob for _,prob in doc_dist]
            topics = [top for top,_ in doc_dist]
            max_prob = max(probs)
            max_top = topics[argmax(probs)]
            store_doc_info[max_top].append((max_prob, idx))
            
            
        top_cluster_videos_title = [[] for kkk in range(self.num_topics)]
        top_cluster_videos_id = [[] for kkk in range(self.num_topics)]
        for idx, doc_info in enumerate(store_doc_info):
                
            doc_array = array(doc_info)
            sorted_doc_array = doc_array[argsort(-doc_array[:, 0])]
            sorted_ind = sorted_doc_array[:,1].tolist()
            for top_video_ind in sorted_ind:
                top_cluster_videos_title[idx].append(self.title_store[int(top_video_ind)])
                top_cluster_videos_id[idx].append(self.video_id_store[int(top_video_ind)])
    
        return top_cluster_videos_title, top_cluster_videos_id
    
    def print_cluster_help(self):
        help_str = """ 
        Are you satisfied with the clusters?
        If not then try these guidelines:
        If the clusters contain several topics, try increasing the amount of clusters
        If the cluster are too vague/seem to contain different topics, try decreasing the amount of clusters.
        If there are few clusters but they are still vague, try increasing num_passes
        Are the clusters dominated by un-informative words, try decreasing no_below.
        """
        print(help_str)
        
        
        
        
        
