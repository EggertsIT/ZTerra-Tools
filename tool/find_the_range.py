from ipaddress import ip_network

def read_input_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines() if line.strip()]

def extract_stage_ip_ranges(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    resources = []
    lines = content.split("\n")
    current_resource = None
    for line in lines:
        if line.startswith('resource "zia_location_management"'):
            parts = line.split('"')
            if len(parts) >= 4:
                current_resource = {"name": parts[3], "ip_addresses": []}
                resources.append(current_resource)
        elif "ip_addresses" in line and current_resource:
            ip_addresses = line[line.find("[")+1:line.find("]")].replace('"', '').split(",")
            ip_addresses = [ip.strip() for ip in ip_addresses if ip.strip()]
            current_resource["ip_addresses"].extend(ip_addresses)
    return resources

def find_overlapping_resources(input_networks, resources):
    overlapping_resources = {}

    for resource in resources:
        resource_networks = [ip_network(ip) for ip in resource["ip_addresses"] if ip]
        for input_net in input_networks:
            for resource_net in resource_networks:
                if input_net.overlaps(resource_net):
                    if resource["name"] not in overlapping_resources:
                        overlapping_resources[resource["name"]] = []
                    overlapping_resources[resource["name"]].append((str(input_net), str(resource_net)))
                    break  # Stop checking further if overlap is found for this resource
    return overlapping_resources

def main(input_file_path, stage_file_path):
    input_ip_ranges = read_input_file(input_file_path)
    input_networks = [ip_network(ip_range) for ip_range in input_ip_ranges]
    stage_resources = extract_stage_ip_ranges(stage_file_path)
    overlapping_resources = find_overlapping_resources(input_networks, stage_resources)
    
    if overlapping_resources:
        print("Resources with overlapping IP ranges:")
        for resource, overlaps in overlapping_resources.items():
            print(f"{resource}:")
            for input_range, resource_range in overlaps:
                print(f"  Overlap between input {input_range} and resource {resource_range}")
    else:
        print("No overlapping IP ranges found.")

if __name__ == "__main__":
    input_file_path = 'input.txt' 
    stage_file_path = 'zia_location_management.tf_cidr_stage' 
    main(input_file_path, stage_file_path)
