import pandas as pd
import sqlite3
print pd.__version__
# Ipython Notebook settings

# This is necessary to show lots of columns in pandas 0.12. 
# Not necessary in pandas 0.13.
pd.set_option('display.width', 5000) 
pd.set_option('display.max_columns', 60)

import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (15, 5)


"""-------------------------------------------------------------------------------"""
# dfx = pd.DataFrame()
# df = pd.DataFrame()

con = sqlite3.connect("C:/Users/jdingus/Documents/projects/cnc-data/sql questions/test.db")
df = pd.read_sql("SELECT start_time, stop_time, cnc_id, part1_num, part1_qty, part2_num, part2_qty FROM data LIMIT 100", con)   #,parse_dates=True,index_col='start_time,datetime'
# print df[30:40].to_dict()
# dfx = dfx.from_dict(x)
# print df[24:30]

from pandas.lib import Timestamp
df.start_time = df.start_time.apply(Timestamp)
df.stop_time = df.stop_time.apply(Timestamp)
df['duration'] = df.stop_time - df.start_time
df['t_gap'] = (df['start_time']-df['stop_time'].shift()).fillna(0) # t_gap is elapsed 'not running time' when a start_time begins
df['running'] = df['duration']                
df['not_running'] = df.duration - df.duration
# print df[24:30]

"""---------------------------------------------------------------------------"""
not_running = []
keys = ['start_time','stop_time','part1_num','duration','running','not_running']
for i in range(0, df.shape[0]):
    start_time_0 = df.irow(i)['start_time']
    stop_time_0 = df.irow(i)['stop_time'] 

    if i < df.shape[0]-1: #last i row
        start_time_1 = df.irow(i+1)['start_time']
        stop_time_1 = df.irow(i+1)['stop_time']

    gap_sec = df.irow(i)['t_gap'].astype('timedelta64[s]')
    if gap_sec < 0:
        raise SystemError
    if gap_sec < 11: # No downtime entry needed, rename start_time to previous stop_time
        if not i == 0:
            df.loc[i,'start_time'] = df.loc[(i-1),'stop_time']
    else:           # We need to insert downtime entry
        entry = (df.loc[(i-1),'stop_time'],df.loc[i,'start_time'],'not_running',df.loc[i,'start_time']-df.loc[(i-1),'stop_time'],0,df.loc[i,'start_time']-df.loc[(i-1),'stop_time'])
        entry_dict = dict(zip(keys, entry))
        not_running.append(entry_dict)
dfnot = pd.DataFrame(not_running)
dfnot

"""--------------------------------------------------------------------------"""
# print pd.merge(left=df, right=dfnot, on=['start_time', 'stop_time', 'part1_num', 'duration'], how='outer')

dfx = pd.merge(left=df.reset_index(), right=dfnot.reset_index(), on=['start_time', 'stop_time', 'part1_num', 'duration','running','not_running'], how='outer').set_index(['stop_time'])


dfx.reset_index()

# dfx.reindex(index = ['stop_time'], columns=['part1_num','part1_qty','part2_num','part2_qty','duration','t_gap','running','not_running'])

drop_columns=['index_x','index_y','duration','t_gap','cnc_id'] #Remove unneeded data
dfx.drop(drop_columns, axis=1, inplace=True)
print dfx
raise SystemExit
# dfx.sort().to_clipboard()
# dfx.sort('start_time').to_clipboard()
# dfx.info()
# dfx.head()
# dfx.sort('start_time')[20:40].sort('start_time')

"""---------------------------------------------------------------------------"""
conversion = {'running':'sum','not_running':'sum'}
dfplot = dfx.resample('15min', how=conversion)
dfplot.not_running = dfplot.not_running#.astype('timedelta64[m]')
dfplot.running = dfplot.running#.astype('timedelta64[m]')

# dfplot.plot(kind='bar', stacked=True, ylim=((0,30)))
dfplot

"""--------------------------------------------------------------------------"""
dfnew = pd.read_csv('running_notrunning.csv', sep=',', dialect=None, engine='python', parse_dates=True)
dfnew


