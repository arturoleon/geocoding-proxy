[![CircleCI](https://circleci.com/gh/arturoleon/geocoding-proxy/tree/master.svg?style=svg)](https://circleci.com/gh/arturoleon/geocoding-proxy/tree/master)

# Geocoding proxy

Simple Django REST application that receives an address and resolves the latitude and longitude coordinates for that address.

The service implements two geocoding services; [Google](https://developers.google.com/maps/documentation/geocoding/start) as primary and [HERE](https://developer.here.com/documentation/geocoder/topics/quick-start.html) as secondary. If the first one doesn't return a successful response it will fallback to the second.

## How to run the service
Before running the service, you will need to populate the API keys in the environment variables either in your system or updating the `.env` file.

To run the service locally, you just need to run the following command:
```
python manage.py runserver
```

Then you should be able to hit the service locally: http://127.0.0.1:8000/geocoding/

## How to deploy the service
Since this is a small app, you can deploy it to AWS Lambda and run it in a serverless infrastructure, to do that you can use [Zappa](https://github.com/Miserlou/Zappa) the configuration file is already on the repository.

You will need to update `zappa_settings.json` to define the `s3_bucket` and the `environment_variables`. After that, you can just run `zappa deploy`. This assumes that you have your [AWS keys defined in your local environment](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html#cli-quick-configuration).

## How to use the service
To find the corresponding geocoordinates to an address you just need to send the following request
```
GET http://serviceAddress/?address=365+N+Halsted+St
```

### Successful response
If the request is successful you will see a response with the following structure
```
200 OK
{
    "formatted_address": "365 N Halsted St, Chicago, IL 60654, USA",
    "location": {
        "latitude": 41.888716,
        "longitude": -87.6466287
    }
}
```

### Error response
If an error occurs you will receive a response with the following structure
```
404 Not Found
{
    "error": "Address not found."
}
```
You should expect HTTP status codes to match with the error response (e.g., 400 for bad requests)