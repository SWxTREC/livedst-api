"""
LiveDst API

This is the Lambda function handler to handle the requests coming
into the APIGateway. The module will parse the query parameters,
get the necessary files, and return the data requested in JSON
format to the APIGateway requester.
"""
from datetime import datetime, timedelta, timezone
from pathlib import Path
import json

import h5py


def lambda_handler(event, context):
    """Handle the incoming API event and route properly."""
    # Data is passed in the URL, so pull it out of the query string
    params = event["queryStringParameters"]
    print(params)
    # Get the end_date if it exists. If it isn't there, default to now.
    if params and "end_date" in params:
        end_date = datetime.strptime(params["end_date"], "%Y-%m-%dT%H:%M")
    else:
        end_date = datetime.now()

    # Get the start_date if it exists. If it isn't there, default to t - 7 days.
    if params and "start_date" in params:
        # Parse it if it is present
        start_date = datetime.strptime(params["start_date"], "%Y-%m-%dT%H:%M")
    else:
        # 7 days before if it isn't present
        start_date = end_date - timedelta(days=7)

    # Get the files covering this time period
    data = get_livedst_data(start_date, end_date)

    return {
        "statusCode": 200,
        # JSON needs null not NaN
        # 'body': json.dumps(output.tolist()).replace("NaN", 'null'),
        "body": json.dumps(data),
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "content-type": "application/json",
        },
    }


def get_livedst_data(start_date: datetime, end_date: datetime) -> dict:
    """Load and return data between the start and end date"""
    # Each file is stored at a one-hour cadence, so load each hour
    # between those files and format the return data properly for
    # the frontend.
    one_hour = timedelta(hours=1)
    t = start_date
    data = []
    while t <= end_date:
        # TODO: Open up the files on disk and create the response
        # Make the filepath
        # path = Path(f"/tmp/{datetime.strftime(t, '%Y-%m-%dT%H:%M')}.hdf")
        # if path.exists:
        #     f = h5py.File(path)
        # get the variables...

        t += one_hour
        # Need milliseconds since epoch for the time
        data.append([int(t.replace(tzinfo=timezone.utc).timestamp() * 1000), 5, 6])

    response = {
        "predictions": {
            "metadata": {
                "time": {
                    "units": "milliseconds since 1970-01-01",
                    "length": f"{len(data)}",
                },
                "pred": {
                    "missing_value": "99999.99",
                    "description": "Equatorial Dst Index Prediction",
                    "units": "nT",
                },
                "std": {
                    "missing_value": "99999.99",
                    "description": "Standard Deviation of the Equatorial Dst Index Predictions",
                    "units": "nT",
                },
            },
            "parameters": ["time", "pred", "std"],
            "data": data,
        }
    }

    return response
