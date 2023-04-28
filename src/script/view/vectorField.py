
import numpy as np
import plotly.figure_factory as ff

def viewVectorField(x, y, u, v, figurepath, isVisualize=False):

    # USAGE: 
    # x_mesh,y_mesh = np.meshgrid(np.arange(-2, 2, 0.2), np.arange(-2, 0, 0.2))
    # u_mesh = np.sin(x_mesh)
    # v_mesh = np.cos(y_mesh)
    # viewVectorField(x = x_mesh,
    #                 y = y_mesh,
    #                 u = u_mesh,
    #                 v = v_mesh
    #                 figurepath = "../figures/my_figure.html")
    #
    # NOTE: https://ai-research-collection.com/plotly-quiver-plots/

    fig = ff.create_quiver(x, y, u, v)
    if isVisualize:
        fig.show()
    fig.write_html(figurepath)

if __name__ == "__main__":
    x_mesh,y_mesh = np.meshgrid(np.arange(-2, 2, 0.2), np.arange(-2, 0, 0.2))
    u_mesh = np.tan(x_mesh)
    v_mesh = np.cos(y_mesh)
    viewVectorField(x = x_mesh,
                    y = y_mesh,
                    u = u_mesh,
                    v = v_mesh,
                    figurepath = "../figures/my_figure.html")