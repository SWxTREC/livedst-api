# LiveDst API

Version 0.1

This creates a web API that enables easier public access to the live Dst predictions made by CU's space weather machine learning group. This API has been developed with AWS's Serverless Application Model (SAM), for details on deploying this API see the [SAM documentation](SAM_README.md)

## Endpoints

There is one endpoint to query for the data over a given time.

- [`/livedst`](#/livedst) : GET
  - Returns the livedst model predictions

### /livedst

Returns the data from the server corresponding to the given parameters

#### Query parameters

The request uses query parameters for the input data.

- `start_date` : string

The starting date and time of the desired data, the required format is `YYYY-mm-ddTHH:MM`.
The default is `end_date - 7 days`.

- `end_date` : string

The ending date and time for the desired data, the required format is `YYYY-mm-ddTHH:MM`.
The default is the current time.

#### Example request

Get the most recent 7-days worth of data (default request):

```html
http://127.0.0.1:3000/livedst
```

Get everything from 2018 to the present:

```html
http://127.0.0.1:3000/livedst?start_date=2018-01-01T00:00
```
