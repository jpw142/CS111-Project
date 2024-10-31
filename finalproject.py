import math

class TextModel:
    def __init__(self, model_name):
        """ creates the model """
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.punctuation = {}


    def __repr__(self):
        """ string representation of the model """
        s = ""
        s += "text model name: " + self.name + "\n"
        s += "  number of words: " + str(len(self.words)) + "\n"
        s += "  number of word lengths: " + str(len(self.word_lengths)) + "\n"
        s += "  number of stems: " + str(len(self.stems)) + "\n"
        s += "  number of sentence lengths: " + str(len(self.sentence_lengths)) + "\n"
        s += "  number of punctuation: " + str(len(self.punctuation))
        return s

    def add_string(self, s):
        """Analyzes the string txt and adds its pieces
           to all of the dictionaries in this text model.
        """

        # sentance lengths
        num_words = 1
        for i in range(1, len(s) - 1):
            if s[i] == " ":
                num_words += 1
            if s[i] in ".!?":
                if num_words in self.sentence_lengths:
                    self.sentence_lengths[num_words] += 1
                else:
                    self.sentence_lengths[num_words] = 1
                num_words = 0
        if num_words != 0:
            if num_words in self.sentence_lengths:
                self.sentence_lengths[num_words] += 1
            else:
                self.sentence_lengths[num_words] = 1

        # punctuation count
        for i in range(len(s)):
            if s[i] in """!"#$%&'()*+, -./:;<=>?@[\]^_`{|}~""":
                if s[i] in self.punctuation:
                    self.punctuation[s[i]] += 1
                else:
                    self.punctuation[s[i]] = 1

        word_list = clean_text(s)

        for w in word_list:

            # Words
            if w in self.words:
                self.words[w] += 1
            else:
                self.words[w] = 1
            
            # word lengths
            if len(w) in self.word_lengths:
                self.word_lengths[len(w)] += 1
            else:
                self.word_lengths[len(w)] = 1

            # Stem
            if stem(w) in self.stems:
                self.stems[stem(w)] += 1
            else:
                self.stems[stem(w)] = 1

    def add_file(self, filename):
        """ adds an entire file worth of strings """
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        self.add_string(f.read())

    def save_model(self):
        """ saves the model to a text file"""
        words_name = self.name + "_words"
        word_lengths_name = self.name + "_word_lengths"
        stems_name = self.name + "_stems"
        sentence_lengths_name = self.name + "_sentence_lengths"
        punctuation_name = self.name + "_punctuation"
        # words
        f = open(words_name, 'w')
        f.write(str(self.words))
        f.close()
        # word_lengths
        f = open(word_lengths_name, 'w')
        f.write(str(self.word_lengths))
        f.close()
        # stems
        f = open(stems_name, 'w')
        f.write(str(self.stems))
        f.close()
        # sentance lengths
        f = open(sentence_lengths_name, 'w')
        f.write(str(self.sentence_lengths))
        f.close()
        # punctuation
        f = open(punctuation_name, 'w')
        f.write(str(self.punctuation))
        f.close()

    def read_model(self):
        """ reads model from file into program """
        words_name = self.name + "_words"
        word_lengths_name = self.name + "_word_lengths"
        stems_name = self.name + "_stems"
        sentence_lengths_name = self.name + "_sentence_lengths"
        punctuation_name = self.name + "_punctuation"
        # words
        f = open(words_name, 'r')
        self.words = dict(eval(f.read()))
        f.close()
        # word_lengths
        f = open(word_lengths_name, 'r')
        self.word_lengths = dict(eval(f.read()))
        f.close()
        # stems
        f = open(stems_name, 'r')
        self.stems = dict(eval(f.read()))
        f.close()
        # sentence lengths
        f = open(sentence_lengths_name, 'r')
        self.sentence_lengths = dict(eval(f.read()))
        f.close()
        # punctuation
        f = open(punctuation_name, 'r')
        self.punctuation = dict(eval(f.read()))
        f.close()

    def similarity_scores(self, other):
        """ computes list of similarity scores """
        word_score = compare_dictionaries(other.words, self.words)
        word_lengths_score = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        stem_score = compare_dictionaries(other.stems, self.stems)
        sentence_len_score = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        punctuation_score = compare_dictionaries(other.punctuation, self.punctuation)
        return [word_score, word_lengths_score, stem_score, sentence_len_score, punctuation_score]
    
    def classify(self, source1, source2):
        """ classifies current text model based on 2 sources """
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        print('scores for ' + source1.name + ':' + str(scores1))
        print('scores for ' + source2.name + ':' + str(scores2))

        average1 = 0
        average2 = 0
        for i in range(len(scores1)):
            average1 += scores1[i]
            average2 += scores2[i]
        average1 /= len(scores1)
        average2 /= len(scores2)
        winner = ''
        if average1 > average2:
            winner = source1.name
        else:
            winner = source2.name
        print(self.name + ' is more likely to have come from ' + winner)

