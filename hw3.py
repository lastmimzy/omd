class CountVectorizer:
    def __init__(self):  # инициализирует созданный объект (class CV)
        self.names = (
            []
        )  # если вызывем get_feature_names сразу, получим пустой список. Без этого - ошибка

    def _fit(self, texts: list):  # служебный метод для внутренних рассчетов
        """
        Метод, который создает список уникальных слов для всего корпуса. 
        """
        self.names = []

        for text in texts:
            for word in text.lower().split():
                if word not in self.names:
                    self.names.append(word)

    def _transform(
        self, texts: list
    ) -> list:  # служебный метод для внутренних рассчетов
        """
        Метод, считающий количество слов в каждом предложении
        """
        result = []
        for text in texts:
            vector = [0] * len(
                self.names
            )  # создаем список нулей длины массива с уникальными словами корпуса
            for word in text.lower().split():
                index = self.names.index(
                    word
                )  # находит индекс слова в массиве уникальных слов
                vector[index] += 1  # счетчик слов по индексу

            result.append(vector)

        return result

    def fit_transform(self, texts: list) -> list:
        """
        Метод, который создает список уникальных слов (через метод fit) 
        и считает слова в каждом предложении (через метод transform)
        """
        self._fit(texts)
        return self._transform(texts)

    def get_feature_names(self) -> list:
        """
        Get feature names list
        """
        return self.names


def main():
    vectorizer = CountVectorizer()

    corpus = [
        "Crock Pot Pasta Never boil pasta again",
        "Pasta Pomodoro Fresh ingredients Parmesan to taste",
    ]

    print(vectorizer.fit_transform(corpus))
    print(vectorizer.get_feature_names())


if __name__ == "__main__":
    main()
