#!/bin/bash

if [ -f .env ]; then
    source .env
else
    echo ".env file not found. Make sure it's in the current directory."
    exit 1
fi

client_ids = ($CLIENT_ID_1, $CLIENT_ID_2, $CLIENT_ID_3, $CLIENT_ID_4, $CLIENT_ID_5, $CLIENT_ID_6, $CLIENT_ID_7, $CLIENT_ID_8, $CLIENT_ID_9, $CLIENT_ID_10, $CLIENT_ID_11, $CLIENT_ID_12, $CLIENT_ID_13, $CLIENT_ID_14, $CLIENT_ID_15, $CLIENT_ID_16, $CLIENT_ID_17, $CLIENT_ID_18, $CLIENT_ID_19, $CLIENT_ID_20)
client_secrets = ($SECRET_1, $SECRET_2, $SECRET_3, $SECRET_4, $SECRET_5, $SECRET_6, $SECRET_7, $SECRET_8, $SECRET_9, $SECRET_10, $SECRET_11, $SECRET_12, $SECRET_13, $SECRET_14, $SECRET_15, $SECRET_16, $SECRET_17, $SECRET_18, $SECRET_19, $SECRET_20)
locations = ("EastUS" "WestUS" "CentralUS" "NorthCentralUS" "SouthCentralUS" "WestEurope")

# Create a resource groups
for location in "${locations[@]}"
do
    az group create --name Ruiz_$location --location $location
done

for i in {0..19}
do

    funcname="proxy_$i"
    
    region_idx=$(( $i % ${#locations[@]} ))
    region=${locations[$region_idx]} 

    client_id=${client_ids[$i]}
    client_secret="SECRET_$i"

    # Create the Function App
    az functionapp create --resource-group Ruiz_$region --name $funcname --consumption-plan-location $region --os-type Linux --runtime python --runtime-version 3.9 --functions-version 3 --disable-app-insights true

    # Set environment variables
    az functionapp config appsettings set --name $funcname --resource-group Ruiz_$region --settings "CLIENT_ID=$client_id" "CLIENT_SECRET=$client_secret"
done

