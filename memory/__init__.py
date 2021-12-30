# Copyright (c) 2021 Johnathan P. Irvin
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from curses import halfdelay
from typing import List

from psutil import Process, cpu_percent, virtual_memory, process_iter

from enum import Enum

class OrderBy(Enum):
    """
    Enum for the order by options.
    """
    MEMORY = 0
    CPU = 1

def get_processes(order_by: OrderBy) -> List[Process]:
    """
    Get the processes to display.
    """
    # Get the processes as a list
    processes = list(process_iter())

    # Order the processes
    try:
        if order_by == OrderBy.MEMORY:
            processes = sorted(processes, key=lambda p: p.memory_percent(), reverse=True)
        elif order_by == OrderBy.CPU:
            processes = sorted(processes, key=lambda p: p.cpu_percent(), reverse=True)
    except Exception:
        pass

    return processes

def main(stdscr) -> None:
    """
    Main entry point for the application.
    """
    order_by = OrderBy.MEMORY

    while True:
        # Get the memory usage
        memory = virtual_memory()
        memory_percentage = memory.percent

        # Get the CPU usage
        cpu_percentage = cpu_percent()

        # Print the results
        stdscr.addstr(0, 4, f'Memory Usage: {memory_percentage}%')
        stdscr.addstr(1, 4, f'CPU Usage: {cpu_percentage}%')

        # Get the processes
        processes = get_processes(order_by)

        # Display Processes
        stdscr.addstr(4, 4, 'PID')
        stdscr.addstr(4, 15, 'Name')
        stdscr.addstr(4, 30, 'Memory')
        stdscr.addstr(4, 40, 'CPU')
        stdscr.addstr(5, 4, '-' * 40)

        # Display top 10 processes
        for i, process in enumerate(processes[:10]):
            try:
                pid = process.pid
                name = process.name()
                memory_percentage = process.memory_percent()
                cpu_percentage = process.cpu_percent()

                # Align the text to column, and truncate float
                pid = f'{pid:<5}'
                name = f'{name:<15}'
                memory_percentage = f'{memory_percentage:<10.2f}'
                cpu_percentage = f'{cpu_percentage:<10.2f}'

                # Print the results in proper columns
                stdscr.addstr(i + 7, 4, pid)
                stdscr.addstr(i + 7, 15, name)
                stdscr.addstr(i + 7, 30, memory_percentage)
                stdscr.addstr(i + 7, 40, cpu_percentage)
            except:
                continue

        # Update the screen
        stdscr.refresh()

        # Sleep for a second
        halfdelay(5)
        character = stdscr.getch()
        
        if character == ord('q'):
            break
        elif character == ord('m'):
            order_by = OrderBy.MEMORY
        elif character == ord('c'):
            order_by = OrderBy.CPU
