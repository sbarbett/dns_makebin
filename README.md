# dns_makebin

This is a basic script for generating DNS queries in binary format, for testing purposes. 

## Usage

Enter a hostname followed by an (optional) DNS record type. If no DNS record type is specified, the default will be A.

```
% python makebin.py           
Usage: makebin.py <FQDN> [Record Type]
% python makebin.py google.com
DNS query for google.com saved to 'google-com_query-A.bin'
% python makebin.py google.com AAAA
DNS query for google.com saved to 'google-com_query-AAAA.bin'
```

### Record Types

I only added a few of the basic record types: A, AAAA, MX, CNAME and TXT. To support others, you will need to update the dictionary in the script, under `get_dns_record_type`.

## License

This project is licensed under the terms of the MIT license. See LICENSE.md for more details.
