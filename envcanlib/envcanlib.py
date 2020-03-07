#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 23:35:15 2019

@author: guilherme
"""

def downloadData(IDs, start, end, method = 'hourly', path = '', dataFormat = 'default', continuous = True):
    '''
    Description: It downloads weather information from the Environment Canada website. 
    It is possible to download daily or hourly information in a slice of time passed as an argument.
    
    Input: IDs:  list of the target stations IDs.
    
           start: A tuple with start year and start month.
           
           end: A tuple with end year and end month.
           
           method: 'hourly' for hourly information (default) or 'daily' for daily information.
           
           path: Path in the machine to save the data downloaded. Default is the path where the code is running.
           
           dataFormat: 'default' (each station has its own file) or 'oneFile' (just one file for all stations).
    '''
    
    import pandas as pd
    import urllib.request as url
    
    if start[0] > end[0]:
        raise ValueError('Start year is greater than end year')
    if start[0] == end[0] and start[1] > end[1]:
        raise ValueError('Start month is greater than end month')
    
    if method == 'hourly':
        method  = "&timeframe=1&submit=Download+Data"
    elif method == 'daily':
        method  = "&timeframe=2&submit=Download+Data"
    else:
        print('method = ' + method + 'is not valid.')
        print('avalible methods are "h" or "d".')
    
    if dataFormat == 'default':
        for ID in IDs:
            data = pd.DataFrame([])
            for intYr in range(start[0], end[0]+1):
                if continuous:
                    if intYr == start[0]:
                        if start[0] == end[0]:
                            monthRange = range(start[1], end[1]+1)
                        else:
                            monthRange = range(start[1],13)
                    elif intYr == end[0]:
                        monthRange = range(1, end[1]+1)
                    else:
                        monthRange = range(1, 13)
                else:
                    monthRange = range(start[1],end[1]+1)
                
                if method == "&timeframe=1&submit=Download+Data":
                    for intMnt in monthRange:
                        #build the query
                        strQry = 'http://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID=' + str(ID) + "&Year=" + str(intYr) +'&Month=' + str(intMnt) + method 
                        #print strQry
                        print ('Querying station ' + str(ID) + ' for year ' + str(intYr) + ' and month ' + str(intMnt))
                        try:
                            response = url.urlopen(strQry)
                            rawData = response.readlines()
                            response.close()
                            rawData = [row.decode('utf8').replace('"','').replace('\n','') for row in rawData]
                           
                            columns = rawData[0].split(',')
                            d = [line.split(',') for line in rawData[1:]]
                            
                            for i in range(len(d)):
                                if len(d[i]) > len(columns):
                                    d[i][len(columns)-1] = "".join(d[i][len(columns)-1:])
                                    d[i] = d[i][:len(columns)]
                                    
                                if len(d[i]) < len(columns):
                                    while len(d[i]) < len(columns):
                                        d[i].append('')
                                    
                            newData = pd.DataFrame(d, columns=columns)
                            data = data.append(newData, ignore_index=True, sort=False)
                        except Exception as e:
                            print ('Failure getting data for '  + str(ID) + ' for year ' + str(intYr) + '. ',e)
                else:
                    #build the query
                    strQry = 'http://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID=' + str(ID) + "&Year=" + str(intYr) + method 
                    #print strQry
                    print ('Querying station ' + str(ID) + ' for year ' + str(intYr))
                    try:
                        response = url.urlopen(strQry)
                        rawData = response.readlines()
                        response.close()
                        rawData = [row.decode('utf8').replace('"','').replace('\n','') for row in rawData]
                       
                        columns = rawData[0].split(',')
                        d = [line.split(',') for line in rawData[1:]]
                        
                        for i in range(len(d)):
                            if len(d[i]) > len(columns):
                                d[i][len(columns)-1] = "".join(d[i][len(columns)-1:])
                                d[i] = d[i][:len(columns)]
                                
                            if len(d[i]) < len(columns):
                                while len(d[i]) < len(columns):
                                    d[i].append('')
                                
                        newData = pd.DataFrame(d, columns=columns)
                        data = data.append(newData, ignore_index=True, sort=False)
                        data['Month'] = data['Month'].astype(int)
                        data['Year'] = data['Year'].astype(int)
                        if start[0] != end[0]:
                            data = data[((data['Month'] >= start[1]) & (data['Year'] == start[0]))
                                        | ((data['Year'] != start[0]) & (data['Year'] != end[0]))
                                        | ((data['Month'] <= end[1]) & (data['Year'] == end[0]))]
                        else:
                            data = data[(data['Month'] >= start[1]) & (data['Month'] <= end[1])]
    
                    except Exception:
                        print ('Failure getting data for '  + str(ID) + ' for year ' + str(intYr))
            
            data = data.dropna(axis = 0, how = 'all')
            data.to_csv(path+str(ID)+".csv", index=False, line_terminator="")
            
    else:
        data = pd.DataFrame([])
        for ID in IDs:
            for intYr in range(start[0], end[0]+1):
                if continuous:
                    if intYr == start[0]:
                        if start[0] == end[0]:
                            monthRange = range(start[1], end[1]+1)
                        else:
                            monthRange = range(start[1],13)
                    elif intYr == end[0]:
                        monthRange = range(1, end[1]+1)
                    else:
                        monthRange = range(1, 13)
                else:
                    monthRange = range(start[1],end[1]+1)    
                
                if method == "&timeframe=1&submit=Download+Data":
                    for intMnt in monthRange:
                        #build the query
                        strQry = 'http://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID=' + str(ID) + "&Year=" + str(intYr) +'&Month=' + str(intMnt) + method 
                        #print strQry
                        print ('Querying station ' + str(ID) + ' for year ' + str(intYr) + ' and month ' + str(intMnt))
                        try:
                            response = url.urlopen(strQry)
                            rawData = response.readlines()
                            response.close()
                            rawData = [row.decode('utf8').replace('"','').replace('\n','') for row in rawData]
                           
                            columns = rawData[0].split(',')
                            d = [line.split(',') for line in rawData[1:]]
                            
                            for i in range(len(d)):
                                if len(d[i]) > len(columns):
                                    d[i][len(columns)-1] = "".join(d[i][len(columns)-1:])
                                    d[i] = d[i][:len(columns)]
                                    
                                if len(d[i]) < len(columns):
                                    while len(d[i]) < len(columns):
                                        d[i].append('')
                                    
                            newData = pd.DataFrame(d, columns=columns)
                            newData.insert(0, column='Station ID', value = [ID for i in range(newData.shape[0])])
                            
                            data = data.append(newData, ignore_index=True, sort=False)
                        except Exception as e:
                            print ('Failure getting data for '  + str(ID) + ' for year ' + str(intYr) + '. ',e)
                else:
                    #build the query
                    strQry = 'http://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID=' + str(ID) + "&Year=" + str(intYr) + method 
                    #print strQry
                    print ('Querying station ' + str(ID) + ' for year ' + str(intYr))
                    try:
                        response = url.urlopen(strQry)
                        rawData = response.readlines()
                        response.close()
                        rawData = [row.decode('utf8').replace('"','').replace('\n','') for row in rawData]
                       
                        columns = rawData[0].split(',')
                        d = [line.split(',') for line in rawData[1:]]
                        
                        for i in range(len(d)):
                            if len(d[i]) > len(columns):
                                d[i][len(columns)-1] = "".join(d[i][len(columns)-1:])
                                d[i] = d[i][:len(columns)]
                                
                            if len(d[i]) < len(columns):
                                while len(d[i]) < len(columns):
                                    d[i].append('')
                                
                        newData = pd.DataFrame(d, columns=columns)
                        newData.insert(0, column='Station ID', value = [ID for i in range(newData.shape[0])])
                        
                        data = data.append(newData, ignore_index=True, sort=False)
                        data['Month'] = data['Month'].astype(int)
                        data['Year'] = data['Year'].astype(int)
                        if start[0] != end[0]:
                            data = data[((data['Month'] >= start[1]) & (data['Year'] == start[0]))
                                        | ((data['Year'] != start[0]) & (data['Year'] != end[0]))
                                        | ((data['Month'] <= end[1]) & (data['Year'] == end[0]))]
                        else:
                            data = data[(data['Month'] >= start[1]) & (data['Month'] <= end[1])]
    
                    except Exception:
                        print ('Failure getting data for '  + str(ID) + ' for year ' + str(intYr))
            
        data = data.dropna(axis = 0, how = 'all')
        data.to_csv(path+'allStations.csv', index=False, line_terminator="")        