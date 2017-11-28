from collections import defaultdict
import gzip

class LexiconFeaturizer(object):
    """ A class that featurizes a tweet affect/sentiment lexicons"""

    def __init__(self, list_of_featurizers=[]):
        self.list_of_featurizers = []
        
        # load all of the data
        print("Loading all affect/sentiment lexicon data...")
        self.nrc_hashtag_emotion_map = self.get_nrc_hashtag_emotion()
        self.nrc_affect_intensity_map = self.get_nrc_affect_intensity()
        self.nrc_hashtag_sentiment_unigrams_map = self.get_nrc_hashtag_sentiment_lexicon_unigrams()
        self.nrc_hashtag_sentiment_bigrams_map = self.get_nrc_hashtag_sentiment_lexicon_bigrams()
        self.sentiment140_unigrams_map = self.get_sentiment140_unigrams()
        self.sentiment140_bigrams_map = self.get_sentiment140_bigrams()
        self.senti_wordnet_map = self.get_senti_wordnet()
        self.bing_lui_sent_lexicons_map = self.get_bing_lui_sentiment_lexicons()
        self.get_nrc_10_expanded_map = self.get_nrc_10_expanded()
        self.negating_word_list = self.get_negating_word_list()
        
    def get_nrc_hashtag_emotion(self):
        nrc_hashtag_emotion_path = "./data/lexicons/NRC-Hashtag-Emotion-Lexicon-v0.2.txt"
        lexicon_map = defaultdict(list)

        with open(nrc_hashtag_emotion_path, 'rb') as f:
            lines = f.read().splitlines()
            for l in lines[1:]:
                splits = l.decode('utf-8').split('\t')
                lexicon_map[splits[0]] = [float(num) for num in splits[1:]]
        return lexicon_map

    def get_nrc_affect_intensity(self):
        nrc_affect_intensity_path = "./data/lexicons/nrc_affect_intensity.txt"
        lexicon_map = defaultdict(list)

        with open(nrc_affect_intensity_path, 'rb') as f:
            lines = f.read().splitlines()
            for l in lines[1:]:
                splits = l.decode('utf-8').split('\t')
                lexicon_map[splits[0]] = [float(num) for num in splits[1:]]

        return lexicon_map

    def get_nrc_hashtag_sentiment_lexicon_unigrams(self):
        nrc_hashtag_sentiment_lexicon_unigrams_path = "./data/lexicons/NRC-Hashtag-Sentiment-Lexicon-v0.1/unigrams-pmilexicon.txt"
        with open(nrc_hashtag_sentiment_lexicon_unigrams_path, 'rb') as f:
            lines = f.read().splitlines()
            lexicon_map = {}
            for l in lines:
                splits = l.decode('utf-8').split('\t')
                lexicon_map[splits[0]] = float(splits[1])
        return lexicon_map

    def get_nrc_hashtag_sentiment_lexicon_bigrams(self):
        nrc_hashtag_sentiment_lexicon_bigrams_path = "./data/lexicons/NRC-Hashtag-Sentiment-Lexicon-v0.1/bigrams-pmilexicon.txt"
        with open(nrc_hashtag_sentiment_lexicon_bigrams_path, 'rb') as f:
            lines = f.read().splitlines()
            lexicon_map = {}
            for l in lines:
                splits = l.decode('utf-8').split('\t')
                lexicon_map[splits[0]] = float(splits[1])
        return lexicon_map

    def get_sentiment140_unigrams(self):
        sentiment140_unigrams = "./data/lexicons/Sentiment140-Lexicon-v0.1/unigrams-pmilexicon.txt"
        with open(sentiment140_unigrams, 'rb') as f:
            lines = f.read().splitlines()
            lexicon_map = {}
            for l in lines:
                splits = l.decode('utf-8').split('\t')
                lexicon_map[splits[0]] = float(splits[1])
        return lexicon_map

    def get_sentiment140_bigrams(self):
        sentiment140_bigrams = "./data/lexicons/Sentiment140-Lexicon-v0.1/bigrams-pmilexicon.txt"
        with open(sentiment140_bigrams, 'rb') as f:
            lines = f.read().splitlines()
            lexicon_map = {}
            for l in lines:
                splits = l.decode('utf-8').split('\t')
                lexicon_map[splits[0]] = float(splits[1])
        return lexicon_map
    
    def get_senti_wordnet(self):
        senti_wordnet_path = "./data/lexicons/SentiWordNet_3.0.0.txt"
        with open(senti_wordnet_path, 'rb') as f:
            lines = f.read().splitlines()
            senti_wordnet_lexicon_map = defaultdict(float)

            for l in lines:
                l = l.decode('utf-8')
                if l.strip().startswith('#'):
                    continue
                splits = l.split('\t')
                # positive score - negative score
                score = float(splits[2]) - float(splits[3])
                words = splits[4].split(" ")
                # iterate through all words
                for word in words:
                    word, rank = word.split('#')
                    # scale scores according to rank
                    # more popular => less rank => high weight
                    senti_wordnet_lexicon_map[word] += (score / float(rank))
        return senti_wordnet_lexicon_map

    def get_bing_lui_sentiment_lexicons(self):
        bing_lui_sentiment_lexicons_path = "./data/lexicons/BingLiu.txt"
        lexicon_map = defaultdict(list)
        
        with open(bing_lui_sentiment_lexicons_path, 'rb') as f:
            lines = f.read().splitlines()
            lexicon_map = {}
            for l in lines:
                splits = l.decode('utf-8').split('\t')
                lexicon_map[splits[0]] = splits[1]
        return lexicon_map
    
    def get_nrc_10_expanded(self):
        nrc_10_expanded_path = "./data/lexicons/w2v-dp-BCC-Lex.txt"
        lexicon_map = defaultdict(list)
        with open(nrc_10_expanded_path, 'rb') as f:
            lines = f.read().splitlines()
            for l in lines[1:]:
                splits = l.decode('utf-8').split('\t')
                lexicon_map[splits[0]] = [float(num) for num in splits[1:]]
        return lexicon_map   


    def get_negating_word_list(self):
        negating_word_list_path = "./data/lexicons/NegatingWordList.txt"
        negating_words = []
        with open(negating_word_list_path, "r") as f:
            for word in f.readlines():
                word = word.rstrip("\n")
                negating_words.append(word)
        return negating_words        
    
    def get_bigrams(self, tokens):
        """ Return a list of bigram from a set of tokens """
        return [a + " " + b for a, b in zip(tokens, tokens[1:])]
    
    
    def nrc_hashtag_emotion(self, tokens):
        """ Build features using NRC Hashtag emotion dataset """
        num_features = 10  # 'anger', 'anticipation', 'disgust', 'fear', 'joy', 'negative', 'positive', 'sadness', 'surprise', 'trust'
        sum_vec = [0.0] * num_features
        for token in tokens:
            if token in self.nrc_hashtag_emotion_map:
                sum_vec = [a + b for a, b in zip(sum_vec, self.nrc_hashtag_emotion_map[token])] # sum up the individual word feature vectors
        feature_names = ['anger', 'anticipation', 'disgust', 'fear', 'joy', 'negative', 'positive', 'sadness', 'surprise', 'trust']
        feature_names = ['nrc_hashtag_emotion_' + name for name in feature_names]
        return dict(zip(feature_names, sum_vec))
    
    
    def nrc_affect_intensity(self, tokens):
        """ Build feature vector using NRC affect intensity lexicons """ 
        num_features = 10  # 'anger', 'anticipation', 'disgust', 'fear', 'joy', 'negative', 'positive', 'sadness', 'surprise', 'trust'
        sum_vec = [0.0] * num_features
        for token in tokens:
            if token in self.nrc_affect_intensity_map:
                sum_vec = [a + b for a, b in zip(sum_vec, self.nrc_affect_intensity_map[token])]
        
        feature_names = ['anger', 'anticipation', 'disgust', 'fear', 'joy', 'negative', 'positive', 'sadness', 'surprise', 'trust']
        feature_names = ['nrc_affect_intensity_' + name for name in feature_names]
        return dict(zip(feature_names, sum_vec))
    
    
    def nrc_hashtag_sentiment_lexicon_unigrams(self, tokens):
        """
        Function returns sum of intensities of
        positive and negative tokens using only unigrams. Also returns
        the number of positive and negative tokens
        """

        positive_score, negative_score = 0.0, 0.0
        positive_unigram_words, negative_unigram_words = 0, 0

        for token in tokens:
            if token in self.nrc_hashtag_sentiment_unigrams_map:
                if self.nrc_hashtag_sentiment_unigrams_map[token] >= 0:
                    positive_score += self.nrc_hashtag_sentiment_unigrams_map[token]
                    positive_unigram_words += 1
                else:
                    negative_score += self.nrc_hashtag_sentiment_unigrams_map[token]
                    negative_unigram_words += 1

        return {
            "nrc_hashtag_sentiment_positive_unigram_score": positive_score, 
            "nrc_hastag_sentiment_negative_unigram_score": negative_score, 
            "nrc_hashtag_sentiment_postive_unigram_words": positive_unigram_words, 
            "nrc_hashtag_sentiment_negative_unigram_words": negative_unigram_words
        }

    
    def nrc_hashtag_sentiment_lexicon_bigrams(self, tokens):
        """ 
        Function returns sum of intensities of 
        positive and negative tokens using only unigrams. Also returns
        the number of positive and negative tokens
        """

        positive_score, negative_score = 0.0, 0.0
        positive_bigram_words, negative_bigram_words = 0, 0

        # loop through the bigrams
        for token in self.get_bigrams(tokens):
            if token in self.nrc_hashtag_sentiment_bigrams_map:
                if self.nrc_hashtag_sentiment_bigrams_map[token] >= 0:
                    positive_score += self.nrc_hashtag_sentiment_bigrams_map[token]
                    positive_bigram_words += 1
                else:
                    negative_score += self.nrc_hashtag_sentiment_bigrams_map[token]
                    negative_bigram_words += 1
        return {
            "nrc_hashtag_sentiment_positive_bigram_score": positive_score, 
            "nrc_hastag_sentiment_negative_bigram_score": negative_score, 
            "nrc_hashtag_sentiment_postive_bigram_words": positive_bigram_words, 
            "nrc_hashtag_sentiment_negative_bigram_words": negative_bigram_words
        }
    
    
    def sentiment140_unigrams(self, tokens):
        """ Sentiment 140 Unigram Lexicons features """
        positive_score, negative_score = 0.0, 0.0
        positive_unigram_words, negative_unigram_words = 0, 0

        # loop through the bigrams
        for token in tokens:
            if token in self.sentiment140_unigrams_map:
                if self.sentiment140_unigrams_map[token] >= 0:
                    positive_score += self.sentiment140_unigrams_map[token]
                    positive_unigram_words += 1
                else:
                    negative_score += self.sentiment140_unigrams_map[token]
                    negative_unigram_words += 1
        return {
            "sentiment140_positive_unigram_score": positive_score, 
            "sentiment140_negative_unigram_score": negative_score, 
            "sentiment140_postive_unigram_words": positive_unigram_words, 
            "sentiment140_negative_unigram_words": negative_unigram_words
        }
    
    
    def sentiment140_bigrams(self, tokens):
        """ Sentiment 140 Unigram Lexicons features """
        positive_score, negative_score = 0.0, 0.0
        positive_bigram_words, negative_bigram_words = 0, 0 

        # loop through the bigrams
        for token in self.get_bigrams(tokens):
            if token in self.sentiment140_bigrams_map:
                if self.sentiment140_bigrams_map[token] >= 0:
                    positive_score += self.sentiment140_bigrams_map[token]
                    positive_bigram_words += 1
                else:
                    negative_score += self.sentiment140_bigrams_map[token]
                    negative_bigram_words += 1

        return {
            "sentiment140_positive_bigram_score": positive_score, 
            "sentiment140_negative_bigram_score": negative_score, 
            "sentiment140_postive_bigram_words": positive_bigram_words, 
            "sentiment140_negative_bigram_words": negative_bigram_words
        }
    
     
    def senti_wordnet(self, tokens):
        """ Returns features based on the SentiWordNet features """

        positive_score, negative_score = 0.0, 0.0
        positive_unigram_words, negative_unigram_words = 0, 0

        # loop through the bigrams  
        for token in tokens:
            if token in self.senti_wordnet_map:
                if self.senti_wordnet_map[token] >= 0:
                    positive_score += self.senti_wordnet_map[token]
                    positive_unigram_words += 1
                else:
                    negative_score += self.senti_wordnet_map[token]
                    negative_unigram_words += 1

        return  {
            "senti_wordnet_positive_score": positive_score, 
            "senti_wordnet_negative_score": negative_score, 
            "senti_wordnet_postive_words": positive_unigram_words, 
            "senti_wordnet_negative_words": negative_unigram_words
        }

    
    def bing_lui_sentiment_lexicons(self, tokens):
        """ Build features using NRC Hashtag emotion dataset """
        positive_count, negative_count = 0.0, 0.0
        for token in tokens:
            if token in self.bing_lui_sent_lexicons_map:
                if self.bing_lui_sent_lexicons_map[token] == 'positive':
                    positive_count += 1
                else:
                    negative_count += 1
        return {
            "bing_lui_sentiment_lexicon_positive_count" : positive_count,
            "bing_lui_sentiment_lexicon_negative_count" : negative_count
        }
    
    
    def nrc_10_expanded(self, tokens): 
        """ Build features using NRC 10 Expanded lexicons dataset """
        num_features = 10  # 'anger', 'anticipation', 'disgust', 'fear', 'joy', 'negative', 'positive', 'sadness', 'surprise', 'trust'
        sum_vec = [0.0] * num_features
        for token in tokens:
            if token in self.get_nrc_10_expanded_map:
                sum_vec = [a + b for a, b in zip(sum_vec, self.get_nrc_10_expanded_map[token])] # sum up the individual word feature vectors
        feature_names = ['anger', 'anticipation', 'disgust', 'fear', 'joy', 'negative', 'positive', 'sadness', 'surprise', 'trust']
        feature_names = ['nrc_expanded_' + name for name in feature_names]
        return dict(zip(feature_names, sum_vec))

    def negating_word_list(self, tokens):
        num_of_negating_words = 0
        for token in tokens:
            if token in self.get_negating_word_list_map:
                num_of_negating_words += 1
        return {"num_of_negating_words": num_of_negating_words}

    
    def featurize(self, tokens):
        """ Build a feature vector for the tokens """
        features = []
        
    
        nrc_hashtag_emotion_features = self.nrc_hashtag_emotion(tokens)
        nrc_affect_intensity_features = self.nrc_affect_intensity(tokens)
        nrc_hashtag_sentiment_lexicon_unigrams_features = self.nrc_hashtag_sentiment_lexicon_unigrams(tokens)
        nrc_hashtag_sentiment_lexicon_bigrams_features = self.nrc_hashtag_sentiment_lexicon_bigrams(tokens)
        sentiment140_unigrams_features = self.sentiment140_unigrams(tokens)
        sentiment140_bigrams_features = self.sentiment140_bigrams(tokens)
        senti_wordnet_features = self.senti_wordnet(tokens)
        bing_lui_sentiment_lexicons_features = self.bing_lui_sentiment_lexicons(tokens)
        nrc_expanded_lexicon_features = self.nrc_10_expanded(tokens)
        negating_word_list_features = self.negating_word_list(tokens)
        
        features.extend(nrc_hashtag_emotion_features.values()) # 10 features
        features.extend(nrc_affect_intensity_features.values()) # 10 features
        features.extend(nrc_hashtag_sentiment_lexicon_unigrams_features.values()) # 4 features
        features.extend(nrc_hashtag_sentiment_lexicon_bigrams_features.values()) # 4 features
        features.extend(sentiment140_unigrams_features.values()) # 4 features 
        features.extend(sentiment140_bigrams_features.values()) # 4 features
        features.extend(senti_wordnet_features.values()) # 4 features
        features.extend(bing_lui_sentiment_lexicons_features.values()) # 2 features
        features.extend(nrc_expanded_lexicon_features.values()) # 10 features
        features.extend(negating_word_list_features.values())
        return features
