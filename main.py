from flask import Flask, render_template, request
import logging, json, urllib, random

app = Flask(__name__)

def getIdeas(keyword):
    baseurl = "https://developer.nps.gov/api/v1/thingstodo?api_key=H9QwVhEXpfAnSPHRAFuCns5Ok5FrFov6sDZAx2Wj"
    tenideas = {"q": keyword}
    paramstr = urllib.parse.urlencode(tenideas)
    getideas = baseurl + "&" + paramstr
    result = urllib.request.urlopen(getideas)
    jsonresult = result.read()
    dict = json.loads(jsonresult)
    return dict

def getSafeIdeas(keyword):
    try:
        return getIdeas(keyword)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print("Error trying to retrieve data: Error code: ", e.code)
        elif hasattr(e,'reason'):
            print("We failed to reach a server")
            print("Reason: ", e.reason)
        return None


@app.route("/")
def main_handler():
    app.logger.info("In MainHandler")
    key = request.args.get('key')
    season = request.args.get('season')
    if key:
        dict = getSafeIdeas(key)
        if dict is not None:
            newd = []
            for i in range(int(len(dict))):
                if season in dict["data"][i]["season"]:
                    newd.append(dict["data"][i])
            idea = random.choice(newd)
            park = idea["relatedParks"][0]["fullName"]
            title = "You can see %s at %s"%(key, park)
            activity = idea["title"]
            photo = idea["images"][0]["crops"][0]["url"]
            caption = idea ["images"][0]["altText"]
            shortdes = idea["shortDescription"]
            return render_template('ideas.html',
                page_title=title,
                searchdata=dict,
                activity_title=activity,
                short_des=shortdes,
                photo_url = photo,
                caption_text = caption
                 )
    elif key =="":
        return render_template('ideas.html',
            page_title="NP Activity Finder - Error",
            prompt="Please type something in the search bar.")
    else:
        return render_template('ideas.html',page_title="ideas")


if __name__ == "__main__":
    # Used when running locally only. 
	# When deploying to Google AppEngine, a webserver process
	# will serve your app. 
    app.run(host="localhost", port=8080, debug=True)
    