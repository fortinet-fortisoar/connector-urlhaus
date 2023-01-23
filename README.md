# connector-urlhaus
URLhaus Abuse.ch connector for FortiSOAR

Descriptions:
This connector to fetch live bad URLs (only) and ingest into its module. 
Sharing here for review . https://urlhaus.abuse.ch/api/#csv

**Connector has below actions:**

1. query_ip >> It queries a single IPv4 or IPv6 address
2. query_domain >> It queries a single fully qualified domain name (FQDN)
3. query_hash >> It queries MD5 or SHA256 hash
4. query_url >> It queries an exact match URI / URL
5. submit_url >> It submits an exact match URI / URL (**TODO**)
6. get_feed >> It fetches daily active / live malicious URLs

Configuration: 

1. Submit URL Address = https://urlhaus.abuse.ch/
2. Search IOC Address = https://urlhaus-api.abuse.ch/
3. URLhaus API KEY = Go to https://urlhaus.abuse.ch/api/login/ >> use your twitter account to register and get API KEY, its free to use, no limit.
4. 
![image](https://user-images.githubusercontent.com/764987/213965775-564e7a3d-6af2-4139-8e27-8154f1b911dc.png)

5. API Key is only required to submit malicious full URL.
6. https://urlhaus-api.abuse.ch/ for searching IOCs like, full URL, domain/hostname/ip, hash (md5/sha256)
7. https://urlhaus.abuse.ch/api for feed ingestion


