import os
import numpy as np
from collections import Counter
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.svm import SVC, NuSVC, LinearSVC
import pickle
from sklearn.metrics import confusion_matrix
# Create a dictionary of words with its frequency


def make_Dictionary(train_dir):
    emails = [os.path.join(train_dir, f) for f in os.listdir(train_dir)]
    all_words = []
    for mail in emails:
        with open(mail) as m:
            for i, line in enumerate(m):
                if i == 2:  # Body of email is only 3rd line of text file
                    words = line.split()
                    all_words += words

    dictionary = Counter(all_words)

    list_to_remove = list(dictionary.keys())
    # type(list_to_remove)
    # l = list(list_to_remove)
    for item in list_to_remove:
        if not item.isalpha():
            del dictionary[item]
        elif len(item) == 1:
            del dictionary[item]
    dictionary = dictionary.most_common(3000)

    return dictionary


def extract_features(mail_dir):
    files = [os.path.join(mail_dir, fi) for fi in os.listdir(mail_dir)]
    features_matrix = np.zeros((len(files), 3000))
    docID = 0
    for fil in files:
      with open(fil) as fi:
        for i, line in enumerate(fi):
          if i == 2:
            words = line.split()
            for word in words:
              wordID = 0
              for i,d in enumerate(dictionary):
                if d[0] == word:
                  wordID = i
                  features_matrix[docID,wordID] = words.count(word)
        docID = docID + 1
    return features_matrix


train_dir = 'Text_resources/train-mails'
dictionary = make_Dictionary(train_dir)

# Prepare feature vectors per training mail and its labels

train_labels = np.zeros(702)
train_labels[351:701] = 1
train_matrix = extract_features(train_dir)

# Training SVM and Naive bayes classifier

model1 = MultinomialNB()
model2 = LinearSVC()
model1.fit(train_matrix,train_labels)
model2.fit(train_matrix,train_labels)

filename = '../../../resources/text_resources/MultinomialNB_model.pkl'
pickle.dump(model1, open(filename, 'wb'))
filename = '../../../resources/text_resources/LinearSVC.pkl'
pickle.dump(model2, open(filename, 'wb'))

# Test the unseen mails for Spam
test_dir = 'Text_resources/test-mails'
test_matrix = extract_features(test_dir)
test_labels = np.zeros(260)
test_labels[130:260] = 1
result1 = model1.predict(test_matrix)
result2 = model2.predict(test_matrix)
pos_r1 = 0
neg_r1 = 0
pos_r2 = 0
neg_r2 = 0
for i in range(len(test_labels)):
    if result1[i] == test_labels[i]:
        pos_r1 += 1
    else:
        neg_r1 += 1
    if result2[i] == test_labels[i]:
        pos_r2 += 1
    else:
        neg_r2 += 1
print("Accuracy 1: ", pos_r1/len(test_labels))
print("Accuracy 2: ", pos_r2/len(test_labels))
# print(confusion_matrix(test_labels, result1))
# print(confusion_matrix(test_labels, result2))
