echo "Downloading dump..."
echo "Database creation..."
mysql -u root -e "DROP DATABASE IF EXISTS magento;"
mysql -u root -e "CREATE DATABASE magento;"
echo "Dump to db..."
bunzip2 -f dump.sql.bz2
mysql -u root magento < dump.sql
rm dump.sql
mysql -u root magento -e "UPDATE core_config_data SET value = 'http://magento.dev/' WHERE PATH = 'web/unsecure/base_url'"
mysql -u root magento -e "UPDATE core_config_data SET value = 'http://magento.dev/' WHERE PATH = 'web/secure/base_url'"
