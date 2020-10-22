osascript -e 'tell app "Terminal" to do script "docker exec -it spark1 python init.py"' &
​
osascript -e 'tell app "Terminal" to do script "docker exec -it spark2 python init.py"' &
​
osascript -e 'tell app "Terminal" to do script "docker exec -it spark3 python init.py"' &