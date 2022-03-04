import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
  
def create_graph(value, timestamp):
    # data = {
    #     "value": value,
    #     "timestamp": timestamp
    # }
    
    # df = pd.DataFrame(data)
    # print(df)

    # fig, ax = plt.subplots(figsize =(10, 7))
    # df.plot(x="timestamp", y="value", kind="line")
    # plt.xlabel('Timestamp')
    # plt.ylabel('Value')
    # # plt.show()
    # plt.savefig('../../static/histogram.png')

    
    fig, ax = plt.subplots(figsize =(10, 7))
    ax.plot(x=timestamp, y=value, kind="line")
    plt.xlabel('Marks')
    plt.ylabel('Frequency')
    # plt.show()
    fig.savefig('../../static/histogram.png')