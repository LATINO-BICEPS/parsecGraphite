# What is this?

![](https://i.imgur.com/EKjvtTU.png)

This is a Python script that will send the current status of Parsec on the computer that it is installed on set to run every 5 seconds.

# Installation

Run `parse.py` in `C:\ProgramData\Parsec` where the `log.txt` file resides. Modify the IP address as necessary. Make a shortcut to run on startup inside of `shell:startup`.

In the panel settings, set `Connect null values` to `always` to cover up the missing points when you initially connect to the host. 

A sample dashboard `sampleGrafanaDash.json` has been included. Simply import it directly into Grafana.

# Limitations

As it is run on the same machine as the Parsec host, it will only be able to send data when it is online. When the host is shutdown, there will be null fields that Grafana cannot make a graph with - creating an air gap between data:

![](https://i.imgur.com/FspFZI7.png)

My bandaid solution for the time being is to run a simple ping script, locally on the Graphite server, that is run every 5 seconds that will set each record to 0 if the Parsec host is offline. 

A more ideal solution would be to run the script entirely on the Graphite server mounting the `C:\ProgramData\Parsec` via SMB/CIFS to avoid the mess of running 2 different scripts doing the same thing.

***