# Image Display module

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.widgets import Button, SpanSelector
from matplotlib_scalebar.scalebar import ScaleBar
import numpy as np
import time
import string
import collections


ButtonParams = collections.namedtuple('bp', ['text', 'x', 'y', 'functioncall'])


class ImageDisplay(object):
    """Display 2d arrays with interactive parameters:
                - Contrast
                - Colormap
                - Axis label
                - Legend
                - Calibration
                - Scalebar
                - Line profile
                - Export"""
    def __init__(self, data_to_display):
        # 2D array to display
        self.image_data = data_to_display
        # Window for image display + matplotlib parameters
        self.fig_image = plt.figure(figsize=(10, 7), dpi=100)
        # Layout figure
        self.gs_fig_image = gridspec.GridSpec(8, 8)

        # Make buttons and assign function calls
        buttons = (
            ButtonParams('Refresh', 0, 0, self.test),
            ButtonParams('Set\nColourmap', 1, 0, self.colourmap_button),
            ButtonParams('Num 2', 2, 0, self.test),
            ButtonParams('Num 3', 3, 0, self.test),
            ButtonParams('Num 4', 4, 0, self.test),
            ButtonParams('Num 5', 5, 0, self.test),
            ButtonParams('Num 6', 6, 0, self.test),
            ButtonParams('Export', 7, 0, self.test)
        )
        self.fig_image_parameter = []

        # Assign button to subplot in figure
        for ii in buttons:
            button = Button(plt.subplot(self.gs_fig_image[ii.x, ii.y]), ii.text)
            button.on_clicked(ii.functioncall)
            self.fig_image_parameter.append(button)

        # Define image axis
        self.ax_image = plt.subplot(self.gs_fig_image[1:-1, 1:-1])
        self.ax_image.set_axis_off()
        self.image = self.ax_image.imshow(self.image_data, cmap='gray')

        # Contrast histogram display and span selector
        self.ax_contrast = plt.subplot(self.gs_fig_image[0, 1:-1])
        self.contrastbins = 256
        self.cmin = np.min(self.image_data)
        self.cmax = np.max(self.image_data)
        self.imhist, self.imbins = np.histogram(self.image_data, bins=self.contrastbins)
        self.plot_contrast_histogram()

        # Colormaps
        self.maps = sorted([m for m in plt.cm.datad if not m.endswith("_r")])
        # (https://scipy.github.io/old-wiki/pages/Cookbook/Matplotlib/Show_colormaps)

        # Show the display window
        plt.show()

    @staticmethod
    def test(event):
        print(event)

    # Button to open colourmap selection window
    def colourmap_button(self, event):
        nummaps = len(self.maps)
        self.cmapfig = plt.figure('Colourmap options, pick one!', figsize=(5, 2 * nummaps))
        self.cmapaxes = {}
        gradient = np.linspace(0, 1, 100) * np.ones((3, 100))

        for mm in range(nummaps):
            corners = [0., mm / float(nummaps), 0.75, 1. / nummaps]
            self.cmapaxes[mm] = plt.axes(corners)
            self.cmapaxes[mm].annotate(self.maps[mm], xy=(0.77, (mm + 0.2) / float(nummaps)),
                                       xycoords='figure fraction', fontsize=11)
            self.cmapaxes[mm].set_axis_off()
            self.cmapaxes[mm].imshow(gradient, cmap=plt.get_cmap(self.maps[mm]))

        self.cmapfig.canvas.mpl_connect('button_press_event', self.colourmap_axis_select)

        plt.show()

    # Set colourmap based on clicking on an axis in the colourmap window
    def colourmap_axis_select(self, event):
        for aa in self.cmapaxes:
            if event.inaxes == self.cmapaxes[aa]:
                self.image.set_cmap(plt.get_cmap(self.maps[aa]))
                self.fig_image.canvas.draw()

    # Function to update image after changing it
    def update_image(self):
        self.image.set_clim(vmin=self.cmin, vmax=self.cmax)

    # Calculates and plots image histogram and connects interactive spanselector
    def plot_contrast_histogram(self):
        self.ax_contrast.cla()
        self.ax_contrast.plot(self.imbins[:-1], self.imhist, color='k')
        self.ax_contrast.set_axis_off()
        self.contrast_span = SpanSelector(self.ax_contrast, self.contrast_span, 'horizontal',
                                          span_stays=True, rectprops=dict(alpha=0.5, facecolor='green'))

    # Function for interactive spanselector for contrast histogram
    def contrast_span(self, cmin, cmax):
        self.cmin = cmin
        self.cmax = cmax
        self.update_image()
