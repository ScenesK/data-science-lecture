docker start dslec
chmod 777 workspace/notebook.sh
docker exec dslec nohup /root/workspace/notebook.sh > out.log 2> err.log &
echo 'Access 127.0.0.1:8888 for Jupyter (pass:jupyter)'