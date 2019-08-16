. ".\config.ps1"

docker start $CONTAINER
cacls ./workspace/notebook.sh /g everyone:f
docker exec $CONTAINER nohup /root/workspace/notebook.sh > out.log 2> err.log &
echo "Access 127.0.0.1:$(JUPYTER_PORT) for Jupyter (pass:jupyter)"
