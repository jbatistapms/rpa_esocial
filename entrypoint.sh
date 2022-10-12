if [ $1 = "web" ]; then
    gunicorn -w 4 -b 0.0.0.0:5000 'run:app'
else
    echo "Argument invalid: $1"
fi