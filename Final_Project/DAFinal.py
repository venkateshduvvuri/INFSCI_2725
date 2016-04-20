import pandas
import numpy as np
from sklearn.ensemble import RandomForestRegressor, BaggingRegressor
from nltk.stem.snowball import SnowballStemmer

# Snowball Stemmer Object
snowball_stemmer = SnowballStemmer('english')

# Loading each of the csv files into Data Frames
train_data_frame = pandas.read_csv('train.csv', encoding="ISO-8859-1")
test_data_frame = pandas.read_csv('test.csv', encoding="ISO-8859-1")
attributes_data_frame = pandas.read_csv('attributes.csv')
attributes_data_frame = attributes_data_frame[["product_uid", "value"]]
product_desc_data_frame = pandas.read_csv('product_descriptions.csv')

# Getting Dimesion of the Data Frame
num_train = train_data_frame.shape[0]

print(train_data_frame.shape)


# Method for Correcting Typos and Stemming the Word
def string_stemmer(str_stem):
    if isinstance(str_stem, str):
        str_stem = str_stem.lower()
        str_stem = str_stem.replace("'", "in.")
        str_stem = str_stem.replace("inches", "in.")
        str_stem = str_stem.replace("inch", "in.")
        str_stem = str_stem.replace(" in ", "in. ")
        str_stem = str_stem.replace(" in.", "in.")
        str_stem = str_stem.replace("''", "ft.")

        str_stem = str_stem.replace(" feet ", "ft. ")
        str_stem = str_stem.replace("feet", "ft.")
        str_stem = str_stem.replace("foot", "ft.")
        str_stem = str_stem.replace(" ft ", "ft. ")
        str_stem = str_stem.replace(" ft.", "ft.")

        str_stem = str_stem.replace(" pounds ", "lb. ")
        str_stem = str_stem.replace(" pound ", "lb. ")
        str_stem = str_stem.replace("pound", "lb.")
        str_stem = str_stem.replace(" lb ", "lb. ")
        str_stem = str_stem.replace(" lb.", "lb.")
        str_stem = str_stem.replace(" lbs ", "lb. ")
        str_stem = str_stem.replace("lbs.", "lb.")

        str_stem = str_stem.replace("*", " xby ")
        str_stem = str_stem.replace(" by", " xby")
        str_stem = str_stem.replace("x0", " xby 0")
        str_stem = str_stem.replace("x1", " xby 1")
        str_stem = str_stem.replace("x2", " xby 2")
        str_stem = str_stem.replace("x3", " xby 3")
        str_stem = str_stem.replace("x4", " xby 4")
        str_stem = str_stem.replace("x5", " xby 5")
        str_stem = str_stem.replace("x6", " xby 6")
        str_stem = str_stem.replace("x7", " xby 7")
        str_stem = str_stem.replace("x8", " xby 8")
        str_stem = str_stem.replace("x9", " xby 9")

        str_stem = str_stem.replace(" sq ft", "sq.ft. ")
        str_stem = str_stem.replace("sq ft", "sq.ft. ")
        str_stem = str_stem.replace("sqft", "sq.ft. ")
        str_stem = str_stem.replace(" sqft ", "sq.ft. ")
        str_stem = str_stem.replace("sq. ft", "sq.ft. ")
        str_stem = str_stem.replace("sq ft.", "sq.ft. ")
        str_stem = str_stem.replace("sq feet", "sq.ft. ")
        str_stem = str_stem.replace("square feet", "sq.ft. ")

        str_stem = str_stem.replace(" gallons ", "gal. ")  # character
        str_stem = str_stem.replace(" gallon ", "gal. ")  # whole word
        str_stem = str_stem.replace("gallons", "gal.")  # character
        str_stem = str_stem.replace("gallon", "gal.")  # whole word
        str_stem = str_stem.replace(" gal ", "gal. ")  # character
        str_stem = str_stem.replace(" gal", "gal")  # whole word

        str_stem = str_stem.replace(" ounces", "oz.")
        str_stem = str_stem.replace(" ounce", "oz.")
        str_stem = str_stem.replace("ounce", "oz.")
        str_stem = str_stem.replace(" oz ", "oz. ")

        str_stem = str_stem.replace(" centimeters", "cm.")
        str_stem = str_stem.replace(" cm.", "cm.")
        str_stem = str_stem.replace(" cm ", "cm. ")

        str_stem = str_stem.replace(" milimeters", "mm.")
        str_stem = str_stem.replace(" mm.", "mm.")
        str_stem = str_stem.replace(" mm ", "mm. ")
        return " ".join([snowball_stemmer.stem(word) for word in str_stem.lower().split()])
    else:
        return str_stem


