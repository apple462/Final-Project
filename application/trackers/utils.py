import matplotlib.pyplot as plt

def create_graph(value, timestamp):
        print(timestamp)
        plt.switch_backend('Agg') 
        fig, ax = plt.subplots(figsize = (15, 5))
        ax.plot(timestamp, value)
        plt.xlabel('TimeStamp')
        plt.ylabel('Value')
        fig.savefig("static/graph.png")