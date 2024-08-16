import psutil
import time

def get_network_usage():
    net_before = psutil.net_io_counters()
    time.sleep(1)  # Wait for 1 second
    net_after = psutil.net_io_counters()
    
    # Calculate bytes sent and received in the last second
    bytes_sent = net_after.bytes_sent - net_before.bytes_sent
    bytes_recv = net_after.bytes_recv - net_before.bytes_recv
    
    # Convert bytes to megabits for easier reading
    bits_sent = bytes_sent * 8
    bits_recv = bytes_recv * 8
    mbps_sent = bits_sent / 1_000_000
    mbps_recv = bits_recv / 1_000_000
    
    return mbps_sent, mbps_recv

def main():
    print("Monitoring network bandwidth...")
    try:
        while True:
            mbps_sent, mbps_recv = get_network_usage()
            print(f"Upload Speed: {mbps_sent:.2f} Mbps | Download Speed: {mbps_recv:.2f} Mbps")
            time.sleep(1)  # Adjust the interval as needed
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

if __name__ == "__main__":
    main()
