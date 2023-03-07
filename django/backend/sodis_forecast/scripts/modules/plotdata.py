import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from pandas import DataFrame
import io
import base64

def plotsodisforecast(location: dict, disdata: DataFrame, message: str = None):
    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(8,7))
    fig.suptitle("possible solar disinfection in %s, %s" %(location["city"], location["country"]))
    disdata["actual Radiation"].plot(ax=axes[0], legend=True, color="red")
    #disdata["total Radiation"].plot(ax=axes[0], legend=True, color="brown")
    axes[0].set_ylabel("Irradiance (in W/m²)")
    disdata["Water Temp"].plot(ax=axes[1], legend=True, color="blue")
    disdata["Air Temp"].plot(ax=axes[1], legend=True, color="orange")
    axes[1].set_ylabel("Temperature (in °C)")
    disdata["Log Dis"].plot(ax=axes[2], legend=False, color="green")
    axes[2].set_ylabel("Logarithmic Inactivation")
    axes[2].set_xlabel("Time (in h)")
    if message != None:
        plt.figtext(0.5, 0.005, message, ha="center")
    plt.show()
    #plt.savefig(r'sustainable-drinking-water-treatment-plant\webapp_interface\static\images\sodisplot.png')
    # Convert plot to PNG image
    #pngImage = io.BytesIO()
    #FigureCanvas(fig).print_png(pngImage)
    # Encode PNG image to base64 string
    #pngImageB64String = "data:image/png;base64,"
    #pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')

    #return fig, pngImageB64String