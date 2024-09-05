import sys
import re

def validate_fqdn(fqdn):
    # Regular expression to validate a FQDN (very basic validation)
    pattern = r'^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$'
    return re.match(pattern, fqdn, re.IGNORECASE)

def get_dns_record_type(type_name):
    # Dictionary of DNS record types
    record_types = {
        'A': b'\x00\x01',      # IPv4 address
        'AAAA': b'\x00\x1c',   # IPv6 address
        'MX': b'\x00\x0f',     # Mail exchange
        'TXT': b'\x00\x10',    # Text record
        'CNAME': b'\x00\x05'   # Canonical name
    }
    return record_types.get(type_name.upper())

def create_dns_query(fqdn, record_type='A'):
    if not validate_fqdn(fqdn):
        raise ValueError("Invalid FQDN provided.")
    if (dns_type := get_dns_record_type(record_type)) is None:
        raise ValueError("Invalid DNS record type provided.")
    
    # Header section
    transaction_id = b'\x1a\x2b'  # Example transaction ID
    flags = b'\x01\x00'           # Standard recursive query
    question_count = b'\x00\x01'  # One question
    answer_rcount = b'\x00\x00'   # No answers
    authority_rcount = b'\x00\x00'
    additional_rcount = b'\x00\x00'

    # Construct the question section
    labels = fqdn.split('.')
    domain_name = b''.join(len(label).to_bytes(1, 'big') + label.encode() for label in labels) + b'\x00'
    
    # Combine all parts into one byte array
    dns_query = (transaction_id + flags + question_count + answer_rcount +
                 authority_rcount + additional_rcount + domain_name + dns_type + b'\x00\x01')
    
    return dns_query

def main():
    if len(sys.argv) < 2:
        print("Usage: makebin.py <FQDN> [Record Type]")
        sys.exit(1)
    
    fqdn = sys.argv[1]
    record_type = sys.argv[2] if len(sys.argv) > 2 else 'A'
    
    try:
        dns_query = create_dns_query(fqdn, record_type)
        # Filename formatted with FQDN and record type
        filename = f"{fqdn.replace('.', '-')}_query-{record_type.upper()}.bin"
        # Save to a .bin file
        with open(filename, 'wb') as file:
            file.write(dns_query)
        print(f"DNS query for {fqdn} saved to '{filename}'")
    except ValueError as e:
        print(e)

if __name__ == '__main__':
    main()

