# hurt-chrup-integration
Integration of products between terra-natur wholesale and Chrup Na Zdrowie shop.
This program uses wholesale FTP to fetch product data and shop API to fetch and update products.
### Preparations
Need to have a notebook.cfg file in root folder wth all wholesale and shop credentials based on [secrets_template.cfg](secrets_template.cfg)

### Run
To start, run [main.py](main.py)

### CRON
set up cron with command 
`crontab -e` according to file template [here](CRON/crontab)
### Other
There are also Jupyter Notebook scripts located in [jupyter](jupyter) folder for CSV way of sync. You can use [jupyter-starter.sh](jupyter/jupyter-starter.sh) to start local installation. 

Temporary folder with data files from wholesale is in [data_files](data_files) folder.

Logs are here: [logs](logs)
