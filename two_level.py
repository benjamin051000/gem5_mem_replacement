import m5
from m5.objects import *
from caches import *
import argparse

import argparse

parser = argparse.ArgumentParser(description='A simple system with 2-level cache.')
parser.add_argument("--binary", default="configs/tutorial/part1/project/bin/matmult.c.o", nargs="?", type=str,
                    help="Path to the binary to execute.")
parser.add_argument("--l1i_size",default="16kB",
                    help=f"L1 instruction cache size. Default: 16kB.")
parser.add_argument("--l1d_size",default="64kB",
                    help="L1 data cache size. Default: Default: 64kB.")
parser.add_argument("--l1i_assoc",default=2,
                    help="Default: 2.")
parser.add_argument("--l2_size",default="256kB",
                    help="L2 cache size. Default: 256kB.")
parser.add_argument("--rp",default="LRU",
                    help="replacement policy")

options = parser.parse_args()

system = System()

#clock 
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

#memory settings
system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('512MB')]

#make the cpu 
system.cpu = TimingSimpleCPU()

#add L1 cache
#connect cpu to l1 cache
system.cpu.icache = L1ICache(options)
system.cpu.dcache = L1DCache(options)

#connect l1 cache to cpu
system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

#set up L2 cache 
system.l2bus = L2XBar()
system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)

system.l2cache = L2Cache(options)
system.l2cache.connectCPUSideBus(system.l2bus)

#connect l2 to main memory bus
system.membus = SystemXBar()
system.l2cache.connectMemSideBus(system.membus)


#connect io and interrupt controller
system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

system.system_port = system.membus.cpu_side_ports

#memory controller
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

binary = options.binary

#for gem5 V21 and beyond
system.workload = SEWorkload.init_compatible(binary)

process = Process()
process.cmd = [binary]
system.cpu.workload = process
system.cpu.createThreads()

root = Root(full_system = False, system = system)
m5.instantiate()

print("Beginning simulation!")
exit_event = m5.simulate()

print('Exiting @ tick {} because {}'
      .format(m5.curTick(), exit_event.getCause()))
