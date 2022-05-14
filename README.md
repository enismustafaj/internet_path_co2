# internet-co2

This is a CLI program which measures the carbon intensity value for the routing path to a certain destination. To run the program install the dependencies by running the command:

```
pip3 install -r requirements.txt
```

The tool offers the option to make measurements or to make graphical representation of the data. To make measurements run the following command:

```
python3 ./main --command "traceroute command" --source ./source_files/top_sites_batch1 --output "output file name"
```

To create graphical representation and summary of the data, run the following command:

```
python3 ./main --export "option type" --source ./source_dir --output "output file name"
```
