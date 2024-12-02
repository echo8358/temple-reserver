echo "starting"
cd /home/temple-reserver/temple-reserver
source ./venv/bin/activate
while :
do
	echo "running program"
	date +%Y-%m-%d_%H:%M:%S
	python3 ./main.py > ./log.log
	echo "sleeping 15m"
	sleep 15m
	i=$(((RANDOM)%300))
	echo "waiting for an additional $i seconds"
	sleep $i
done
