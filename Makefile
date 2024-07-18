setup:
	pip install -e ".[dev]"
	cd dbt_project
	dbt deps 
	cd ..

startMinio:
	 docker run -p 9000:9000 -p 9001:9001 --name minio1 -e "MINIO_ROOT_USER=youraccesskey" -e "MINIO_ROOT_PASSWORD=yoursecretkey" minio/minio server /data --console-address ":9001"