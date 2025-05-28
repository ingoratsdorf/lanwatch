import subprocess
import datetime
import logging

arp_args = ""


def scan_iface(iface):
    """Scans a complete interface.
    This function uses the arp-scan command to scan a specified network interface
    """    
    global arp_args
    cmd = ["arp-scan", "-glNx", "-I", iface]

    if arp_args:
        # If arp_args is provided, insert it into the command
        if isinstance(arp_args, list):
            cmd.extend(arp_args)
        else:
            # If arp_args is a string, split it into a list
            arp_args = arp_args.split(" ")
        cmd.insert(-1, arp_args)

    try:
        # Execute the arp-scan command with the specified interface
        out = subprocess.check_output(cmd, text=True)
        logging.debug(f"Scanning interface {iface}")
    except subprocess.CalledProcessError as err:
        # Handle errors in the command execution
        logging.error(f"Error: {err}")
        return ""
    return out


def scan_str(string):
    args = string.split(" ")
    cmd = ["arp-scan"] + args

    try:
        # Execute the arp-scan command with the specified command
        out = subprocess.check_output(cmd, text=True)
        logging.debug(f"Scanning string {string}")
    except subprocess.CalledProcessError as err:
        # Handle errors in the command execution
        logging.error(f"Error: {err}")
        return ""
    return out


def parse_output(text, iface):
    """Parses arp-scan output.
    This function takes the output of arp-scan and parses it to extract host information.
    """    
    found_hosts = []
    lines = text.strip().split("\n")

    for line in lines:
        if line:
            # Split the line into parts, expecting at least 3 columns: IP, MAC, and HW
            parts = line.split("\t")
            if len(parts) >= 3:
                single_host = {
                    "Iface": iface,
                    "IP": parts[0],
                    "Mac": parts[1],
                    "Hw": parts[2],
                    "Date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Now": 1
                }
                found_hosts.append(single_host)

    return found_hosts


def scan(ifaces, args, strs):
    global arp_args
    arp_args = args
    found_hosts = []

    if ifaces:
        interfaces = ifaces.split(" ")

        for iface in interfaces:
            output = scan_iface(iface)
            print(f"Found IPs:\n{output}")
            found_hosts.extend(parse_output(output, iface))

    for string in strs:
        output = scan_str(string)
        logging.debug(f"Found IPs:\n{output}")
        parts = string.split(" ")
        found_hosts.extend(parse_output(output, parts[-1]))

    return found_hosts
