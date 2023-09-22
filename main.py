from flask import Flask ,render_template,request,jsonify,redirect
import requests
from api.add_travel import add_travel
from api.all_travels import get_all_travels
from api.delete_travel import delete_travel
from api.get_travel_by_id import get_travel_by_id 
from api.edit_travel import edit_travel

app = Flask(__name__)
app.debug = True


# API -----------------------------------------------------------------------------------
#Endpoint: Dodaj nową podróż
@app.route("/api/add-travel",methods=["POST"])
def api_add_travel():
    response = add_travel()
    return redirect("/travels")


# Endpoint: dla uzyskania wszysstkich podróży (z naszej aplikacji lub dowolnej innej)
@app.route("/api/get-all-travels")
def api_get_all_travels():
    data = get_all_travels()
    return data

#Endpoint: usuwanie wybranej podróży
@app.route("/api/delete-travel", methods=["DELETE","POST"])
def api_delete_travel():
    id = request.form.get("id_to_delete")
    print(id)
    response = delete_travel(id) 
    return redirect("/travels")

# Endpoint: edytowanie wybranego posta
@app.route("/api/edit-travel", methods=["POST"])
def api_edit_travel():
    id = request.form.get("id_to_edit")
    response = edit_travel(id)
    
    return redirect("/travels")

# Endpoint: jedna podróż zgodna z id
@app.route("/api/get-travel-by-id/<id>")
def api_get_travel_by_id(id):
    data = get_travel_by_id(id)
    return data



# ROUTY -------------------------------------------------------------------------------------

@app.route("/travels")
def travels_page():
      response = requests.get("http://127.0.0.1:5000/api/get-all-travels")
      travels = response.json()

      return render_template("travels.html", travels=travels['data'])


@app.route("/edit-travel/<id>")
def edit_travel_page(id):

    try:
        response = requests.get(f"http://127.0.0.1:5000/api/get-travel-by-id/{id}")
        travel = response.json() 

        countries_response = requests.get("https://restcountries.com/v3.1/all")
        countries = countries_response.json()

        names = list(map(lambda country: country['name']['common'], countries))


        return render_template("edit-travel.html",travel=travel['data'], names=names)

    except Exception as e:
        print(e)
        return render_template("edit-travel.html",travel={})



   


@app.route("/add-travel")
def add_travel_page():
    try:
      response = requests.get("https://restcountries.com/v3.1/all")
      countries = response.json()

      names = list(map(lambda country: country['name']['common'], countries))

      return render_template("add-travel.html",names=sorted(names) )
    
    except Exception as e:
      print("Error",e)
      return render_template("add-travel.html",names=[])
        

   



@app.route("/", methods=["GET","POST"])
def home_page():

    search_query = request.form.get("query")
    continent_filter = request.form.get("continent_filter")

    url = ""
    if search_query:
        url = f"https://restcountries.com/v3.1/name/{search_query}"
    else:
        url = "https://restcountries.com/v3.1/all"

    try:
       response = requests.get(url)
       countries = response.json()

       if continent_filter:
           countries = filter(lambda country: country['region'] == continent_filter,countries)

       return render_template("index.html",countries=countries)
    except Exception as e:
       print("Wystąpił błąd", str(e))
       return "Nie działa"


@app.route("/country/<name>")
def country_page(name):
     
      response = requests.get(f"https://restcountries.com/v3.1/name/{name}")
      data = response.json()

      currency_key = list(data[0]['currencies'].keys())[0] if data[0].get("currencies") is not None else []
      native_name_key = list(data[0]['name']['nativeName'].keys())[0] if data[0]['name'].get("nativeName") is not None else []
      languages = list(data[0]['languages'].values()) if data[0].get("languages") is not None else []

      neighbours = []

      for field in data:
          if "borders" not in field:
              print("NIE MA BORDERS!!")
          else:
              border_countries = ",".join(data[0]['borders']) 
              response_neighbours= requests.get(f"https://restcountries.com/v3.1/alpha?codes={border_countries}")
              neighbours_data = list(response_neighbours.json())
              neighbours = map(lambda neighbour: neighbour['name']['common'], neighbours_data)


      country = {
          "common_name":data[0]['name']['common'],
          "native_name":data[0]['name']['nativeName'][native_name_key]['common'] if data[0]['name'].get('nativeName') else "?",
          "currency_name": data[0]['currencies'][currency_key]['name'] if data[0].get("currencies") else "?",
          "languages":", ".join(languages),
          "population":data[0]['population'],
          "region":data[0]['region'],
          "capital":data[0]['capital'][0] if data[0].get('capital') else '?',
          "sub_region":data[0]['subregion'] if data[0].get("subregion") else '?',
          'tld':data[0]['tld'],
          "coat_of_arms":data[0]["coatOfArms"]['svg'] if data[0]['coatOfArms'] else data[0]['flags']['svg']
      }

     
      return render_template("country.html",country=country, neighbours=neighbours)

  









