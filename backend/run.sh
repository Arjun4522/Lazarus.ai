#!/bin/bash

# Run the Python script to extract dependencies
python3 scanner.py

# Check if the Python script ran successfully
if [ $? -eq 0 ]; then
    echo "Python script executed successfully."

    # Compile and run the Go script to fetch CVE details
    go build -o fetch fetch.go

    # Check if the Go build was successful
    if [ $? -eq 0 ]; then
        echo "Go build successful."
        ./fetch
    else
        echo "Go build failed."
    fi
else
    echo "Python script execution failed."
fi

#Scrape retrived data
python3 scrape.py
