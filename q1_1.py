import random

class Simulator:
    def __init__(self, noc_frequency):
        self.noc_frequency = noc_frequency
        self.cpu_buffer_size = 100
        self.io_buffer_size = 100
        self.system_memory_latency = 10  # Example value for memory read latency
        self.cpu_arbitration_rate = 0.5  # Example value for CPU arbitration rate
        self.io_arbitration_rate = 0.5  # Example value for IO arbitration rate

    def generate_monitor_output(self, num_transactions):
        output = "Timestamp TxnType Data (32B)\n"
        timestamp = 0
        for _ in range(num_transactions):
            txn_type = random.choice(['Rd', 'Wr'])
            if txn_type == 'Rd':
                data = '-'
                latency = self.system_memory_latency
            else:
                data = ''.join(random.choices('0123456789abcdef', k=8))  # Example data for write transaction
                latency = random.randint(1, 10)  # Randomize write latency
            output += f"{timestamp} {txn_type} {data}\n"
            timestamp += latency * self.noc_frequency  # Convert latency to cycles based on NOC frequency
        return output

    def get_buffer_occupancy(self, buffer_id):
        # Simulate buffer occupancy
        if buffer_id == 'CPU':
            return random.randint(0, self.cpu_buffer_size)
        elif buffer_id == 'IO':
            return random.randint(0, self.io_buffer_size)
        else:
            return 0  # Placeholder for other buffers

    def get_arbrates(self, agent_type):
        # Simulate arbitration rates
        if agent_type == 'CPU':
            return self.cpu_arbitration_rate
        elif agent_type == 'IO':
            return self.io_arbitration_rate
        else:
            return 0  # Placeholder for other agents

    def get_powerlimit_threshold(self):
        # Simulate power threshold (random values for demonstration)
        return random.choice([0, 1])

# Example usage
simulator = Simulator(noc_frequency=1)  # Assuming NOC frequency is 1 cycle per second

# Generate monitor output
monitor_output = simulator.generate_monitor_output(10)
print("Generated Monitor Output:")
print(monitor_output)

# Access buffer occupancy and arbitration rate
cpu_buffer_occupancy = simulator.get_buffer_occupancy('CPU')
io_arbitration_rate = simulator.get_arbrates('IO')

print("\nCPU Buffer Occupancy:", cpu_buffer_occupancy)
print("IO Arbitration Rate:", io_arbitration_rate)


###########################################################################################################################3
# Utility function to parse monitor output
class Transaction:
    def __init__(self, timestamp, txn_type, data=None):
        self.timestamp = timestamp
        self.txn_type = txn_type
        self.data = data


def parse_monitor_output(output):
    transactions = []
    lines = output.split('\n')
    for line in lines[1:]:  # Skip header line
        if line.strip():  # Check if the line is not empty
            parts = line.split(' ')
            if len(parts) >= 3:  # Check if the line contains enough parts
                timestamp = int(parts[0])
                txn_type = parts[1]
                data = ' '.join(parts[2:]) if len(parts) > 2 else None
                transactions.append(Transaction(timestamp, txn_type, data))
            else:
                print("Invalid line format:", line)
    return transactions



def calculate_latency(transactions):
    read_timestamps = []
    total_latency = 0
    total_reads = 0
    for txn in transactions:
        if txn.txn_type == 'Rd':
            read_timestamps.append(txn.timestamp)
        elif txn.txn_type == 'Wr':
            if read_timestamps:
                read_timestamp = read_timestamps.pop(0)
                latency = txn.timestamp - read_timestamp
                total_latency += latency
                total_reads += 1
    average_latency = total_latency / total_reads if total_reads > 0 else 0
    return average_latency


def calculate_bandwidth(transactions):
    if not transactions:
        return 0

    total_data_transferred = 0
    start_time = transactions[0].timestamp
    end_time = transactions[-1].timestamp
    total_time = end_time - start_time

    for txn in transactions:
        if txn.txn_type == 'Wr':
            total_data_transferred += len(txn.data) if txn.data else 0
    bandwidth = total_data_transferred / total_time if total_time > 0 else 0
    return bandwidth


# Example usage
simulator = Simulator(noc_frequency=1)  # Assuming NOC frequency is 1 cycle per second
monitor_output = simulator.generate_monitor_output(10)
print("Generated Monitor Output:")
print(monitor_output)

# Parse monitor output
transactions = parse_monitor_output(monitor_output)

# Calculate average latency
average_latency = calculate_latency(transactions)
print("\nAverage Latency:", average_latency)

# Calculate bandwidth
bandwidth = calculate_bandwidth(transactions)
print("Bandwidth:", bandwidth)


"""class System:
    def __init__(self):
        self.cpu = CPU()
        self.io_peripheral = IOPeripheral()
        self.system_memory = SystemMemory()
        self.noc = NetworkOnChip(self.cpu, self.io_peripheral, self.system_memory)
        self.throttle_probability = 0.05  # Throttling probability (5%)

    def run_simulation(self, num_cycles, min_latency, max_bandwidth):
        total_throttling_cycles = 0
        for cycle in range(num_cycles):
            # Generate traffic patterns (reads and writes) on CPU and IO Peripheral
            cpu_traffic = self.cpu.generate_traffic()
            io_traffic = self.io_peripheral.generate_traffic()

            # Route traffic through NOC
            self.noc.route_traffic(cpu_traffic)
            self.noc.route_traffic(io_traffic)

            # Simulate memory access latency
            self.system_memory.process_requests()

            # Monitor buffer occupancy and adjust as needed
            self.noc.adjust_buffer_sizes()

            # Adjust arbiter weights based on workload and traffic patterns
            self.noc.adjust_arbiter_weights()

            # Throttle based on power threshold
            if self.noc.get_powerlimit_threshold() and random.random() < self.throttle_probability:
                self.noc.throttle()

            # Check if requirements are met
            if (self.system_memory.get_latency() <= min_latency and
                    self.noc.get_bandwidth() >= 0.95 * max_bandwidth and
                    self.noc.get_buffer_occupancy() >= 0.9):
                print("Optimal NOC design achieved.")
                break
"""
