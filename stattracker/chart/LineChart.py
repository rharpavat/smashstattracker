from pychartjs import BaseChart, ChartType, Color                                     

class LineChart(BaseChart):

    type = ChartType.Line

    class data:
        backgroundColor = ["#ea5545", "#f46a9b", "#ef9b20", "#edbf33", "#ede15b", "#bdcf32", "#87bc45", "#27aeef", "#b33dc6"]
    
    class options:
        legend = {
            'position': 'right'
        }
        responsive: True