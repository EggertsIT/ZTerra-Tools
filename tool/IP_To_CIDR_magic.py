import re
import ipaddress

def find_cidr_for_range(start_ip, end_ip):
    start = ipaddress.IPv4Address(start_ip)
    end = ipaddress.IPv4Address(end_ip)
    cidrs = list(ipaddress.summarize_address_range(start, end))
    return [str(cidr) for cidr in cidrs]

def replace_ip_range_with_cidr(line, line_number):
    ip_range_pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})-(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    matches = re.findall(ip_range_pattern, line)
    changes = []
    if matches:
        for start_ip, end_ip in matches:
            original_range = f"{start_ip}-{end_ip}"
            cidrs = find_cidr_for_range(start_ip, end_ip)
            cidr_str = ', '.join([f'{cidr}' for cidr in cidrs])
            line = re.sub(f"{start_ip}-{end_ip}", cidr_str, line, 1)
            changes.append((line_number, original_range, cidr_str))
    return line, changes

input_file_path = './zia_location_management.tf'
output_file_path = './zia_location_management.tf_cidr_stage'

all_changes = []

with open(input_file_path, 'r') as file:
    lines = file.readlines()

modified_lines = []
for line_number, line in enumerate(lines, start=1):
    modified_line, changes = replace_ip_range_with_cidr(line, line_number)
    modified_lines.append(modified_line)
    all_changes.extend(changes)

with open(output_file_path, 'w') as file:
    file.writelines(modified_lines)

for change in all_changes:
    print(f"Changed line {change[0]}: from '{change[1]}', to '{change[2]}'")

print(f"File {output_file_path} has been modified and saved.")
