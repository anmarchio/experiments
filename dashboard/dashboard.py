import os

import matplotlib.pyplot as plt
from matplotlib_dashboard import MatplotlibDashboard
import pandas as pd, numpy as np
import hvplot.pandas  # noqa

def hvplot_test():
    idx = pd.date_range('1/1/2000', periods=1000)
    df = pd.DataFrame(np.random.randn(1000, 4), index=idx, columns=list('ABCD')).cumsum()
    #df.hvplot()
    df.plot()

def matplot_dashboard():
    # https://pypi.org/project/matplotlib-dashboard/
    plt.figure(figsize=(10, 10))

    dashboard = MatplotlibDashboard([
        ['top', 'top', 'top', 'top'],
        ['left', 'left', None, 'right'],
        ['left', 'left', 'down', 'right'],
    ], as3D=['left'], wspace=0.5, hspace=0.5)

    import numpy as np
    dashboard['top'].plot(np.random.rand(200), color='red')
    dashboard['top'].set_ylabel('y')
    dashboard['top'].set_xlabel('x')
    dashboard['top'].set_title('top plot')

    dashboard['right'].bar(['A', 'B', 'C'], [10, 35, 17], color='blue')
    dashboard['right'].set_ylabel('freq')
    dashboard['right'].set_xlabel('label')
    dashboard['right'].set_title('right bar')

    from PIL import Image
    img = os.path.join("C:\\","dev","experiments", "test_api","results","202301010003_incompl","Images","0","16.bmp.jpg")
    dashboard['down'].imshow(Image.open(img))
    dashboard['down'].get_xaxis().set_ticks([])
    dashboard['down'].get_yaxis().set_ticks([])
    dashboard['down'].set_title('down image')

    z = ((5 - np.arange(100) % 10) ** 3).reshape(10, 10)
    x, y = np.meshgrid(np.arange(z.shape[0]), np.arange(z.shape[1]))
    dashboard['left'].plot_surface(x, y, z, color='green')
    dashboard['left'].set_ylabel('x')
    dashboard['left'].set_xlabel('y')
    dashboard['left'].set_zlabel('z')
    dashboard['left'].set_title('left surface')

    plt.show()


def main():
    matplot_dashboard()


if __name__ == '__main__':
    main()
