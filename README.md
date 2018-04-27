# Spatan-Network-Tool
## What does the Tool
The tool is for Monitoring Hardware utilization from Many PCs (cluster)




## Start the Tool
Python3 Tool.py

Argument: -s
Start a Client from this PC (optional).

Python3 Client_Script.py -h (host)

Host must be the host (IP) from the PC where your Tool.py script runs.

### Example1

PC 1:
python3 Tool.py -s

Now you See your Hardware utilization from this PC.

### Example2

PC 1:
python3 Tool.py

PC 2:
python3 Client_Script.py -h 192.168.54.37

Now you see on PC1 the Hardware utilization from PC2.
## Requirements
- Phyton3

Tool.py

- curses

Client_Script.py

- cpuinfo
- psutil

Other modules should be allready installed.
