import re
import ipaddress


def cidr_to_ip_range(cidr):
    network = ipaddress.ip_network(cidr, strict=False)
    return f"{network[0]}-{network[-1]}"

def replace_cidrs_with_ip_ranges(line, line_number):
    cidr_pattern = r'"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2})"'
    cidrs = re.findall(cidr_pattern, line)
    changes = []

    for cidr in cidrs:
        ip_range = cidr_to_ip_range(cidr)
        line = line.replace(f'"{cidr}"', f'"{ip_range}"')
        changes.append((line_number, cidr, ip_range))

    return line, changes


input_file_path = './zia_location_management.tf_cidr_stage' 
output_file_path = './zia_location_management.tf'  

all_changes = []

with open(input_file_path, 'r') as file:
    lines = file.readlines()

modified_lines = []
for line_number, line in enumerate(lines, start=1):
    modified_line, changes = replace_cidrs_with_ip_ranges(line, line_number)
    modified_lines.append(modified_line)
    all_changes.extend(changes)

with open(output_file_path, 'w') as file:
    file.writelines(modified_lines)

for change in all_changes:
    print(f"Changed line: {change[0]} from {change[1]} to {change[2]}")

print(f"File {output_file_path} has been modified with IP ranges.")