def stem(s):
    """ removes any suffixes """
    # ness
    if len(s) > 4:
        if s[-4:] == 'ness':
            s = s[:-4]
    # s
    if len(s) > 1:
        if s[-1] == 's':
            s = s[:-1]
    # ing
    if len(s) > 3:
        if s[-3:] == 'ing':
            s = s[:-3]
    # ist
    if len(s) > 3:
        if s[-3:] == 'ist':
            s = s[:-3]
    # ism
    if len(s) > 3:
        if s[-3:] == 'ism':
            s = s[:-3]
    # er
    if len(s) > 2:
        if s[-2:] == 'er':
            s = s[:-2]
    # y
    if len(s) > 1:
        if s[-1] == 'y':
            s = s[:-1]
    # e
    if len(s) > 1:
        if s[-1] == 'e':
            s = s[:-1]
    # i
    if len(s) > 1:
        if s[-1] == 'i':
            s = s[:-1]
    return s

def clean_text(txt):
    """ returns list of cleaned words with no punctuation"""
    list_words = []
    s = txt
    for symbol in """.,?"'!;:""":
        s = s.replace(symbol, '')
    return s.lower().split()

def compare_dictionaries(d1, d2):
    """ compares baysian distribution of two dictionaries """
    if d1 == {}:
        return -50
    score = 0

    denominator = 0
    for i in d1.values():
        denominator += i

    for key, value in d2.items():
        if key in d1:
            probability = d1[key] / denominator
            score += value * math.log(probability)
        else:
            probability = 0.5 / denominator
            score += value * math.log(probability)
    return score

def run_tests():
    source1 = TextModel('wikipedia')
    source1.add_file('wikipedia.txt')
    
    source2 = TextModel('starwars')
    source2.add_file('star.txt')

    source3 = TextModel('shakespear')
    source3.add_file('alls.txt')

    source4 = TextModel('bible')
    source4.add_file('bible.txt')
    
    new1 = TextModel('wr120')
    new1.add_file('weber.txt')

    new2 = TextModel('everythingeverywhere')
    new2.add_file('everything.txt')

    new1.classify(source1, source2)
    new1.classify(source1, source3)
    new1.classify(source1, source4)
    new1.classify(source2, source1)
    new1.classify(source2, source3)
    new1.classify(source2, source4)
    new1.classify(source3, source1)
    new1.classify(source3, source2)
    new1.classify(source3, source4)
    new1.classify(source4, source1)
    new1.classify(source4, source2)
    new1.classify(source4, source3)

    new2.classify(source1, source2)
    new2.classify(source1, source3)
    new2.classify(source1, source4)
    new2.classify(source2, source1)
    new2.classify(source2, source3)
    new2.classify(source2, source4)
    new2.classify(source3, source1)
    new2.classify(source3, source2)
    new2.classify(source3, source4)
    new2.classify(source4, source1)
    new2.classify(source4, source2)
    new2.classify(source4, source3)

    
