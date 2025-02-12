# -*- coding: utf-8 -*-
"""TextAnalisys.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1AsLrVhby7evHdKuCvQuuvy4rGZCfhF0B
"""

import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Загрузка необходимых ресурсов NLTK
nltk.download('punkt')
nltk.download('stopwords')

# Определение стоп-слов и стеммера для русского языка
stop_words = set(stopwords.words('russian'))
stemmer = SnowballStemmer("russian")

# Функция предварительной обработки текста
def preprocess_text(text):
    tokens = nltk.word_tokenize(text, language='russian')
    tokens = [token.lower() for token in tokens if token.isalnum()]
    tokens = [stemmer.stem(token) for token in tokens if token not in stop_words]
    return ' '.join(tokens)


documents = [
    """Экономика России включает как государственный, так и частный сектор.
    За последние годы страна прошла через несколько экономических кризисов, но смогла адаптироваться к новым условиям.
    На сегодняшний день Россия является одной из крупнейших экономик мира по объему ВВП, а также крупным экспортером природных ресурсов.""",

    """Промышленность России включает добычу полезных ископаемых, производство товаров и услуг.
    Одной из важнейших отраслей является нефтегазовая промышленность, которая приносит значительную часть доходов государства.
    Также развиты металлургия, химическая промышленность, машиностроение и сельское хозяйство.""",

    """Финансовый сектор России представлен банками, страховыми компаниями, фондовыми биржами и другими финансовыми институтами.
    Центральный банк России выполняет функцию регулирования финансовой системы и денежно-кредитной политики.
    В последние годы наблюдается рост цифровых финансовых технологий и активное внедрение инноваций.""",

    """Внешняя торговля России играет важную роль в экономике страны.
    Экспорт природных ресурсов, таких как нефть, газ, металлы и зерно, составляет значительную часть внешнеторгового оборота.
    В то же время Россия импортирует оборудование, технологии, продовольствие и другие товары.""",

    """Социально-экономическое развитие России сопровождается изменениями в уровне жизни населения.
    Государство проводит политику по улучшению социальных стандартов, здравоохранения, образования и пенсионного обеспечения.
    Однако существуют и вызовы, связанные с демографической ситуацией и неравенством доходов.""",

    """Транспортная система России включает железные дороги, автомобильные дороги, водные пути и воздушный транспорт.
    Россия обладает одной из самых протяженных железнодорожных сетей в мире, обеспечивая транспортировку грузов и пассажиров на большие расстояния.
    Автомобильные дороги связывают крупные города и регионы страны.""",

    """Энергетический сектор России основывается на использовании природных ресурсов, таких как нефть, газ, уголь и гидроэнергетика.
    Россия является одним из ведущих мировых производителей и экспортеров нефти и природного газа.
    Значительная часть электроэнергии производится на тепловых и гидроэлектростанциях.""",

    """Образовательная система России охватывает дошкольное, школьное, среднее профессиональное и высшее образование.
    В стране действует большое количество университетов и научных институтов, предлагающих разнообразные программы обучения.
    Образование играет ключевую роль в социально-экономическом развитии страны.""",

    """Здравоохранение в России включает государственные и частные медицинские учреждения.
    В стране функционирует разветвленная система больниц, поликлиник и специализированных медицинских центров.
    Государство активно инвестирует в развитие здравоохранения и улучшение качества медицинских услуг.""",

    """Культура России богата и разнообразна, включает литературу, музыку, театр, изобразительное искусство и кино.
    В стране множество музеев, театров, концертных залов и библиотек, представляющих богатое культурное наследие.
    Российская культура имеет значительное влияние на мировую культуру.""",
]


# Предварительная обработка документов
processed_docs = [preprocess_text(doc) for doc in documents]
print("Предварительно обработанные документы:")
print(processed_docs)

# Вычисление TF-IDF
def compute_tfidf(docs):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(docs)
    return X, vectorizer.get_feature_names_out()

tfidf_matrix, feature_names = compute_tfidf(processed_docs)
print("\nМатрица TF-IDF:")
print(pd.DataFrame(tfidf_matrix.toarray(), columns=feature_names))

# Метод локтя для определения оптимального количества кластеров
def plot_elbow_method(tfidf_matrix):
    num_samples = tfidf_matrix.shape[0]
    max_clusters = min(num_samples, 15)  # Устанавливаем максимум кластеров не больше количества документов
    wcss = []
    for i in range(1, max_clusters + 1):
        kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init='auto', random_state=0)
        kmeans.fit(tfidf_matrix)
        wcss.append(kmeans.inertia_)

    plt.figure(figsize=(10, 7))
    plt.plot(range(1, max_clusters + 1), wcss, marker='o')
    plt.title('Метод локтя')
    plt.xlabel('Количество кластеров')
    plt.ylabel('WCSS (within-cluster sums of squares)')
    plt.show()

plot_elbow_method(tfidf_matrix)

"""Берем количество кластеров, где идет изгиб"""

# Кластеризация текстов
def cluster_texts(X, n_clusters=2):
    kmeans = KMeans(n_clusters=n_clusters, random_state=0, n_init='auto')
    clusters = kmeans.fit_predict(X)
    return clusters

clusters = cluster_texts(tfidf_matrix, n_clusters=6) # Вот тут меняем относительно от количества кластеров
print("\nКластеры документов:")
print(clusters)

# Понижение размерности для визуализации
def reduce_dimensions(X, n_components=2):
    lda = LatentDirichletAllocation(n_components=n_components, random_state=0)
    X_reduced = lda.fit_transform(X)
    return X_reduced

reduced_matrix = reduce_dimensions(tfidf_matrix, n_components=6) # Вот тут меняем относительно от количества кластеров
print("\nПониженная размерность матрицы:")
print(reduced_matrix)

# Визуализация кластеров
def visualize_clusters(reduced_matrix, clusters):
    plt.figure(figsize=(10, 7))
    scatter = plt.scatter(reduced_matrix[:, 0], reduced_matrix[:, 1], c=clusters, cmap='viridis')
    plt.colorbar(scatter)
    plt.xlabel('Dimension 1')
    plt.ylabel('Dimension 2')
    plt.title('Кластеры текстовых документов')
    plt.show()

visualize_clusters(reduced_matrix, clusters)

# Дополнительное использование numpy для обработки данных
def print_statistics(matrix):
    mean_values = np.mean(matrix, axis=0)
    std_dev_values = np.std(matrix, axis=0)
    print("\nСредние значения по столбцам:")
    print(mean_values)
    print("\nСтандартное отклонение по столбцам:")
    print(std_dev_values)

print_statistics(tfidf_matrix.toarray())

def additional_visualizations(tfidf_matrix, clusters):
    df_tfidf = pd.DataFrame(tfidf_matrix.toarray(), columns=feature_names)
    df_tfidf['cluster'] = clusters

    # Распределение кластеров
    plt.figure(figsize=(10, 6))
    sns.countplot(x='cluster', data=df_tfidf)
    plt.title('Распределение документов по кластерам')
    plt.xlabel('Кластеры')
    plt.ylabel('Количество документов')
    plt.show()

additional_visualizations(tfidf_matrix, clusters)

