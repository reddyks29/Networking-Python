import nmap
begain=75
end=80
target='127.0.0.1'
scanner=nmap.PortScanner()
for i in range(begain,end+1):
    res=scanner.scan(target,str(i))
    res=res['scan'][target]['tcp'][i]['state']
    print(f'port {i} is {res} ')