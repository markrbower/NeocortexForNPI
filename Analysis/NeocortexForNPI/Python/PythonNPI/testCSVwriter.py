# https://docs.python.org/3/library/csv.html
import csv
import io
import numpy as np

data = np.array( [[1,2,3],[4,5,6],[7,8,9]])

with io.StringIO() as csvfile:
    writer = csv.writer(csvfile)
    for row in data:
        writer.writerow(row)
    print(csvfile.getvalue())

