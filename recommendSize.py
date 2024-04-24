from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np

def recommendGridSize(width: int, height:int):
    np.random.seed(42)
    widths = np.random.randint(800, 2000, 1000)
    heights = np.random.randint(600, 1500, 1000)

    sizes = np.maximum(widths, heights)
    gaps = np.where(sizes>1080 , 100, 50)
    grid_size = np.arange(0,sizes.max()+1,gaps)

    x = np.column_stack((widths, heights))
    y = np.column_stack((sizes / 10).astype(int) % 10 == 0)

    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    gap = model.predict([[width, height]])[0]
    return [i for i in range(0, max(width, height) + 1, int(gap)) if i % 10 == 0]


photo_width = 1200
photo_height = 800
recommended_sizes = recommendGridSize(photo_width, photo_height)
print(recommended_sizes)