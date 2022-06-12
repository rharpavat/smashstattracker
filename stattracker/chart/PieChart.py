from pychartjs import BaseChart, ChartType, Color                                     

class PieChart(BaseChart):

    def __init__(self, datalist, labellist):
        self.data.data = datalist
        self.labels.grouped = labellist

    type = ChartType.Pie

    class data:
        backgroundColor = ["#ea5545", "#f46a9b", "#ef9b20", "#edbf33", "#ede15b", "#bdcf32", "#87bc45", "#27aeef", "#b33dc6"]
    
    class options:
        legend = {
            'position': 'right'
        }
        responsive: True