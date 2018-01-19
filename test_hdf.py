import pandas as pd
import numpy as np

def convert_with_excel():
  xls_file = pd.ExcelFile('mitos.xls')
  df = xls_file.parse('Sheet1')    # this is dataframe
  print(df.iloc[0,:])
  df.drop(df.columns[[0, 1, 3]], axis=1, inplace=True)
  print(df.iloc[0,:])
  
  writer = pd.ExcelWriter('mitos_013.xls')
  df.to_excel(writer, 'DataFrame')
  writer.save()

def create_dataframe():
  data = np.array([ ['',      'Col1', 'Col2'],
                    ['Row1',  1,      2],
                    ['Row2',  3,      4],
                 ])  
  df = pd.DataFrame(data=data[1:,1:], index=data[1:,0],  columns=data[0,1:])
  print(df)
  print(df["Col1"])       # column 1
  print(df.loc["Row1"]["Col1"])  
  print(df.iloc[0][0])  
  print(df["Col1"])   # access a col
  print(df.loc["Row1"]  )   # access a rowl
  # add row
  df.loc["Row3"] = [5,6]
  # add col
  df["Col3"] = [7,8,9]
  print(df)

  # if index or columns are not set, it will be 0, 1, 2, 3, ...
  df1 = pd.DataFrame(data=np.array([[1,2],[3,4]]))
  print(df1)
  
  writer = pd.ExcelWriter('test.xls')
  df.to_excel(writer, 'DataFrame')
  writer.save()

def test_with_hdf5():
  data = np.array([[3,4],[5,6]])
  index = ["R1", "R2"]
  cols = ["C1", "C2"]
  df = pd.DataFrame(data=data, index=index, columns=cols) 
  # df = pd.DataFrame(data=data, columns=cols) 
  print(df)

  hdf = pd.HDFStore('test.h5', 'w', append=True)
  # dataframe df as stored in hdf as d1
  hdf.put('d1', df, format='table', data_columns=True)
  print(hdf["d1"])

  # add more data in df with hdf
  idx1 = ["R3", "R4"]
  df1 = pd.DataFrame(np.array([[5,6],[7,8]]), columns=cols, index=idx1)
  hdf.append('d1', df1, format='table', data_columns=True)
  print(hdf["d1"])

  df = pd.DataFrame(np.random.rand(5,5))
  print(df)
  hdf.put('d2', df)

  se = pd.Series(np.random.randn(5))
  hdf.put('s1', se)

  print("hdf: ", hdf)

  hdf.close()

  # load some data from hdf5
  hdf = pd.HDFStore("test.h5", 'r')
  print(hdf)
  df = hdf.select('d1', columns=['C2']) 
  print(df)
  df = hdf.select('d1', where=['C2>5'],  columns=['C1', 'C2']) 
  print(df)
  df = hdf.select('d2') 
  print(df)
  se = hdf.select("s1", 

  hdf.close() 
  
# convert_with_excel()
# create_dataframe()
test_with_hdf5()