# Finding the No. of Common Words between 2 given Strings
def string_common_word_count(str1, str2):
    if isinstance(str1, str) and isinstance(str2, str):
        return sum(int(str2.find(word) >= 0) for word in str1.split())
    else:
        return 0

# Concatinating Training and Testing Data
final_data_frame = pandas.concat((train_data_frame, test_data_frame), axis=0, ignore_index=True)

# Merge Product Desciptions into the Above Data Frame
final_data_frame = pandas.merge(final_data_frame, product_desc_data_frame, how='left', on='product_uid')

# Merge Attributes into the Above Data Frame
final_data_frame = pandas.merge(final_data_frame, attributes_data_frame, how='left', on='product_uid')

# Storing the Result of Stemming(Search Term) back into the Data Frame
final_data_frame['search_term'] = final_data_frame['search_term'].map(lambda x: string_stemmer(x))

# Stemming Product Title
final_data_frame['product_title'] = final_data_frame['product_title'].map(lambda x: string_stemmer(x))

# Stemming Product Description
final_data_frame['product_description'] = final_data_frame['product_description'].map(lambda x: string_stemmer(x))

# Stemming Attribute Value
final_data_frame['value'] = final_data_frame['value'].map(lambda x: string_stemmer(x))

# Storing Length of the Query in a different Column in the same Data Frame
final_data_frame['len_of_query'] = final_data_frame['search_term'].map(lambda x: len(x.split())).astype(np.int64)

# Storing the Combination of Search Term, Product Title & Product Description(Stemmed) in a New Column
final_data_frame['product_info'] = final_data_frame['search_term'] + "\t" + \
                                   final_data_frame['product_title'] + "\t" + \
                                   final_data_frame['product_description'] + \
                                   final_data_frame['value']

final_data_frame['ratio_title'] = final_data_frame['word_in_title'] / final_data_frame['len_of_query']
final_data_frame['ratio_description'] = final_data_frame['word_in_description'] / final_data_frame['len_of_query']


# Storing the No. of Common Words in the Search Query and Product Title
final_data_frame['word_in_title'] = final_data_frame['product_info'].map(
    lambda x: string_common_word_count(x.split('\t')[0], x.split('\t')[1]))

# Storing the No. of Common Words in the Search Query and Product Description
final_data_frame['word_in_description'] = final_data_frame['product_info'].map(
    lambda x: string_common_word_count(x.split('\t')[0], x.split('\t')[2]))

# Storing the No. of Common Words in the Search Query and Attribute Value
final_data_frame['word_in_value'] = final_data_frame['product_info'].map(
    lambda x: string_common_word_count(x.split('\t')[0], x.split('\t')[3]))

#  Final Data Frame used for Regression dropping columns that are not used
data_frame_regression = final_data_frame.drop(['search_term', 'product_title', 'product_description', 'product_info'],
                                              axis=1)

# Getting Training Data out of the DF
train_data_frame = data_frame_regression.iloc[:num_train]

# Getting Testing Data out of the DF
test_data_frame = data_frame_regression.iloc[num_train:]

# Getting IDs for Testing Data
id_test = test_data_frame['id']

relevance_train = train_data_frame['relevance'].values

# All the Independent Variables in the Regressor
# These are Words in Title, Desription, Values
X_train = train_data_frame.drop(['id', 'relevance'], axis=1).values

# Same for Test Data
X_test = test_data_frame.drop(['id', 'relevance'], axis=1).values

# Using RandomForest Regressor
rf = RandomForestRegressor(n_estimators=15, max_depth=6, random_state=0)

# Using Bagging Regressor
clf = BaggingRegressor(rf, n_estimators=45, max_samples=0.1, random_state=25)

# Fit the Training Data to a Model
clf.fit(X_train, relevance_train)

# Predicting the relevance for Testind Data
relevance_pred = clf.predict(X_test)

# Writing the Relevance Values to Submission.csv
pandas.DataFrame({"id": id_test, "relevance": relevance_pred}).to_csv('submission.csv', index=False)
