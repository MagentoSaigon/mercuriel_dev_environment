# mercuriel_dev_environment
(Install a Docker version that is compatible with symlinks (>1.12.1 on Windows))
1. Clone respository
2. Add docker.local point to 127.0.0.1 in your hosts file
3. Go to the docker folder in the repository and run _docker-compose up -d_
4. Run _docker exec -it web_server /bin/bash_
5. In the container run _cd bin && composer install_
6. Open your browser and go to http://docker.local:8080/
7. Install Magento with these settings:
 * Database host: db_server
 * Username: root
 * No password
 * DB Name: magento
 * Check the first three checkboxes (enable charts, skip base URL verification, use webserver rewrite)