import requests, json
  
# Enter your API key here 

  
# base_url variable to store url 


def getCityWeather(city, api):
  city_name = city
  api_key = api
  base_url = "https://api.openweathermap.org/data/2.5/weather?q="
  # complete url address 
  complete_url = base_url + city_name + "&appid=" + api_key
    
  # get method of requests module 
  # return response object 
  response = requests.get(complete_url) 
    
  # json method of response object  
  # convert json format data into 
  # python format data 
  x = response.json() 
    
  # Now x contains list of nested dictionaries 
  # Check the value of "cod" key is equal to 
  # "404", means city is found otherwise, 
  # city is not found 
  if x["cod"] != "404" and x["cod"] != "400": 
      
      return x
    
  else: 
      return 0

def getDailyWeather(lat, lon, api):
  url = "https://api.openweathermap.org/data/2.5/onecall?lat=" + str(lat) + "&lon=" + str(lon) + "&exclude=current,minutely,hourly,alerts&appid=" + api

  response = requests.get(url)
  weather = response.json()
  if weather["lat"] is not None:
    return weather
  else:
    return 0
