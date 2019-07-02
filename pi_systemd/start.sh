
#pid=0;

end_process() {
    # perform cleanup here
    echo "Ctrl-C caught...performing clean up"

    kill $pid 
		     
}
			 


echo "### Starting bt scanner... ###"
systemctl start bt-scanner &
sleep 1
echo "###  Starting the drone... ###"
systemctl start drone & 
sleep 1

echo "###    Displaying logs..   ###"
journalctl -u drone --since now --no-pager -o cat -f &
pid=$!

trap end_process INT TERM
wait $pid

echo "###  Stopping the drone... ###"
systemctl stop drone

echo "### Stopping the scanner.. ###"
systemctl stop bt-scanner

echo "#####  Done, exiting...  #####"
